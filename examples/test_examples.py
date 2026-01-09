import pytest


@pytest.fixture(autouse=True)
def example_autoused():
    return 1


@pytest.fixture(scope="session")
def example_session_scoped():
    return 2


@pytest.fixture
def example_fixture_1(example_session_scoped):
    return example_session_scoped + 1


@pytest.fixture
def example_fixture_2():
    return 4


def test_example1(example_fixture_1):
    assert example_fixture_1 == 3


def test_example2(example_fixture_2):
    assert example_fixture_2 == 4
