import unittest
from app import create_app
from models import setup_db, Videographer
from flask_sqlalchemy import SQLAlchemy
import json
from functools import wraps
from mock import patch, Mock


permission = ''


class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(self):
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

        self.new_video = {
            'videographerId': 1,
            'title': 'Car race',
            'description': 'Filmed with iphone on i-25',
            'url': 'ab32dRe7'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    @classmethod
    def tearDownClass(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "portfolio_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.engine.execute('drop table videographer cascade;')
            self.db.engine.execute('drop table video cascade;')
            pass


    def test_1_create_videographer_success(self):
        returned = {
                'permissions': ['post:videographer']
            }

        mock = Mock(return_value=returned)
        patch('auth.auth.verify_decode_jwt', mock).start()

        res = self.client().post('/videographers', json=self.new_videographer, headers={'Authorization': 'bearer 123jasdflkj'} )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['videographer']['firstName'], 'Dan')


    def test_2_create_videographer_not_authorized_fail(self):
        returned = {
                'permissions': ['']
            }

        mock = Mock(return_value=returned)
        patch('auth.auth.verify_decode_jwt', mock).start()


        res = self.client().delete('/videographers/1', headers= {'Authorization': 'bearer 123jasdflkj'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'Not authorized.')


    def test_3_patch_videographer_success(self):
        returned = {
                'permissions': ['patch:videographer']
            }

        mock = Mock(return_value=returned)
        patch('auth.auth.verify_decode_jwt', mock).start()

        editedVideographer = self.new_videographer
        editedVideographer['firstName'] = "Daniel"
        editedVideographer['id'] = 1

        res = self.client().patch('/videographers', json=editedVideographer, headers={'Authorization': 'bearer 123jasdflkj'} )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['videographer']['firstName'], 'Daniel')


    def test_4_patch_videographer_not_authorized_fail(self):
        returned = {
                'permissions': ['']
            }

        mock = Mock(return_value=returned)
        patch('auth.auth.verify_decode_jwt', mock).start()

        editedVideographer = self.new_videographer
        editedVideographer['firstName'] = "Mike"
        editedVideographer['id'] = 1

        res = self.client().patch('/videographers', json=editedVideographer, headers={'Authorization': 'bearer 123jasdflkj'} )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'Not authorized.')



    def test_5_get_single_videographer_success(self):
        returned = {
                'permissions': ['']
            }

        mock = Mock(return_value=returned)
        patch('auth.auth.verify_decode_jwt', mock).start()

        res = self.client().get('/videographers/daniel-man', headers={'Authorization': 'bearer 123jasdflkj'} )
        data = json.loads(res.data)

        self.assertEqual(data['firstName'], "Daniel")
        self.assertEqual(res.status_code, 200)


    def test_6_get_single_videographer_404_error(self):
        returned = {
                'permissions': ['']
            }

        mock = Mock(return_value=returned)
        patch('auth.auth.verify_decode_jwt', mock).start()

        res = self.client().get('/videographers/mike-brown', headers={'Authorization': 'bearer 123jasdflkj'} )
        data = json.loads(res.data)
        print(data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')


    def test_7_add_video_success(self):
        returned = {
                'permissions': ['post:video']
            }

        mock = Mock(return_value=returned)
        patch('auth.auth.verify_decode_jwt', mock).start()

        res = self.client().post('/videos', json=self.new_video, headers={'Authorization': 'bearer 123jasdflkj'} )
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['video']['title'], self.new_video['title'])


    def test_8_add_video_not_authorized_401_error(self):
        returned = {
                'permissions': ['']
            }


        mock = Mock(return_value=returned)
        patch('auth.auth.verify_decode_jwt', mock).start()


        res = self.client().post('/videos', json=self.new_video, headers= {'Authorization': 'bearer 123jasdflkj'})
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'Not authorized.')


    def test_9_delete_video_resource_not_found_401_failure(self):
        returned = {
                'permissions': ['post:video']
            }


        mock = Mock(return_value=returned)
        patch('auth.auth.verify_decode_jwt', mock).start()


        res = self.client().delete('/videos/1', headers={'Authorization': 'bearer 123jasdflkj'} )
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 401)


    def test_11_delete_video_success(self):
        returned = {
                'permissions': ['delete:video']
            }

        mock = Mock(return_value=returned)
        patch('auth.auth.verify_decode_jwt', mock).start()

        res = self.client().post('/videos', json=self.new_video, headers={'Authorization': 'bearer 123jasdflkj'} )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['video']['title'], self.new_video['title'])
    

    def test_12_delete_videographer_not_authorized_401_error(self):
        returned = {
                'permissions': ['post:videographer']
            }

        mock = Mock(return_value=returned)
        patch('auth.auth.verify_decode_jwt', mock).start()


        res = self.client().delete('/videographers/1', headers= {'Authorization': 'bearer 123jasdflkj'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'], 'Not authorized.')


    def test_13_delete_video_not_authorized_404_error(self):
        returned = {
                'permissions': ['delete:video']
            }


        mock = Mock(return_value=returned)
        patch('auth.auth.verify_decode_jwt', mock).start()


        res = self.client().delete('/videos/565', headers={'Authorization': 'bearer 123jasdflkj'} )
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')


    def test_14_delete_videographer_success(self):
        returned = {
                'permissions': ['delete:videographer']
            }

        mock = Mock(return_value=returned)
        patch('auth.auth.verify_decode_jwt', mock).start()


        res = self.client().delete('/videographers/1', headers= {'Authorization': 'bearer 123jasdflkj'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted']['id'], 1)


if __name__ == '__main__':
    unittest.main()
