"""Bounded official-source acquisition. No labels, splits, or model inference."""
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import gzip
import struct
import json
import lzma
import os
from pathlib import Path, PureWindowsPath
import re
import stat
import tarfile
import tempfile
import time
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import build_opener, HTTPRedirectHandler, Request
import zipfile


class AcquisitionError(ValueError):
    """Acquisition failed closed; never means data/model readiness."""


@dataclass(frozen=True)
class Limits:
    max_archive_bytes: int = 2 * 1024**3
    max_total_bytes: int = 6 * 1024**3
    max_file_bytes: int = 64 * 1024**2
    max_members: int = 20000
    max_ratio: int = 200


SOURCES = {
    'mvtec_3d_ad': {
        'source_url': 'https://www.mvtec.com/research-teaching/datasets/mvtec-3d-ad',
        'download_url': None,
        'attribution': 'MVTec Software GmbH; Bergmann, Sattlegger, Steger, The MVTec 3D-AD Dataset (VISAPP 2022).',
    },
    'mvtec_ad': {
        'source_url': 'https://www.mvtec.com/research-teaching/datasets/mvtec-ad',
        'download_url': None,
        'attribution': 'MVTec Software GmbH; Bergmann et al., MVTec AD (CVPR 2019).',
    },
    'ksdd2': {
        'source_url': 'https://www.vicos.si/resources/kolektorsdd2/',
        'download_url': 'https://go.vicos.si/kolektorsdd2',
        'attribution': 'Kolektor Group; Bozic, Tabernik, Skocaj (2021), Mixed supervision for surface-defect detection: from weakly to fully supervised learning, Computers in Industry.',
    },
}
LICENSE_URL = 'https://creativecommons.org/licenses/by-nc-sa/4.0/'
TERMS = 'Research only for this build. Retain attribution/license and disclose changes; NonCommercial and ShareAlike apply. Public-demo/commercial suitability is not established.'


def sha256(path):
    with Path(path).open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def _safe_path(name):
    if not name or '\\' in name or PureWindowsPath(name).drive or name.startswith('/'):
        raise AcquisitionError('Unsafe absolute/Windows archive path')
    parts = name.rstrip('/').split('/')
    for part in parts:
        if (part in ('', '.', '..') or part.endswith((' ', '.'))
                or re.search(r'[\x00-\x1f<>:"|?*]', part)
                or part.split('.')[0].upper() in {'CON', 'PRN', 'AUX', 'NUL',
                    *('COM' + str(i) for i in range(1, 10)), *('LPT' + str(i) for i in range(1, 10))}):
            raise AcquisitionError('Unsafe portable archive path')
    return '/'.join(parts)


def _no_links(path):
    for parent in (path, *path.parents):
        if parent.is_symlink() or parent.is_junction():
            raise AcquisitionError('Storage path contains a link/junction')


def _copy_bounded(src, dst, maximum):
    count = 0
    digest = hashlib.sha256()
    while chunk := src.read(1024 * 1024):
        count += len(chunk)
        if count > maximum:
            raise AcquisitionError('Byte limit exceeded')
        dst.write(chunk)
        digest.update(chunk)
    return count, digest.hexdigest()


class _XZReader:
    """XZ stream with a bounded dictionary and bounded output allocations."""
    def __init__(self, stream):
        self.stream = stream
        self.decoder = lzma.LZMADecompressor(memlimit=128 * 1024**2)

    def read(self, size):
        output = bytearray()
        while len(output) < size and not self.decoder.eof:
            data = self.stream.read(65536) if self.decoder.needs_input else b''
            if not data and self.decoder.needs_input:
                raise AcquisitionError('Truncated XZ stream')
            output.extend(self.decoder.decompress(data, max_length=size - len(output)))
        return bytes(output)


