from flask import Flask, request, jsonify, abort, make_response, json
from flask.ext.sqlalchemy import SQLAlchemy
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/grader_api_dev'
db = SQLAlchemy(app)

class JsondModel(object):
    @property
    def to_dict(self):
        return {key: getattr(self, key) for key in self.external_attrs}

#method to prepare data within the classify_response method
    @property
    def tim_to_dict(self):
        return {key: getattr(self, key) for key in self.dumb_ass_attrs}


class Unit(db.Model, JsondModel):
    __tablename__ = 'units'
    external_attrs = ['title', 'description']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.Text)
    questions = db.relationship('Question', backref='unit', lazy= 'dynamic')

    def __init__(self, title, description):
        self.title = title
        self.description = description


    def __repr__(self):
        return '<id {}>'.format(self.id)


class Question(db.Model, JsondModel):
    __tablename__ = 'questions'
    external_attrs = ['title', 'prompt', 'unit_id']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    prompt = db.Column(db.Text)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'))
    responses = db.relationship('Response', backref='question', lazy= 'dynamic')
    categories = db.relationship('Category', backref='question', lazy= 'dynamic')

    def __init__(self, title, prompt, unit_id):
        self.title = title
        self.prompt = prompt
        self.unit_id = unit_id

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Category(db.Model, JsondModel):
    __tablename__ = 'categories'
    external_attrs = ['title', 'feedback', 'question_id', 'responses']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    feedback = db.Column(db.Text)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    responses = db.relationship('Response', backref='category', lazy='dynamic')

    def __init__(self, title, feedback, question_id):
        self.title = title
        self.feedback = feedback
        self.question_id = question_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @property
    def responses(self):
        return {'unit':self.question.unit.title, 'question': self.question.title}

class Response(db.Model, JsondModel):
    __tablename__ = 'responses'
    external_attrs = ['answer', 'categories_id', 'id', 'active', 'info', 'classify_response']
    dumb_ass_attrs= ['answer','categories_id', 'id']

    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text)
    active = db.Column(db.Boolean)
    categories_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    questions_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    def __init__(self, answer, active, categories_id, questions_id):
        self.answer = answer
        self.active = False
        self.categories_id = categories_id
        self.questions_id = questions_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @property
    def info(self):
        return {'unit':self.question.unit.title, 'question': self.question.prompt}

    @property
    def classify_response(self):
        #test data point to pass into the classify method
        test_response= ("Something", "Correct")

        #pulls the training data from previous responses for this question
        # train = db.session.query(Response).filter(Response.questions_id==1)
        question_responses= db.session.query(Response).filter(Response.questions_id==self.questions_id)
        #prepare that data for the classifier by creating a list
        training_responses = [data_item.tim_to_dict for data_item in question_responses]
        #empty array to put the training tuples in
        training_data = []
        #loop to take the info from the list and create the tuples that go in the training data array
        for data_point in training_responses:
            training_data.append((data_point["answer"], data_point["categories_id"]))
        #creates the classifier for the response that is recieved
        question = NaiveBayesClassifier(training_data)
        #classiifies the response into a category based on probability
        category_decision = question.classify(test_response)
        #get the category object that belongs to that response
        category_object = Category.query.get(int(category_decision))
        #gets the probability that the response falls in one of the categories
        prob_cat = question.prob_classify(test_response)
        #loop to return the prob that the response falls in each of the categories
        cat_probabilities = []
        #loop to get the probability of all the categories that exist for that classifier
        for cat in question.labels():
            cat_probabilities.append((cat, prob_cat.prob(cat)))
        #return a hash with the category picked as well as the probabilities fo all the categories of the classifier
        return {'category' : category_object.title, 'probabilities' : cat_probabilities}

#responses routes
@app.route('/grader/api/v1.0/responses', methods=['GET'])
def get_responses():
    return jsonify({'responses' : prepare_index_json(Response)})


@app.route('/grader/api/v1.0/responses/<int:response_id>', methods=['GET'])
def get_response(response_id):
    response = Response.query.get(response_id)
    if not response:
        abort(404)
    return jsonify({'response': response.to_dict})

@app.route('/grader/api/v1.0/responses', methods=['POST'])
def create_response():
    if not request.json or not 'answer' in request.json:
        abort(400)
    response = Response(
        answer= request.json['answer'],
        active = False,
        categories_id= int(request.json['category_id']),
        questions_id= int(request.json['question_id'])
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
