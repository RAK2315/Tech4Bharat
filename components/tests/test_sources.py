"""Fictional archives only; these test acquisition safety, never model accuracy."""
import hashlib
import importlib
import importlib.util
import io
import json
from pathlib import Path
import stat
import struct
import subprocess
import sys
import tarfile
import zipfile
import zlib

import pytest


def get_api():
    name = 'component_inspector.data.acquire'
    assert importlib.util.find_spec(name) is not None, 'safe acquisition module is not implemented'
    return importlib.import_module(name)


def zip_fixture(path, entries):
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, value in entries:
            archive.writestr(name, value)
    return path


def png():
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 2, 2, 8, 0, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(b'\x00\x00\xff\x00\xff\x00')) + chunk(b'IEND', b''))


def test_zip_roundtrip_inventory_hashes_and_no_overwrite(tmp_path):
    api = get_api()
    source = zip_fixture(tmp_path / 'tiny.zip', [('train/a.png', b'fictional'), ('test/b', b'x')])
    dest = tmp_path / 'raw'
    inventory = api.safe_extract(source, dest)
    assert (dest / 'train/a.png').read_bytes() == b'fictional'
    assert inventory[0] == {'path': 'train/a.png', 'bytes': 9, 'sha256': hashlib.sha256(b'fictional').hexdigest()}
    with pytest.raises(api.AcquisitionError, match='exists'):
        api.safe_extract(source, dest)
    assert (dest / 'test/b').read_bytes() == b'x'


def test_tar_roundtrip(tmp_path):
    api = get_api()
    source = tmp_path / 'tiny.tar.gz'
    with tarfile.open(source, 'w:gz') as archive:
        entry = tarfile.TarInfo('metal_nut/train/good/a.png')
        entry.size = 3
        archive.addfile(entry, io.BytesIO(b'abc'))
    api.safe_extract(source, tmp_path / 'raw')
    assert (tmp_path / 'raw/metal_nut/train/good/a.png').read_bytes() == b'abc'


@pytest.mark.parametrize('name', ['../escape', '/absolute', 'C:/escape', 'C:escape', '\\server\\share',
    'a\\..\\escape', 'a/../escape', 'a:stream', 'CON', 'aux.txt', 'dir./x', 'dir /x', 'a//b'])
def test_rejects_unsafe_portable_paths_without_partial_output(tmp_path, name):
    api = get_api()
    source = zip_fixture(tmp_path / 'unsafe.zip', [('safe', b'ok'), (name, b'bad')])
    with pytest.raises(api.AcquisitionError):
        api.safe_extract(source, tmp_path / 'raw')
    assert not (tmp_path / 'raw').exists()
    assert not (tmp_path / 'escape').exists()


@pytest.mark.parametrize('kind', ['symlink', 'hardlink', 'fifo', 'device'])
def test_rejects_tar_links_and_special_files(tmp_path, kind):
    api = get_api()
    source = tmp_path / 'unsafe.tar'
    with tarfile.open(source, 'w') as archive:
        entry = tarfile.TarInfo('link')
        entry.type = {'symlink': tarfile.SYMTYPE, 'hardlink': tarfile.LNKTYPE,
                      'fifo': tarfile.FIFOTYPE, 'device': tarfile.CHRTYPE}[kind]
        entry.linkname = '../outside'
        archive.addfile(entry)
    with pytest.raises(api.AcquisitionError):
        api.safe_extract(source, tmp_path / 'raw')
    assert not (tmp_path / 'raw').exists()


def test_rejects_zip_symlink(tmp_path):
    api = get_api()
    link = zipfile.ZipInfo('link')
    link.create_system = 3
    link.external_attr = (stat.S_IFLNK | 0o777) << 16
    source = zip_fixture(tmp_path / 'link.zip', [(link, '../escape')])
    with pytest.raises(api.AcquisitionError):
        api.safe_extract(source, tmp_path / 'raw')


@pytest.mark.parametrize('entries', [[('A', b'1'), ('a', b'2')], [('a', b'1'), ('a/b', b'2')]])
def test_rejects_collisions(tmp_path, entries):
    api = get_api()
    source = zip_fixture(tmp_path / 'collision.zip', entries)
    with pytest.raises(api.AcquisitionError):
        api.safe_extract(source, tmp_path / 'raw')
    assert not (tmp_path / 'raw').exists()


@pytest.mark.parametrize('limits', [dict(max_members=1), dict(max_file_bytes=3),
    dict(max_total_bytes=7), dict(max_ratio=1)])
