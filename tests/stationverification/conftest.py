import pytest


@pytest.fixture(scope="session")
def testdata() -> str:
    return 'tests/data'
