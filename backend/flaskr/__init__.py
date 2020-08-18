import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_ques(request, ques_list):
    index = request.args.get('page', 1, int)
    start = (index-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    curr_list = ques_list[start:end]
    return curr_list


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app)
    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods",
                             "GET, POST, DELETE, PATCH, OPTIONS")
        return response

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route("/categories")
    def categories():
        try:
            categories = Category.query.all()
            ans = {y.id: y.type for y in categories}
            return jsonify({
                "success": True,
                "categories": ans
            })
        except:
            abort(404)

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
    @app.route("/questions/")
    def questions_get():
        ques = Question.query.all()
        ques = [q.format() for q in ques]
        curr_ques = paginate_ques(request, ques)
        if len(curr_ques) == 0:
            abort(404)

        categor = Category.query.all()
        categor = {c.id: c.type for c in categor}

        return jsonify({
                "success": True,
                "questions": curr_ques,
                "total_questions": len(ques),
                "categories": categor,
                "current_category": None
            })

    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''

    @app.route('/questions/<ques_id>', methods=['DELETE'])
    def delete_question(ques_id):
        print(ques_id)
        ans = Question.query.filter(Question.id == ques_id).one_or_none()

        if not ans:
            abort(422)

        deleted_ques = ans.question
        ans.delete()
        return jsonify({
            "success": True,
            "deleted_ques": deleted_ques
        })

    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        term = request.args.get('search')

        if term is None:
            abort(422)
        search_term = '%{}%'.format(term)
        ans = Question.query.filter(Question.question.ilike(search_term)).all()
        search_ans = [s.format() for s in ans]
        return jsonify({
            'success': True,
            'questions': search_ans,
            'totalQuestions': len(search_ans),
            'currentCategory': None
        })

    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    @app.route('/questions/form', methods=['POST'])
    def new_question():
        data = request.get_json()
        question = request.get_json().get("question")

        answer = request.get_json().get("answer")

        diff = request.get_json().get("difficulty")

        cate = request.get_json().get("category")
        ques = Question(question=question, answer=answer,
                        category=cate, difficulty=diff)
        ques.insert()

        return jsonify({
            "success": True,
            "created_ques": question,
            "answer": answer,
            "difficulty": diff,
            "category": cate
        })
    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<category_id>/questions', methods=['GET'])
    def get_ques_by_category(category_id):
        ques = Question.query.filter(Question.category == category_id).all()
        if len(ques) == 0:
            abort(422)
        answer = [q.format() for q in ques]
        return jsonify({
            'success': True,
            'questions': answer,
            'totalQuestions': len(answer),
            'currentCategory': category_id
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
    @app.route('/quizzes', methods=['POST'])
    def random_ques():
        try:
            data = request.get_json()

            previous_questions = data.get('previous_questions', None)
            category_id = data.get('quiz_category', None)['id']
            if category_id:
                ans = Question.query.filter(
                    Question.category == category_id).all()
            else:
                ans = Question.query.all()

            s = []
            for i in ans:
                if i.id not in previous_questions:
                    s.append(i)

            random.shuffle(s)
            ans = ''
            if len(s) != 0:
                ans = s[0].format()
            return jsonify({
                "success": True,
                "question": ans
            })
        except:
            abort(422)

    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422
    return app

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400
    return app
