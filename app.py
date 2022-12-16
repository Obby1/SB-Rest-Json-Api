from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Todo

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///todos_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)



@app.route('/')
def index_page():
    # pre populate page with some todos
    todos = Todo.query.all()
    return render_template('index.html', todos = todos)

@app.route('/api/todos')
def list_todos():
    all_todos = [todo.serialize() for todo in Todo.query.all()]
    # below returns an error - object type not serializable 
    # jsonify(all_todos)
    
    # common in json to assign list to key
    # return jsonify(all_todos)
    return jsonify(todos = all_todos)

@app.route('/api/todos/<int:id>')
def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return jsonify(todo=todo.serialize())

# if request is made with content type json, it will be in request.json (not .args or .form)
# if you wanted to interact with a form, your route would specify that. In this case we're showing API post request which is usually in JSON
@app.route('/api/todos', methods = ["POST"])
def create_todo():
    # below assumes dev passes in a title, but its a good idea to do some error handling
    # here - if no title, respond with error status code and json that says missing title
    # missing title = respond with x and status code x 
    new_todo = Todo(title = request.json["title"])
    db.session.add(new_todo)
    db.session.commit()
    # return (jsonify(todo = new_todo.serialize()), 201)
    #or :
    response_json= jsonify(todo = new_todo.serialize())
    return (response_json, 201)

@app.route('/api/todos/<int:id>', methods = ["PATCH"])
def update_todo(id):
    todo = Todo.query.get_or_404(id)
    # request.json
    # theoretically we could assume every time this route is hit we update the todo w/ below
    # however, what if we just toggle T/F or change title? or pass in unexpected data like priority:high?
    # db.session.query(Todo).filter_by(id=id).update(request.json)
    # {
    #     'title': 'something',
    #     'done': True
    # }
    # app will break - safer to update each piece at a time
    # another approach is doing below, however if one var is not filled up it will update to empty
    # todo.title = request.json["title"]
    # todo.done = request.json["done"]
    # below - set title to json you posted or else default back to existing title/ done
    todo.title = request.json.get("title", todo.title)
    todo.done = request.json.get("done", todo.done)
    db.session.commit()
    return jsonify(todo = todo.serialize())

@app.route('/api/todos/<int:id>', methods = ["DELETE"])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify(message = "deleted")

# note on testing - try to keep routes to maximum of 2 categories /cat1/id/cat2/id otherwise
# it gets unweildly. Most datasets will link cat2 to cat1 (like post-> comments, and 
# comments -> posts, posts->subreddits, etc.) so you prob don't need to list more than2


# testing APIs - you will test response.json NOT response.data
# you will test for stuff in response.json, much easier than tesing for html attributes (or data named stuff)
# def test_all_desserts(self):
    # with app.test_client() as client:
    #     resp = client.get("/desserts")
    #     self.assertEqual(resp.status_code, 200)

    #     self.assertEqual(
    #         resp.json,
    #         {'desserts': [{
    #             'id': self.dessert_id,
    #             'name': 'TestCake',
    #             'calories': 10
    #         }]})





# @app.route('/')
# def index_page():
#     """Renders html template that includes some JS - NOT PART OF JSON API!"""
#     todos = Todo.query.all()
#     return render_template('index.html', todos=todos)


 

# # *****************************
# # RESTFUL TODOS JSON API
# # *****************************
# @app.route('/api/todos')
# def list_todos():
#     """Returns JSON w/ all todos"""
#     all_todos = [todo.serialize() for todo in Todo.query.all()]
#     return jsonify(todos=all_todos)


# @app.route('/api/todos/<int:id>')
# def get_todo(id):
#     """Returns JSON for one todo in particular"""
#     todo = Todo.query.get_or_404(id)
#     return jsonify(todo=todo.serialize())


# @app.route('/api/todos', methods=["POST"])
# def create_todo():
#     """Creates a new todo and returns JSON of that created todo"""
#     new_todo = Todo(title=request.json["title"])
#     db.session.add(new_todo)
#     db.session.commit()
#     response_json = jsonify(todo=new_todo.serialize())
#     return (response_json, 201)


# @app.route('/api/todos/<int:id>', methods=["PATCH"])
# def update_todo(id):
#     """Updates a particular todo and responds w/ JSON of that updated todo"""
#     todo = Todo.query.get_or_404(id)
#     todo.title = request.json.get('title', todo.title)
#     todo.done = request.json.get('done',  todo.done)
#     db.session.commit()
#     return jsonify(todo=todo.serialize())


# @app.route('/api/todos/<int:id>', methods=["DELETE"])
# def delete_todo(id):
#     """Deletes a particular todo"""
#     todo = Todo.query.get_or_404(id)
#     db.session.delete(todo)
#     db.session.commit()
#     return jsonify(message="deleted")
