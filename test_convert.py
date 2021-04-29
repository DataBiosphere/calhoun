import unittest
import utils

class TestConvert(unittest.TestCase):

    def test_convert(self): 
        notebook_json = utils.read_json_file('./notebooks/test1.ipynb')
        notebook_html = utils.perform_notebook_conversion(notebook_json)
        self.assertIsNotNone(notebook_html)

    
    def test_rmd_convert(self):
        with open('./notebooks/test-rmd.Rmd', 'rb') as f:
            rmd_html = utils.perform_rmd_conversion(f)
        self.assertIsNotNone(rmd_html)

if __name__ == '__main__':
    unittest.main()