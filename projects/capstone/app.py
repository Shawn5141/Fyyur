import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from models import db_drop_and_create_all, setup_db,Actor, Movie
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    db_drop_and_create_all()
    CORS(app)
    @app.after_request
    def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 
        'Content-Type, Authorization, true')
      response.headers.add('Access-Control-Allow-Methods', 
        'GET, PATCH, POST, DELETE, OPTIONS')
      return response


    @app.route('/')
    def Hello():
        return "hello world"


    # Get actors

    
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(jwt):
        try:
            actors = [actor.format() for actor in Actor.query.all()]
            return json.dumps({
                "success": True,
                "actors": actors
                })
        except Exception:
            #print(Exception)
            abort(404)


    # Get movie


    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(jwt):
        try:
            movies = [movie.format() for movie in Movie.query.all()]
            return json.dumps({
                "success": True,
                "movies": movies
                })
        except Exception:
            abort(404)


    # Create actor


    @app.route('/actors', methods=["POST"])
    @requires_auth('post:actors')
    def create_actor(jwt):

        try:
            new_actor = request.get_json()
            #name = json.loads(request.data.decode('utf-8'))['name']
            #print("new_actor",new_actor,request.data)
            name = new_actor.get('name')
            age =  new_actor.get('age')
            gender = new_actor.get('gender')
            if name == '' or age == '' or gender == '':
                abort(400)

            actor = Actor(
                name=name,age=age,gender=gender
            )
            actor.insert()
            return jsonify({
                'success': True,
                'actor': [actor.format()]
            }), 200

        except exc.SQLAlchemyError as e:
            #print("e",e)
            abort(422)
        except Exception as error:
            #print(error)
            raise AuthError({
                    'code': '401',
                    'description': 'unable to post.'
                }, 401)


    # Create Movie


    @app.route('/movies', methods=["POST"])
    @requires_auth('post:movies')
    def create_movie(jwt):

        try:
            new_actor = request.get_json()
            title = new_actor.get('title')
            release_date =  new_actor.get('release_date')
            if title == '' or release_date == '':
                abort(400)

            movie = Movie(
                title=title,release_date=release_date
            )
            movie.insert()
            return jsonify({
                'success': True,
                'movie': [movie.format()]
            }), 200

        except exc.SQLAlchemyError as e:
            #print(e)
            abort(422)
        except Exception as error:
            raise AuthError({
                    'code': '401',
                    'description': 'unable to post.'
                }, 401)


    # Edit Actor


    @app.route('/actors/<int:actor_id>', methods=["PATCH"])
    @requires_auth('patch:actors')
    def update_actor(jwt, actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)
        update = request.get_json()
        name = update.get('name')
        age = update.get('age')
        gender = update.get('gender')
        try:
            actor.name = name
            actor.age = age
            actor.gender = gender
            actor.update()
            return jsonify({"success": True,
                            "actor": [actor.format()]})
        except exc.SQLAlchemyError as e:
            #print(e)
            abort(422)
        except Exception as error:
            #print(error)
            raise AuthError({
                    'code': '401',
                    'description': 'unable to patch.'
                }, 401)


    # Edit movie


    @app.route('/movies/<int:movie_id>', methods=["PATCH"])
    @requires_auth('patch:movies')
    def update_movie(jwt, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)
        update = request.get_json()
        title = update.get('title')
        release_date = update.get('release_date')
        try:
            movie.title = title
            movie.release_date = release_date
            movie.update()
            return jsonify({"success": True,
                            "movie": [movie.format()]})
        except exc.SQLAlchemyError as e:
            abort(422)
        except Exception as error:
            #print(error)
            raise AuthError({
                    'code': '401',      
                    'description': 'unable to patch.'
                }, 401)


    # Delete actor


    @app.route('/actors/<int:actor_id>', methods=["DELETE"])
    @requires_auth('delete:actors')
    def delete_actor(jwt, actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)
        try:
            actor.delete()
            return jsonify({"success": True,
                            "delete": actor_id})
        except exc.SQLAlchemyError as e:
            abort(422)
        except Exception as error:
            abort(500)


    # Delete movie


    @app.route('/movies/<int:movie_id>', methods=["DELETE"])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)
        try:
            movie.delete()
            return jsonify({"success": True,
                            "delete": movie_id})
        except exc.SQLAlchemyError as e:
            abort(422)
        except Exception as error:
            #print(error)
            abort(500)


    # Error Handling


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False,
                        "error": 422,
                        "message": "unprocessable"
                        }), 422

    @app.errorhandler(404)
    def Not_found(error):
        return jsonify({
                        "success": False,
                        "error": 404,
                        "message": "Not_found"
                        }), 404

    @app.errorhandler(500)
    def Internal_Server_Error(error):
        return jsonify({
                        "success": False,
                        "error": 500,
                        "message": "Internal Server Error"
                        }), 500

    @app.errorhandler(AuthError)
    def Internal_Server_Error(AuthError):
        return jsonify({
                        "success": False,
                        "error": 401,
                        "message": "AuthError"
                        }), 401

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
                        "success": False,
                        "error": 405,
                        "message": "method not allowed"
                        }), 405
    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
