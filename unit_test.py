"""Run all unit tests."""

import unittest

from test.test_convert import TestConvert
from test.test_html_sanitize import TestHtmlSanitize


test_cases = [
    TestConvert,
    TestHtmlSanitize
]
"""Test cases to run with `unit-test.sh`."""


def get_suite() -> unittest.TestSuite:
    """Collect all unit tests to run together.

    Returns:
        TestSuite with all unit tests defined in `test_cases`.
    """
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