class _BoundedTarReader:
    """Bound reads before tarfile consumes hidden PAX/GNU metadata."""
    def __init__(self, stream, limits, compressed):
        self.stream, self.limits, self.compressed = stream, limits, compressed
        self.total = 0

    def tell(self):
        return self.total

    def seek(self, offset, whence=0):
        target = offset if whence == 0 else self.total + offset
        if whence not in (0, 1) or target < self.total:
            raise AcquisitionError('Backward TAR seek rejected')
        while self.total < target:
            if not self.read(min(target - self.total, 65536)):
                raise AcquisitionError('Truncated TAR stream')
        return self.total

    def read(self, size):
        if size < 0 or size > max(512, min(self.limits.max_file_bytes, 1024**2)):
            raise AcquisitionError("TAR metadata/read allocation exceeds file byte limit")
        data = self.stream.read(size)
        self.total += len(data)
        budget = self.limits.max_total_bytes + self.limits.max_members * 1024 + 10240
        if self.total > min(budget, self.compressed * self.limits.max_ratio):
            raise AcquisitionError("TAR stream expansion limit exceeded (includes metadata)")
        return data


def _zip_directory_limit(archive, limits):
    # Bound the central directory before ZipFile allocates its full member list.
    # ZIP64/multidisk are unnecessary under our 2 GiB / 20,000-member policy.
    with archive.open("rb") as handle:
        handle.seek(max(0, archive.stat().st_size - 65557))
        tail = handle.read(65557)
    offset = tail.rfind(b"PK\x05\x06")
    if offset < 0 or len(tail) - offset < 22:
        raise AcquisitionError("ZIP end record missing")
    _, disk, cd_disk, disk_entries, count, cd_size, cd_offset, comment = struct.unpack_from("<4s4H2LH", tail, offset)
    if count > limits.max_members or disk_entries > limits.max_members:
        raise AcquisitionError("Archive member count exceeded")
    if (disk or cd_disk or disk_entries != count or count == 65535
            or cd_size > limits.max_members * 4096 or cd_offset == 0xFFFFFFFF
            or cd_offset + cd_size > archive.stat().st_size or len(tail) - offset != 22 + comment):
        raise AcquisitionError("Unsupported/oversized ZIP directory")

    # Count actual central-directory headers too: EOCD cardinality is untrusted.
    with archive.open('rb') as handle:
        handle.seek(cd_offset)
        end, actual = cd_offset + cd_size, 0
        while handle.tell() < end:
            header = handle.read(46)
            if len(header) != 46 or header[:4] != b'PK\x01\x02':
                raise AcquisitionError('Invalid ZIP central directory')
            actual += 1
            if actual > limits.max_members:
                raise AcquisitionError('Archive member count exceeded')
            name_len, extra_len, comment_len = struct.unpack_from('<HHH', header, 28)
            handle.seek(name_len + extra_len + comment_len, 1)
            if handle.tell() > end:
                raise AcquisitionError('Truncated ZIP central directory')
        if actual != count:
            raise AcquisitionError('ZIP member count mismatch')


