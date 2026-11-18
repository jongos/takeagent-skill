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
import yaml
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
FILES = ("SKILL.md", "references/setup.md", "references/workflows.md", "LICENSE")
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

class UniqueSafeLoader(yaml.SafeLoader):
    """Safe YAML with duplicate keys rejected instead of silently overwritten."""

def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str) or key in result:
            raise ValueError("Metadata keys must be unique strings")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result

UniqueSafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)

def frontmatter_body(text):
    front = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
    if not front:
        raise ValueError("Missing skill frontmatter")
    try:
        if any(isinstance(token, (yaml.tokens.AnchorToken, yaml.tokens.AliasToken))
               for token in yaml.scan(front.group(1))):
            raise ValueError("Metadata anchors and aliases are not supported")
        fields = yaml.load(front.group(1), Loader=UniqueSafeLoader)
    except yaml.YAMLError as error:
        raise ValueError("Invalid YAML metadata") from error
    if (not isinstance(fields, dict) or set(fields) != {"name", "description"}
            or fields["name"] != "takeagent-skill"
            or not isinstance(fields["description"], str)
            or not fields["description"].strip()):
        raise ValueError("Expected a skill name and nonempty string description")
    return text[front.end():]

def markdown_links(text):
    parser = MarkdownIt("commonmark")
    # Parse unsafe destinations too, so the package validator can reject them.
    parser.validateLink = lambda url: True
    environment = {}
    tokens = parser.parse(text, environment)
    targets = []
    def walk(items):
        for token in items:
            if token.type in {"link_open", "image"}:
                target = token.attrGet("href" if token.type == "link_open" else "src")
                if target is not None:
                    targets.append(target)
            if token.children:
                walk(token.children)
    walk(tokens)
    # Definitions are validated even when not yet used by a link.
    targets.extend(ref["href"] for ref in environment.get("references", {}).values())
    return targets

def snapshot(root):
    skill = checked_path(root, Path(root) / "skills" / "takeagent-skill")
    content = {}
    for name in FILES:
        if name == "LICENSE":
            path = checked_path(root, Path(root) / "LICENSE")
        else:
            path = checked_path(root, skill / name)
        if not path.is_file():
            raise ValueError(f"Missing package input: {name}")
        with path.open("rb") as source:
            raw = source.read(MAX_FILE_BYTES + 1)
        if len(raw) > MAX_FILE_BYTES:
            raise ValueError(f"Package input is too large: {name}")
        text = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
        content[name] = (text.rstrip("\n") + "\n").encode("utf-8")
    main_body = frontmatter_body(content["SKILL.md"].decode("utf-8"))
    for name, raw in content.items():
        text = main_body if name == "SKILL.md" else raw.decode("utf-8")
        for target in markdown_links(text):
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
