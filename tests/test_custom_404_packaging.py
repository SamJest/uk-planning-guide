import importlib.util
from pathlib import Path
import unittest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "43_package_custom_404.py"
SPEC = importlib.util.spec_from_file_location("custom_404_packaging", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class Custom404PackagingTests(unittest.TestCase):
    def test_expected_release_is_add_only_and_preserves_url_counts(self):
        self.assertEqual(MODULE.EXPECTED_PRODUCTION_COMMIT, "7749cbba33bc06075424a82ec7f733822acfbc57")
        self.assertEqual(MODULE.EXPECTED_PRODUCTION_TREE, "bd141850da7f1fceeb208c4e52b5b22296547d01")


if __name__ == "__main__":
    unittest.main()
