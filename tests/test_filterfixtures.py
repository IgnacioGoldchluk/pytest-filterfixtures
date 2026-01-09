import pytest

pytest_plugins = ["pytester"]

EXAMPLE_PATH = "examples/test_examples.py"


class TestInclude:
    def test_no_options_runs_everything(self, pytester: pytest.Pytester):
        pytester.copy_example(EXAMPLE_PATH)
        result = pytester.runpytest("-v")
        result.stdout.fnmatch_lines(
            [
                "*test_examples.py::test_example1 PASSED*",
                "*test_examples.py::test_example2 PASSED*",
            ]
        )
        assert result.ret == 0
        result.assert_outcomes(passed=2)

    def test_excludes_autoused_fixture(self, pytester: pytest.Pytester):
        pytester.copy_example(EXAMPLE_PATH)
        result = pytester.runpytest("-v", "--include-fixtures", "autoused")
        assert result.ret == 0
        result.assert_outcomes(deselected=2)
