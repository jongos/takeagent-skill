"""Build a deterministic skill ZIP from a validated, bounded input snapshot."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import hashlib
import io
import os
import re
import stat
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FILES = ("SKILL.md", "references/setup.md", "references/workflows.md")
MAX_FILE_BYTES = 256 * 1024

def checked_path(root, path):
    """Reject symlinks/junctions and traversal before reading or writing."""
    root, path = Path(root).absolute(), Path(path).absolute()
    if not path.is_relative_to(root):
        raise ValueError("Path escapes repository")
    for part in (path, *path.parents):
        try:
            mode = part.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(mode.st_mode) or getattr(mode, "st_file_attributes", 0) & 0x400:
            raise ValueError(f"Linked/reparse path is not allowed: {part.name}")
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("Resolved path escapes repository")
    return path

def snapshot(root):
    skill = checked_path(root, Path(root) / "skills" / "takeagent-skill")
    content = {}
    for name in FILES:
        path = checked_path(root, skill / name)
        if not path.is_file():
            raise ValueError(f"Missing package input: {name}")
        with path.open("rb") as source:
            raw = source.read(MAX_FILE_BYTES + 1)
        if len(raw) > MAX_FILE_BYTES:
            raise ValueError(f"Package input is too large: {name}")
        text = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
        content[name] = (text.rstrip("\n") + "\n").encode("utf-8")
    main = content["SKILL.md"].decode("utf-8")
    front = re.match(r"\A---\n(.*?)\n---\n", main, re.S)
    if not front:
        raise ValueError("Missing skill frontmatter")
    fields = front.group(1).splitlines()
    if len(fields) != 2 or fields[0] != "name: takeagent-skill" or not fields[1].startswith("description: ") or not fields[1][13:].strip():
        raise ValueError("Invalid skill name or description")
    for name, raw in content.items():
        for target in re.findall(r"\]\(([^)]+)\)", raw.decode("utf-8")):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
                    raise ValueError(f"Unsafe link in {name}")
                continue
            if not parsed.path:
                continue
            resolved = checked_path(root, (skill / name).parent / unquote(parsed.path)).resolve()
            try:
                relative = resolved.relative_to(skill.resolve()).as_posix()
            except ValueError:
                raise ValueError(f"Reference escapes skill: {name}") from None
            if relative not in content:
                raise ValueError(f"Reference is absent from package: {name}")
    return content

def archive_bytes(content):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as bundle:
        for name in FILES:
            info = zipfile.ZipInfo("takeagent-skill/" + name, (2026, 11, 16, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, content[name])
    data = buffer.getvalue()
    with zipfile.ZipFile(io.BytesIO(data)) as bundle:
        expected = ["takeagent-skill/" + name for name in FILES]
        if bundle.testzip() is not None or bundle.namelist() != expected:
            raise ValueError("Archive verification failed")
        for name in FILES:
            if bundle.read("takeagent-skill/" + name) != content[name]:
                raise ValueError("Archive content mismatch")
    return data

def atomic_write(root, path, data):
    path = checked_path(root, path)
    fd, temporary = tempfile.mkstemp(prefix=".skill-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as target:
            target.write(data)
        checked_path(root, path)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)

def build(root=ROOT):
    root = Path(root).absolute()
    # Validate every input and in-memory archive before replacing prior outputs.
    data = archive_bytes(snapshot(root))
    digest = hashlib.sha256(data).hexdigest()
    out = checked_path(root, root / "dist")
    out.mkdir(exist_ok=True)
    archive = checked_path(root, out / "takeagent-skill.zip")
    receipt = checked_path(root, out / "takeagent-skill.zip.sha256")
    atomic_write(root, archive, data)
    atomic_write(root, receipt, (digest + "  takeagent-skill.zip\n").encode("ascii"))
    return archive, digest

if __name__ == "__main__":
    archive, digest = build()
    print(f"PASS: {len(FILES)} snapshotted public files; references and archive verified")
    print(f"SHA256 {digest}")
