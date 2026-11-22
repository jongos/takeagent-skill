"""Fail CI when tracked text leaks private names, host-repo links, or contacts."""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

ALLOWED_EMAIL = "info@filmhedge.com"
EXCEL_INTEGRATION_URL = "https://takeagent.ai/integrations/takeagent-excel"
ALLOWED_HOST_REPO_SUFFIXES = (
    "-skill",
    "-greenslate",
    "-saturation",
    "-smartaccounting",
    "-wrapbook",
)
PRIVATE_REPO_TERMS = (
    "takeagent-excel",
    "takeagent-website",
    "takeagent-smartaccounting-old",
)
INTERNAL_TERMS = (
    "mh brain",
    "mediahedge brain",
    "mh credit",
    "black-top",
    "neon",
    "database_url",
)
TEXT_EXTENSIONS = {".md", ".txt", ".html", ".js", ".css", ".yml", ".yaml", ".py"}
TEXT_NAMES = {"LICENSE", "VERSION"}
POLICY_EXCLUDE_PREFIXES = ("tests/",)
POLICY_EXCLUDE_FILES = {"scripts/content_policy.py"}
HOST_REPO = re.compile(
    r"(?:https?://)?github\.com/jongos/takeagent(?![-\w])",
    re.IGNORECASE,
)
EMAIL_RE = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)
OBFUSCATED_EMAIL_BRACKET = re.compile(
    r"\b[\w.]+\s*\[(?:at)\]\s*[\w.]+\s*\[(?:dot)\]\s*[\w.]+\b",
    re.IGNORECASE,
)
OBFUSCATED_EMAIL_PAREN = re.compile(
    r"\b[\w.]+\s*\((?:at)\)\s*[\w.]+\s*\((?:dot)\)\s*[\w.]+\b",
    re.IGNORECASE,
)


def scrub_allowlisted_phrases(text):
    return text.replace(EXCEL_INTEGRATION_URL, "")


def iter_tracked_text_files(root):
    listing = subprocess.run(
        ["git", "-C", str(root), "ls-files"],
        capture_output=True,
        text=True,
        check=False,
    )
    if listing.returncode != 0:
        raise ValueError("git ls-files failed; run content policy from a git checkout")
    for relative in listing.stdout.splitlines():
        if not relative:
            continue
        if relative in POLICY_EXCLUDE_FILES or relative.startswith(POLICY_EXCLUDE_PREFIXES):
            continue
        path = Path(relative)
        if path.suffix.lower() in TEXT_EXTENSIONS or path.name in TEXT_NAMES:
            yield root / relative


def violations_in_text(text, label):
    issues = []
    lower = scrub_allowlisted_phrases(text).casefold()
    for term in PRIVATE_REPO_TERMS + INTERNAL_TERMS:
        if term.casefold() in lower:
            issues.append(f"{label}: disallowed term {term!r}")
    for match in HOST_REPO.finditer(text):
        tail = text[match.end() : match.end() + 32].casefold()
        if any(tail.startswith(suffix) for suffix in ALLOWED_HOST_REPO_SUFFIXES):
            continue
        issues.append(f"{label}: private host repository link")
        break
    for email in EMAIL_RE.findall(text):
        if email.casefold() != ALLOWED_EMAIL.casefold():
            issues.append(f"{label}: disallowed email {email!r}")
    if OBFUSCATED_EMAIL_BRACKET.search(text) or OBFUSCATED_EMAIL_PAREN.search(text):
        issues.append(f"{label}: disallowed obfuscated email")
    return issues


def collect_violations(root=ROOT):
    issues = []
    for path in iter_tracked_text_files(root):
        if not path.is_file():
            issues.append(f"missing scan path: {path.relative_to(root).as_posix()}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        label = path.relative_to(root).as_posix()
        issues.extend(violations_in_text(text, label))
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