def safe_extract(archive, destination, *, limits=Limits()):
    """Extract regular files manually into a private temp tree, then publish once.

    Never calls extractall, follows archive links, or executes downloaded files.
    Limits include all members (even directories) and declared + actual file bytes.
    """
    archive, destination = Path(archive), Path(destination)
    _no_links(destination)
    if destination.exists():
        raise AcquisitionError('Extraction destination already exists')
    compressed = archive.stat().st_size
    if not 0 < compressed <= limits.max_archive_bytes:
        raise AcquisitionError('Archive byte limit exceeded or empty archive')
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(prefix='.extract-', dir=destination.parent) as scratch:
            target = Path(scratch) / 'tree'
            target.mkdir()
            inventory, seen, members, total = [], {}, 0, 0

            def unpack(name, size, directory, stream):
                nonlocal members, total
                members += 1
                if members > limits.max_members:
                    raise AcquisitionError('Archive member count exceeded')
                relative = _safe_path(name)
                key = relative.casefold()
                if key in seen:
                    raise AcquisitionError('Duplicate/case-colliding archive path')
                for parent in Path(key).parents:
                    if str(parent) != '.' and seen.get(parent.as_posix()) == 'file':
                        raise AcquisitionError('File/directory collision')
                if not directory and any(k.startswith(key + '/') for k in seen):
                    raise AcquisitionError('File/directory collision')
                seen[key] = 'directory' if directory else 'file'
                if size < 0 or size > limits.max_file_bytes:
                    raise AcquisitionError('Archive member byte limit exceeded')
                total += size
                if total > limits.max_total_bytes or total > compressed * limits.max_ratio:
                    raise AcquisitionError('Archive expansion limit exceeded')
                path = target.joinpath(*relative.split('/'))
                if directory:
                    path.mkdir(parents=True, exist_ok=True)
                    return
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open('xb') as output, stream() as incoming:
                    actual, digest = _copy_bounded(incoming, output, min(size, limits.max_file_bytes))
                if actual != size:
                    raise AcquisitionError('Truncated archive member')
                inventory.append({'path': relative, 'bytes': actual, 'sha256': digest})

            if zipfile.is_zipfile(archive):
                _zip_directory_limit(archive, limits)
                with zipfile.ZipFile(archive) as source:
                    for entry in source.infolist():
                        mode = entry.external_attr >> 16
                        if stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR) or entry.flag_bits & 1:
                            raise AcquisitionError('Archive link/special/encrypted member rejected')
                        unpack(entry.filename, entry.file_size, entry.is_dir(), lambda e=entry: source.open(e))
            else:
                with archive.open('rb') as incoming:
                    magic = incoming.read(6)
                    incoming.seek(0)
                    if magic.startswith(b'\x1f\x8b'):
                        stream = gzip.GzipFile(fileobj=incoming)
                    elif magic == b'\xfd7zXZ\x00':
                        stream = _XZReader(incoming)
                    else:
                        stream = incoming
                    bounded = _BoundedTarReader(stream, limits, compressed)
                    with tarfile.open(fileobj=bounded, mode='r:') as source:
                        for entry in source:
                            if not (entry.isfile() or entry.isdir()) or entry.issparse():
                                raise AcquisitionError('Archive link/special/sparse member rejected')
                            unpack(entry.name, entry.size, entry.isdir(), lambda e=entry: source.extractfile(e))
            if not inventory:
                raise AcquisitionError('Archive contains no regular files')
            # Windows rename does not replace an existing directory. Locking at the
            # acquisition layer serializes normal CLI writers; no shared-host claim.
            # OneDrive/indexers can briefly deny a Windows directory publication.
            # Retry only that exact error, rechecking no-overwrite on every attempt.
            for attempt in range(4):
                if destination.exists():
                    raise AcquisitionError('Extraction destination already exists')
                try:
                    target.rename(destination)
                    break
                except PermissionError as exc:
                    if getattr(exc, 'winerror', None) != 5 or attempt == 3:
                        raise
                    time.sleep(.05 * (attempt + 1))
            return inventory
    except AcquisitionError:
        raise
    except (OSError, tarfile.TarError, zipfile.BadZipFile, EOFError, RuntimeError, lzma.LZMAError) as exc:
        raise AcquisitionError(f'Archive extraction failed: {type(exc).__name__}') from exc


def _official_url(url):
    parsed = urlsplit(url)
    if (parsed.scheme != 'https' or parsed.hostname not in {'go.vicos.si', 'data.vicos.si'}
            or parsed.username or parsed.password or parsed.port not in (None, 443)):
        raise AcquisitionError('Non-official or insecure download destination')


