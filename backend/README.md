# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 

Example:
{'0' : "Science",
'1' : "Art",
'2' : "Geography",
'3' : "History",
'4' : "Entertainment",
'5' : "Sports"}

GET '/questions/'
- Fetches a dictionary of paginated questions in which the keys are ids and value is the question, answer , category and difficulty to the corresponding question
- Request Argument: None
- Return: An object with a single key, questions, that contains an object of id: id, value: questions, answer, category, difficulty paginated 10 at a time.

Example:
{
    'questions': [{"id": 1,"question":"What is chemical formula of Sodium?","answer":"Na","difficulty":"1","category":"0"}],
    'total_questions': 1,
    'categories':{"0":"Science","1":"Art","2":"Geography","3":"History","4":"ENTERTAINMENT","5":"Sports"},
    'current_category':None
}

POST '/questions/search'
- Fetches a dictionary of question whose value matches with the search string given as an input by the user
- Request Argument: {'search' : 'Your search term'}
- Return: A JSON object with a list of questions object matching the searching string. 

Example:
search = sodium
{
    'questions':[{"id": 1,"question":"What is chemical formula of Sodium?","answer":"Na","difficulty":"1","category":"0"}],
    'totalQuestions':1,
    'currentCategory':None
}

POST '/questions/form'
-Adds a new question to the database in which question, answer, category and difficulty are provided by the user. 
-Request Argument: {'question':'Your question','answer':'Your answer','category':'category_id','difficulty':'Difficulty level'}
-Return:A JSON object of the created question 

Example:
question = 'How many bones in human body?'
answer = '206'
category = 0
difficulty = 1
{
    'created_ques': 'How many bones in human body?',
    'answer':'206',
    'category': 0,
    'difficulty': 1
}

GET '/categories/<category_id>/questions'
- Fetches a dictionary of all questions corresponding to the category_id passed as an argument in url.
- Request Argument: None
- Returns: A JSON object of all questions corresponding to category_id

Example:
category_id = 0
{
    'questions': [{"id": 1,"question":"What is chemical formula of Sodium?","answer":"Na","difficulty":"1","category":"0"}],
    'totalQuestions':1,
    'currentCategory':0
}

POST '/quizzes'
-Fetches a random question based on the choice of category by the user in form of a JSON object.
-Request Argument:{'previous_ques':'Previous question id "None" if running first time','quiz_category':'category id "None" if all categories included'}
-Returns: A JSON object of a random question based on category passed which is different from it's previous question

Example:
quiz_category = 0
previous_ques = 1
{
    'question':{'id':2,'question':'How many bones in human body?','answer':'206','category':0,'difficulty':1}
}

DELETE '/questions/<ques_id>'
-Delets a question from the database based on the question id passed.
-Request Argument: None
-Returns: A JSON object of deleted question.

Example: 
ques_id = 1
{
    'deleted_ques':'What is chemical formula of Sodium?'
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```