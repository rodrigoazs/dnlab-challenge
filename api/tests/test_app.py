from fastapi.testclient import TestClient
from main import app


def test_view_parts_list():
    client = TestClient(app)

    response = client.get("/api/parts")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_filter_parts_list():
    client = TestClient(app)

    response = client.get("/api/parts?model=ASC100")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]['model'] == 'ASC100'


def test_multiple_filter_parts_list():
    client = TestClient(app)

    response = client.get("/api/parts?model=ASC100&part=ND011710")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]['model'] == 'ASC100'
    assert response.json()[0]['part'] == 'ND011710'


def test_inexistent_filter_parts_list():
    client = TestClient(app)

    response = client.get("/api/parts?model=XXXXINEXISTENTXXXX")
    assert response.status_code == 200
    assert len(response.json()) == 0
