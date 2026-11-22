"""Fail CI when packaged or public instruction files leak private names or contacts."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

PRIVATE_REPO_NAMES = (
    "takeagent-excel",
    "takeagent-website",
    "takeagent-smartaccounting-old",
)
INTERNAL_TERMS = (
    "MH Brain",
    "MH Credit",
    "Black-Top",
    "Neon",
    "DATABASE_URL",
)
ALLOWED_EMAIL = "info@filmhedge.com"
EXCEL_INTEGRATION_URL = "https://takeagent.ai/integrations/takeagent-excel"
PRIVATE_HOST_REPO = re.compile(
    r"https?://github\.com/jongos/takeagent(?![-\w])"
)
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")


def scrub_allowlisted_phrases(text):
    """Remove sanctioned public URLs before scanning for private repository names."""
    return text.replace(EXCEL_INTEGRATION_URL, "")

PACKAGED_SKILL_FILES = (
    "skills/takeagent-skill/SKILL.md",
    "skills/takeagent-skill/references/setup.md",
    "skills/takeagent-skill/references/workflows.md",
)
PUBLIC_SCAN_FILES = PACKAGED_SKILL_FILES + ("README.md", "LICENSE")


def violations_in_text(text, label):
    issues = []
    scrubbed = scrub_allowlisted_phrases(text)
    for term in PRIVATE_REPO_NAMES + INTERNAL_TERMS:
        if term in scrubbed:
            issues.append(f"{label}: disallowed term {term!r}")
    if PRIVATE_HOST_REPO.search(text):
        issues.append(f"{label}: private host repository link")
    for email in EMAIL_RE.findall(text):
        if email.lower() != ALLOWED_EMAIL.lower():
            issues.append(f"{label}: disallowed email {email!r}")
    return issues


def collect_violations(root=ROOT):
    issues = []
    for relative in PUBLIC_SCAN_FILES:
        path = Path(root) / relative
        if not path.is_file():
            issues.append(f"missing scan path: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        issues.extend(violations_in_text(text, relative))
    return issues


def check_repository(root=ROOT):
    issues = collect_violations(root)
    if issues:
        raise ValueError("Public content policy violations:\n" + "\n".join(issues))


def main():
    try:
        check_repository()
    except ValueError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()