from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    data_created = db.Column(db.DateTime, default = db.func.current_timestamp())
    completed = db.Column(db.Boolean, default = False, nullable = False)
    FamilyMember_id = db.Column(db.Integer)
    
    def __repr__(self):
        return '<Task %r>' % self.id

class FamilyMember(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False, unique = True)
    
    def __repr__(self):
        return '<Task %r>' % self.id

# FamilyMember endpoints
@app.route('/FamilyMember', methods = ['POST', 'GET'])
def familyMember():
    if request.method == 'POST':
        data = request.get_json()
        new_familyMember = familyMember(
            name = data['name'],
        )
        db.session.add(new_familyMember)
        db.session.commit()
        return {'message' : 'Family member created!'}
    elif request.method == 'GET':
        familyMembers = FamilyMember.query.all()
        output = []
        for member in familyMembers:
            member_data = {}
            member_data['id'] = member.id
            member_data['name'] = member.name
            output.append(member)
        return {'familyMembers' : output}

@app.route('/FamilyMember/<name>', methods = ['GET', 'DELETE'])
def familyMember_detail(familyMember_id):
    if request.method == 'GET':
        familyMember = FamilyMember.query.get_or_404(familyMember_id)
        family_data = {}
        family_data['id'] = familyMember.id
        family_data['name'] = familyMember.name
        return {'familyMember' : family_data}
    elif request.method == 'DELETE':
        db.session.delete(familyMember)
        db.session.commit()
        return {'message' : 'Family item has been deleted!'}    

# Todo endpoints
@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/Todo', methods = ['POST', 'GET'])
def todo():
    if request.method == 'POST':
        data = request.get_json()
        new_todo = todo(
            content = data['content'],
        )
        db.session.add(new_todo)
        db.session.commit()
        return {'message' : 'Todo created!'}
    elif request.method == 'GET':
        todos = Todo.query.all()
        output = []
        for todo in todos:
            todo_data = {}
            todo_data['id'] = todo.id
            todo_data['content'] = todo.content
            todo_data['completed'] = todo.completed
            todo_data['familyMember_id'] = todo.familyMember_id
            output.append(todo_data)
        return {'todos' : output}

@app.route('/Todo/<todo_id>', methods = ['GET', 'PUT', 'DELETE'])
def todo_detail(todo_id):
    if request.method == 'GET':
        todo = Todo.query.get_or_404(todo_id)
        todo_data = {}
        todo_data['id'] = todo.id
        todo_data['content'] = todo.content
        todo_data['completed'] = todo.completed
        todo_data['familyMember_id'] = todo.familyMember_id
        return {'todo' : todo_data}
    elif request.method == 'PUT':
        todo = Todo.query.get_or_404(todo_id)
        data = request.get_json()
        todo_data = {}
        data.content = todo_data['content']
        data.completed = todo_data['completed']
        data.familyMember_id = todo_data['familyMember_id']
        db.session.merge(todo)
        db.session.commit()
        return {'message' : 'Todo item has been updated!'}
    elif request.method == 'DELETE':
        db.session.delete(todo)
        db.session.commit()
        return {'message' : 'Todo item has been deleted!'}

if __name__ == '__main__':
    app.run(debug = True)