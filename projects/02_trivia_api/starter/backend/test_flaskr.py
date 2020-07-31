import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('caryn', 'mypass','localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # Get paginate questoin 
    def test_get_paginated_questions(self):

        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
    

    def test_get_paginated_questions_fail(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['questions'],[])
        self.assertEqual(data['total_questions'],0)
        self.assertEqual(data['current_category'],[])


    def test_get_category(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])


    def test_create_question(self):
        res = self.client().post('/questions',json={'question':'how many atom in periodic table',
                                        'answer':'144','category':'1','difficulty':'2'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_create_question_fail_by_bad_request(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['questions'],[])
        self.assertEqual(data['total_questions'],0)
        self.assertEqual(data['current_category'],[])


    def test_create_question_fail_because_empty(self):
        res = self.client().post('/questions',json={'question':'',
                                        'answer':'','category':'','difficulty':''})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['questions'],[])
        self.assertEqual(data['total_questions'],0)
        self.assertEqual(data['current_category'],[])

    def test_delete_book(self):
        question = Question(question='a', answer='a', category=1, difficulty=1)
        question.insert()
        question_id = question.id
        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_book_fail_by_empty(self):
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['questions'],[])
        self.assertEqual(data['total_questions'],0)
        self.assertEqual(data['current_category'],[])


    def test_search_question(self):
        question = Question(question='@@@', answer='a', category=1, difficulty=1)
        question.insert()
        res = self.client().post('/questions/search',json={'searchTerm':'@@'})
        data = json.loads(res.data)
        #print("DATA",data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['current_category'])
        question.delete()

    def test_search_question_fail(self):
        res = self.client().post('/questions/search',json={'searchTerm':'WWW'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['questions'],[])
        self.assertEqual(data['total_questions'],0)
        self.assertEqual(data['current_category'],[])

    def test_retrieve_by_categories(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['total_questions'])


    def test_retrieve_by_categories_fail(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['questions'],[])
        self.assertEqual(data['total_questions'],0)
        self.assertEqual(data['current_category'],[])


    def test_play_quiz(self):
        new_quiz = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'Sports',
                'id':'5'
            }
        }
        
        res = self.client().post('/quizzes', json=new_quiz)
        data = json.loads(res.data)
        #print(data['question'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_empty_play_quiz(self):
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['questions'],[])
        self.assertEqual(data['total_questions'],0)
        self.assertEqual(data['current_category'],[])






# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()