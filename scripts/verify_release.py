"""Compare downloaded release assets against a rebuild from the checked-out tag."""
from pathlib import Path
import argparse
import hashlib
import re

def verify(built, downloaded, expected_tag, version_file):
    expected = "v" + Path(version_file).read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"v\d+\.\d+\.\d+", expected_tag) or expected_tag != expected:
        raise ValueError("Release tag does not match VERSION")
    built, downloaded = Path(built), Path(downloaded)
    archive = "takeagent-skill.zip"
    receipt = archive + ".sha256"
    source_bytes = (built / archive).read_bytes()
    release_bytes = (downloaded / archive).read_bytes()
    digest = hashlib.sha256(source_bytes).hexdigest()
    expected_receipt = digest + "  " + archive + "\n"
    if source_bytes != release_bytes:
        raise ValueError("Published ZIP differs from checked-out source build")
    if (built / receipt).read_text(encoding="ascii") != expected_receipt:
        raise ValueError("Build checksum is inconsistent")
    if (downloaded / receipt).read_text(encoding="ascii") != expected_receipt:
        raise ValueError("Published checksum differs from source build")
    return digest

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--built", default="dist")
    parser.add_argument("--downloaded", default="downloaded")
    parser.add_argument("--tag", required=True)
    parser.add_argument("--version-file", default="VERSION")
    args = parser.parse_args()
    print("Verified published assets: " + verify(args.built, args.downloaded, args.tag, args.version_file))
