from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

from tests.test_import_output_adapter import base_args
from tests.test_import_output_adapter import write_manifest


REPO_ROOT = Path(__file__).resolve().parents[1]
BUILD_BUNDLE = REPO_ROOT / "bin" / "artist-os-build-bundle"
VERSION = (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip()


def run(command: list[str], *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )


class ReleaseBundleTests(unittest.TestCase):
    def build(self, output_root: Path) -> tuple[Path, Path]:
        proc = run([sys.executable, str(BUILD_BUNDLE), "--output-root", str(output_root)])
        self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
        bundle = output_root / f"artist-os-{VERSION}"
        archive = output_root / f"artist-os-{VERSION}-codex.tar.gz"
        return bundle, archive

    def extract(self, archive: Path, destination: Path) -> Path:
        destination.mkdir(parents=True)
        with tarfile.open(archive, "r:gz") as handle:
            handle.extractall(destination, filter="data")
        return destination / f"artist-os-{VERSION}"

    def old_release_copy(self, current: Path, destination: Path) -> Path:
        shutil.copytree(current, destination)
        (destination / "VERSION").write_text("0.9.0\n", encoding="utf-8")
        (destination / "OLD-RELEASE-ONLY.txt").write_text(
            "This file must disappear during update.\n",
            encoding="utf-8",
        )
        old_runtime = destination / "bin" / "artist-os-paths"
        old_runtime.write_text(
            old_runtime.read_text(encoding="utf-8") + "\n# old release marker\n",
            encoding="utf-8",
        )
        metadata_path = destination / "RELEASE-METADATA.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata["version"] = "0.9.0"
        metadata_path.write_text(
            json.dumps(metadata, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return destination

    def test_build_materializes_and_verifies_independent_codex_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_root = Path(tmpdir)
            ignored_local_file = REPO_ROOT / "docs" / "IMPLEMENTATION_PLAN.md"
            prior_contents = (
                ignored_local_file.read_bytes() if ignored_local_file.exists() else None
            )
            ignored_local_file.write_text("local-only release notes\n", encoding="utf-8")
            try:
                bundle, archive = self.build(output_root)
            finally:
                if prior_contents is None:
                    ignored_local_file.unlink()
                else:
                    ignored_local_file.write_bytes(prior_contents)

            self.assertTrue((bundle / "SKILL.md").is_file())
            self.assertTrue((bundle / "LICENSE").is_file())
            self.assertTrue((bundle / "bin" / "install-codex-skills").is_file())
            self.assertFalse((bundle / "bin" / "artist-os-eval").exists())
            self.assertFalse((bundle / "tests").exists())
            self.assertFalse((bundle / ".git").exists())
            self.assertFalse(any(bundle.rglob("*.sqlite")))
            self.assertFalse(any(bundle.rglob(".env")))
            self.assertFalse(any(bundle.rglob("__pycache__")))
            self.assertFalse((bundle / "docs" / "IMPLEMENTATION_PLAN.md").exists())
            self.assertFalse((bundle / "release-evidence").exists())

            metadata = json.loads((bundle / "RELEASE-METADATA.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["version"], VERSION)
            self.assertEqual(metadata["host"], "codex")
            self.assertRegex(metadata["commit_sha"], r"^[0-9a-f]{40}$")

            doctor_env = os.environ.copy()
            doctor_env["ARTIST_OS_ROOT"] = str(bundle)
            doctor = run([str(bundle / "bin" / "artist-os-paths"), "doctor"], env=doctor_env)
            self.assertEqual(doctor.returncode, 0, msg=doctor.stdout + doctor.stderr)

            checksum_path = archive.with_suffix(archive.suffix + ".sha256")
            expected_checksum = checksum_path.read_text(encoding="utf-8").split()[0]
            self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(), expected_checksum)
            with tarfile.open(archive, "r:gz") as handle:
                names = handle.getnames()
            self.assertIn(f"artist-os-{VERSION}/SKILL.md", names)
            self.assertNotIn(f"artist-os-{VERSION}/bin/artist-os-eval", names)

    def test_copy_install_update_resume_import_and_uninstall_survive_moved_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _bundle, archive = self.build(root / "build")
            current_bundle = self.extract(archive, root / "extracted-current")
            old_bundle = self.old_release_copy(current_bundle, root / "old-release")
            skills_dir = root / "codex-skills"
            wondermint_root = root / "wondermint-root"
            env = os.environ.copy()
            env.pop("ARTIST_OS_ROOT", None)
            env["CODEX_SKILLS_DIR"] = str(skills_dir)
            env["WONDERMINT_ROOT"] = str(wondermint_root)

            install = run(
                [str(old_bundle / "bin" / "install-codex-skills"), "--mode", "copy"],
                env=env,
            )
            self.assertEqual(install.returncode, 0, msg=install.stdout + install.stderr)
            installed = skills_dir / "artist-os"
            self.assertTrue(installed.is_dir())
            self.assertFalse(installed.is_symlink())
            self.assertEqual((installed / "VERSION").read_text().strip(), "0.9.0")
            self.assertTrue((installed / "OLD-RELEASE-ONLY.txt").is_file())

            update = run(
                [str(current_bundle / "bin" / "install-codex-skills"), "--mode", "copy"],
                env=env,
            )
            self.assertEqual(update.returncode, 0, msg=update.stdout + update.stderr)
            self.assertEqual((installed / "VERSION").read_text(encoding="utf-8").strip(), VERSION)
            self.assertFalse((installed / "OLD-RELEASE-ONLY.txt").exists())
            self.assertEqual(
                (installed / "bin" / "artist-os-paths").read_bytes(),
                (current_bundle / "bin" / "artist-os-paths").read_bytes(),
            )

            current_bundle.rename(root / "retired-release-bundle")
            self._exercise_installed_runtime(installed, wondermint_root, env)

            uninstall = run([str(installed / "bin" / "uninstall-codex-skills")], env=env)
            self.assertEqual(uninstall.returncode, 0, msg=uninstall.stdout + uninstall.stderr)
            self.assertFalse(installed.exists())
            self.assertTrue((wondermint_root / ".wondermint" / "artist-os").is_dir())

    def test_symlink_install_update_resume_import_and_uninstall(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _bundle, archive = self.build(root / "build")
            current_bundle = self.extract(archive, root / "extracted-current")
            old_bundle = self.old_release_copy(current_bundle, root / "old-release")
            skills_dir = root / "codex-skills"
            wondermint_root = root / "wondermint-root"
            env = os.environ.copy()
            env.pop("ARTIST_OS_ROOT", None)
            env["CODEX_SKILLS_DIR"] = str(skills_dir)
            env["WONDERMINT_ROOT"] = str(wondermint_root)

            install = run(
                [str(old_bundle / "bin" / "install-codex-skills"), "--mode", "symlink"],
                env=env,
            )
            self.assertEqual(install.returncode, 0, msg=install.stdout + install.stderr)
            update = run(
                [str(current_bundle / "bin" / "install-codex-skills"), "--mode", "symlink"],
                env=env,
            )
            self.assertEqual(update.returncode, 0, msg=update.stdout + update.stderr)

            installed = skills_dir / "artist-os"
            self.assertTrue(installed.is_symlink())
            self.assertEqual(installed.resolve(), current_bundle.resolve())
            self.assertEqual((installed / "VERSION").read_text().strip(), VERSION)
            self.assertFalse((installed / "OLD-RELEASE-ONLY.txt").exists())
            self.assertEqual(
                (installed / "bin" / "artist-os-paths").read_bytes(),
                (current_bundle / "bin" / "artist-os-paths").read_bytes(),
            )
            self._exercise_installed_runtime(installed, wondermint_root, env)

            uninstall = run(
                [str(current_bundle / "bin" / "uninstall-codex-skills")],
                env=env,
            )
            self.assertEqual(uninstall.returncode, 0, msg=uninstall.stdout + uninstall.stderr)
            self.assertFalse(installed.exists())
            self.assertTrue((wondermint_root / ".wondermint" / "artist-os").is_dir())

    def test_failed_update_restores_previous_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            _bundle, archive = self.build(root / "build")
            current_bundle = self.extract(archive, root / "extracted-current")
            old_bundle = self.old_release_copy(current_bundle, root / "old-release")
            skills_dir = root / "codex-skills"
            wondermint_root = root / "wondermint-root"
            env = os.environ.copy()
            env["CODEX_SKILLS_DIR"] = str(skills_dir)
            env["WONDERMINT_ROOT"] = str(wondermint_root)

            install = run(
                [str(old_bundle / "bin" / "install-codex-skills"), "--mode", "copy"],
                env=env,
            )
            self.assertEqual(install.returncode, 0, msg=install.stdout + install.stderr)

            invalid_root = root / "not-a-directory"
            invalid_root.write_text("blocked\n", encoding="utf-8")
            failed_env = env.copy()
            failed_env["WONDERMINT_ROOT"] = str(invalid_root)
            update = run(
                [str(current_bundle / "bin" / "install-codex-skills"), "--mode", "copy"],
                env=failed_env,
            )
            self.assertNotEqual(update.returncode, 0)
            self.assertIn("prior Artist OS installation restored", update.stderr)
            installed = skills_dir / "artist-os"
            self.assertEqual((installed / "VERSION").read_text().strip(), "0.9.0")

    def _exercise_installed_runtime(
        self,
        installed: Path,
        wondermint_root: Path,
        env: dict[str, str],
    ) -> None:
        runtime_env = env.copy()
        runtime_env["ARTIST_OS_ROOT"] = str(installed)
        doctor = run([str(installed / "bin" / "artist-os-paths"), "doctor"], env=runtime_env)
        self.assertEqual(doctor.returncode, 0, msg=doctor.stdout + doctor.stderr)

        library_root = wondermint_root / ".wondermint" / "artist-os"
        project_dir = library_root / "projects" / "proj_release_smoke"
        project_dir.mkdir(parents=True, exist_ok=True)
        manifest = json.loads(
            (REPO_ROOT / "examples" / "project-manifest.example.json").read_text(encoding="utf-8")
        )
        manifest["project_id"] = "proj_release_smoke"
        manifest["title"] = "Release Smoke"
        manifest["summary"] = "Disposable installed-runtime resume fixture."
        manifest["paths"]["project_dir"] = "projects/proj_release_smoke"
        manifest["paths"]["events"] = "projects/proj_release_smoke/events.jsonl"
        (project_dir / "project.json").write_text(json.dumps(manifest), encoding="utf-8")
        (project_dir / "events.jsonl").write_text("", encoding="utf-8")

        sync = run(
            [
                str(installed / "bin" / "artist-os-db"),
                "sync",
                "--project",
                "proj_release_smoke",
                "--wondermint-root",
                str(wondermint_root),
            ],
            env=runtime_env,
        )
        self.assertEqual(sync.returncode, 0, msg=sync.stdout + sync.stderr)
        resume = run(
            [
                str(installed / "bin" / "artist-os-db"),
                "show",
                "proj_release_smoke",
                "--wondermint-root",
                str(wondermint_root),
            ],
            env=runtime_env,
        )
        self.assertEqual(resume.returncode, 0, msg=resume.stdout + resume.stderr)
        self.assertIn("Release Smoke", resume.stdout)

        write_manifest(library_root)
        artifact = wondermint_root / "release-import.png"
        artifact.write_bytes(b"release import smoke")
        import_args = base_args(library_root, artifact)
        import_args[1] = str(installed / "bin" / "artist-os-import-output")
        imported = run(import_args, env=runtime_env)
        self.assertEqual(imported.returncode, 0, msg=imported.stdout + imported.stderr)
        self.assertIn("imported output record", imported.stdout)


if __name__ == "__main__":
    unittest.main()
