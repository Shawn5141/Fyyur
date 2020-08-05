import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, db_drop_and_create_all, Actor, Movie
from config import bearer_tokens
from sqlalchemy import desc
from datetime import date


# casting_assistant_auth_header = {
#     'Authorization': bearer_tokens['casting_assistant']
# }

# casting_director_auth_header = {
#     'Authorization': bearer_tokens['casting_director']
# }

# executive_producer_auth_header = {
#     'Authorization': bearer_tokens['executive_producer']
# }


class AgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.assistant_t = bearer_tokens['casting_assistant']
        self.producer_t = bearer_tokens['executive_producer']
        self.director_t = bearer_tokens['casting_director']

        self.new_movie1 = {
            'title': 'Fast & Furious 1',
            "release_date":"2001-08-01"
        }

        self.new_movie2 = {
            'title': 'Fast & Furious 2',
            "release_date":"2001-08-02"
        }
        self.new_movie3 = {
            'title': 'Fast & Furious 3',
            "release_date":"2001-08-03"
        }

        self.new_actor1 = {
            'name': 'Jack',
            'age': 27,
            'gender': 'Male'
        }

        self.new_actor2 = {
            'name': 'Pull Allen',
            'age': 27,
            'gender': 'Male'
        }

        self.new_actor3 = {
            'name': 'Mike Jason',
            'age': 40,
            'gender': 'Male'
        }

    def tearDown(self):
        pass

# ---------------------------------------------------------------------------  
#            Producer           Director        Assistance
#         success | Fail    success | Fail    success | Fail  
# Movie 
# -GET     
# -POST                      N/A               N/A
# -PATCH                                       N/A
# -DELETE                    N/A               N/A
# Actor
# -GET
# -POST                                        N/A
# -PATCH                                       N/A
# -DELETE                                      N/A
#  
#  N/A stands for not possible case
#-----------------------------------------------------------------------------


