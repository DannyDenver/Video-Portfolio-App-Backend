# Videographer Portfolio Backend

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

## Running the server

First ensure that you are working using your created virtual environment.

```bash
python manage.py runserver
```

## Roles 

#### Public (no sign in)
- able to see list of videographers
- able to see individual portfolios

#### Videographer
- able to create videographer profiles
- able to add videos to profiles
- able to update videographer profiles

#### Portfolio Site Admin
- all permissions of a videographer
- can delete videographers and their corresponding profile
- can delete videos


## Error Handling

Errors are returned as JSON objects in the following format: 
    {
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'

    }

This API will return three error types when requests fail: 
    - 400: Bad Request
    - 404: Not Found
    - 422: Unprocessable Entity
    - 500: Internal Server Error

## Endpoints
- GET '/categories'
- GET '/questions'
- GET '/categories/<int:category_id>/questions'
- POST '/questions'
- POST '/quizzes'
- POST '/questions/search'
- DELETE '/questions/<int:id>'

### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetches all the questions
- Request Arguments: None
- Request Parameters: page number
- Returns: an object with properties:
      questions - with current questions on the page
      total_questions - number of total questions in the database
      categories - dictionary of categories in which the keys are the ids and the value is the                    string category name
      currentCategory - is the currently selected category
    {
        'success': boolean
    }


GET '/categories/<int:category_id>/questions'
- Fetches all the questions by a category id
- Request Arguments: category_id- number
- Request Parameter: page -number
- Returns: an object with properties:
      questions - current questions on the page
      totalQuestions - number of total questions in this category
      categories - dictionary of categories in which the keys are the ids and the value is the                    string category name
      currentCategory - is the currently selected category id
    {
        'questions': [questions],
        'totalQuestions': number,
        'categories': categoryDictionary,
        'currentCategory': number
    }

POST '/questions'
- creates a new question using the submitted question, answer, category and difficulty. Returns success or a 422 error.
    { 'success': boolean }

POST '/quizzes'
- fetches the next quiz question based on the submitted category and previous question ids. 
- Returns: a question object with the following properties: id, question, answer, category and difficulty. 
    { 'question': question }

POST '/questions/search'
- fetches the questions based on the submitted searchTerm 
- Returns: an array of questions and the total number of questions that match the search term
    {
      'questions': [questions],
      'total_questions': number
    }

DELETE '/questions/<int:id>'
- removes a question from the quiz
- Request Arguments: question id
- Returns: a success object with the id of the deleted question:
    {
        'success': True,
        'deleted': number
    }
    or a 404 error if deleting fails.


## Testing
To run the tests, run

python tests.py
