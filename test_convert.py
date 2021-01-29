import unittest
import utils

class TestConvert(unittest.TestCase):

    def test_convert(self): 
        notebook_json = utils.read_json_file('./notebooks/test1.ipynb')
        notebook_html = utils.perform_notebook_conversion(notebook_json)
        self.assertIsNotNone(notebook_html)

if __name__ == '__main__':
    unittest.main()