import unittest
import utils

class TestConvert(unittest.TestCase):

    def test_convert(self):
        notebook_json = utils.read_json_file('./notebooks/test1.ipynb')
        notebook_html = utils.perform_notebook_conversion(notebook_json)
        self.assertIsNotNone(notebook_html)
        self.assertIn("<html>", notebook_html)
        self.assertIn("Check out this cool notebook site", notebook_html)
        self.assertIn("<img", notebook_html)
        self.assertNotIn("onload=", notebook_html)
        self.assertNotIn("alert(", notebook_html)
        self.assertNotIn("<script", notebook_html)

    def test_rmd_convert(self):
        with open('./notebooks/test-rmd.Rmd', 'rb') as f:
            rmd_html = utils.perform_rmd_conversion(f)
        self.assertIsNotNone(rmd_html)
        self.assertIn("<html>", str(rmd_html))
        self.assertIn("This is an R Markdown document", str(rmd_html))
        self.assertIn("<img", rmd_html)
        self.assertNotIn("onload=", rmd_html)
        self.assertNotIn("alert(", notebook_html)
        self.assertNotIn("<script", rmd_html)

if __name__ == '__main__':
    unittest.main()
