### Creating a new question

To add a question to the NB-Grader database make a post request to the endpoint https://naive-bayes-grader.herokuapp.com/grader/api/v1.0/questions with the content-type set to application json.

ex:
```ruby
title = "Hello World!"
prompt = "Please write the code the will output the string 'Hello World!' to the screen"

response = HTTParty.post("https://naive-bayes-grader.herokuapp.com/grader/api/v1.0/questions",
      :body => {
              'title' => title,
              'prompt' => prompt
        }.to_json,
      :headers => {
        'Content-type' => 'application/json'
        })
```
###  How to create a new test set

The test set is a series of tuples that we will use to determine how accurate out classifiers are when it comes to categorizing responses. This is not to be confused with the training set that will be used to build the classifiers. The test set can be thought of like a control group, so we must very sure that these responses are categorized accurately.

This means a couple of things:
  1. Create categories

  We need to have a category to assign the test data to. This means we need to response categories for that question.

  To create a category we need to make a post to the following endpoint "https://naive-bayes-grader.herokuapp.com//grader/categories" with the content-type set to application/json.

  ```ruby
  title = "Missing quotation marks"
  feedback = "It looks like you are missing some punctuation, remember strings are denoted by using quotation marks. Please try again!"
  question_id = 1

  response = HTTParty.post("https://naive-bayes-grader.herokuapp.com/grader/categories",
        :body => {
                'title' => title,
                'feedback' => feedback,
                'question_id' => question_id
          }.to_json,
        :headers => {
          'Content-type' => 'application/json'
          })
  ```

You likely will have an idea of the categories that you want to make. You likely want to think about the categories that you are going to have most often. The instructor responses in Goodmeasure already will give you a good idea of what is commonly missed.

  2. Create a new response with the role of "test".

  Before we begin training a classifier, we need to create the test set so we can ensure accurate decisions are being made. The test set will also be tested to see if a new piece of training data is in fact improving the accuracy of a classifier.

  To start we should have the most common answers that we know about for that category in the test set one time.

  For instance a test set for the sample question may look something like the following:
  ```python
  test = [
    ('puts "Hello world!"', 1), #1 being the id of the category that indicates correct
    ('p "Hello world!"', 1),
    ('print "Hello world!"', 1),
    ('puts Hello world!' , 2),
    ('p Hello world!', 2), # 2 is the id of the category that indicates missing quotation marks
    ('print Hello world!', 2)
  ]
  ```
  All of the response that are used to build the test set and the training set are held in the same table. The sets are built by querying for all of the responses that belong to that question id having the role of "test". So building your test set is done simply by creating response items with the role "test" and the category id for the category the response belongs to.

  Think of the test set as your control group. These response must be different from the responses in your training set, and 100% accurate to the category they belong to.

  Below is an example of a sample post request to add a response to the test set.

  ```ruby
  answer = 'puts "Hello world!"'
  category_id = 1
  question_id = 1

  response = HTTParty.post("https://naive-bayes-grader.herokuapp.com/grader/test_set",
        :body => {
                'answer' => answer,
                'category_id' => category_id,
                'question_id' => question_id
          }.to_json,
        :headers => {
          'Content-type' => 'application/json'
          })
  ```

  3. Now that we have the question created, the categories that will be decided upon for that question, and test set that will judge the accuracy of the classifier for that question. We need to create the training set that will be used to build the classifier for that question.

  Creating the responses for the training set will be very similar to creating the test responses. The only difference being the endpoint that we send the response to.

  ```ruby
  answer = 'p "Hello world!"'
  category_id = 1
  question_id = 1

  response = HTTParty.post("https://naive-bayes-grader.herokuapp.com/grader/training_set",
        :body => {
                'answer' => answer,
                'category_id' => category_id,
                'question_id' => question_id
          }.to_json,
        :headers => {
          'Content-type' => 'application/json'
          })
  ```
  If there are less than 5 responses in the training set, the training response will be added to the training set. If there are more, the response will be evaluated to determine if adding the response will improve the accuracy of the classifier or not.

  4. Now we have created the question, it's decision categories, test set, and training set we have everything that we need to build a classifier. That means we are ready to start classifying submissions

  Very similar to above, to classify a submission we send the response over to the endpoint `classify` with the only parameters being the students answer and the question id for the question that it belongs to:

  ```ruby
  answer = 'puts "Hello world!"'
  question_id = 1

  response = HTTParty.post("https://naive-bayes-grader.herokuapp.com/grader/classify",
        :body => {
                'answer' => answer,
                'question_id' => question_id
          }.to_json,
        :headers => {
          'Content-type' => 'application/json'
          })
  ```

  A JSON response will be returned containing the decision information for the submitted response
  ```js
    {"question_id" :  "1",
    "category": "Missing quotation marks",
    "feedback" :"It looks like you are missing some punctuation, remember strings are denoted by using quotation marks. Please try again!",
    "probabilities" : [
                      "Missing quotation marks" : "92.0",
                      "Correct" : "8.0"
                      ]
    }), 201
    ```
  With the information received it is then the to the clients discretion to act upon the results that are returned.
