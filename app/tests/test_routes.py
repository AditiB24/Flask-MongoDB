import pytest
from app.models import mongo

@pytest.fixture
def client():
    from main import create_app
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            mongo.drop_collection("todos")
        yield client

def test_add_todo(client):
    response = client.post("/todos", json={"title": "Test Task", "description": "Testing"})
    assert response.status_code == 201

def test_get_all_todos(client):
    client.post("/todos", json={"title": "Test Task"})
    response = client.get("/todos")
    assert response.status_code == 200
    assert len(response.json) > 0

def test_edit_todo(client):
    task = client.post("/todos", json={"title": "Test Task"}).json
    response = client.put(f"/todos/{task['id']}", json={"title": "Updated Task"})
    assert response.status_code == 200

def test_delete_todo(client):
    task = client.post("/todos", json={"title": "Test Task"}).json
    response = client.delete(f"/todos/{task['id']}")
    assert response.status_code == 200

def test_delete_all_todos(client):
    client.post("/todos", json={"title": "Task 1"})
    client.post("/todos", json={"title": "Task 2"})
    response = client.delete("/todos")
    assert response.status_code == 200
