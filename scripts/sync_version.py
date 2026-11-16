"""Keep the README and landing-page release links derived from VERSION."""
from pathlib import Path
import argparse
import re

ROOT = Path(__file__).resolve().parents[1]

def version(root=ROOT):
    value = (Path(root) / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", value):
        raise ValueError("VERSION must be a numeric major.minor.patch")
    return value

def synchronize(root=ROOT, check=False):
    root = Path(root)
    tag = "v" + version(root)
    changed = []
    for name in ("README.md", "docs/index.html"):
        path = root / name
        original = path.read_text(encoding="utf-8")
        updated, count = re.subn(
            r"(https://github\.com/jongos/takeagent-skill/releases/(?:download|tag)/)v\d+\.\d+\.\d+",
            lambda match: match.group(1) + tag, original)
        if not count:
            raise ValueError(f"No release links in {name}")
        if name.endswith(".html"):
            updated, badge_count = re.subn(r"OPEN SOURCE · v\d+\.\d+\.\d+", "OPEN SOURCE · " + tag, updated)
            if badge_count != 1:
                raise ValueError("Expected one landing-page version badge")
        if updated != original:
            changed.append(name)
            if not check:
                path.write_text(updated, encoding="utf-8", newline="\n")
    if check and changed:
        raise ValueError("Version links are stale: " + ", ".join(changed))
    return tag

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--check", action="store_true")
    print(synchronize(check=args.parse_args().check))
