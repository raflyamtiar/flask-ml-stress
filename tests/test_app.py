import pytest


from app import create_app


@pytest.fixture
def app():
    yield create_app()


@pytest.fixture
def client(app):
    return app.test_client()


def test_index(client):
    resp = client.get('/')
    assert resp.status_code == 200
