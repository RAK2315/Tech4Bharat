"""Download the registered public datasets; never execute archive content."""
import concurrent.futures
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import time
import urllib.request
import zipfile

ROOT = Path("components/outputs/external-transfer-20261023")
SOURCES = {
    "magnetic": "https://codeload.github.com/abin24/Magnetic-tile-defect-datasets./zip/cc4eb530b57b9cb7225bf76023873043ffd50655",
    "ksdd1": "https://data.vicos.si/datasets/KSDD/KolektorSDD.zip",
    "dagm1-normal": "https://conferences.mpi-inf.mpg.de/dagm/2007/Class1.zip",
    "dagm1-defect": "https://conferences.mpi-inf.mpg.de/dagm/2007/Class1_def.zip",
}


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def write(path, value):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, sort_keys=True); stream.write("\n")


def extract(archive, destination):
    destination.mkdir(exist_ok=False)
    with zipfile.ZipFile(archive) as package:
        assert package.testzip() is None
        names = set(); total = 0
        for member in package.infolist():
            path = PurePosixPath(member.filename.replace("\\", "/"))
            if path.is_absolute() or ".." in path.parts or any(":" in p for p in path.parts):
                raise ValueError("Unsafe archive name")
            if stat.S_ISLNK(member.external_attr >> 16):
                raise ValueError("Archive symlink rejected")
            name = str(path).casefold()
            if name in names:
                raise ValueError("Duplicate archive path")
            names.add(name); total += member.file_size
            if total > 3 * 1024**3 or member.file_size > 100 * 1024**2:
                raise ValueError("Archive uncompressed cap exceeded")
            target = destination.joinpath(*path.parts)
            if member.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with package.open(member) as source, target.open("xb") as output:
                    shutil.copyfileobj(source, output)
    return {"entries": len(names), "uncompressed_bytes": total}


def acquire(name, url):
    tick = time.monotonic(); attempts = []
    for attempt in range(1, 4):
        target = ROOT / "archives" / f"{name}-attempt-{attempt}.zip"
        if target.exists():
            raise ValueError("Acquisition destination already exists")
        record = {"url": url, "attempt": attempt, "created_utc": datetime.now(timezone.utc).isoformat()}
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "Tech4Bharat-frozen-model-research"})
            with urllib.request.urlopen(request, timeout=45) as response, target.open("xb") as output:
                record["final_url"] = response.url
                record["content_type"] = response.headers.get("Content-Type")
                total = 0; last_print = time.monotonic()
                while data := response.read(1024**2):
                    total += len(data)
                    if total > 600 * 1024**2 or time.monotonic() - tick > 1200:
                        raise ValueError("Download size/time cap exceeded")
                    output.write(data)
                    if time.monotonic() - last_print > 20:
                        print("DOWNLOAD", name, total, "bytes", flush=True); last_print = time.monotonic()
            record.update(bytes=target.stat().st_size, sha256=sha(target))
            record["extraction"] = extract(target, ROOT / "raw" / name)
            record["status"] = "completed"; attempts.append(record)
            write(ROOT / f"acquisition-{name}.json", {"attempts": attempts, "selected_archive": str(target.resolve())})
            print("ACQUIRED", name, record["bytes"], flush=True)
            return name, True
        except Exception as exc:
            record.update(status="failed", error=f"{type(exc).__name__}: {exc}")
            if target.exists(): record.update(bytes=target.stat().st_size, sha256=sha(target))
            attempts.append(record); write(ROOT / f"acquisition-{name}-failure-{attempt}.json", record)
            print("ACQUISITION FAILURE", name, record["error"], flush=True)
            # Retry transport failures only. Extraction/data errors are preserved and stop.
            if (ROOT / "raw" / name).exists(): break
    write(ROOT / f"acquisition-{name}.json", {"attempts": attempts, "selected_archive": None})
    return name, False


def main():
    ROOT.mkdir(exist_ok=False)
    (ROOT / "archives").mkdir(); (ROOT / "raw").mkdir()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        result = dict(executor.map(lambda pair: acquire(*pair), SOURCES.items()))
    write(ROOT / "acquisition-complete.json", {"sources": result, "downloader_sha256": sha(Path(__file__))})
    print("ACQUISITION FINISHED", result, flush=True)


if __name__ == "__main__": main()
