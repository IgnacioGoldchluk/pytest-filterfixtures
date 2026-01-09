"""pytest plugin to filter tests by the fixtures they use"""

import pytest

__version__ = "0.0.1"


def pytest_addoption(parser: pytest.Parser):
    parser.addoption(
        "--exclude-fixtures",
        dest="exclude_fixtures",
        nargs="+",
        default=set(),
        type=set,
        required=False,
        help="Ignores tests that use any of the fixtures provided",
    )
    parser.addoption(
        "--include-fixtures",
        dest="include_fixtures",
        nargs="+",
        default=set(),
        type=set,
        required=False,
        help="Collects only the tests that use at least one of the fixtures provided",
    )


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(
    session: pytest.Session, config: pytest.Config, items: list[pytest.Item]
):
    include: set[str] = set(config.getoption("include_fixtures"))
    exclude: set[str] = set(config.getoption("exclude_fixtures"))

    tmp_items = items

    if exclude:
        tmp_items = [
            item
            for item in tmp_items
            if not any(f in exclude for f in getattr(item, "fixturenames", []))
        ]

    if include:
        tmp_items = [
            item
            for item in tmp_items
            if any(f in include for f in getattr(item, "fixturenames", []))
        ]

    items[:] = tmp_items