class _OfficialRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        _official_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download(url, destination, *, limits=Limits(), opener=None):
    """Stream approved HTTPS sources with byte/length checks. Remove own partials."""
    _official_url(url)
    destination = Path(destination)
    opener = opener or build_opener(_OfficialRedirects()).open
    created = False
    try:
        with opener(Request(url, headers={'User-Agent': 'Tech4Bharat-research/0.1'}), timeout=60) as response:
            resolved = response.geturl()
            _official_url(resolved)
            if 'text/html' in response.headers.get('Content-Type', '').lower():
                raise AcquisitionError('Download returned a form/HTML instead of an archive')
            declared = response.headers.get('Content-Length')
            declared = int(declared) if declared is not None else None
            if declared is not None and not 0 < declared <= limits.max_archive_bytes:
                raise AcquisitionError('Download Content-Length exceeds byte limit')
            with destination.open('xb') as output:
                created = True
                size, digest = _copy_bounded(response, output, limits.max_archive_bytes)
            if size == 0 or (declared is not None and size != declared):
                raise AcquisitionError('Download is empty/truncated')
            return {'requested_url': url, 'resolved_url': resolved, 'bytes': size, 'sha256': digest,
                    'last_modified': response.headers.get('Last-Modified'), 'etag': response.headers.get('ETag')}
    except (OSError, URLError, ValueError) as exc:
        if created:
            destination.unlink(missing_ok=True)
        if isinstance(exc, AcquisitionError):
            raise
        raise AcquisitionError(f'Download failed: {type(exc).__name__}') from exc


def _write_json(path, value):
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, indent=2, ensure_ascii=True)
        handle.write('\n')


def _training_sample(tree, dataset):
    # Stage 1 decodes one training image only. Labels/masks/role audits are T02.
    from PIL import Image
    candidates = sorted(p for p in tree.rglob('*.png') if 'train' in p.relative_to(tree).parts
                        and not p.stem.endswith(('_GT', '_mask')))
    if dataset == 'mvtec_ad':
        candidates = [p for p in candidates if 'good' in p.parts]
    elif dataset == 'mvtec_3d_ad':
        candidates = [p for p in candidates
                      if p.relative_to(tree).parts[:4] == ('cable_gland', 'train', 'good', 'rgb')]
    if not candidates:
        raise AcquisitionError('No PNG training sample found; source layout needs review')
    try:
        with Image.open(candidates[0]) as image:
            if image.width * image.height > 20_000_000 or getattr(image, 'n_frames', 1) != 1:
                raise AcquisitionError('Training sample exceeds decode bounds')
            image.load()
            return {'path': candidates[0].relative_to(tree).as_posix(), 'width': image.width,
                    'height': image.height, 'mode': image.mode, 'format': image.format,
                    'scope': 'one training image decoded; not a full image/mask audit'}
    except (OSError, ValueError, Image.DecompressionBombError) as exc:
        raise AcquisitionError('Training sample is not readable') from exc


