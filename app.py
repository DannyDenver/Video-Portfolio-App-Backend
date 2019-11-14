import os
import sys
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS
from sqlalchemy import func

app = Flask(__name__)

app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
CORS(app)
from models import Videographer, Video


@app.route('/videographers', methods=['POST'])
def setup_videographer():
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


   


if __name__ == '__main__':
    app.run()