def test_rejects_bounded_expansion_and_member_count(tmp_path, limits):
    api = get_api()
    source = zip_fixture(tmp_path / 'bomb.zip', [('a', b'0' * 200), ('b', b'1' * 200)])
    with pytest.raises(api.AcquisitionError):
        api.safe_extract(source, tmp_path / 'raw', limits=api.Limits(**limits))
    assert not (tmp_path / 'raw').exists()
    assert not list(tmp_path.glob('.extract-*'))


def test_rejects_corrupt_archive(tmp_path):
    api = get_api()
    source = tmp_path / 'broken.zip'
    source.write_bytes(b'not a zip')
    with pytest.raises(api.AcquisitionError):
        api.safe_extract(source, tmp_path / 'raw')
    assert not (tmp_path / 'raw').exists()


def test_local_archive_records_provenance_samples_inventory_and_is_idempotent(tmp_path):
    api = get_api()
    source = zip_fixture(tmp_path / 'fixture.zip', [('train/1.png', png()), ('test/2.png', png())])
    original = source.read_bytes()
    record = api.acquire('ksdd2', root=tmp_path / 'project', archive=source)
    assert record['status'] == 'acquired'
    assert record['archive']['sha256'] == hashlib.sha256(original).hexdigest()
    assert record['archive']['bytes'] == len(original)
    assert record['acquisition_mode'] == 'local_archive_unverified_provider_identity'
    assert record['source_url'] == 'https://www.vicos.si/resources/kolektorsdd2/'
    assert record['license'] == 'CC-BY-NC-SA-4.0'
    assert record['retrieved_at_utc']
    assert record['inventory']['files'] == 2
    assert record['readable_training_sample']['width'] == 2
    assert record['readable_training_sample']['height'] == 2
    assert 'test/' not in record['readable_training_sample']['path']
    inventory = json.loads((tmp_path / 'project' / record['inventory']['path']).read_text())
    assert len(inventory) == 2
    assert source.read_bytes() == original
    assert api.acquire('ksdd2', root=tmp_path / 'project', archive=source) == record
    changed = zip_fixture(tmp_path / 'changed.zip', [('train/1.png', png())])
    with pytest.raises(api.AcquisitionError, match='different|existing'):
        api.acquire('ksdd2', root=tmp_path / 'project', archive=changed)


def test_invalid_training_sample_does_not_publish_raw(tmp_path):
    api = get_api()
    source = zip_fixture(tmp_path / 'bad.zip', [('train/a.png', b'not an image')])
    with pytest.raises(api.AcquisitionError):
        api.acquire('ksdd2', root=tmp_path / 'project', archive=source)
    assert not (tmp_path / 'project/data/raw/ksdd2').exists()


def test_mvtec_network_request_records_form_blocker_without_downloading(tmp_path):
    api = get_api()
    record = api.acquire('mvtec_ad', category='metal_nut', root=tmp_path)
    assert record['status'] == 'blocked_access'
    assert 'form' in record['required_human_action'].lower()
    assert record['archive'] is None
    assert not (tmp_path / 'data/raw/mvtec_ad').exists()


def test_cli_acquire_runs_actual_local_import_and_unsupported_commands_still_fail(tmp_path):
    source = zip_fixture(tmp_path / 'fixture.zip', [('train/1.png', png())])
    result = subprocess.run([sys.executable, '-m', 'component_inspector.cli', 'acquire',
        '--dataset', 'ksdd2', '--archive', str(source), '--root', str(tmp_path / 'project')],
        text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)['status'] == 'acquired'


@pytest.mark.parametrize('dataset,category', [('mvtec_ad', None), ('mvtec_ad', 'bottle'), ('ksdd2', 'metal_nut')])
def test_rejects_invalid_dataset_category_combinations(tmp_path, dataset, category):
    api = get_api()
    with pytest.raises(api.AcquisitionError):
        api.acquire(dataset, category=category, root=tmp_path)

class Response(io.BytesIO):
    """Fictional network transport, not dataset/model evidence."""
    def __init__(self, body, headers=None, url='https://data.vicos.si/datasets/KSDD/KolektorSDD2.zip'):
        super().__init__(body)
        self.headers = headers or {}
        self.url = url
    def geturl(self):
        return self.url


