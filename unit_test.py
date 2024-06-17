import unittest
from test.test_convert import TestConvert
from test.test_html_sanitize import TestHtmlSanitize


def get_suite():
    # Add new test cases here to run automatically when `unit-test.sh` is run
    test_cases = [
        TestConvert,
        TestHtmlSanitize
    ]

    suites = []
    for test_case in test_cases:
        case_suite = unittest.defaultTestLoader.loadTestsFromTestCase(test_case)
        suites.append(case_suite)
    suite = unittest.TestSuite()
    suite.addTests(suites)
    num_tests = suite.countTestCases()

    print("Found {count} tests in suite.".format(count=num_tests))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(get_suite())
