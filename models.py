from app import db
from flask.ext.sqlalchemy import SQLAlchemy
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob

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
    external_attrs = ['title', 'id', 'feedback', 'question_id', 'info']

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
    def info(self):
        return {'unit':self.question.unit.title, 'question': self.question.title}

class Response(db.Model, JsondModel):
    __tablename__ = 'responses'
    external_attrs = ['answer', 'categories_id', 'id', 'role', 'info', 'classify_response']
    dumb_ass_attrs= ['answer','categories_id', 'id']

    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text)
    role = db.Column(db.String()    )
    categories_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    questions_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    def __init__(self, answer, role, categories_id, questions_id):
        self.answer = answer
        self.role = role
        self.categories_id = categories_id
        self.questions_id = questions_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @property
    def info(self):
        return {'unit':self.question.unit.title, 'question': self.question.prompt}

    @property
    def classify_response(self):
        #pulls the training data from previous responses for this question
        # train = db.session.query(Response).filter(Response.questions_id==1)
        # question_responses= db.session.query(Response).filter(Response.questions_id==self.questions_id)
        # #prepare that data for the classifier by creating a list
        # training_responses = [data_item.tim_to_dict for data_item in question_responses]
        # #empty array to put the training tuples in
        # training_data = []
        # #loop to take the info from the list and create the tuples that go in the training data array
        # for data_point in training_responses:
        #     training_data.append((data_point["answer"], data_point["categories_id"]))
        # #creates the classifier for the response that is recieved
        # question = NaiveBayesClassifier(training_data)
        question = self.generate_classifier
        #classiifies the response into a category based on probability
        category_decision = question.classify(self.answer)
        #get the category object that belongs to that response
        category_object = Category.query.get(int(category_decision))
        #gets the probability that the response falls in one of the categories
        prob_cat = question.prob_classify(self.answer)
        #loop to return the prob that the response falls in each of the categories
        cat_probabilities = []
        #loop to get the probability of all the categories that exist for that classifier
        for cat in question.labels():
            cat_title = Category.query.get(int(cat)).title
            cat_probabilities.append((cat_title, prob_cat.prob(cat)))
        #return a hash with the category picked as well as the probabilities fo all the categories of the classifier
        return {'category' : category_object.title, 'probabilities' : cat_probabilities}
# "++++++++++++++++++++++++++++++++++++++++++++"
#         def improves_training_set(self, test_data):
#             #query the response table for responses that are used for test_data, these data points should be choosen by an instructor
#             test_data = Response.query.filter(Response.role = "test" AND Response.question_id)
#
#              current_accuracy = self.classify_response
#             #check the accuracy of the classifier without the new response added
#             current_accuracy = classifier.accuracy(test_data)
#             #add the current candidate that was just labeled to the classifier
#             classifier.update(self)
#             #check if the new dat_point improves the accuracy of the training set
#             updated_accuracy = classifier.accuracy(test_data)
#
#             if updated_accuracy > current_accuracy:
#                 self.role = "training"


        def generate_classifier(self):
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
            return question