@pytest.mark.parametrize('body,headers,url,limits', [
    (b'123456', {}, 'https://data.vicos.si/a', dict(max_archive_bytes=5)),
    (b'12', {'Content-Length': '4'}, 'https://data.vicos.si/a', {}),
    (b'12', {'Content-Type': 'text/html'}, 'https://data.vicos.si/a', {}),
    (b'12', {}, 'https://untrusted.example/a', {}),
    (b'12', {}, 'http://data.vicos.si/a', {}),
])
def test_download_rejects_overflow_truncation_forms_and_untrusted_destinations(tmp_path, body, headers, url, limits):
    api = get_api()
    dest = tmp_path / 'archive.part'
    with pytest.raises(api.AcquisitionError):
        api.download('https://go.vicos.si/kolektorsdd2', dest, limits=api.Limits(**limits),
                     opener=lambda *_args, **_kwargs: Response(body, headers, url))
    assert not dest.exists()


def test_download_streams_bytes_and_records_redirect(tmp_path):
    api = get_api()
    dest = tmp_path / 'archive.part'
    result = api.download('https://go.vicos.si/kolektorsdd2', dest,
                         opener=lambda *_args, **_kwargs: Response(b'abc', {'Content-Length': '3'}))
    assert dest.read_bytes() == b'abc'
    assert result['bytes'] == 3
    assert result['resolved_url'] == 'https://data.vicos.si/datasets/KSDD/KolektorSDD2.zip'


def test_reimport_detects_raw_tampering(tmp_path):
    api = get_api()
    source = zip_fixture(tmp_path / 'fixture.zip', [('train/1.png', png())])
    project = tmp_path / 'project'
    record = api.acquire('ksdd2', root=project, archive=source)
    (project / record['raw_path'] / 'train/1.png').write_bytes(b'changed')
    with pytest.raises(api.AcquisitionError, match='hash mismatch'):
        api.acquire('ksdd2', root=project, archive=source)


def test_cli_blocked_access_has_nonzero_exit_and_no_false_success(tmp_path):
    result = subprocess.run([sys.executable, '-m', 'component_inspector.cli', 'acquire',
        '--dataset', 'mvtec_ad', '--category', 'metal_nut', '--root', str(tmp_path)],
        text=True, capture_output=True)
    assert result.returncode == 3
    assert json.loads(result.stdout)['status'] == 'blocked_access'


def test_tar_gzip_expansion_is_bounded_even_for_hidden_pax_metadata(tmp_path):
    api = get_api()
    source = tmp_path / 'pax.tar.gz'
    with tarfile.open(source, 'w:gz', format=tarfile.PAX_FORMAT) as archive:
        entry = tarfile.TarInfo('file')
        entry.pax_headers = {'comment': 'x' * 20000}
        entry.size = 1
        archive.addfile(entry, io.BytesIO(b'a'))
    with pytest.raises(api.AcquisitionError):
        api.safe_extract(source, tmp_path / 'raw', limits=api.Limits(max_total_bytes=1000, max_file_bytes=1000))
    assert not (tmp_path / 'raw').exists()


def test_zip_member_limit_checked_before_opening_payloads(tmp_path):
    api = get_api()
    source = zip_fixture(tmp_path / 'many.zip', [('a', b'1'), ('b', b'2')])
    with pytest.raises(api.AcquisitionError, match='member count'):
        api.safe_extract(source, tmp_path / 'raw', limits=api.Limits(max_members=1))


def test_rejects_forged_oversized_zip_directory_before_parser_allocation(tmp_path):
    api = get_api()
    source = tmp_path / 'forged.zip'
    source.write_bytes(struct.pack('<4s4H2LH', b'PK\x05\x06', 0, 0, 20001, 20001, 0, 0, 0))
    with pytest.raises(api.AcquisitionError, match='member count'):
        api.safe_extract(source, tmp_path / 'raw')


def test_crc_failure_removes_partial_extraction(tmp_path):
    api = get_api()
    source = tmp_path / 'crc.zip'
    with zipfile.ZipFile(source, 'w', compression=zipfile.ZIP_STORED) as archive:
        archive.writestr('a', b'uniquepayload')
    source.write_bytes(source.read_bytes().replace(b'uniquepayload', b'changedbytes'))
    with pytest.raises(api.AcquisitionError):
        api.safe_extract(source, tmp_path / 'raw')
    assert not (tmp_path / 'raw').exists()


def test_reimport_rejects_unrecorded_raw_files(tmp_path):
    api = get_api()
    source = zip_fixture(tmp_path / 'fixture.zip', [('train/1.png', png())])
    project = tmp_path / 'project'
    record = api.acquire('ksdd2', root=project, archive=source)
    (project / record['raw_path'] / 'extra.png').write_bytes(b'new')
    with pytest.raises(api.AcquisitionError, match='inventory'):
        api.acquire('ksdd2', root=project, archive=source)


