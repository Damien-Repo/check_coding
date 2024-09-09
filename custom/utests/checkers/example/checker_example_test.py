from lib.utests import UTest, MockFile
from lib.icheck_exception import *

from custom.checkers.example.checker_example import CheckerExample as C


class CheckerExampleTest(UTest):

    def test_check_file_example(self):
        pass

    def test_check_line_example(self):
        pass

    def test_check_function_example(self):
        # Test with MockFile context
        with MockFile('example_test_file.c') as f:
            self.check(f, should_succeed=False)
            self.check_exception_in(CheckWarning(C.TOO_MANY_PARAMETERS, error_pos=(24, 54, 24, 71)))
            self.check_exception_in(CheckWarning(C.TOO_MANY_PARAMETERS, error_pos=(33, 17, 34, 18)))
            self.check_exception_not_in(CheckWarning(C.TOO_MANY_PARAMETERS, error_pos=(0, 0, 0, 0)))

        # Same test with check_from_file() and check_exception() functions
        self.check_from_file('example_test_file.c', should_succeed=False)
        self.check_exception(CheckWarning(C.TOO_MANY_PARAMETERS, error_pos=(24, 54, 24, 71)), self.assertIn)
        self.check_exception(CheckWarning(C.TOO_MANY_PARAMETERS, error_pos=(33, 17, 34, 18)), self.assertIn)
        self.check_exception(CheckWarning(C.TOO_MANY_PARAMETERS, error_pos=(0, 0, 0, 0)), self.assertNotIn)
