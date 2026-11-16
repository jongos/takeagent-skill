import hashlib
import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("package_skill", Path(__file__).resolve().parents[1] / "scripts/package_skill.py")
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)

class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / "skills/takeagent-skill"
        (self.skill / "references").mkdir(parents=True)
        self.main = "---\nname: takeagent-skill\ndescription: Test fixture.\n---\n\n[Setup](references/setup.md)\n"
        (self.skill / "SKILL.md").write_text(self.main, encoding="utf-8")
        (self.skill / "references/setup.md").write_text("Setup\n", encoding="utf-8")
        (self.skill / "references/workflows.md").write_text("Workflows\n", encoding="utf-8")

    def test_only_allowlisted_files_are_published(self):
        (self.skill / ".env").write_text("DO_NOT_PACKAGE", encoding="utf-8")
        archive, digest = package.build(self.root)
        with zipfile.ZipFile(archive) as bundle:
            self.assertEqual(bundle.namelist(), ["takeagent-skill/" + n for n in package.FILES])
            self.assertNotIn(b"DO_NOT_PACKAGE", b"".join(bundle.read(n) for n in bundle.namelist()))
        self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(), digest)
        self.assertEqual(archive.with_suffix(".zip.sha256").read_text(), digest + "  takeagent-skill.zip\n")

    def test_atomic_write_failure_preserves_previous_file_and_cleans_temp(self):
        target = self.root / "artifact"
        target.write_bytes(b"previous")
        with patch.object(package.os, "replace", side_effect=OSError("synthetic replace failure")):
            with self.assertRaisesRegex(OSError, "synthetic replace failure"):
                package.atomic_write(self.root, target, b"replacement")
        self.assertEqual(target.read_bytes(), b"previous")
        self.assertEqual(list(self.root.glob(".skill-*")), [])

    def test_atomic_write_replaces_complete_file_and_cleans_temp(self):
        target = self.root / "artifact"
        target.write_bytes(b"previous")
        package.atomic_write(self.root, target, b"replacement")
        self.assertEqual(target.read_bytes(), b"replacement")
        self.assertEqual(list(self.root.glob(".skill-*")), [])

    def test_line_endings_do_not_change_release(self):
        archive, digest = package.build(self.root)
        first = archive.read_bytes()
        for name in package.FILES:
            path = self.skill / name
            path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
        archive, second = package.build(self.root)
        self.assertEqual(first, archive.read_bytes())
        self.assertEqual(digest, second)

    def test_reference_to_unshipped_file_is_rejected(self):
        (self.skill / "hidden.md").write_text("Not in ZIP")
        (self.skill / "SKILL.md").write_text(self.main + "[Hidden](hidden.md)")
        with self.assertRaisesRegex(ValueError, "absent from package"):
            package.build(self.root)

    def test_escape_reference_is_rejected(self):
        (self.root / "outside.md").write_text("Private")
        (self.skill / "SKILL.md").write_text(self.main + "[Outside](../../outside.md)")
        with self.assertRaises(ValueError):
            package.build(self.root)

    def test_encoded_escape_reference_is_rejected(self):
        (self.skill / "SKILL.md").write_text(self.main + "[Outside](%2e%2e/%2e%2e/outside.md)")
        with self.assertRaises(ValueError):
            package.build(self.root)

    def test_unsafe_link_schemes_are_rejected(self):
        for target in ["file:///private", "javascript:alert", "//evil.example/file", "https://user:password@example.com"]:
            with self.subTest(target=target):
                (self.skill / "SKILL.md").write_text(self.main + f"[Link]({target})")
                with self.assertRaisesRegex(ValueError, "Unsafe link"):
                    package.build(self.root)

    def test_failed_validation_preserves_last_good_archive(self):
        archive, _ = package.build(self.root)
        before = archive.read_bytes()
        receipt = archive.with_suffix(".zip.sha256").read_bytes()
        (self.skill / "SKILL.md").write_text("---\nname: wrong\n---\n")
        with self.assertRaises(ValueError):
            package.build(self.root)
        self.assertEqual(before, archive.read_bytes())
        self.assertEqual(receipt, archive.with_suffix(".zip.sha256").read_bytes())

    def test_size_limit_is_enforced(self):
        (self.skill / "references/setup.md").write_bytes(b"x" * (package.MAX_FILE_BYTES + 1))
        with self.assertRaisesRegex(ValueError, "too large"):
            package.build(self.root)

    def test_snapshot_is_the_packaged_content(self):
        original = package.archive_bytes
        def change_after_validation(content):
            (self.skill / "references/setup.md").write_text("Changed after validation")
            return original(content)
        with patch.object(package, "archive_bytes", side_effect=change_after_validation):
            archive, _ = package.build(self.root)
        with zipfile.ZipFile(archive) as bundle:
            self.assertEqual(bundle.read("takeagent-skill/references/setup.md"), b"Setup\n")

    def link(self, target, link, directory=False):
        try:
            link.symlink_to(target, target_is_directory=directory)
        except OSError as error:
            self.skipTest(f"OS does not permit test symlinks: {error}")

    def test_linked_input_file_is_rejected(self):
        target = self.root / "external.md"
        target.write_text("Private")
        path = self.skill / "references/setup.md"
        path.unlink()
        self.link(target, path)
        with self.assertRaisesRegex(ValueError, "Linked/reparse"):
            package.build(self.root)

    def test_linked_skill_root_is_rejected(self):
        original = self.root / "moved"
        self.skill.rename(original)
        self.link(original, self.skill, True)
        with self.assertRaisesRegex(ValueError, "Linked/reparse"):
            package.build(self.root)

    def test_linked_output_does_not_overwrite_target(self):
        out = self.root / "dist"
        out.mkdir()
        target = self.root / "important.txt"
        target.write_text("Keep")
        self.link(target, out / "takeagent-skill.zip")
        with self.assertRaisesRegex(ValueError, "Linked/reparse"):
            package.build(self.root)
        self.assertEqual(target.read_text(), "Keep")

if __name__ == "__main__":
    unittest.main()
