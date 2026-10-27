import unittest

from generators.link_graph import build_link_graph


class LinkGraphDeterminismTests(unittest.TestCase):
    def test_repeated_builds_produce_identical_link_graphs(self):
        self.assertEqual(build_link_graph(), build_link_graph())


if __name__ == "__main__":
    unittest.main()
