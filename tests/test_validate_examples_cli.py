from __future__ import annotations

import argparse
import importlib.util
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "bin" / "validate-examples"


def load_validate_examples_module():
    loader = SourceFileLoader("validate_examples_cli", str(SCRIPT_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None:
        raise RuntimeError(f"cannot load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class ValidateExamplesCliTests(unittest.TestCase):
    def test_zero_validation_targets_is_a_failure(self) -> None:
        module = load_validate_examples_module()
        parsed = argparse.Namespace(examples_only=False)
        fake_parser = mock.Mock()
        fake_parser.parse_args.return_value = parsed

        with (
            mock.patch.object(module, "parser", return_value=fake_parser),
            mock.patch.object(module, "iter_validation_targets", return_value=[]),
            mock.patch("builtins.print"),
        ):
            self.assertEqual(module.main(), 1)


if __name__ == "__main__":
    unittest.main()
