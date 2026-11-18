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

def semver_tuple(value):
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", value.strip())
    if not match:
        raise ValueError("Version must be major.minor.patch")
    return tuple(int(part) for part in match.groups())

def compare_semver(left, right):
    l_tuple, r_tuple = semver_tuple(left), semver_tuple(right)
    if l_tuple < r_tuple:
        return -1
    if l_tuple > r_tuple:
        return 1
    return 0

def is_strictly_newer(candidate, current):
    return compare_semver(candidate, current) > 0

def normalize_release_tag(tag):
    value = tag.strip()
    if value.startswith("v"):
        value = value[1:]
    semver_tuple(value)
    return value

def apply_release_version(tag, root=ROOT, check_only=False):
    root = Path(root)
    try:
        candidate = normalize_release_tag(tag)
    except ValueError:
        print(f"Skipping release metadata sync: release tag {tag!r} is not semver major.minor.patch.")
        return None
    current = version(root)
    if not is_strictly_newer(candidate, current):
        print(
            f"Release {tag} ({candidate}) is not newer than VERSION {current}; "
            "skipping metadata sync."
        )
        return None
    if check_only:
        return candidate
    path = root / "VERSION"
    path.write_text(candidate + "\n", encoding="utf-8", newline="\n")
    synchronize(root)
    return candidate

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
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--apply-release",
        metavar="TAG",
        help="Write VERSION only when TAG is strictly newer than the current file",
    )
    options = parser.parse_args()
    if options.apply_release:
        result = apply_release_version(options.apply_release)
        if result is None:
            raise SystemExit(0)
        print("v" + result)
    else:
        print(synchronize(check=options.check))