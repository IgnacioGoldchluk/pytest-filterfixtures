import pytest

pytest_plugins = ["pytester"]

EXAMPLE_PATH = "examples/test_examples.py"


@pytest.fixture(autouse=True)
def copy_example_test(pytester: pytest.Pytester):
    pytester.copy_example(EXAMPLE_PATH)


def test_no_options_runs_everything(pytester: pytest.Pytester):
    result = pytester.runpytest("-v")
    result.stdout.fnmatch_lines(
        [
            "*test_examples.py::test_example1 PASSED*",
            "*test_examples.py::test_example2 PASSED*",
        ]
    )
    assert result.ret == 0
    result.assert_outcomes(passed=2)


def test_contradicting_options_dont_crash(pytester: pytest.Pytester):
    result = pytester.runpytest(
        "-v",
        "--exclude-fixtures",
        "example_fixture_1",
        "--include-fixtures",
        "example_fixture_1",
    )
    assert result.ret == 5


class TestExclude:
    def test_excludes_autouse_fixture(self, pytester: pytest.Pytester):
        result = pytester.runpytest("--exclude-fixtures", "example_autoused", "-v")
        # No tests collected
        assert result.ret == 5
        result.assert_outcomes(deselected=2)

    def test_excludes_multiple_fixtures(self, pytester: pytest.Pytester):
        result = pytester.runpytest(
            "--exclude-fixtures", "example_fixture_1", "example_fixture_2", "-v"
        )
        # No tests collected
        assert result.ret == 5
        result.assert_outcomes(deselected=2)

    def test_excludes_implicit_fixture(self, pytester: pytest.Pytester):
        result = pytester.runpytest(
            "--exclude-fixtures", "example_session_scoped", "-v"
        )
        result.stdout.fnmatch_lines(["*test_examples.py::test_example2 PASSED*"])
        assert result.ret == 0
        result.assert_outcomes(passed=1, deselected=1)

    def test_excludes_specified_fixture(self, pytester: pytest.Pytester):
        result = pytester.runpytest("--exclude-fixtures", "example_fixture_2", "-v")
        result.stdout.fnmatch_lines(["*test_examples.py::test_example1 PASSED*"])
        assert result.ret == 0
        result.assert_outcomes(passed=1, deselected=1)


class TestInclude:
    def test_includes_autouse_fixture(self, pytester: pytest.Pytester):
        result = pytester.runpytest("--include-fixtures", "example_autoused", "-v")
        result.stdout.fnmatch_lines(
            [
                "*test_examples.py::test_example1 PASSED*",
                "*test_examples.py::test_example2 PASSED*",
            ]
        )
        assert result.ret == 0
        result.assert_outcomes(passed=2)

    def test_includes_multiple_fixtures(self, pytester: pytest.Pytester):
        result = pytester.runpytest(
            "--include-fixtures", "example_fixture_1", "example_fixture_2", "-v"
        )
        result.stdout.fnmatch_lines(
            [
                "*test_examples.py::test_example1 PASSED*",
                "*test_examples.py::test_example2 PASSED*",
            ]
        )
        assert result.ret == 0
        result.assert_outcomes(passed=2)

    def test_includes_specified_fixture(self, pytester: pytest.Pytester):
        result = pytester.runpytest("--include-fixtures", "example_fixture_1", "-v")
        result.stdout.fnmatch_lines("*test_examples.py::test_example1 PASSED*")
        assert result.ret == 0
        result.assert_outcomes(passed=1, deselected=1)

    def test_includes_implicit_fixture(self, pytester: pytest.Pytester):
        result = pytester.runpytest(
            "--include-fixtures", "example_session_scoped", "-v"
        )
        result.stdout.fnmatch_lines(["*test_examples.py::test_example1 PASSED*"])
        assert result.ret == 0
        result.assert_outcomes(passed=1, deselected=1)
