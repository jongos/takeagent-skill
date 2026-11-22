import importlib.util
import tempfile
import unittest
from pathlib import Path
import test_package_skill as fixtures
package = fixtures.package

def load_script(name):
    path = Path(__file__).resolve().parents[1] / "scripts" / (name + ".py")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

sync = load_script("sync_version")
release = load_script("verify_release")
policy = load_script("content_policy")

class PublicContentPolicyTests(unittest.TestCase):
    def test_repository_packaged_files_pass_policy(self):
        policy.check_repository(Path(__file__).resolve().parents[1])

    def test_private_names_and_contacts_fail_policy(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        skill = root / "skills/takeagent-skill/references"
        skill.mkdir(parents=True)
        (root / "README.md").write_text("ok\n", encoding="utf-8")
        (root / "LICENSE").write_text("info@filmhedge.com\n", encoding="utf-8")
        (skill / "setup.md").write_text("see takeagent-excel repo\n", encoding="utf-8")
        (root / "skills/takeagent-skill/SKILL.md").write_text("---\nname: takeagent-skill\ndescription: x\n---\n", encoding="utf-8")
        (root / "skills/takeagent-skill/references/workflows.md").write_text("ok\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "takeagent-excel"):
            policy.check_repository(root)

    def test_private_host_repo_link_fails_policy(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        skill = root / "skills/takeagent-skill"
        (skill / "references").mkdir(parents=True)
        for name, body in [
            ("SKILL.md", "---\nname: takeagent-skill\ndescription: x\n---\n"),
            ("references/setup.md", "https://github.com/jongos/takeagent/issues/1\n"),
            ("references/workflows.md", "ok\n"),
        ]:
            (skill / name).parent.mkdir(parents=True, exist_ok=True)
            (skill / name).write_text(body, encoding="utf-8")
        (root / "README.md").write_text("ok\n", encoding="utf-8")
        (root / "LICENSE").write_text("info@filmhedge.com\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "private host"):
            policy.check_repository(root)

    def test_disallowed_email_fails_policy(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        skill = root / "skills/takeagent-skill"
        (skill / "references").mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: takeagent-skill\ndescription: x\n---\n", encoding="utf-8")
        (skill / "references/setup.md").write_text("contact ops@evil.example\n", encoding="utf-8")
        (skill / "references/workflows.md").write_text("ok\n", encoding="utf-8")
        (root / "README.md").write_text("ok\n", encoding="utf-8")
        (root / "LICENSE").write_text("info@filmhedge.com\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "ops@evil.example"):
            policy.check_repository(root)


class MetadataAndMarkdownTests(unittest.TestCase):
    setUp = fixtures.PackageTests.setUp

    def set_main(self, text):
        (self.skill / "SKILL.md").write_text(text, encoding="utf-8")

    def test_yaml_order_quotes_and_multiline_are_supported(self):
        for description in ['"A description: with a colon"', '>\n  A multiline\n  description']:
            with self.subTest(description=description):
                self.set_main("---\ndescription: " + description + "\nname: takeagent-skill\n---\n")
                package.build(self.root)

    def test_invalid_yaml_types_duplicates_and_tags_are_rejected(self):
        for metadata in [
            "name: takeagent-skill\ndescription: [unterminated",
            "name: takeagent-skill\ndescription: [list]",
            "name: takeagent-skill\ndescription: null",
            "name: takeagent-skill\ndescription: true",
            "name: takeagent-skill\ndescription: good\ndescription: bad",
            "name: takeagent-skill\ndescription: !!python/object:example {}",
            "name: takeagent-skill\ndescription: &a words",
        ]:
            with self.subTest(metadata=metadata):
                self.set_main("---\n" + metadata + "\n---\n")
                with self.assertRaises(ValueError):
                    package.build(self.root)

    def test_reference_style_link_is_checked(self):
        self.set_main(self.main_text() + "\n[Guide][setup]\n\n[setup]: missing.md\n")
        with self.assertRaisesRegex(ValueError, "absent from package"):
            package.build(self.root)

    def main_text(self):
        return "---\nname: takeagent-skill\ndescription: Fixture.\n---\n"

    def test_reference_style_valid_link_and_title_work(self):
        self.set_main(self.main_text() + '\n[Guide][setup]\n\n[setup]: references/setup.md "Setup guide"\n')
        package.build(self.root)

    def test_code_examples_are_not_validated_as_links(self):
        self.set_main(self.main_text() + "\n~~~markdown\n[Example](missing.md)\n[ref]: missing.md\n~~~\n\n    [Indented](missing.md)\n\n\u0060[Inline](missing.md)\u0060\n")
        package.build(self.root)

    def test_image_and_autolink_destinations_are_checked(self):
        for body in ["![Image](missing.png)", "<http://example.com>", "[Guide][bad]\n\n[bad]: javascript:alert"]:
            with self.subTest(body=body):
                self.set_main(self.main_text() + "\n" + body)
                with self.assertRaises(ValueError):
                    package.build(self.root)

class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "docs").mkdir()
        (self.root / "VERSION").write_text("0.1.3\n")
        self.base = "https://github.com/jongos/takeagent-skill/releases/"
        readme = (
            self.base
            + "download/v0.1.2/takeagent-skill.zip) · [Release notes]("
            + self.base
            + "tag/v0.1.2)"
        )
        (self.root / "README.md").write_text(readme)
        landing = (
            "TAKEAGENT SKILL · v0.1.2 "
            + sync.LATEST_DOWNLOAD
            + " "
            + sync.LATEST_RELEASE
            + " "
            + sync.LATEST_DOWNLOAD
        )
        (self.root / "docs/index.html").write_text(landing, encoding="utf-8")

    def test_stale_version_links_fail_check_and_sync_repairs(self):
        with self.assertRaisesRegex(ValueError, "stale"):
            sync.synchronize(self.root, check=True)
        self.assertEqual(sync.synchronize(self.root), "v0.1.3")
        self.assertEqual(sync.synchronize(self.root, check=True), "v0.1.3")
        readme = (self.root / "README.md").read_text()
        self.assertIn(sync.LATEST_DOWNLOAD, readme)
        self.assertIn(sync.LATEST_RELEASE, readme)
        self.assertNotIn("/v0.1.3/", readme)
        self.assertIn("TAKEAGENT SKILL · v0.1.3", (self.root / "docs/index.html").read_text())

    def test_readme_versioned_release_urls_fail_check(self):
        readme = (
            self.base
            + "download/v0.1.3/takeagent-skill.zip) · [Release notes]("
            + self.base
            + "tag/v0.1.3)"
        )
        (self.root / "README.md").write_text(readme)
        landing = (
            "TAKEAGENT SKILL · v0.1.3 "
            + sync.LATEST_DOWNLOAD
            + " "
            + sync.LATEST_RELEASE
            + " "
            + sync.LATEST_DOWNLOAD
        )
        (self.root / "docs/index.html").write_text(landing, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "stale: README"):
            sync.synchronize(self.root, check=True)

    def test_pinned_landing_release_urls_are_rejected(self):
        pinned = (
            "TAKEAGENT SKILL · v0.1.3 "
            + self.base
            + "download/v0.1.2/takeagent-skill.zip"
        )
        (self.root / "docs/index.html").write_text(pinned, encoding="utf-8")
        readme = (
            sync.LATEST_DOWNLOAD
            + ") · [Release notes]("
            + sync.LATEST_RELEASE
            + ")"
        )
        (self.root / "README.md").write_text(readme)
        with self.assertRaisesRegex(ValueError, "latest-release download URL"):
            sync.synchronize(self.root, check=True)

    def test_unsafe_version_is_rejected(self):
        (self.root / "VERSION").write_text("../main")
        with self.assertRaises(ValueError):
            sync.synchronize(self.root)

    def test_compare_semver_orders_numeric_parts(self):
        self.assertEqual(sync.compare_semver("0.1.12", "0.1.13"), -1)
        self.assertEqual(sync.compare_semver("0.2.0", "0.1.99"), 1)
        self.assertEqual(sync.compare_semver("1.0.0", "1.0.0"), 0)

    def test_apply_release_skips_older_or_equal_tags(self):
        (self.root / "VERSION").write_text("0.1.13\n")
        self.assertIsNone(sync.apply_release_version("v0.1.8", root=self.root))
        self.assertEqual((self.root / "VERSION").read_text(), "0.1.13\n")

    def test_apply_release_skips_malformed_tag(self):
        (self.root / "VERSION").write_text("0.1.13\n")
        self.assertIsNone(sync.apply_release_version("vnot-semver", root=self.root))
        self.assertEqual((self.root / "VERSION").read_text(), "0.1.13\n")

    def test_apply_release_updates_on_newer_tag(self):
        (self.root / "VERSION").write_text("0.1.12\n")
        readme = (
            sync.LATEST_DOWNLOAD
            + ") · [Release notes]("
            + sync.LATEST_RELEASE
            + ")"
        )
        (self.root / "README.md").write_text(readme)
        landing = (
            "TAKEAGENT SKILL · v0.1.12 "
            + sync.LATEST_DOWNLOAD
            + " "
            + sync.LATEST_RELEASE
            + " "
            + sync.LATEST_DOWNLOAD
        )
        (self.root / "docs/index.html").write_text(landing, encoding="utf-8")
        self.assertEqual(sync.apply_release_version("v0.1.13", root=self.root), "0.1.13")
        self.assertEqual((self.root / "VERSION").read_text(), "0.1.13\n")
        self.assertIn("TAKEAGENT SKILL · v0.1.13", (self.root / "docs/index.html").read_text())

    def assets(self):
        import hashlib
        built, downloaded = self.root / "built", self.root / "downloaded"
        built.mkdir(); downloaded.mkdir()
        data = b"fixture archive bytes"
        digest = hashlib.sha256(data).hexdigest()
        for directory in (built, downloaded):
            (directory / "takeagent-skill.zip").write_bytes(data)
            (directory / "takeagent-skill.zip.sha256").write_text(digest + "  takeagent-skill.zip\n")
        return built, downloaded, digest

    def test_matching_release_assets_pass(self):
        built, downloaded, digest = self.assets()
        self.assertEqual(release.verify(built, downloaded, "v0.1.3", self.root / "VERSION"), digest)

    def test_tampered_zip_is_rejected_even_with_matching_new_receipt(self):
        import hashlib
        built, downloaded, _ = self.assets()
        data = b"different archive"
        (downloaded / "takeagent-skill.zip").write_bytes(data)
        (downloaded / "takeagent-skill.zip.sha256").write_text(hashlib.sha256(data).hexdigest() + "  takeagent-skill.zip\n")
        with self.assertRaisesRegex(ValueError, "differs"):
            release.verify(built, downloaded, "v0.1.3", self.root / "VERSION")

    def test_tampered_checksum_is_rejected(self):
        built, downloaded, _ = self.assets()
        (downloaded / "takeagent-skill.zip.sha256").write_text("wrong")
        with self.assertRaisesRegex(ValueError, "checksum"):
            release.verify(built, downloaded, "v0.1.3", self.root / "VERSION")

    def test_wrong_tag_is_rejected(self):
        built, downloaded, _ = self.assets()
        with self.assertRaisesRegex(ValueError, "tag"):
            release.verify(built, downloaded, "v9.9.9", self.root / "VERSION")
