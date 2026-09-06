import unittest

from generators.error_pages import render_not_found_page


class NotFoundPageTests(unittest.TestCase):
    def test_custom_page_is_noindex_and_has_no_canonical_or_redirect(self):
        html = render_not_found_page()

        self.assertIn('data-not-found-page="true"', html)
        self.assertIn('<meta name="robots" content="noindex, follow">', html)
        self.assertNotIn('<link rel="canonical"', html)
        self.assertNotIn('http-equiv="refresh"', html.lower())

    def test_custom_page_has_recovery_routes(self):
        html = render_not_found_page()

        for route in ("/", "/tools/", "/councils/", "/workflows/", "/my-planning-project/"):
            self.assertIn(f'href="{route}"', html)


if __name__ == "__main__":
    unittest.main()