def acquire(dataset, *, category=None, root=None, archive=None, limits=Limits()):
    categories = {'mvtec_ad': 'metal_nut', 'mvtec_3d_ad': 'cable_gland', 'ksdd2': None}
    if dataset not in SOURCES or category != categories[dataset]:
        raise AcquisitionError('Supported sources: mvtec_ad/metal_nut, mvtec_3d_ad/cable_gland, ksdd2/no category')
    root = Path(root) if root else Path(__file__).resolve().parents[3]
    _no_links(root)
    key = {'mvtec_ad': 'mvtec_metal_nut', 'mvtec_3d_ad': 'mvtec_3d_cable_gland', 'ksdd2': 'ksdd2'}[dataset]
    data = root / 'data'
    for path in (data / 'archives', data / 'raw', data / 'manifests'):
        _no_links(path)
        path.mkdir(parents=True, exist_ok=True)
    record_path = data / 'manifests' / f'{key}_source.json'
    raw = data / 'raw' / key
    lock = data / f'.acquire-{key}.lock'
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise AcquisitionError('Acquisition already active; inspect stale lock before manual recovery') from exc
    os.close(descriptor)
    try:
        if record_path.exists():
            prior = json.loads(record_path.read_text(encoding='utf-8'))
            if prior['status'] == 'acquired':
                if archive and sha256(archive) != prior['archive']['sha256']:
                    raise AcquisitionError('A different archive conflicts with existing acquisition')
                inventory_path = root / prior['inventory']['path']
                if sha256(inventory_path) != prior['inventory']['sha256']:
                    raise AcquisitionError('Existing inventory hash mismatch')
                if sha256(root / prior['archive']['path']) != prior['archive']['sha256']:
                    raise AcquisitionError('Existing archive hash mismatch')
                saved_inventory = json.loads(inventory_path.read_text(encoding='utf-8'))
                actual_paths = {p.relative_to(raw).as_posix() for p in raw.rglob('*') if p.is_file()}
                if actual_paths != {entry['path'] for entry in saved_inventory}:
                    raise AcquisitionError('Existing raw inventory membership mismatch')
                for entry in saved_inventory:
                    path = raw / entry['path']
                    _no_links(path)
                    if sha256(path) != entry['sha256']:
                        raise AcquisitionError('Existing raw file hash mismatch')
                return prior
            if not archive:
                return prior
        base = {**SOURCES[dataset], 'dataset': dataset, 'category': category,
                'checked_at_utc': datetime.now(timezone.utc).isoformat(),
                'license': 'CC-BY-NC-SA-4.0', 'license_url': LICENSE_URL, 'terms': TERMS,
                'provider_release_id': None, 'limits': asdict(limits)}
        if dataset in ('mvtec_ad', 'mvtec_3d_ad') and not archive:
            blocked = {**base, 'status': 'blocked_access', 'archive': None,
                       'required_human_action': f'Personally complete the official MVTec download form/terms if acceptable; obtain only {category} and rerun with --archive PATH. No form was submitted by Codex.'}
            if not record_path.exists():
                _write_json(record_path, blocked)
            return blocked
        if raw.exists():
            raise AcquisitionError('Existing raw destination has no completed source record; review manually')
        with tempfile.TemporaryDirectory(prefix='.acquire-', dir=data) as scratch:
            temp = Path(scratch)
            local = temp / 'archive.part'
            if archive:
                source = Path(archive)
                if source.stat().st_size > limits.max_archive_bytes:
                    raise AcquisitionError('Local archive byte limit exceeded')
                with source.open('rb') as incoming, local.open('xb') as output:
                    size, digest = _copy_bounded(incoming, output, limits.max_archive_bytes)
                transport = {'bytes': size, 'sha256': digest, 'requested_url': None, 'resolved_url': None}
                mode = 'local_archive_unverified_provider_identity'
            else:
                transport = download(SOURCES[dataset]['download_url'], local, limits=limits)
                mode = 'official_https_download'
            inventory = safe_extract(local, temp / 'raw', limits=limits)
            sample = _training_sample(temp / 'raw', dataset)
            archive_path = data / 'archives' / (transport['sha256'] + ('.zip' if zipfile.is_zipfile(local) else '.tar'))
            inventory_path = data / 'manifests' / f'{key}_{transport["sha256"]}_inventory.json'
            if archive_path.exists():
                if sha256(archive_path) != transport['sha256']:
                    raise AcquisitionError('Existing content-addressed archive mismatch')
            else:
                local.rename(archive_path)
            if not inventory_path.exists():
                _write_json(inventory_path, inventory)
            record = {**base, 'status': 'acquired', 'acquisition_mode': mode,
                      'retrieved_at_utc': datetime.now(timezone.utc).isoformat(),
                      'retrieval_note': 'Local import time; original provider retrieval date unknown' if archive else 'HTTPS retrieval completed',
                      'archive': {**transport, 'path': archive_path.relative_to(root).as_posix()},
                      'raw_path': raw.relative_to(root).as_posix(),
                      'inventory': {'path': inventory_path.relative_to(root).as_posix(),
                                    'sha256': sha256(inventory_path), 'files': len(inventory),
                                    'extracted_bytes': sum(e['bytes'] for e in inventory)},
                      'readable_training_sample': sample,
                      'validation_status': 'acquired_not_audited_or_split'}
            _write_json(temp / 'record.json', record)
            (temp / 'raw').rename(raw)
            # A blocked-access record can only be replaced by a successful import.
            (temp / 'record.json').replace(record_path)
            return record
    except (OSError, json.JSONDecodeError) as exc:
        raise AcquisitionError(f'Acquisition storage failure: {type(exc).__name__}') from exc
    finally:
        lock.unlink(missing_ok=True)
