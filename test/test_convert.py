"""Unit tests for convert_ipynb_file and convert_rmd_file."""

import json
import unittest

import convert_ipynb_file
import convert_rmd_file


class TestConvert(unittest.TestCase):
    """Test the code which converts input files to HTML."""

    def test_convert(self):
        """Converting a .ipynb file to HTML strips injected code and leaves safe content in place."""
        with open('./notebooks/test_ipynb.ipynb') as f:
            notebook_json = json.load(f)
        notebook_html = convert_ipynb_file.to_safe_html(notebook_json)
        self.assertIsNotNone(notebook_html)
        self.assertIn("<html>", notebook_html)
        self.assertIn("check out this cool notebook site", notebook_html)
        self.assertIn("<img src=\"https://", notebook_html)
        self.assertIn("src=\"data:image/png", notebook_html)
        self.assertIn("<div>TEST: `img` tag stripped of its on* attributes    <img src=\"https://www.pixelstalk.net/wp-content/uploads/2016/08/Lovely-dog-wallpaper-download-cute-puppy.jpg\"/>", notebook_html)
        self.assertIn("title=\"dummy title&quot; onload=alert(\'XSS\'); onerror=&quot;\"", notebook_html)
        self.assertNotIn("<script type=\"text/javascript\">", notebook_html)
        self.assertNotIn("<style scoped>", notebook_html)

    def test_convert_widgets(self):
        """Converting a .ipynb file with widgets does not add code to the <head> block."""
        with open('./notebooks/test_widgets.ipynb') as f:
            notebook_json = json.load(f)
        notebook_html = convert_ipynb_file.to_safe_html(notebook_json)
        self.assertNotIn("function addWidgetsRenderer()", notebook_html)

    def test_rmd_convert(self):
        """Converting a .rmd file strips injected code and leaves safe content in place."""
        with open('./notebooks/test_rmd.Rmd', 'rb') as f:
            rmd_html = convert_rmd_file.to_safe_html(f)
        self.assertIsNotNone(rmd_html)
        self.assertIn("<div>", rmd_html)
        self.assertIn("This is an R Markdown document", rmd_html)
        self.assertIn("src=\"data:image/png", rmd_html)
        self.assertIn("TEST: <code>img</code> tag with javascript injected &lt;img src=\"<a class=\"uri\" rel=\"noopener noreferrer\">javascript:alert</a>(‘XSS 2’);\"", rmd_html)
        self.assertNotIn("href=\"javascript", rmd_html)
        self.assertIn("<code> &lt;script", rmd_html)
        self.assertNotIn("<style scoped>", rmd_html)
        self.assertNotIn("```{", rmd_html)


if __name__ == '__main__':
    unittest.main()
