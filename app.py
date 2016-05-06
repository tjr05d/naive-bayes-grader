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


class Unit(db.Model):
    __tablename__ = 'units'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.Text)
    questions = db.relationship('Question', backref='unit', lazy= 'dynamic')

    def __init__(self, title, description):
        self.title = title
        self.description = description


    def __repr__(self):
        return '<id {}>'.format(self.id)


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.String())
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'))
    responses = db.relationship('Response', backref='question', lazy= 'dynamic')

    def __init__(self, prompt, unit_id):
        self.prompt = prompt
        self.unit_id = unit_id

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Response(db.Model, JsondModel):
    __tablename__ = 'responses'
    external_attrs = ['answer', 'cat', 'feedback', 'id', 'active', 'score', 'info', 'classify_response']
    dumb_ass_attrs= ['answer','cat', 'feedback', 'id']

    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String())
    cat = db.Column(db.String())
    feedback = db.Column(db.String())
    active = db.Column(db.Boolean)
    questions_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    def __init__(self, answer, cat, feedback, questions_id):
        self.answer = answer
        self.cat = cat
        self.feedback = feedback
        self.active = False
        self.questions_id = questions_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @property
    def info(self):
        return {'unit':self.question.unit.title, 'question': self.question.prompt}

    @property
    def classify_response(self):
        #test data point to pass into the classify method
        test_response= ("Classes are cool", "Correct")

        #pulls the training data from previous responses for this question
        # train = db.session.query(Response).filter(Response.questions_id==1)
        question_responses= db.session.query(Response).filter(Response.questions_id==self.questions_id)
        #prepare that data for the classifier by creating a list
        training_responses = [data_item.tim_to_dict for data_item in question_responses]
        #empty array to put the training tuples in
        training_data = []
        #loop to take the info from the list and create the tuples that go in the training data array
        for data_point in training_responses:
            training_data.append((data_point["answer"], data_point["cat"]))
        #creates the classifier for the response that is recieved
        question = NaiveBayesClassifier(training_data)
        #classiifies the response into a category based on probability
        category_decision = question.classify(test_response)
        #gets the probability that the response falls in one of the categories
        prob_cat = question.prob_classify(test_response)
        #loop to return the prob that the response falls in each of the categories
        cat_probabilities = []
        #loop to get teh probability of all the categores that exist for that classifier
        for cat in question.labels():
            cat_probabilities.append((cat, prob_cat.prob(cat)))
        #return a hash with the category picked as well as the probabilities fo all the categories of the classifier
        return {'category' : category_decision, 'probabilities' : cat_probabilities}

    @property
    def score(self):
        return {'methods':95, 'syntax':20}


@app.route('/grader/api/v1.0/responses', methods=['GET'])
def get_responses():
    return jsonify({'responses' : prepare_index_json()})


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
        cat= request.json['cat'],
        feedback= request.json['feedback']
        )
    db.session.add(response)
    db.session.commit()
    return jsonify({'response': response.to_dict}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def prepare_index_json():
    responses = db.session.query(Response).all()
    response_arr = [response.to_dict for response in responses]
    return response_arr

if __name__ == '__main__':
    app.run(debug=True)
