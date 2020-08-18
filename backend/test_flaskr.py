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
        self.database_name = "trivia"
        self.database_path = "postgres://{}@{}/{}".format(
            'postgres:abcd', 'localhost:5432', self.database_name)
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

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        res = self.client().get('/questions/')
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_404_questions(self):
        res = self.client().get('/questions/?page=3')
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Not found')

    def test_delete_question(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data.decode('utf-8'))

        question = Question.query.filter(Question.id == 1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_ques'])
        self.assertEqual(question, None)

    def test_422_delete_question(self):
        res = self.client().delete('/questions/3000')
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Unprocessable')

    def test_search_successfull(self):
        res = self.client().post('/questions/?search=a')
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])

    def test_search_unsuccessfull(self):
        res = self.client().post('/questions/')
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_successfull_new_question(self):
        res = self.client().post('/questions/form',
                                 json={'question': "", 'answer': "", 'difficulty': 3, 'category': '0'})
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created_ques'], "")
        self.assertEqual(data['answer'], "")
        self.assertEqual(data['difficulty'], 3)
        self.assertEqual(data['category'], '0')

    def test_successfull_get_by_category(self):
        res = self.client().get('/categories/0/questions')
        data = json.loads(res.data.decode('utf-8'))

        ques = Question.query.filter(Question.category == '0').all()
        answer = [q.format() for q in ques]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['questions'], answer)
        self.assertTrue(data['totalQuestions'])
        self.assertEqual(data['currentCategory'], '0')

    def test_unsuccessfull_get_by_category(self):
        res = self.client().get('/categories/5/questions')
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
