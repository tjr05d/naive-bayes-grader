from flask import Flask, request, jsonify, abort, make_response, json, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/grader_api_dev'
db = SQLAlchemy(app)


#training area routes
@app.route('/grader/api/v1.0/training', methods=['GET'])
def training():
    questions = Question.query.all()
    return render_template('training.html', questions = questions)

@app.route('/grader/training_question_responses', methods=['POST'])
def get_training_question_responses():
    responses = Response.query.filter(Response.questions_id==int(request.form['question_id']))
    return jsonify([(response.id, response.answer) for response in responses])

@app.route('/grader/response_role', methods=['PUT'])
def response_role():
    # db.session.query(Response).filter_by(id=request.form['response_id']).update({role: u"%{request.form['role']}", categories_id: u"%{request.form['category_id']}" })

    response_id= request.form['response_id']
    new_role = request.form['role']
    new_categories_id= int(request.form['category_id'])

    db.session.query(Response).filter(Response.id==response_id).update({'role': new_role, 'categories_id': new_categories_id})

    db.session.commit()
    response = Response.query.get(response_id)
    return jsonify({'response': response.tim_to_dict}), 201

#responses routes
@app.route('/grader/api/v1.0/responses', methods=['GET'])
def get_responses():
    responses= Response.query.all()
    categories = Category.query.all()
    questions = Question.query.all()
    # jsonify({'responses' : prepare_index_json(Response)})
    return render_template('show_responses.html', responses = responses, categories = categories, questions= questions)


@app.route('/grader/api/v1.0/responses/<int:response_id>', methods=['GET'])
def get_response(response_id):
    response = Response.query.get(response_id)
    if not response:
        abort(404)
    return jsonify({'response': response.to_dict})

#experimental post route to classify a response item
@app.route('/grader/classify', methods=['POST'])
def classify_response():
    if not request.form or not 'answer' in request.form:
        abort(400)
    question_responses= db.session.query(Response).filter((Response.questions_id==request.form['question_id']) & (Response.role == "training") & (Response.categories_id != None))
    training_responses = [data_item.tim_to_dict for data_item in question_responses]
    #empty array to put the training tuples in
    training_data = []
    #loop to take the info from the list and create the tuples that go in the training data array
    for data_point in training_responses:
        training_data.append((data_point["answer"], data_point["categories_id"]))
    #creates the classifier for the response that is recieved
    question = NaiveBayesClassifier(training_data)
    #classiifies the response into a category based on probability
    category_decision = question.classify(request.form['answer'])
    print(category_decision)
    print(training_data)
    #get the category object that belongs to that response
    category_object = Category.query.get(int(category_decision))
    #gets the probability that the response falls in one of the categories
    prob_cat = question.prob_classify(request.form['answer'])
    print(prob_cat)
    #loop to return the prob that the response falls in each of the categories
    cat_probabilities = []
    #loop to get the probability of all the categories that exist for that classifier
    print(question.labels())
    for cat in question.labels():
        cat_title = Category.query.get(int(cat)).title
        cat_probabilities.append((cat_title, prob_cat.prob(cat)))
    #return a hash with the category picked as well as the probabilities fo all the categories of the classifier
    return jsonify({ 'question_id' :  request.form['question_id'], 'category' : category_object.title, 'probabilities' : cat_probabilities}), 201

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
        categories_id= int(request.form['category']),
        questions_id= int(request.form['question_id'])
        )
    db.session.add(response)
    response.improves_training_set()
    db.session.commit()
    return jsonify({'response': response.to_dict}), 201

#categories routes
@app.route('/grader/categories', methods=['GET'])
def get_categories():
    return jsonify({'categories' : prepare_index_json(Category)})

@app.route('/grader/api/v1.0/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        abort(404)
    return jsonify({'category': category.to_dict})

@app.route('/grader/categories', methods=['POST'])
def create_category():
    if not request.form or not 'title' in request.form:
        abort(400)
    category = Category(
        title= request.form['title'],
        feedback= request.form['feedback'],
        question_id= int(request.form['question_id'])
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
