from app import db, Todo

def test_add_task(test_client):
    """Test adding a new task."""
    response = test_client.post('/', data={
        "name": "Test Book",
        "publication_date": "2024",
        "author": "Alice",
        "category": "Fiction"
    }, follow_redirects=True)

    assert response.status_code == 200
    task = Todo.query.first()
    assert task is not None
    assert task.name == "Test Book"


def test_api_tasks(test_client):
    """Test the /api/tasks JSON output."""
    task = Todo(name="Sample", publication_date="2020",
                author="Bob", category="Category")
    db.session.add(task)
    db.session.commit()

    response = test_client.get('/api/tasks')
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["name"] == "Sample"


def test_delete_task(test_client):
    """Test deleting a task."""
    task = Todo(name="DeleteMe", publication_date="1999",
                author="Carol", category="Testing")
    db.session.add(task)
    db.session.commit()

    response = test_client.get(f'/delete/{task.id}', follow_redirects=True)

    assert response.status_code == 200
    assert Todo.query.get(task.id) is None
