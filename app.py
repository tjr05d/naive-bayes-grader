from flask import Flask, request, jsonify, abort, make_response, json, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from models import *
from views import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/grader_api_dev'
db = SQLAlchemy(app)

#responses routes
@app.route('/grader/api/v1.0/responses', methods=['GET'])
def get_responses():
    responses= Response.query.all()
    # jsonify({'responses' : prepare_index_json(Response)})
    return render_template('show_responses.html', responses = responses)


@app.route('/grader/api/v1.0/responses/<int:response_id>', methods=['GET'])
def get_response(response_id):
    response = Response.query.get(response_id)
    if not response:
        abort(404)
    return jsonify({'response': response.to_dict})

@app.route('/grader/api/v1.0/responses', methods=['POST'])
def create_response():
    print(request.form['answer'])
    if not request.form or not 'answer' in request.form:
        abort(400)
    response = Response(
        answer= request.form['answer'],
        active = False,
        categories_id= int(request.form['category_id']),
        questions_id= int(request.form['question_id'])
        )
    db.session.add(response)
    db.session.commit()
    return jsonify({'response': response.to_dict}), 201

#categories routes
@app.route('/grader/api/v1.0/categories', methods=['GET'])
def get_categories():
    return jsonify({'categories' : prepare_index_json(Category)})

@app.route('/grader/api/v1.0/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        abort(404)
    return jsonify({'category': category.to_dict})

@app.route('/grader/api/v1.0/categories', methods=['POST'])
def create_category():
    if not request.json or not 'title' in request.json:
        abort(400)
    category = Category(
        title= request.json['title'],
        feedback= request.json['feedback'],
        question_id= int(request.json['question_id'])
        )
    db.session.add(category)
    db.session.commit()
    return jsonify({'category': category.to_dict}), 201

#Questions routes
@app.route('/grader/api/v1.0/questions', methods=['GET'])
def get_questions():
    return jsonify({'questions' : prepare_index_json(Question)})

@app.route('/grader/api/v1.0/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        abort(404)
    return jsonify({'question': question.to_dict})

@app.route('/grader/api/v1.0/questions', methods=['POST'])
def create_question():
    if not request.json or not 'title' in request.json:
        abort(400)
    question = Question(
        title= request.json['title'],
        prompt= request.json['prompt'],
        unit_id= int(request.json['unit_id'])
        )
    db.session.add(question)
    db.session.commit()
    return jsonify({'question': question.to_dict}), 201

#Unit routes
@app.route('/grader/api/v1.0/units', methods=['GET'])
def get_units():
    return jsonify({'units' : prepare_index_json(Unit)})

@app.route('/grader/api/v1.0/units/<int:unit_id>', methods=['GET'])
def get_unit(unit_id):
    unit = Unit.query.get(unit_id)
    if not unit:
        abort(404)
    return jsonify({'unit': unit.to_dict})

@app.route('/grader/api/v1.0/units', methods=['POST'])
def create_unit():
    if not request.json or not 'title' in request.json:
        abort(400)
    unit= Unit(
        title= request.json['title'],
        description= request.json['description'],
        )
    db.session.add(unit)
    db.session.commit()
    return jsonify({'unit': unit.to_dict}), 201

#error handler route
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def prepare_index_json(request_type):
    index_items = db.session.query(request_type).all()
    index_items_arr = [item.to_dict for item in index_items]
    return index_items_arr

if __name__ == '__main__':
    app.run(debug=True)