#----------------------------------------------------------------------------#
# Tests for /movies GET
#----------------------------------------------------------------------------#
# Producer Success
    def test_get_producer(self):
        res = self.client().get('/movies', headers={
            'Authorization': self.producer_t,
            'Content-Type': 'Text'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

# Director Success
    def test_get_Director(self):
        res = self.client().get('/movies', headers={
            'Authorization': self.director_t,
            'Content-Type': 'Text'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
# Assistant Success
    def test_get_Assistant(self):
        res = self.client().get('/movies', headers={
            'Authorization': self.assistant_t,
            'Content-Type': 'Text'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
# Producer Fail
    def test_get_fial_Producer(self):
        # No header
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 401)
# Director Fail
    def test_get_fial_Director(self):
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 401)
# Assistant Fail
    def test_get_fial_Assistant(self):
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 401)
#----------------------------------------------------------------------------#
# Tests for /movies POST
#----------------------------------------------------------------------------#
# Producer Success
    def test_post_Producer(self):
        res = self.client().post('/movies', json=self.new_movie1,
                                 headers={
                                     'Authorization':
                                     self.producer_t,
                                     'Content-Type': 'Text'
                                     })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        
# Director Success
    # No possible success case
# Assistant Success 
    # No possible success case
# Producer Fail
    def test_post_fail_Producer(self): 
        # No json
        res = self.client().post('/movies',
                                 headers={
                                     'Authorization':
                                     self.producer_t,
                                     'Content-Type': 'Text'
                                     })
        self.assertEqual(res.status_code, 401)
    
# Director Fail
    def test_post_fail_Director(self): 
        # No json
        res = self.client().post('/movies', json=self.new_movie2,
                                 headers={
                                     'Authorization':
                                     self.director_t,
                                     'Content-Type': 'Text'
                                     })
        self.assertEqual(res.status_code, 401)

# Assistant Fail
    def test_post_fail_Assistant(self): 
        res = self.client().post('/movies', json=self.new_movie2,
                                     headers={
                                         'Authorization':
                                         self.assistant_t,
                                         'Content-Type': 'Text'
                                         })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        
#----------------------------------------------------------------------------#
# Tests for /movies PATCH
#----------------------------------------------------------------------------#
# Producer Success
    def test_patch_Producer(self):  
        res = self.client().patch('/movies/1', json=self.new_movie1,
                                 headers={
                                     'Authorization':
                                     self.producer_t,
                                     'Content-Type': 'Text'
                                     })
        data = json.loads(res.data)
        #print("id",self.id,"data",data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
# Director Success
    def test_patch_Director(self):  
        res = self.client().patch('/movies/1', json=self.new_movie1,
                                 headers={
                                     'Authorization':
                                     self.director_t,
                                     'Content-Type': 'Text'
                                     })
        data = json.loads(res.data)
        #print("id",self.id,"data",data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

# Assistant Success
    # Not possible for success
# Producer Fail
    def test_patch_fail_Producer(self):
        # Not exist
        res = self.client().patch('/movies/30', json=self.new_movie2,
                                 headers={
                                     'Authorization':
                                     self.producer_t,
                                     'Content-Type': 'Text'
                                     })
        
        self.assertEqual(res.status_code, 404)
# Director Fail
    def test_patch_fail_Director(self):
        # Not exist
        res = self.client().patch('/movies/30', json=self.new_movie2,
                                 headers={
                                     'Authorization':
                                     self.director_t,
                                     'Content-Type': 'Text'
                                     })
        
        self.assertEqual(res.status_code, 404)
# Assistant Fail
    def test_patch_fail_Director(self):
        # Not exist
        res = self.client().patch('/movies/30', json=self.new_movie2,
                                 headers={
                                     'Authorization':
                                     self.assistant_t,
                                     'Content-Type': 'Text'
                                     })
        
        self.assertEqual(res.status_code, 401)
#----------------------------------------------------------------------------#
# Tests for /movies DELETE
#----------------------------------------------------------------------------#
# Producer Success
    def test_delete_Producer(self):
        res = self.client().delete('/movies/1',
                                   headers={
                                       'Authorization':
                                       self.producer_t,
                                       'Content-Type': 'Text'
                                       })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'])
# Director Success
    def test_delete_Director(self):
        res = self.client().delete('/movies/1',
                                   headers={
                                       'Authorization':
                                       self.producer_t,
                                       'Content-Type': 'Text'
                                       })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'])
# Assistant Success
    # No possible
# Producer Fail
    def test_delete_fail_Producer(self):
        # Not exist
        res = self.client().delete('/movies/30',
                                   headers={
                                       'Authorization':
                                       self.producer_t,
                                       'Content-Type': 'Text'
                                       })
        self.assertEqual(res.status_code, 404)

# Director Fail
    def test_delete_fail_Director(self):
        # Not exist
        res = self.client().delete('/movies/30',
                                   headers={
                                       'Authorization':
                                       self.director_t,
                                       'Content-Type': 'Text'
                                       })
        self.assertEqual(res.status_code, 404)
# Assistant Fail
    def test_delete_fail_Director(self):
        # Not exist
        res = self.client().delete('/movies/1',
                                   headers={
                                       'Authorization':
                                       self.assistant_t,
                                       'Content-Type': 'Text'
                                       })
        self.assertEqual(res.status_code, 401)
    







"""
#----------------------------------------------------------------------------#
# Tests for /actors GET
#----------------------------------------------------------------------------#
# Producer Success
    def test_get_actor_producer(self):
        res = self.client().get('/actors', headers={
            'Authorization': self.producer_t,
            'Content-Type': 'Text'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

# Director Success
    def test_get_actor_Director(self):
        res = self.client().get('/actors', headers={
            'Authorization': self.director_t,
            'Content-Type': 'Text'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
# Assistant Success
    def test_get_actor_Assistant(self):
        res = self.client().get('/actors', headers={
            'Authorization': self.assistant_t,
            'Content-Type': 'Text'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
# Producer Fail
    def test_get_actor_fial_Producer(self):
        # No header
        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 401)
# Director Fail
    def test_get_actor_fial_Director(self):
        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 401)
# Assistant Fail
    def test_get_actor_fial_Assistant(self):
        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 401)
#----------------------------------------------------------------------------#
# Tests for /actors POST
#----------------------------------------------------------------------------#
# Producer Success
    def test_post_actors_Producer(self):
        res = self.client().post('/actors', json=self.new_actor1,
                                 headers={
                                     'Authorization':
                                     self.producer_t,
                                     'Content-Type': 'Text'
                                     })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        
# Director Success
    def test_post_actors_Producer(self):
        res = self.client().post('/actors', json=self.new_actor2,
                                 headers={
                                     'Authorization':
                                     self.director_t,
                                     'Content-Type': 'Text'
                                     })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
# Assistant Success 
    # No possible success case
# Producer Fail
    def test_post_actors_fail_Producer(self): 
        # No json
        res = self.client().post('/actors',
                                 headers={
                                     'Authorization':
                                     self.producer_t,
                                     'Content-Type': 'Text'
                                     })
        self.assertEqual(res.status_code, 401)
    
# Director Fail
    def test_post_actors_fail_Director(self): 
        # Repeated post
        self.client().post('/actors', json=self.new_actor1
                                 headers={
                                     'Authorization':
                                     self.director_t,
                                     'Content-Type': 'Text'
                                     })
        res = self.client().post('/actors', json=self.new_actor1
                                 headers={
                                     'Authorization':
                                     self.director_t,
                                     'Content-Type': 'Text'
                                     })
        self.assertEqual(res.status_code, 422)

# Assistant Fail
    def test_post_actors_fail_Assistant(self): 
        res = self.client().post('/actors', json=self.new_actor2,
                                     headers={
                                         'Authorization':
                                         self.assistant_t,
                                         'Content-Type': 'Text'
                                         })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        
#----------------------------------------------------------------------------#
# Tests for /actors PATCH
#----------------------------------------------------------------------------#
# Producer Success
    def test_patch_actors_Producer(self):   
        res = self.client().patch('/actors/1', json=self.new_actor1,
                                 headers={
                                     'Authorization':
                                     self.producer_t,
                                     'Content-Type': 'Text'
                                     })
        data = json.loads(res.data)
        #print("id",self.id,"data",data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
# Director Success
    def test_patch_actors_Director(self):   
        res = self.client().patch('/actors/1', json=self.new_actor1,
                                 headers={
                                     'Authorization':
                                     self.director_t,
                                     'Content-Type': 'Text'
                                     })
        data = json.loads(res.data)
        #print("id",self.id,"data",data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

# Assistant Success
    # Not possible for success
# Producer Fail
    def test_patch_actors_fail_Producer(self):
        # Not exist
        res = self.client().patch('/actors/30', json=self.new_movie2,
                                 headers={
                                     'Authorization':
                                     self.producer_t,
                                     'Content-Type': 'Text'
                                     })
        
        self.assertEqual(res.status_code, 404)
# Director Fail
    def test_patch_actors_fail_Director(self):
        # Not exist
        res = self.client().patch('/actors/30', json=self.new_movie2,
                                 headers={
                                     'Authorization':
                                     self.director_t,
                                     'Content-Type': 'Text'
                                     })
        
        self.assertEqual(res.status_code, 404)
# Assistant Fail
    def test_patch_actors_fail_Director(self):
        # Not exist
        res = self.client().patch('/actors/30', json=self.new_movie2,
                                 headers={
                                     'Authorization':
                                     self.assistant_t,
                                     'Content-Type': 'Text'
                                     })
        
        self.assertEqual(res.status_code, 401)
#----------------------------------------------------------------------------#
# Tests for /actors DELETE
#----------------------------------------------------------------------------#
# Producer Success
    def test_delete_actors_Producer(self):
        res = self.client().delete('/actors/1',
                                   headers={
                                       'Authorization':
                                       self.producer_t,
                                       'Content-Type': 'Text'
                                       })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'])
# Director Success
    def test_delete_actors_Director(self):
        res = self.client().delete('/actors/1',
                                   headers={
                                       'Authorization':
                                       self.producer_t,
                                       'Content-Type': 'Text'
                                       })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'])
# Assistant Success
    # No possible
# Producer Fail
    def test_delete_actors_fail_Producer(self):
        # Not exist
        res = self.client().delete('/actors/30',
                                   headers={
                                       'Authorization':
                                       self.producer_t,
                                       'Content-Type': 'Text'
                                       })
        self.assertEqual(res.status_code, 404)

# Director Fail
    def test_delete_actors_fail_Director(self):
        # Not exist
        res = self.client().delete('/actors/30',
                                   headers={
                                       'Authorization':
                                       self.director_t,
                                       'Content-Type': 'Text'
                                       })
        self.assertEqual(res.status_code, 404)
# Assistant Fail
    def test_delete_actors_fail_Director(self):
        # Not Auth
        res = self.client().delete('/actors/1',
                                   headers={
                                       'Authorization':
                                       self.assistant_t,
                                       'Content-Type': 'Text'
                                       })
        self.assertEqual(res.status_code, 401)
"""

if __name__ == "__main__":
    unittest.main()
