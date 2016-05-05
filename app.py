from flask import Flask, request, jsonify, abort, make_response, json
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/grader_api_dev'
db = SQLAlchemy(app)

class JsondModel(object):
    @property
    def to_dict(self):
        return {key: getattr(self, key) for key in self.external_attrs}

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
    external_attrs = ['answer', 'cat', 'feedback', 'id', 'score']

    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String())
    cat = db.Column(db.String())
    feedback = db.Column(db.String())
    questions_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    def __init__(self, answer, cat, feedback, questions_id):
        self.answer = answer
        self.cat = cat
        self.feedback = feedback
        self.questions_id = questions_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

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
