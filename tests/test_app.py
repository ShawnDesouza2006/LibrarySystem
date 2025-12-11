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


def test_index_renders_template_simple(test_client):
    """Simple check that the index page contains the frontend markers."""
    # Ensure there's at least one task so the template renders the table/container
    sample = Todo(name="Sample", publication_date="2020", author="Tester", category="Sample")
    db.session.add(sample)
    db.session.commit()

    resp = test_client.get('/')
    assert resp.status_code == 200
    body = resp.data.decode('utf-8', errors='ignore')

    # These are the attributes/strings your JS expects in the template.
    assert 'data-user-cards-container' in body
    assert 'data-user-template' in body
    assert 'data-search' in body
    assert 'data-category-select' in body
    assert 'class="enter"' in body or "class='enter'" in body
    # Also check the Add button or form text exists
    assert 'Add Media' in body or 'Add' in body


def test_delete_task(test_client):
    """Test deleting a task."""
    task = Todo(name="DeleteMe", publication_date="1999",
                author="Carol", category="Testing")
    db.session.add(task)
    db.session.commit()

    response = test_client.get(f'/delete/{task.id}', follow_redirects=True)

    assert response.status_code == 200
    assert Todo.query.get(task.id) is None