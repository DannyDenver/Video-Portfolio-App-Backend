import os
import sys
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS
from sqlalchemy import func
from auth.auth import AuthError, requires_auth

app = Flask(__name__)

app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
CORS(app)
from models import Videographer, Video

@app.route('/videographers', methods=['POST'])
@requires_auth('post:videographer')
def setup_videographer(jwt):
    videogooForm = request.get_json()
    print(videogooForm)
    videographer = Videographer(first_name=videogooForm['firstName'], last_name=videogooForm['lastName'], location=videogooForm['location'], bio=videogooForm['bio'], profile_url=videogooForm['profilePictureUrl'])
    videogooCopy = videographer.serialize()

    try:
        db.session.add(videographer)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    return jsonify({
        "videographer": [videogooCopy]
    })

@app.route('/videographers', methods=['GET'])
def get_videographers():
    videogoos = Videographer.query.all()
    return jsonify([videogoo.serialize() for videogoo in videogoos])

@app.route('/videographers/<string:name>', methods=['GET'])
def get_videographer(name):
    print(name)
    names = name.split('-')
    videogoo = Videographer.query.filter(func.lower(Videographer.first_name).match(names[0])).filter(func.lower(Videographer.last_name).match(names[1])).first()
    
    return jsonify(videogoo.serialize())


@app.route('/videographers/<int:id>', methods=['DELETE'])
@requires_auth('delete:videographer')
def delete_videographer(jwt, id):
    videogoo = Videographer.query.get(id)
    print(videogoo)

    try:
        db.session.delete(videogoo)
        db.session.commit()
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()

    return jsonify({
        'success': True,
        'delete': videogoo.first_name
    })



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


@app.errorhandler(404)
def notfound(error):
    return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
            }), 404


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


if __name__ == '__main__':
    app.run()