"""Keep the README and landing-page release metadata derived from VERSION."""
from pathlib import Path
import argparse
import re

ROOT = Path(__file__).resolve().parents[1]
REPO = "jongos/takeagent-skill"
LATEST_DOWNLOAD = f"https://github.com/{REPO}/releases/latest/download/takeagent-skill.zip"
LATEST_RELEASE = f"https://github.com/{REPO}/releases/latest"
VERSIONED_RELEASE_LINK = re.compile(
    r"https://github\.com/jongos/takeagent-skill/releases/(?:download|tag)/v\d+\.\d+\.\d+"
)

def version(root=ROOT):
    value = (Path(root) / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", value):
        raise ValueError("VERSION must be a numeric major.minor.patch")
    return value

def landing_download_links(html):
    issues = []
    if html.count(LATEST_DOWNLOAD) != 2:
        issues.append("landing page must use the latest-release download URL twice")
    if LATEST_RELEASE not in html:
        issues.append("landing page must link to releases/latest for checksums")
    if VERSIONED_RELEASE_LINK.search(html):
        issues.append("landing page must not pin versioned release URLs")
    if issues:
        raise ValueError("; ".join(issues))

def readme_release_links(text):
    issues = []
    if text.count(LATEST_DOWNLOAD) != 1:
        issues.append("README must use the latest-release download URL once")
    if LATEST_RELEASE not in text:
        issues.append("README must link to releases/latest for release notes")
    if VERSIONED_RELEASE_LINK.search(text):
        issues.append("README must not pin versioned release URLs")
    if issues:
        raise ValueError("; ".join(issues))

def repair_readme_release_links(text):
    text = re.sub(
        r"https://github\.com/jongos/takeagent-skill/releases/download/v\d+\.\d+\.\d+/takeagent-skill\.zip",
        LATEST_DOWNLOAD,
        text,
    )
    return re.sub(
        r"https://github\.com/jongos/takeagent-skill/releases/tag/v\d+\.\d+\.\d+",
        LATEST_RELEASE,
        text,
    )

def synchronize_readme(path, check):
    original = path.read_text(encoding="utf-8")
    try:
        readme_release_links(original)
    except ValueError as error:
        if check:
            raise ValueError("Version links are stale: README.md") from error
        updated = repair_readme_release_links(original)
        readme_release_links(updated)
        path.write_text(updated, encoding="utf-8", newline="\n")
        return "README.md"
    return None

def synchronize_landing(path, tag, check):
    original = path.read_text(encoding="utf-8")
    landing_download_links(original)
    updated, badge_count = re.subn(r"TAKEAGENT SKILL · v\d+\.\d+\.\d+", "TAKEAGENT SKILL · " + tag, original)
    if badge_count != 1:
        raise ValueError("Expected one landing-page version badge")
    if updated != original:
        if check:
            raise ValueError("Version links are stale: docs/index.html")
        path.write_text(updated, encoding="utf-8", newline="\n")
        return "docs/index.html"
    return None

def synchronize(root=ROOT, check=False):
    root = Path(root)
    tag = "v" + version(root)
    changed = [
        name
        for name in (
            synchronize_readme(root / "README.md", check),
            synchronize_landing(root / "docs/index.html", tag, check),
        )
        if name
    ]
    if check and changed:
        raise ValueError("Version links are stale: " + ", ".join(changed))
    return tag

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--check", action="store_true")
    print(synchronize(check=args.parse_args().check))