def test_download_refuses_to_overwrite_existing_archive(tmp_path):
    api = get_api()
    dest = tmp_path / 'archive'
    dest.write_bytes(b'original')
    with pytest.raises(api.AcquisitionError):
        api.download('https://go.vicos.si/kolektorsdd2', dest,
                     opener=lambda *_args, **_kwargs: Response(b'abc'))
    assert dest.read_bytes() == b'original'


def test_xz_tar_from_local_provider_archive(tmp_path):
    api = get_api()
    source = tmp_path / 'metal_nut.tar.xz'
    with tarfile.open(source, 'w:xz') as archive:
        entry = tarfile.TarInfo('train/good/a.png')
        content = png()
        entry.size = len(content)
        archive.addfile(entry, io.BytesIO(content))
    record = api.acquire('mvtec_ad', category='metal_nut', root=tmp_path / 'project', archive=source)
    assert record['status'] == 'acquired'
    assert record['readable_training_sample']['path'] == 'train/good/a.png'


def test_tiny_tar_member_limit_does_not_reject_header_blocks(tmp_path):
    api = get_api()
    source = tmp_path / 'tiny.tar'
    with tarfile.open(source, 'w') as archive:
        entry = tarfile.TarInfo('file')
        entry.size = 3
        archive.addfile(entry, io.BytesIO(b'abc'))
    api.safe_extract(source, tmp_path / 'raw', limits=api.Limits(max_file_bytes=3))
    assert (tmp_path / 'raw/file').read_bytes() == b'abc'


def test_zip_directory_limit_does_not_trust_forged_entry_count(tmp_path):
    api = get_api()
    source = zip_fixture(tmp_path / 'forged-count.zip', [('a', b'1'), ('b', b'2')])
    payload = bytearray(source.read_bytes())
    offset = payload.rfind(b'PK\x05\x06')
    struct.pack_into('<HH', payload, offset + 8, 1, 1)
    source.write_bytes(payload)
    with pytest.raises(api.AcquisitionError, match='member count'):
        api._zip_directory_limit(source, api.Limits(max_members=1))


def test_cable_gland_import_selects_training_rgb_and_keeps_separate_identity(tmp_path):
    api = get_api()
    source = zip_fixture(tmp_path / 'cable.zip', [
        ('cable_gland/train/good/gt/000.png', b'not an RGB image'),
        ('cable_gland/train/good/rgb/000.png', png()),
        ('cable_gland/train/good/xyz/000.tiff', b'inert 3D data'),
        ('cable_gland/test/cut/rgb/000.png', b'test must not be decoded'),
    ])
    record = api.acquire('mvtec_3d_ad', category='cable_gland', root=tmp_path / 'project', archive=source)
    assert record['dataset'] == 'mvtec_3d_ad'
    assert record['category'] == 'cable_gland'
    assert record['raw_path'] == 'data/raw/mvtec_3d_cable_gland'
    assert record['source_url'].endswith('/mvtec-3d-ad')
    assert record['readable_training_sample']['path'] == 'cable_gland/train/good/rgb/000.png'
    assert record['inventory']['files'] == 4
    assert api.acquire('mvtec_3d_ad', category='cable_gland', root=tmp_path / 'project', archive=source) == record


def test_cable_gland_cli_records_access_blocker_without_archive(tmp_path):
    result = subprocess.run([sys.executable, '-m', 'component_inspector.cli', 'acquire',
        '--dataset', 'mvtec_3d_ad', '--category', 'cable_gland', '--root', str(tmp_path)],
        text=True, capture_output=True)
    assert result.returncode == 3, result.stderr
    assert json.loads(result.stdout)['status'] == 'blocked_access'


@pytest.mark.parametrize('category', [None, 'metal_nut', 'screw'])
def test_cable_gland_rejects_wrong_categories(tmp_path, category):
    with pytest.raises(get_api().AcquisitionError):
        get_api().acquire('mvtec_3d_ad', category=category, root=tmp_path)


def test_transient_windows_publish_denial_retries_without_overwriting(tmp_path, monkeypatch):
    source = zip_fixture(tmp_path/'tiny.zip',[('a',b'preserved')])
    original = Path.rename
    attempts=[]
    def transient(self,target):
        if self.name=='tree':
            attempts.append(str(target))
            if len(attempts)<3:
                error=PermissionError('fictional Windows sharing/indexer denial')
                error.winerror=5
                raise error
        return original(self,target)
    monkeypatch.setattr(Path,'rename',transient)
    get_api().safe_extract(source,tmp_path/'raw')
    assert (tmp_path/'raw/a').read_bytes()==b'preserved'
    assert len(attempts)==3
