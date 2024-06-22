import unittest

from sanitize_html import sanitize


class TestHtmlSanitize(unittest.TestCase):

    def test_none_on_empty(self):
        sanitized_output = sanitize("")
        self.assertIsNone(sanitized_output)


    def test_removes_unsafe_attributes(self):
        input_html = "<div><p style='width: 20;background-image: `wingnut.png`;'>This has an unsafe style attribute</p></div>"
        expected_output = "<div><p>This has an unsafe style attribute</p></div>"
        sanitized_output = sanitize(input_html)
        self.assertEqual(expected_output, sanitized_output)


    def test_removes_script(self):
        input_html = "<div><p>This has a <script>alert('hack!')</script>script tag</p></div>"
        expected_output = "<div><p>This has a script tag</p></div>"
        sanitized_output = sanitize(input_html)
        self.assertEqual(expected_output, sanitized_output)


    def test_removes_style(self):
        input_html = "<div><p>This has a <style>body { background-color: #000; }</style>style tag</p></div>"
        expected_output = "<div><p>This has a style tag</p></div>"
        sanitized_output = sanitize(input_html)
        self.assertEqual(expected_output, sanitized_output)


    def test_retains_allowed_tags(self):
        input_html = "<div><p>This has a <a href=\"#\">link</a> and some <em>emphasis</em>.</p></div>"
        # a `rel` tag is also added
        expected_output = "<div><p>This has a <a href=\"#\" rel=\"noopener noreferrer\">link</a> and some <em>emphasis</em>.</p></div>"
        sanitized_output = sanitize(input_html)
        self.assertEqual(expected_output, sanitized_output)


    def test_retains_img(self):
        input_html = "<div><p>This has an <img src=\"#\">image.</p></div>"
        expected_output = "<div><p>This has an <img src=\"#\">image.</p></div>"
        sanitized_output = sanitize(input_html)
        self.assertEqual(expected_output, sanitized_output)


    def test_removes_unsafe_scheme(self):
        input_html = "<div><p>This has an <img src=\"file://foo.bar\">image with an unsafe URL scheme.</p></div>"
        expected_output = "<div><p>This has an <img>image with an unsafe URL scheme.</p></div>"
        sanitized_output = sanitize(input_html)
        self.assertEqual(expected_output, sanitized_output)


if __name__ == '__main__':
    unittest.main()
