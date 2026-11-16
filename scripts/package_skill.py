"""Validate and package only explicitly approved public skill files."""
from pathlib import Path
import hashlib
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "takeagent-skill"
FILES = ("SKILL.md", "references/setup.md", "references/workflows.md")

def build():
    for name in FILES:
        path = SKILL / name
        if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(SKILL.resolve()):
            raise ValueError(f"Invalid package input: {name}")
        content = path.read_text(encoding="utf-8")
        if name == "SKILL.md":
            if not content.startswith("---\nname: takeagent-skill\ndescription: ") or "\n---\n" not in content[4:]:
                raise ValueError("Invalid skill frontmatter")
        for target in re.findall(r"\]\(([^)]+)\)", content):
            if "://" not in target and not target.startswith("#"):
                resolved = (path.parent / target.split("#")[0]).resolve()
                if not resolved.is_relative_to(SKILL.resolve()) or not resolved.is_file():
                    raise ValueError(f"Broken local reference in {name}")
    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    archive = out / "takeagent-skill.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
        for name in FILES:
            info = zipfile.ZipInfo("takeagent-skill/" + name, date_time=(2026, 11, 16, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, (SKILL / name).read_bytes())
    with zipfile.ZipFile(archive) as bundle:
        if bundle.testzip() is not None or set(bundle.namelist()) != {"takeagent-skill/" + n for n in FILES}:
            raise ValueError("Archive verification failed")
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (out / "takeagent-skill.zip.sha256").write_text(digest + "  takeagent-skill.zip\n", encoding="ascii")
    print(f"PASS: {len(FILES)} public skill files; references and archive verified")
    print(f"SHA256 {digest}")

if __name__ == "__main__":
    build()
