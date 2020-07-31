import os
from flask import Flask, request, abort, jsonify,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category,db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  # CORS Headers 
  CORS(app)

  
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')

      return response

  

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def retrieve_categories():
      categories  ={category.format()['id']:category.format()['type'] for category in  Category.query.order_by(Category.id).all()}
      #print("category get",categories)
      return jsonify({
        'success':True,
        'categories':categories
        })


  def paginate_data(request, selection):
      #print("paginate")
      page = request.args.get('page', 1, type=int)
      #print("page",page)
      start =  (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE

      questions = [question.format() for question in selection]
      current_question = questions[start:end]
      current_category = [question['category'] for question in questions[start:end]]

      #print("current category",current_category)
      return current_question,current_category

  # DOTO Need to check this
  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/')
  @app.route('/questions', methods=['GET'])
  def retrieve_questions():

      selection = Question.query.order_by(Question.id).all()
      
      current_question,current_category = paginate_data(request, selection)
      
      #categories  =[category.format()['type'] for category in  Category.query.order_by(Category.id).all()]
      categories  ={category.format()['id']:category.format()['type'] for category in  Category.query.order_by(Category.id).all()}
      
      #categories = ["Undefined"]+categories
      #print("current category",current_category,categories)
      current_category = [categories[i] for i in current_category]
      #current_category = current_category
      #print("current_question",current_question)
      #print("current category",current_category)
      if len(current_question) == 0:
          #print("no selection")
          abort(404)
      
      
      return jsonify({
          'success': True,
          'questions': current_question,
          'categories': categories,
          'total_questions': len(Question.query.all()),
          'current_category': current_category
      })



 


 

  
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_book(question_id):
      question = Question.query.filter(Question.id == question_id).one_or_none()
      #print("question",question)
      if question is None:
          abort(404)
      try:
          question.delete()
          return jsonify({
          'id': question_id,
          'success': True
          }), 200
      except:

          abort(422)
     
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
    if not body:
        abort(400)
    new_question = body.get('question', '')
    new_answer = body.get('answer', '')
    new_category = body.get('category', '')
    new_difficulty = body.get('difficulty', '')
    #print(new_question,new_answer,new_category)

    if ((new_question == '') or (new_answer == '')
        or (new_category == '') or (new_difficulty == '')):
        #print(new_question,new_answer,new_category,new_difficulty)
        #print("empty")
        abort(422)
   

    try:
      #print("create question")
      question = Question(question=new_question, answer=new_answer,
                   category=new_category, difficulty=new_difficulty)
      question.insert()
      #print("insert")
      selection = Question.query.filter(Question.id == question.id).order_by(Question.id).all()
      #print("selection",selection)
      paginate,current_category = paginate_data(request, selection)
      
      return jsonify({
        'success': True,
        'created': question.id,
        'questions': paginate,   # TODO need to paginate
        'total_questions': len(Question.query.all())
      })
    except:
      #print("abort")
      abort(422)
  




  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''


  @app.route('/questions/search', methods=['POST'])
  def search_question(): 
    data = request.get_json()
    search_term = data.get('searchTerm', '')
    #print("search_term",search_term)
    if not search_term:
      abort(422)

    try:
      results = Question.query.filter(Question.question.ilike("%"+search_term+"%")).all()

      
      if len(results) == 0:
          #print("result",result)
          abort(404)
      paginate,current_category = paginate_data(request, results)
      return jsonify({
        'success':True,
        'questions': paginate,
        'total_questions': len(results),
        'current_category': current_category
        })
    except:
      abort(404)

      
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def retrieve_by_categories(category_id):
      
      
      selection = Question.query.order_by(Question.id).filter(Question.category==category_id).all()
      
      current_question,current_category = paginate_data(request, selection)
      
      categories  ={category.format()['id']:category.format()['type'] for category in  Category.query.order_by(Category.id).all()}
      
      #print(categories)
      current_category = [categories[i] for i in current_category]
      #print(categories,current_category)
      if len(current_question) == 0:
          
          abort(404)
      
      
      return jsonify({
          'success': True,
          'questions': current_question,
          'total_questions': len(Question.query.all()),
          'current_category': current_category
      })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes',methods=['POST'])
  def play_quizzes():
      data = request.get_json()
      previous_questions = data.get('previous_questions', '')
      quiz_category = data.get('quiz_category', '')
      #print("quiz",quiz_category,int(quiz_category['id']))
      if not quiz_category :
        abort(404)
     
      
      
      if quiz_category['type'] == 'click':
        available_questions = Question.query.filter(
            Question.id.notin_(previous_questions)).all()
      
      else:
        available_questions = Question.query.filter_by(
          category = quiz_category['id']).filter(Question.id.notin_(previous_questions)).all()

      new_question = available_questions[random.randrange(
          0, len(available_questions))].format() if len(available_questions) > 0 else None
      #print("new ",new_question,available_questions)
      return jsonify({
        'success': True,
        'question': new_question
        })
    


  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):

      return jsonify({
          "success": False, 
         'questions': [],
          'total_questions': 0,
          'current_category': []
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
        return jsonify({
            "success": False, 
            'questions': [],
            'total_questions': 0,
            'current_category': []
        }), 422

  @app.errorhandler(400)
  def bad_request(error):
      #print("400==",error)
      return jsonify({
          "success": False, 
          'questions': [],
          'total_questions': 0,
          'current_category': []
      }), 400
  return app

    