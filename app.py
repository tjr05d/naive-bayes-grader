import pdb
from shared import *
from flask import Flask, request, jsonify, abort, make_response, json, render_template
from models import *

#responses routes
@app.route('/grader/responses', methods=['GET'])
def get_responses():
    responses = Response.query.all()
    categories = Category.query.all()
    questions = Question.query.all()
    return render_template('show_responses.html',
                            responses = responses,
                            categories = categories,
                            questions= questions)

@app.route('/grader/responses/<int:response_id>', methods=['GET'])
def get_response(response_id):
    response = Response.query.get(response_id)
    if not response:
        abort(404)
    return jsonify({'response': response.safe_to_dict})

#route to recieve a request and create a response for a test or training set
@app.route('/grader/test_set', methods=['POST'])
def create_test_set_response():
    if not request.json or not 'answer' in request.json:
        abort(400)
    response = Response(
        answer= request.json['answer'],
        role = "test",
        category_id = int(request.json['category_id']),
        question_id = int(request.json['question_id'])
        )
    db.session.add(response)
    db.session.commit()
    #query to return the current test set with the response added
    # current_set = Response.query.filter(
    #                                     (Response.question_id ==request.json['question_id']) &
    #                                     (Response.role == "test")
    #                                     )
    return jsonify({'response': response.safe_to_dict}), 201

@app.route('/grader/training_set', methods=['POST'])
def create_training_set_response():
    if not request.json or not 'answer' in request.json:
        abort(400)
    response = Response(
        answer= request.json['answer'],
        role = "training",
        category_id = int(request.json['category_id']),
        question_id = int(request.json['question_id'])
        )
        #check how many responses are in the current training set for this question
    question_responses = Response.query.filter(
        (Response.question_id == response.question_id) &
        (Response.role == "training") &
        (Response.category_id != None))
    if question_responses.count() > 10:
        return response.improves_training_set(response.category_id), 201
    else:
        db.session.add(response)
        db.session.commit()
        message = "Training response added, there are currently less than 5 elements in the training set"
        return jsonify({'message': message, 'response': response.safe_to_dict}), 201

#route to classify a response
@app.route('/grader/classify', methods=['POST'])
def classify_response():
    if not request.form or not 'answer' in request.form:
        abort(400)
    response = Response(
        answer= request.form['answer'],
        role = None,
        category_id= None,
        question_id= int(request.form['question_id'])
        )
    return response.classify_response()

@app.route('/grader/getcategories', methods=['POST'])
def getcategories():
    categories = Category.query.filter(Category.question_id==int(request.form['question_id']))
    return jsonify([(cat.id, cat.title) for cat in categories])

@app.route('/grader/create_response', methods=['POST'])
def create_response():
    print(request.form)
    if not request.form or not 'answer' in request.form:
        abort(400)
    response = Response(
        answer= request.form['answer'],
        role = None,
        category_id = int(request.form['category']),
        question_id = int(request.form['question_id'])
        )
    db.session.add(response)
    response.improves_training_set()
    db.session.commit()
    return jsonify({'response': response.to_dict}), 201

#categories routes
@app.route('/grader/categories', methods=['GET'])
def get_categories():
    return jsonify({'categories' : prepare_index_json(Category)})

@app.route('/grader/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        abort(404)
    return jsonify({'category': category.to_dict})

@app.route('/grader/categories', methods=['POST'])
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
@app.route('/grader/questions', methods=['GET'])
def get_questions():
    return jsonify({'questions' : prepare_index_json(Question)})

@app.route('/grader/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        abort(404)
    return jsonify({'question': question.to_dict})

@app.route('/grader/questions', methods=['POST'])
def create_question():
    if not request.json or not 'title' in request.json:
        abort(400)
    question = Question(
        title= request.json['title'],
        prompt= request.json['prompt'],
        )
    db.session.add(question)
    db.session.commit()
    return jsonify({'question': question.to_dict}), 201

#training area routes
@app.route('/grader/api/v1.0/training', methods=['GET'])
def training():
    questions = Question.query.all()
    return render_template('training.html', questions = questions)

@app.route('/grader/training_question_responses', methods=['POST'])
def get_training_question_responses():
    responses = Response.query.filter(Response.question_id == int(request.form['question_id']))
    return jsonify([(response.id, response.answer) for response in responses])

@app.route('/grader/response_role', methods=['PUT'])
def response_role():
    response_id = request.form['response_id']
    new_role = request.form['role']
    new_category_id = int(request.form['category_id'])

    db.session.query(Response).filter(Response.id==response_id).update({'role': new_role, 'category_id': new_category_id})

    db.session.commit()
    response = Response.query.get(response_id)
    return jsonify({'response': response.safe_to_dict}), 201

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
