import unittest
from app import create_app
from models import setup_db
from flask_sqlalchemy import SQLAlchemy
import json
from functools import wraps
from mock import patch, Mock


permission = ''


class TestStringMethods(unittest.TestCase):


    def mock_verify_decode_jwt(token):
        return {
            'permissions': [permission]
        }

    def mock_get_token_auth_header():
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                print(f)

                return f(*args, **kwargs)
            return decorated_function
        return decorator

    # patch('auth.auth.verify_decode_jwt', mock_verify_decode_jwt).start()


    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "portfolio_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_videographer = {
            'firstName': 'Dan',
            'lastName': 'Man',
            'location': 'Denver',
            'bio': 'Can type.',
            'profilePictureUrl': 'wwww.googs.com'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_create_videographer_success(self):
        def mock_verify_decode_jwt(token):
            return {
                'permissions': [permission]
            }
 
        patch('auth.auth.verify_decode_jwt', mock_verify_decode_jwt).start()


        permission = 'post:videographer'
        res = self.client().post('/videographers', json=self.new_videographer, headers={'Authorization': 'bearer 123jasdflkj'} )
        data = json.loads(res.data)
        print(data)
        self.assertEqual(data['videographer']['firstName'], 'Dan')


if __name__ == '__main__':
    unittest.main()
