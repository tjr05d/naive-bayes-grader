require 'active_record'
require 'pg'

# Open the db connection with the gm_dump db
ActiveRecord::Base.establish_connection(
  adapter:  'postgresql', # or 'postgresql' or 'sqlite3'
  host:     'localhost',
  database: 'gm_dump',
  username: 'whoisjose04',
  password: 'your_password'
)

# Define the classes based on the database
class SubmissionItem < ActiveRecord::Base
  belongs_to :submission
  belongs_to :item_content, polymorphic: true
end

class SubmissionResponse < ActiveRecord::Base
  belongs_to :submission
  has_one :submission_item, as: :item_content
end

class Task < ActiveRecord::Base
  has_many :submissions

  #Get the task of that title from the most recent cohort
  def self.get_cohort_task(task_name)
    ordered_tasks = Task.where(title: task_name).order(created_at: :desc)
    #index 5 in FLL C5
    task = ordered_tasks[10]
  end
end

class Unit < ActiveRecord::Base
end

class Submission < ActiveRecord::Base
  has_many :submission_responses
  has_many :submission_items
  belongs_to :task
end

#Get the task of that title from the most recent cohort
task_name = ARGV[0]
question = Task.get_cohort_task(task_name)
student_responses = []

#loop through the question and collect all the student responses
question.submissions.each do |submission|
  answer = submission.submission_items
                     .where(item_content_type: "SubmissionResponse")
                     .first.item_content
                     .response_raw
  student_responses << answer
end


#close the gm_dump db_connection
ActiveRecord::Base.connection.close

#open the connection with the grader_api_dev db
ActiveRecord::Base.establish_connection(
  adapter:  'postgresql',
  host:     'localhost',
  database: 'grader_api_dev',
  username: 'whoisjose04',
  password: 'your_password'
)

class Question < ActiveRecord::Base

end

class Response < ActiveRecord::Base

end

#create the new question
new_question = Question.create(title: question.title, prompt: question.prompt_raw, unit_id: nil)
puts "You have created one new question titled #{new_question.title}"
#create the new submissions that are asscoiated with that question
#submission items will be the students first submission attempt when addrssing the problem
created_responses = []

student_responses.each do |answer|
   new_response = Response.create(answer: answer,
                                  role: nil,
                                  categories_id: nil,
                                  questions_id: new_question.id)
  created_responses << new_response
  end

puts "#{created_responses.count} have been created for #{new_question.title}"
