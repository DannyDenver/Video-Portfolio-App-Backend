import os
import sys
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
from auth.auth import AuthError, requires_auth
from models import setup_db
from models import db


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    from models import Videographer, Video

    @app.route('/videographers', methods=['POST'])
    @requires_auth('post:videographer')
    def setup_videographer(jwt):
        videogooForm = request.get_json()
        videographer = Videographer(
            created_by=jwt['sub'],
            first_name=videogooForm['firstName'],
            last_name=videogooForm['lastName'],
            location=videogooForm['location'],
            bio=videogooForm['bio'],
            profile_url=videogooForm['profilePictureUrl'])
        videogooCopy = videographer.long()

        try:
            videographer.insert()
        except Exception:
            db.session.rollback()
            error = True
            print(sys.exc_info())
        finally:
            db.session.close()

        return jsonify({
            "videographer": videogooCopy
        })

    @app.route('/videographers', methods=['PATCH'])
    @requires_auth('patch:videographer')
    def patch_videographer(jwt):
        videogooForm = request.get_json()
        videogoo = Videographer.query.get(videogooForm['id'])

        videogoo.first_name = videogooForm['firstName']
        videogoo.last_name = videogooForm['lastName']
        videogoo.location = videogooForm['location']
        videogoo.bio = videogooForm['bio']
        videogoo.profile_url = videogooForm['profilePictureUrl']
        videogooCopy = videogoo.long()

        try:
            videogoo.update()
        except Exception:
            db.session.rollback()
            abort(422)
            print(sys.exc_info())
        finally:
            db.session.close()

        return jsonify({
            "videographer": videogooCopy
        })

    @app.route('/videographers', methods=['GET'])
    def get_videographers():
        videogoos = Videographer.query.all()
        return jsonify([videogoo.short() for videogoo in videogoos])

    @app.route('/videographers/<string:name>', methods=['GET'])
    def get_videographer(name):
        names = name.split('-')
        videogoo = Videographer.query.filter(
            Videographer.first_name == names[0].capitalize()
            ).filter(
                Videographer.last_name == names[1].capitalize()
                ).first()

        if videogoo is None:
            abort(404)

        return jsonify(videogoo.long())

    @app.route('/videographers/<int:id>', methods=['DELETE'])
    @requires_auth('delete:videographer')
    def delete_videographer(jwt, id):
        videographer = Videographer.query.get(id)

        if videographer is None:
            abort(404)

        try:
            videographer.delete()
        except Exception:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

        return jsonify({
            'success': True,
            'deleted': {
                "id": videographer.id,
                "firstName": videographer.first_name,
                "lastName": videographer.last_name
            }
        })

    @app.route('/videos', methods=['POST'])
    @requires_auth('post:video')
    def add_video(jwt):
        videoForm = request.get_json()
        video = Video(
            videographer_id=videoForm['videographerId'],
            title=videoForm['title'],
            description=videoForm['description'],
            url=videoForm['url'])
        videoCopy = video.serialize()

        try:
            video.insert()
        except Exception:
            db.session.rollback()
            error = True
            print(sys.exc_info())
        finally:
            db.session.close()

        return jsonify({
            "video": videoCopy
        })

    @app.route('/videos/<int:id>', methods=['DELETE'])
    @requires_auth('delete:video')
    def delete_video(jwt, id):
        video = Video.query.get(id)

        if video is None:
            abort(404)

        try:
            video.delete()
        except Exception:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

        return jsonify({
            'success': True
        })

    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                "success": False,
                "error": 422,
                "message": "unprocessable"
                }), 422

    @app.errorhandler(404)
    def notfound(error):
        return jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found"
                }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app
