#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for,jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from sqlalchemy.exc import SQLAlchemyError
import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d

class Shows(db.Model):
  __tablename__ = 'Shows'
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer,db.ForeignKey('Venue.id'), nullable=False)
  artist_id = db.Column(db.Integer,db.ForeignKey('Artist.id'), nullable=False)
  start_time =db.Column(db.DateTime)

#Shows = Shows()

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent =db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    # Artist_id = db.relationship('Artist', secondary=Shows,
      # backref=db.backref('Venue', lazy=True))
    

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link= db.Column(db.String(120))
    seeking_venue =db.Column(db.Boolean())
    seeking_description = db.Column(db.String(120))
    # Venue_id = db.relationship('Venue', secondary=Shows,
      # backref=db.backref('Artist', lazy=True))


    
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  #create_database_from_mock_data()
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  state_name = db.session.query(Venue.state).group_by('state').all()
  
  body =[]
  datetime_now =  datetime.datetime.now()
  for state in state_name:
    #count = db.session.query(db.func.count(Venue.id)).filter(Venue.state==state)
    city_name = db.session.query(Venue.city).filter(Venue.state==state).first()[0]
    venue_id = db.session.query(Venue.id).filter(Venue.state==state).all()
    map = {}
    map['city']=city_name
    map['state']=state[0]
    venues = []
    
    for id in venue_id:
      venue_dict ={}
      venue_dict['id'] =id[0]
      venue_dict['name']= db.session.query(Venue.name).filter(Venue.id==id).first()[0]
      venue_dict['num_upcoming_shows'] = db.session.query(Shows.venue_id).filter(Shows.venue_id==id,Shows.start_time>datetime_now).count()
      venues.append(venue_dict)
    #print(id[0],venues)
    map['venues'] =venues
    body.append(map)
 
  return render_template('pages/venues.html', areas=body);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  search_term = request.form.get('search_term', '')
  datetime_now = datetime.datetime.now()
  data = []
  for search_result in Venue.query.filter(Venue.name.ilike("%"+search_term+"%")):
      data.append({
        "id":search_result.id,
        "name":search_result.name,
         "num_upcoming_shows": db.session.query(Shows.id).filter(Shows.venue_id==search_result.id,Shows.start_time>datetime_now).count()
         })   
  response={
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  
  datetime_now =  datetime.datetime.now()
  past_shows=[]

  for id in db.session.query(Shows.id).filter(Shows.venue_id==venue_id,Shows.start_time<datetime_now):
    map = {}
    artist_id = db.session.query(Shows.artist_id).filter(Shows.id==id).first()[0]
    map['artist_id']=artist_id
    map['artist_name']=db.session().query(Artist.name).filter(Artist.id==artist_id).first()[0]
    map['start_time']=db.session().query(Shows.start_time).filter(Shows.artist_id==artist_id).first()[0].strftime("%Y-%m-%dT%H:%M:%S")
    past_shows.append(map)
    #print(db.session().query(Shows.start_time).filter(Shows.artist_id==artist_id).first()[0].strftime("%Y-%m-%dT%H:%M:%S"))
  upcoming_shows=[]
  for id in db.session.query(Shows.id).filter(Shows.venue_id==venue_id,Shows.start_time>datetime_now):
    map = {}
    artist_id = db.session.query(Shows.artist_id).filter(Shows.id==id).first()[0]
    map['artist_id']=artist_id
    map['artist_name']=db.session().query(Artist.name).filter(Artist.id==artist_id).first()[0]
    map['start_time']=db.session().query(Shows.start_time).filter(Shows.artist_id==artist_id).first()[0].strftime("%Y-%m-%dT%H:%M:%S")
    upcoming_shows.append(map)
  

  data  = row2dict(Venue.query.get(venue_id))
  data["past_shows_count"]= len(past_shows)#db.session.query(Shows.venue_id).filter(Shows.venue_id==venue_id,Shows.start_time<datetime_now).count(),
  data["upcoming_shows_count"]=len(upcoming_shows) #db.session.query(Shows.venue_id).filter(Shows.venue_id==venue_id,Shows.start_time>datetime_now).count(),
   
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()

  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  error =False
  body = {}
  try:
      
      name = request.form.get('name')
      city = request.form.get('city')
      state = request.form.get('state')
      address = request.form.get('address')
      phone = request.form.get('phone')
      genres = request.form.get('genres')
      image_link = request.form.get('image_link')
      facebook_link = request.form.get('facebook_link')
      website_link = request.form.get('website_link')
      seeking_talent =True if 'seeking_talent' in request.form else False
      seeking_description = request.form.get('seeking_description')
      
      venue=Venue(name=name,city=city,state=state,address=address,genres=genres,phone=phone,image_link=image_link,
        facebook_link=facebook_link,website_link=website_link,seeking_talent=seeking_talent,seeking_description=seeking_description)
      
      db.session.add(venue)
      db.session.commit()
  except SQLAlchemyError as e:
      #print(type(e))
      errorInfo = e.orig.args
      print("error Info",errorInfo)
      error = True
      db.session.rollback()
  finally:    
      db.session.close()
  if not error:
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
      # TODO: on unsuccessful db insert, flash an error instead.
      return render_template('pages/home.html')
  else:
      flash('An error occurred. Venue ' + request.form['name']  + ' could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
      error = False
      try:
          venue = Venue.query.get(venue_id)
          db.sessoin.delete(venue)
          db.session.commit()
          flash("Venue " + request.form['name'] + " was deleted successfully!")
      except:
          db.session.rollback()
      finally:
          db.session.close()
      if error:
          flash("Venue " + request.form['name'] + " could not be deleted!")

      # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
      return render_template('pages/home.html')
    #return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = db.session().query(Artist.id,Artist.name).all()
  data = []
  
  for id,name in artists:
    map={}
    map['id']=id
    map['name']=name
    data.append(map)
 
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  datetime_now = datetime.datetime.now()
  data = []
  for search_result in Artist.query.filter(Artist.name.ilike("%"+search_term+"%")):
      data.append({
        "id":search_result.id,
        "name":search_result.name,
         "num_upcoming_shows": db.session.query(Shows.id).filter(Shows.artist_id==search_result.id,Shows.start_time>datetime_now).count()
         })
  response={
    "count": len(data),
    "data": data
  }
 
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  datetime_now =  datetime.datetime.now()
  past_shows=[]

  for id in db.session.query(Shows.id).filter(Shows.artist_id==artist_id,Shows.start_time<datetime_now):
    map = {}
    map['artist_id']=artist_id
    map['artist_name']=db.session().query(Artist.name).filter(Artist.id==artist_id).first()[0]
    map['start_time']=db.session().query(Shows.start_time).filter(Shows.artist_id==artist_id).first()[0].strftime("%Y-%m-%dT%H:%M:%S")
    past_shows.append(map)
    print(db.session().query(Shows.start_time).filter(Shows.artist_id==artist_id).first()[0].strftime("%Y-%m-%dT%H:%M:%S"))
  upcoming_shows=[]
  for id in db.session.query(Shows.id).filter(Shows.artist_id==artist_id,Shows.start_time>datetime_now):
    map = {}
    map['artist_id']=artist_id
    map['artist_name']=db.session().query(Artist.name).filter(Artist.id==artist_id).first()[0]
    map['start_time']=db.session().query(Shows.start_time).filter(Shows.artist_id==artist_id).first()[0].strftime("%Y-%m-%dT%H:%M:%S")
    upcoming_shows.append(map)
  

  data  = row2dict(Artist.query.get(artist_id))
  data["past_shows_count"]= len(past_shows)#db.session.query(Shows.venue_id).filter(Shows.venue_id==venue_id,Shows.start_time<datetime_now).count(),
  data["upcoming_shows_count"]=len(upcoming_shows)
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  
  # TODO: populate form with fields from artist with ID <artist_id>
  artist=Artist.query.get(artist_id)
  if artist:
    return render_template('forms/edit_artist.html', form=form, artist=artist) 
  else:
    return not_found_error(True)
  #flash(artist_id,Artist.query.get(artist_id))
  

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
      artist = Artist.query.get(artist_id)
      artist.name = request.form.get('name')
      artist.city = request.form.get('city')
      artist.state = request.form.get('state')
      artist.phone = request.form.get('phone')
      artist.genres = request.form.get('genres')
      artist.image_link = request.form.get('image_link')
      artist.facebook_link = request.form.get('facebook_link')
      artist.website_link= request.form.get('website_link')
      artist.seeking_venue =True if 'seeking_venue' in request.form else False
      artist.seeking_description = request.form.get('seeking_description')

      db.session.commit()

  except:
      db.session.rollback()
  finally:
      db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  
  venue = Venue.query.get(venue_id)
  if venue:
  # TODO: populate form with values from venue with ID <venue_id>
      return render_template('forms/edit_venue.html', form=form, venue=venue)
  else:
      return not_found_error(True)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  try:
      venue = Artist.query.get(artist_id)
      venue.name = request.form.get('name')
      venue.city = request.form.get('city')
      venue.state = request.form.get('state')
      venue.phone = request.form.get('phone')
      venue.genres = request.form.get('genres')
      venue.image_link = request.form.get('image_link')
      venue.facebook_link = request.form.get('facebook_link')
      venue.website_link= request.form.get('website_link')
      venue.seeking_talent =seeking_talent = True if 'seeking_talent' in request.form else False
      venue.seeking_description = request.form.get('seeking_venue')

      db.session.commit()

  except:
      db.session.rollback()
  finally:
      db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  error =False
  
  try:
      
      name = request.form.get('name')
      city = request.form.get('city')
      state = request.form.get('state')
      address = request.form.get('address')
      phone = request.form.get('phone')
      image_link = request.form.get('image_link')
      genres = request.form.get('genres')
      facebook_link = request.form.get('facebook_link')
      website_link = request.form.get('website_link')
      seeking_venue =True if 'seeking_venue' in request.form else False
      seeking_description = request.form.get('seeking_description')
      
      artist=Artist(name=name,city=city,state=state,image_link=image_link,phone=phone,genres=genres,
        facebook_link=facebook_link,website_link=website_link,seeking_description=seeking_description)
      db.session.add(artist)
      db.session.commit()
      
  except:
     
      error = True
      db.session.rollback()
  finally:    
      db.session.close()
  if not error:
      flash('artist ' + request.form['name'] + ' was successfully listed!')
      # TODO: on unsuccessful db insert, flash an error instead.
      
  else:
      flash('An error occurred. artist ' + request.form['name']  + ' could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  
  data = []
  shows_id= db.session.query(Shows.id).all()
  for id in shows_id:
    artist_id = db.session().query(Shows.artist_id).filter(Shows.id==id).first()[0]
    venue_id = db.session().query(Shows.venue_id).filter(Shows.id==id).first()[0]
    data.append({
    "venue_id": venue_id,
    "venue_name":  db.session().query(Venue.name).filter(Venue.id==venue_id).first()[0],
    "artist_id": artist_id ,
    "artist_name": db.session.query(Artist.name).filter(Artist.id==artist_id).first()[0],
    "artist_image_link": db.session.query(Artist.image_link).filter(Artist.id==artist_id).first()[0],
    "start_time": db.session().query(Shows.start_time).filter(Shows.id==id).first()[0].strftime("%Y-%m-%dT%H:%M:%S")
      })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  error =False
  
  print("enter show create")
  try:
      
      artist_id = request.form.get('artist_id')
      venue_id = request.form.get('venue_id')
      start_time = request.form.get('start_time')
      #print("half success========")
      
      shows=Shows(artist_id=artist_id,venue_id=venue_id,start_time=start_time)
     # print("next success========")
      db.session.add(shows)
      #print("next next success========")
      db.session.commit()
      #print("final success========")

  except SQLAlchemyError as e:
      #print(type(e))
      errorInfo = e.orig.args
     # print("error Info",errorInfo)
      error = True
      db.session.rollback()
  finally:    
      db.session.close()
  #if not error:
      # flash('Shows ' + request.form['id'] + ' was successfully listed!')
      # TODO: on unsuccessful db insert, flash an error instead.
  return render_template('pages/home.html')
  #else:
  #    flash('An error occurred. Venue ' + request.form['id']  + ' could not be listed.')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  #return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


# 

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')



#def create_database_from_mock_data():
#   print("enter create database from mock data")
#   artist_3 = {"id": 6,
#     "name": "The Wild Sax Band",
#     "genres": ["Jazz", "Classical"],
#     "city": "San Francisco",
#     "state": "CA",
#     "phone": "432-325-5432",
#     "seeking_venue": False,
#     "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#   }
 
 
#   try:
#       artist_3=Artist(**artist_3)
#       db.session.add(artist_3)
#       db.session.commit()
#   except SQLAlchemyError as e:
#       #print(type(e))
#       errorInfo = e.orig.args
#       print("error Info",errorInfo)
      
#       db.session.rollback()
#   finally:
#       db.session.close()

#   ## Insert Venue

#   data3={
#     "id": 3,
#     "name": "Park Square Live Music & Coffee",
#     "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
#     "address": "34 Whiskey Moore Ave",
#     "city": "San Francisco",
#     "state": "CA",
#     "phone": "415-000-1234",
#     "website_link": "https://www.parksquarelivemusicandcoffee.com",
#     "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
#     "seeking_talent": False,
#     "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80"
#   }

#   venue_list = [data3]
#   for _venue in venue_list:
#     try:
#       venue=Venue(**_venue)
#       db.session.add(venue)
#       db.session.commit()
#     except SQLAlchemyError as e:
#       #print(type(e))
#       errorInfo = e.orig.args
#       print("error Info",errorInfo)
      
#       db.session.rollback()
#     finally:
#       db.session.close()
#   ## Insert shows
#     data=[{
#     "venue_id": 3,
#     "artist_id": 2,
#     "start_time": "2019-05-21T21:30:00.000Z"
#   }, {
#     "venue_id": 3,
#     "artist_id": 2,
#     "start_time": "2019-06-15T23:00:00.000Z"
#   }, {
#     "venue_id": 10,
#     "artist_id": 3,
#     "start_time": "2035-04-01T20:00:00.000Z"
#   }, {
#     "venue_id": 3,
#     "artist_id": 3,
#     "start_time": "2035-04-08T20:00:00.000Z"
#   }, {
#     "venue_id": 10,
#     "artist_id": 6,
#     "start_time": "2035-04-15T20:00:00.000Z"
#   }]
#   for val in data:
    
#     try:
#       show=Shows(**val)
#       db.session.add(show)
#       db.session.commit()
#     except SQLAlchemyError as e:
#       #print(type(e))
#       errorInfo = e.orig.args
#       print("error Info",errorInfo)
      
#       db.session.rollback()
#     finally:
#       db.session.close()
#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
