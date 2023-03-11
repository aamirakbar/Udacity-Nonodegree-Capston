import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


'''
Unit Test for Movie Class
Using RBAC for the Exective producer role 
which include all CRUD operations for both Movie and Actor
'''
class MovieTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        # RBAC: Exective producer role include all CRUD operations 
        # for movies and actors
        self.EX_PROD_HEADER = {
            "Authorization": "Bearer " + os.getenv("EXECTIVE_PROD_TOKEN")
        }

    def tearDown(self):
        """Executed after each test"""
        pass

    #------one test each for successful operation---------

    def test_get_movies(self):
        """
        Check the status code, and get data success and total movies 
        """
        res = self.client().get('/movies', headers=self.EX_PROD_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_create_movie(self):
        # first create and post new movie and test
        new_movie = {
            "title":"Mission: Impossible - Dead Reckoning Part One", 
            "release_date":"01/01/2024"
        }
        res = self.client().post('/movies', 
                                headers=self.EX_PROD_HEADER,
                                json=new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_update_movie(self):
        # update a movie and test
        movies = json.loads(self.client().get('/movies', 
                                headers=self.EX_PROD_HEADER).data)["movies"]
        a_movie = movies[0]
        if a_movie is not None:
            update_move = {
                "title": "Title",
                "release_date": "01/01/2025"
            }

            res = self.client().patch('/movies/'+ str(a_movie['id']),
                                        headers=self.EX_PROD_HEADER,
                                        json=update_move)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])

    def test_delete_movie(self):
        # delete a movie and test
        movies = json.loads(self.client().get('/movies',
                                headers=self.EX_PROD_HEADER).data)["movies"]
        a_movie = movies[0]
        if a_movie is not None:
            res = self.client().delete('/movies/'+ str(a_movie['id']),
                                        headers=self.EX_PROD_HEADER)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])

    #------one test each for error operation---------

    def test_get_movies_error(self):
        # test for getting a wrong page 
        res = self.client().get('/movies?page=10', headers=self.EX_PROD_HEADER)
        self.assertEqual(res.status_code, 404)
        
    def test_create_movie_error(self):
        # test for posting movie with no release data
        new_movie = {
            "title":"Mission: Impossible - Dead Reckoning Part One"
        }
        res = self.client().post('/movies', headers=self.EX_PROD_HEADER, 
                                json=new_movie)
        self.assertEqual(res.status_code, 400)

    def test_update_movie_error(self):
        # test for updating non existing movie
        update_move = {
                "title": "Title",
                "release_date": "01/01/2025"
            }
        res = self.client().patch('/movies/10000', 
                                  headers=self.EX_PROD_HEADER,
                                  json=update_move)
        self.assertEqual(res.status_code, 404)

    def test_delete_movie_error(self):
       # test for deleting non existing movie
        res = self.client().delete('/movies/10000', headers=self.EX_PROD_HEADER)
        self.assertEqual(res.status_code, 404)

#-----------------------------------------------------------------

'''
Unit Test for Actor Class
Using RBAC for the Casting Director role, 
which include all CRUD operations for Actor
'''
class ActorTestCase(unittest.TestCase):
    """This class represents the casting agency test case for Actor"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        # RBAC: Casting Director role include all CRUD operations actors
        self.CAST_DIR_HEADER = {
            "Authorization": "Bearer " + os.getenv("CASTING_DIR_TOKEN")
        }

    def tearDown(self):
        """Executed after each test"""
        pass

    #------one test each for successful operation---------

    def test_get_actors(self):
        """
        Check the status code, and get data success and total movies 
        """
        res = self.client().get('/actors', headers=self.CAST_DIR_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_create_actor(self):
        # first create and post new movie and test
        new_actor = {
            "name":"Tom Cruise", 
            "age":60,
            "gender": "male"
        }
        res = self.client().post('/actors',
                                    headers=self.CAST_DIR_HEADER,
                                    json=new_actor
                                )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_update_actor(self):
        # update a movie and test
        actors = json.loads(self.client().get('/actors', headers=self.CAST_DIR_HEADER).data)["actors"]
        an_actor = actors[0]
        if an_actor is not None:
            update_actor = {
                "name": "name",
                "age": 70,
                "gender": "female"
            }

            res = self.client().patch('/actors/'+ str(an_actor['id']),
                                        headers=self.CAST_DIR_HEADER,
                                        json=update_actor
                                     )
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])

    def test_delete_actor(self):
        # delete a movie and test
        actors = json.loads(self.client().get('/actors', headers=self.CAST_DIR_HEADER).data)["actors"]
        an_actor = actors[0]
        if an_actor is not None:
            res = self.client().delete('/actors/'+ str(an_actor['id']), headers=self.CAST_DIR_HEADER)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])

    #------one test each for error operation---------

    def test_get_actors_error(self):
        # test for getting a wrong page 
        res = self.client().get('/actors?page=10', headers=self.CAST_DIR_HEADER)
        self.assertEqual(res.status_code, 404)
        
    def test_create_actor_error(self):
        # test for posting actor with no age and gender attributes
        new_actor = {
            "name":"name"
        }
        res = self.client().post('/actors', json=new_actor, headers=self.CAST_DIR_HEADER)
        self.assertEqual(res.status_code, 400)

    def test_update_movie_error(self):
        # test for updating non existing actor with error
        update_actor = {
                "name": "name",
                "age": 45,
                "gender": "male"
            }
        res = self.client().patch('/actors/10000', json=update_actor, headers=self.CAST_DIR_HEADER)
        self.assertEqual(res.status_code, 404)

    def test_delete_movie_error(self):
       # test for deleting non existing actor
        res = self.client().delete('/actors/10000', headers=self.CAST_DIR_HEADER)
        self.assertEqual(res.status_code, 404)

'''
Unit Test for Movie Class 
Using the RBAC for the Casting Director role, 
who is un-authorized to add or delete movies
'''
class UnAuthorizedMovieTestCase(unittest.TestCase):
    """This class represents the casting agency test case for Movie"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        # RBAC: Casting Director role include all CRUD operations actors
        self.CAST_DIR_HEADER = {
            "Authorization": "Bearer " + os.getenv("CASTING_DIR_TOKEN")
        }

    def tearDown(self):
        """Executed after each test"""
        pass

    #------testing un-authorized operations---------

    def test_create_movie(self):
        # first create and post new movie and test
        new_movie = {
            "title":"Mission: Impossible - Dead Reckoning Part One", 
            "release_date":"01/01/2024"
        }
        res = self.client().post('/movies', 
                                    headers=self.CAST_DIR_HEADER,
                                    json=new_movie
                                )
        self.assertEqual(res.status_code, 401)

    def test_delete_movie(self):
        # delete a movie and test
        movies = json.loads(self.client().get('/movies',
                                headers=self.CAST_DIR_HEADER).data)["movies"]
        a_movie = movies[0]
        if a_movie is not None:
            res = self.client().delete('/movies/'+ str(a_movie['id']),
                                        headers=self.CAST_DIR_HEADER
                                    )
            self.assertEqual(res.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()