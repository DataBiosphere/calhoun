import unittest
import convert_ipynb
import convert_rmd
import json


class TestConvert(unittest.TestCase):

    def test_convert(self):
        with open('./notebooks/test1.ipynb') as f:
            notebook_json = json.load(f)
        notebook_html = convert_ipynb.convert(notebook_json)
        self.assertIsNotNone(notebook_html)
        self.assertIn("<div>", notebook_html)
        self.assertIn("Check out this cool notebook site", notebook_html)
        self.assertIn("<img src=\"https://", notebook_html)
        self.assertIn("<img src=\"data:image/png", notebook_html)
        self.assertNotIn("onload=", notebook_html)
        self.assertNotIn("alert(", notebook_html)
        self.assertNotIn("<script", notebook_html)


    def test_rmd_convert(self):
        with open('./notebooks/test-rmd.Rmd', 'rb') as f:
            rmd_html = convert_rmd.convert(f)
        self.assertIsNotNone(rmd_html)
        self.assertIn("<div>", rmd_html)
        self.assertIn("This is an R Markdown document", rmd_html)
        self.assertIn("<img src=\"data:image/png", rmd_html)
        self.assertNotIn("onload=", rmd_html)
        self.assertNotIn("href=\"javascript", rmd_html)
        self.assertNotIn("<script", rmd_html)
        self.assertNotIn("```{", rmd_html)


if __name__ == '__main__':
    unittest.main()
