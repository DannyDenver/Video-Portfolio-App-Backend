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


## Signing up 

- New users will be set up with the videographer role
- Link: https://dannydenver.auth0.com/login?state=g6Fo2SBCeHFneGlxVWltTC0wLUp6QVVvNG43WXRHT21CTjJTT6N0aWTZIG85WnhVLWU2WjJfRWI5M1dqTXMzZjdwa3lUSVE1eEVzo2NpZNkgUXozQ0w4OHRHcFpZSlFGcVhRTmpkemdYVzBRQ210Y3A&client=Qz3CL88tGpZYJQFqXQNjdzgXW0QCmtcp&protocol=oauth2&audience=videoportfolio&response_type=token&redirect_uri=https%3A%2F%2Fvideo-portfolio.herokuapp.com



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

## Resources

### Videographer
#### with properties
- id
- firstName
- lastName
- location
- bio
- profilePictureUrl
- videos

### Video
#### with properties 
- id
- videographer_id
- url
- title
- description


## Endpoints
- GET '/videographers'
- POST '/videographers'
- PATCH '/videographers'
- GET '/videographers/<string:name>'
- DELETE '/videographers/<int:id>'
- POST '/videos'
- DELETE '/videos/<int:id>'


#### GET '/videographers'
- Fetches all the videographer profiles
- Request Arguments: None
- Returns: an array of videographers in short format without videos

#### POST '/videographers'
- creates a new videographer
- Body: new videographer
- Returns: the created videographer


#### PATCH '/videographers'
- Updates an existing videographer
- Body: updated videographer
- Returns: videographer in long form

#### GET '/videographers/<string:name>
- Gets an individual videographer with videos
- Request Arguments: name of videographer in form first name '-' last name ex 'dan-taylor'

#### DELETE '/videographers/<int:id>'
- Deletes an individual videographer using their id
- Request Arguments: videographer's id
- Returns: object with the following properties: 
        {
            'success': True,
            'deleted': {
                "id": videographer.id,
                "firstName": videographer.first_name,
                "lastName": videographer.last_name
            }
        }

#### POST '/videos'
- Adds a video to a videographer's portfolio
- Body: video
- Returns video

#### DELETE '/videos/<int:id>'
- Deletes a video from a videographer's portfolio
- Request Arguments: video's id
- Returns: { 'success': True} or errors 404, 422


## Testing
To run the tests, run

python tests.py
