import os
import sys
from flask import Flask, jsonify, abort, request
from models import setup_db, Movie, Actor
from flask_cors import CORS

from auth import AuthError, requires_auth

ITEMS_PER_PAGE = 10

def pagination(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    items = [i.format() for i in selection]
    return items[start:end]

def create_app(test_config=None):

    app = Flask(__name__)
    app.app_context().push()
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        return "Casting Agency."

    #-----------------------MOVIES-----------------------------------

    """
    - Implementation of endpoint GET /movies
    - It returns status code 200 and json {"success": True, "movies": []} 
        where movies is the list of all movies, or returns appropriate 
        status code indicating reason for failure
    """
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        selection = Movie.query.all()
        current_movies = pagination(request, selection)

        if len(current_movies) == 0:
            abort(404)
        
        return jsonify({
            'success': True,
            'movies': current_movies
        }), 200

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        try:
            movie.delete()

            return jsonify({
                'success': True, 
                'deleted_movie_id': movie_id
            }), 200

        except:
            print(sys.exc_info())
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)
                    
        req = request.get_json()

        if 'title' not in req or 'release_date' not in req:
            abort(400)

        try:
            movie.title = req['title']
            movie.release_date = req['release_date']
            movie.update()

            return jsonify({
                'success': True, 
                'updated_movie': movie.format()
            }), 200

        except:
            print(sys.exc_info())
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        req = request.get_json()
        if 'title' not in req or 'release_date' not in req:
            abort(400)

        try:
            title = req['title']
            release_date = req['release_date']
            movie = Movie(title, release_date)
            movie.insert()

            return jsonify({
                'success': True, 
                'movie': movie.format()
            }), 200

        except:
            print(sys.exc_info())
            abort(422)

    #-------------------------------ACTORS---------------------------    

    """
    - Implementation of endpoint GET /actors
    - It returns status code 200 and json {"success": True, "actors": []} 
        where actors is the list of all actors, or returns appropriate 
        status code indicating reason for failure
    """
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        selection = Actor.query.all()
        current_actors = pagination(request, selection)

        if len(current_actors) == 0:
            abort(404)
        
        return jsonify({
            'success': True,
            'actors': current_actors
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        try:
            actor.delete()

            return jsonify({
                'success': True, 
                'deleted_actor_id': actor_id
            }), 200

        except:
            print(sys.exc_info())
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)
                    
        req = request.get_json()

        if 'name' not in req or 'age' not in req or 'gender' not in req:
            abort(400)

        try:
            actor.name = req['name']
            actor.age = req['age']
            actor.gender = req['gender']
            actor.update()

            return jsonify({
                'success': True, 
                'updated_actor': actor.format()
            }), 200

        except:
            print(sys.exc_info())
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        req = request.get_json()
        if 'name' not in req or 'age' not in req or 'gender' not in req:
            abort(400)

        try:
            name = req['name']
            age = req['age']
            gender = req['gender']
            actor = Actor(name, age, gender)
            actor.insert()

            return jsonify({
                'success': True, 
                'actor': actor.format()
            }), 200

        except:
            print(sys.exc_info())
            abort(422)

    # -------------Error Handling---------------------

    @app.errorhandler(400)
    def bad_request(error):
        """
        Receive the raised Bad request error
        """
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        """
        Receive the raised resource not found error
        """
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
    
    @app.errorhandler(422)
    def unprocessable(error):
        """
        Receive the raised unprocessable entity error
        """
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        """
        Receive the raised authorization error and propagates it as response
        """
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response


    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
