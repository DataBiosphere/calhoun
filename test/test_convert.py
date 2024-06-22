import unittest
import convert_ipynb_file
import convert_rmd_file
import json


class TestConvert(unittest.TestCase):

    def test_convert(self):
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


    def test_rmd_convert(self):
        with open('./notebooks/test_rmd.Rmd', 'rb') as f:
            rmd_html = convert_rmd_file.to_safe_html(f)
        self.assertIsNotNone(rmd_html)
        self.assertIn("<div>", rmd_html)
        self.assertIn("This is an R Markdown document", rmd_html)
        self.assertIn("src=\"data:image/png", rmd_html)
        self.assertIn("<div>TEST: `img` tag stripped of its on* attributes    <img src=\"https://www.pixelstalk.net/wp-content/uploads/2016/08/Lovely-dog-wallpaper-download-cute-puppy.jpg\"/>", rmd_html)
        self.assertNotIn("href=\"javascript", rmd_html)
        self.assertNotIn("<script", rmd_html)
        self.assertNotIn("<style scoped>", rmd_html)
        self.assertNotIn("```{", rmd_html)


if __name__ == '__main__':
    unittest.main()
