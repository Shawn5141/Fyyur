import os
from sqlalchemy import Column, String, Integer,Date,Enum
from flask_sqlalchemy import SQLAlchemy
import json
import os
from datetime import date


db = SQLAlchemy()

'''
setup_db(app)
	binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
	app.config[
	'SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
	db.app = app
	db.init_app(app)



'''
db_drop_and_create_all()
	drops the database tables and starts fresh
	can be used to initialize a clean database
	!!NOTE you can change the database_filename variable to have multiple verisons of a database
'''
def db_drop_and_create_all():
	db.drop_all()
	db.create_all()
	db_init_records()


def db_init_records():
    new_actor = (Actor(
        name = 'Christy',
        age = 22,
        gender = 'Female'
        ))

    new_movie = (Movie(
        title = 'The Great Escape',
        release_date = date.today()
        ))

    # new_performance = Performance.insert().values(
    #     Movie_id = new_movie.id,
    #     Actor_id = new_actor.id,
    #     actor_fee = 50.00
    # )

    new_actor.insert()
    new_movie.insert()
    # db.session.execute(new_performance) 
    # db.session.commit()



'''
Model: Movies with attributes title and release date
'''

class Movie(db.Model):
	__tablename__ = 'movies'
	id = Column(Integer(),primary_key=True)
	title = Column(String(80), unique=True)
	release_date = Column(Date) 

	def insert(self):
		db.session.add(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def update(self):
		db.session.commit()

	def __repr__(self):
		return json.dumps(self.format())

	def format(self):
		return {
			'id': self.id,
			'title': self.title,
			'release_date': self.release_date.strftime("%Y-%m-%dT%H:%M:%S")
		}


'''
Actors with attributes name, age and gender

'''


class Actor(db.Model):
	__tablename__ = 'actors'
	id = Column(Integer(),primary_key=True)
	name = Column(String(20), unique=True)
	age = Column(Integer()) 
	gender =  Column(String)

	def insert(self):
		db.session.add(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def update(self):
		db.session.commit()

	def __repr__(self):
		return json.dumps(self.format())

	def format(self):
		return {
			'id': self.id,
			'name': self.name,
			'age': self.age,
			'gender': self.gender
		}









