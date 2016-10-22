from shared import db
from flask import jsonify
from textblob.tokenizers import WordTokenizer
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob


class JsondModel(object):
    @property
    def to_dict(self):
        return {key: getattr(self, key) for key in self.external_attrs}

#method to prepare data within the classify_response method
    @property
    def safe_to_dict(self):
        return {key: getattr(self, key) for key in self.filler_attrs}

# might not be needed

class Question(db.Model, JsondModel):
    __tablename__ = 'questions'
    external_attrs = ['title', 'prompt']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    prompt = db.Column(db.Text)
    responses = db.relationship('Response', backref='question', lazy= 'dynamic')
    categories = db.relationship('Category', backref='question', lazy= 'dynamic')

    def __init__(self, title, prompt):
        self.title = title
        self.prompt = prompt

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
        return {'question': self.question.title}

class Response(db.Model, JsondModel):
    __tablename__ = 'responses'
    external_attrs = ['answer', 'category_id', 'id', 'role', 'info', 'classify_response']
    filler_attrs = ['answer','category_id', 'id', 'role']

    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text)
    role = db.Column(db.String()    )
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    def __init__(self, answer, role, category_id, question_id):
        self.answer = answer
        self.role = role
        self.category_id = category_id
        self.question_id = question_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @property
    def info(self):
        return {'question': self.question.prompt}

    def generate_classifier(self):
        question_responses = Response.query.filter(
            (Response.question_id == self.question_id) &
            (Response.role == "training") &
            (Response.category_id != None))
        #prepare that data for the classifier by creating a list
        training_responses = [data_item.safe_to_dict for data_item in question_responses]
        #empty array to put the training tuples in
        training_data = []
        #loop to take the info from the list and create the tuples that go in the training data array
        tokenizer = WordTokenizer()
        for data_point in training_responses:
            token_answer = tokenizer.tokenizer(data_point["answer"], include_punc=True)
            training_data.append((token_answer, data_point["category_id"]))
        #creates the classifier for the response that is recieved
        question = NaiveBayesClassifier(training_data)
        return question

    def improves_training_set(self, cat_decision):
        testing_set = Response.query.filter(
            (Response.question_id == self.question_id) &
            (Response.role == "test"))

        test_responses = [data_item.safe_to_dict for data_item in testing_set]

        testing_data = [(dp["answer"], dp["category_id"]) for dp in test_responses]

        classifier = self.generate_classifier()
        #check the accuracy of the classifier without the new response added
        current_accuracy = classifier.accuracy(testing_data)
        print(current_accuracy)
        #add the current candidate that was just labeled to the classifier
        self.category_id = cat_decision
        new_data = [(self.answer, cat_decision)]
        print(classifier.show_informative_features(5))
        classifier.update(new_data)
        print(classifier.show_informative_features(5))
        #check if the new dat_point improves the accuracy of the training set
        updated_accuracy = classifier.accuracy(testing_data)
        print(updated_accuracy)
        if updated_accuracy > current_accuracy:
            self.role = "training"
            db.session.add(self)
            db.session.commit()
            return jsonify({'message': "This made me smarter :)",
                            'current_accuracy': current_accuracy,
                            'updated_accuracy': updated_accuracy
                            })
        else:
            return jsonify({'message': "This keep me dumb, like a dolphin:(",
                            'current_accuracy': current_accuracy,
                            'updated_accuracy': updated_accuracy
                            })

    def classify_response(self):
        question = self.generate_classifier()
        #classiifies the response into a category based on probability
        token_answer = tokenizer.tokenizer(self.answer, include_punc=True)
        category_decision = question.classify(token_answer)
        #get the category object that belongs to that response
        category_object = Category.query.get(int(category_decision))
        #gets the probability that the response falls in one of the categories
        prob_cat = question.prob_classify(token_answer)
        #loop to return the prob that the response falls in each of the categories
        cat_probabilities = []
        self.improves_training_set(category_decision)
        #loop to get the probability of all the categories that exist for that classifier
        for cat in question.labels():
            cat_title = Category.query.get(int(cat)).title
            cat_probabilities.append((cat_title, prob_cat.prob(cat)))
        #return a hash with the category picked as well as the probabilities fo all the categories of the classifier
        return jsonify({'question_id' : self.question_id,
                        'category' : category_object.title,
                        'feedback' : category_object.feedback,
                        'probabilities' : cat_probabilities
                        }), 201
