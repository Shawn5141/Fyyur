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


## End Point Reference 
### GET '/categories'
- Fetches a set with value as name for different category.
- Request Arguments: None
- Returns: json format.
- METHOD URL: curl http://127.0.0.1:5000/categories
- Smaple:
```
  {                                                                                         
  	"categories": [ 
  	  "Science", 
  	  "Art",
  	  "Geography",
  	  "History",
  	  "Entertainment",
  	  "Sports" ], 
  	"success": true
 }     
```

### GET '/questions'
-  Fetch a list of questions includes 'answer', 'category', 'difficulty', 'id', and 'question' inside from dataset and their corresponsding categories as current_category.
-  Request Argument: Page can be use for showing different paginated question
-  Return an object that inclues categories, current_categories, questions, status, total_questions.
-  METHOD URL: curl http://127.0.0.1:5000/questions
-  Smaple:
```
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "current_category": [
    "Entertainment", 
    "Entertainment", 
    "History", 
    "Entertainment", 
    "History", 
    "Sports", 
    "Sports", 
    "History", 
    "Geography", 
    "Geography"
  ], 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 20
}

```

### DELETE '/questions/int:question_id'
- Delete questoin with question_id from database 
- Request Argument: None
- Return : status of delete and deleted question id
- Method URL: curl -X DELETE http://127.0.0.1:5000/questions/1 
- Sample:

```
{
 "id": 2,
 "success": true
}
```

### POST '/questions' 
-  Create question with specified content of question, answer, category and difficulty.
-  Request Argument:  question, answer, category and difficulty.
-  Return status of create, created question id, current questions and number of total question
-  Method URL: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "Who invented E = mc^2?", "answer": "Albert Einstein", "difficulty": 2, "category": "1" }'
```
{
  "created": 27, 
  "questions": [
    {
      "answer": "Albert Einstein", 
      "category": 1, 
      "difficulty": 2, 
      "id": 27, 
      "question": "Who invented E = mc^2?"
    }
  ], 
  "success": true, 
  "total_questions": 20
}

```

### POST '/questions/search'
-  Fetch question based on question with provided keyword
-  Request Argument: searchTerm
-  Return : success status, current question, total question and current_category
-  Method URL: curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "what"}'
-  Sample:
```
{
  "current_category": [
    4, 
    5, 
    5, 
    3, 
    2, 
    1, 
    1
  ], 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_questions": 7
}

```

### GET '/categories/<int:category_id>/questions'
-  Retrieve questions based on categories
-  Request Argument: None
-  Return : success, questions, total_questions and current_category
-  Method URL: curl http://localhost:5000/categories/0/questions
```
{
  "current_category": [
    "Science", 
    "Science", 
    "Science", 
    "Science", 
    "Science", 
    "Science"
  ], 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Shawn", 
      "category": 1, 
      "difficulty": 1, 
      "id": 24, 
      "question": "who am i"
    }, 
    {
      "answer": "Albert Ernestine", 
      "category": 1, 
      "difficulty": 1, 
      "id": 25, 
      "question": "Who invent E=mc^2"
    }, 
    {
      "answer": "Albert Einstein", 
      "category": 1, 
      "difficulty": 2, 
      "id": 27, 
      "question": "Who invented E = mc^2?"
    }
  ], 
  "success": true, 
  "total_questions": 20
}

```

### POST '/quizzes'
- Post questoin randomly from categories.
- Able to select all the categories or a specific one.
- The questions from the category will jump up randomly but without previous shown ones.
- METHOD URL: curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"type": "Sports", "id": "5"}}'
```
{
  "question": {
    "answer": "Brazil", 
    "category": 6, 
    "difficulty": 3, 
    "id": 10, 
    "question": "Which is the only team to play in every soccer World Cup tournament?"
  }, 
  "success": true
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

## Authors
Shou-En Hsiao is in charged of backend Web Api in __init__.py and test_flask.py files.  All other files are contributed by Udacity- Full Stack Web Developer Nanodegree.