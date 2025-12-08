from flask import Flask, redirect, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///text.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Todo(db.Model):
    # Database schematic for media items
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    publication_date = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # Extract form data and create new media item
        name_content = request.form['name'] 
        publication_date_content = request.form['publication_date']
        author_content = request.form['author']
        category_content = request.form['category']

        new_task = Todo(name=name_content, publication_date=publication_date_content, author=author_content, category=category_content)

        try:
            # Add to database and commit changes
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        # Fetch all media items and render template
        tasks = Todo.query.all()
        return render_template('index.html', tasks=tasks)

@app.route('/api/tasks')
def api_tasks():
    # Return all media items as JSON for frontend filtering
    tasks = Todo.query.all()
    result = [
        {
            "id": task.id,
            "name": task.name,
            "publication_date": task.publication_date,
            "author": task.author,
            "category": task.category
        }
        for task in tasks
    ]
    return jsonify(result)

@app.route('/delete/<int:id>')
def delete(id):
    # Delete media item by ID
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)