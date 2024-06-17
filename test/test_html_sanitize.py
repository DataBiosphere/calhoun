import unittest
import utils

class TestHtmlSanitize(unittest.TestCase):

    def test_none_on_empty(self):
        sanitized_output = utils.remove_inline_scripts("")
        self.assertIsNone(sanitized_output)

    # extend
    def test_removes_unsafe_attributes(self):
        input_html = "<body><div><p style='width: 20;background-image: `wingnut.png`;'>This has an unsafe style attribute</p></div></body>"
        expected_output = "<body><div><p style=\"width: 20;\">This has an unsafe style attribute</p></div></body>"
        sanitized_output = utils.remove_inline_scripts(input_html)
        self.assertEqual(expected_output, sanitized_output)

    # extend
    def test_removes_script(self):
        input_html = "<body><div><p>This has a <script>alert('hack!')</script>script tag</p></div></body>"
        expected_output = "<body><div><p>This has a script tag</p></div></body>"
        sanitized_output = utils.remove_inline_scripts(input_html)
        self.assertEqual(expected_output, sanitized_output)

    def test_removes_style(self):
        input_html = "<body><div><p>This has a <style>body { background-color: #000; }</style>style tag</p></div></body>"
        expected_output = "<body><div><p>This has a style tag</p></div></body>"
        sanitized_output = utils.remove_inline_scripts(input_html)
        self.assertEqual(expected_output, sanitized_output)

    def test_retains_allowed_tags(self):
        input_html = "<body><div><p>This has a <a href=\"#\">link</a> and some <em>emphasis</em>.</p></div></body>"
        expected_output = "<body><div><p>This has a <a href=\"#\">link</a> and some <em>emphasis</em>.</p></div></body>"
        sanitized_output = utils.remove_inline_scripts(input_html)
        self.assertEqual(expected_output, sanitized_output)

    def test_retains_img(self):
        input_html = "<body><div><p>This has an <img src=\"#\">image</img>.</p></div></body>"
        expected_output = "<body><div><p>This has an <img src=\"#\">image</img>.</p></div></body>"
        sanitized_output = utils.remove_inline_scripts(input_html)
        self.assertEqual(expected_output, sanitized_output)

    def test_removes_unsafe_scheme(self):
        input_html = "<body><div><p>This has an <img src=\"file://foo.bar\">image</img> with an unsafe URL scheme.</p></div></body>"
        expected_output = "<body><div><p>This has an <img>image</img> with an unsafe URL scheme.</p></div></body>"
        sanitized_output = utils.remove_inline_scripts(input_html)
        self.assertEqual(expected_output, sanitized_output)

if __name__ == '__main__':
    unittest.main()
