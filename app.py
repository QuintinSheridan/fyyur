#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
 
import datetime 
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
  __tablename__ = 'venues'
  # columns
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  website = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  seeking_talent = db.Column(db.Boolean, nullable=False, default=True)
  seeking_description = db.Column(db.String)
  image_link = db.Column(db.String)
  # relationships
  shows = db.relationship('Show',  cascade="all,delete", backref='venue', lazy=True)
  genres = db.relationship('VenueGenre',  cascade="all,delete", backref='venue', lazy=True)

  # method to return uniquely identifying venue attributes
  def get_attributes(self):
    return [self.name, self.city, self.state, self.address, self.phone, self.website] 

  def __repr__(self):
    return f'<Venue {self.id} {self.name}>'


class VenueGenre(db.Model):
  __tablename__ = 'venue_genres'
  # columns
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), primary_key=True)
  genre = db.Column(db.String(120), primary_key=True)

  def __repr__(self):
    return f'<VenueGenre {self.venue_id} {self.genre}>'



class Artist(db.Model):
  __tablename__ = 'artists'
  # columns
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  seeking_venue = db.Column(db.Boolean, nullable=False, default=True)
  seeking_description = db.Column(db.String)
  image_link = db.Column(db.String)
  # relationships
  shows = db.relationship('Show',  cascade="all,delete", backref='artist', lazy=True)
  genres = db.relationship('ArtistGenre',  cascade="all,delete", backref='artist', lazy=True)

  # method to return uniquely identifying band attributes
  def get_atttibutes(self):
    return [self.name, self.city, self.state, self.address, self.phone, self.website] 

  def __repr__(self):
    return f'<Artist {self.id} {self.name}>'



class ArtistGenre(db.Model):
  __tablename__ = 'artist_genres'
  # columns
  artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), primary_key=True)
  genre = db.Column(db.String(120), primary_key=True)

  def __repr__(self):
    return f'<VenueGenre {self.venue_id} {self.genre}>'


class Show(db.Model):
  __tablename__ = 'shows'
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id')) 
  artist_id = db.Column(db.Integer, db.ForeignKey('artists.id')) 
  start_time = db.Column(db.DateTime(timezone=False)) 

  def __repr__(self):
        return f'<Show {self.id} {self.venue_id, self.artist_id, self.start_time}>'
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


def get_venue_shows(venue_id, period='upcomming'):
  '''Function that returns upcoming or past shows for a venue
  Args:
    venue_id (int): venue_id
    period (str): 'upcomming' or 'past'
  Returns:
    count ([Show]]): list of shows
  '''
  # upcomming shows
  if period == 'upcomming':
    shows =  Show.query.filter(Show.venue_id == venue_id).filter(Show.start_time > datetime.datetime.now()).all()
  # past shows
  if period == 'past':
    shows =  Show.query.filter(Show.venue_id == venue_id).filter(Show.start_time < datetime.datetime.now()).all()

  return shows



def get_artist_shows(artist_id, period='upcomming'):
  '''Function that returns upcoming or past shows for a venue
  Args:
    artist_id (int): artist_id
    period (str): 'upcomming' or 'past'
  Returns:
    count ([Show]]): list of shows
  '''
  # upcomming shows
  if period == 'upcomming':
    shows =  Show.query.filter(Show.artist_id == artist_id).filter(Show.start_time > datetime.datetime.now()).all()
  # past shows
  if period == 'past':
    shows = Show.query.filter(Show.artist_id == artist_id).filter(Show.start_time < datetime.datetime.now()).all()

  return shows

ass = get_artist_shows(4, period='past')

print(f'\n\n\n ASS {ass} \n\n\n')

for show in ass:
  print(f'show.artist {show.artist}')
  print(show.artist.__dict__)
  print(f'show.venue {show.venue}')



# # "2019-05-21T21:30:00.000Z"
# shows = get_venue_shows(1, period='past')
# print('\n\n\n VS: \n', shows, '\n\n\n')
# print(format_datetime(str(shows[0].start_time)))
# print('timestring: ', str(shows[0].start_time))

# genres = [g.genre for g in Genre.query.filter(Genre.venue_id == 1)]

# print('genres: ', genres)

# show = Show.query.first()
# print('now: ', datetime.datetime.now())
# past_shows =  Show.query.filter(Show.venue_id == 1).filter(Show.start_time < datetime.datetime.now()).join(Artist).all()
# print('past_shows: ', past_shows)
# print('show: ', show)
# get_venue_shows(1)

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

  data=[]

  for venue in Venue.query.distinct(Venue.city):
    city = venue.city
    state = venue.state
    city_dict = {}
    city_dict["city"] = city
    city_dict["state"] = state
    city_venues = []
    for cv in Venue.query.filter(Venue.city==city).all():
      city_venue = {}
      city_venue['id'] = cv.id
      city_venue['name'] = cv.name
      city_venue['num_upcoming_shows'] = len(get_venue_shows(cv.id, period='upcomming'))
      city_venues.append(city_venue)
    city_dict['venues'] = city_venues
    data.append(city_dict)

  return render_template('pages/venues.html', areas=data)


# search venues
@app.route('/venues/search', methods=['POST'])
def search_venues():

  response = {}
  search_term = search_term=request.form.get('search_term', '')
  if search_term:
    print(f'search_term: {search_term}')
    search_term = search_term.lower()
    venues=  Venue.query.all()
    data = []
    count = 0
    for venue in venues:
      venue_name = venue.name.lower()
      
      if search_term in venue_name:
        match = {}
        match['id'] = venue.id
        match['name'] = venue.name
        match['num_upcoming_shows'] = len(get_venue_shows(venue.id, period='upcomming'))
        data.append(match)
        count += 1
    
    response['count'] = count
    response['data'] = data

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


# show venue
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

  venue = Venue.query.get(venue_id)

  past_shows = get_venue_shows(venue_id, period='past')
  upcomming_shows = get_venue_shows(venue_id, period='upcomming')

  ps= []
  for show in past_shows:
    s={}
    s["artist_id"] = show.artist_id
    s["arrtist_name"] = show.artist.name
    s["artist_image_link"] = show.artist.image_link 
    s["start_time"] = str(show.start_time)
    ps.append(s)
  us=[]

  for show in upcomming_shows:
    s={}
    s["artist_id"] = show.artist_id
    s["arrtist_name"] = show.artist.name
    s["artist_image_link"] = show.artist.image_link 
    s["start_time"] = str(show.start_time)
    us.append(s)

  ps_count = len(past_shows)
  us_count = len(upcomming_shows)

  genres = [g.genre for g in venue.genres]

  data = {
    "id":venue.id,
    "name":venue.name,
    "genres":genres,
    "address":venue.address,
    "city":venue.city,
    "state":venue.state,
    "phone":venue.phone,
    "website":venue.website,
    "facebook_link":venue.facebook_link,
    "image_link":venue.image_link,
    "seeking_talent":venue.seeking_talent,
    "past_shows":ps,
    "upcoming_shows":us,
    "past_shows_count":ps_count,
    "upcoming_shows_count":us_count
  }

  if venue.seeking_description:
    data['seeking_description'] = venue.seeking_description

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form_data = request.form.to_dict()
  successful_add = True
  print('/n/n/n form_data: ', form_data, '/n/n/n')
  try:
    # create venue object
    venue = Venue(name=form_data['name'], city=form_data['city'], state=form_data['state'], address=form_data['address'], 
      phone=form_data['phone'], facebook_link=form_data['facebook_link'] )
    # check to make sure the venue doesn't exist already
    old_venues = Venue.query.filter(Venue.name==venue.name).all()
    for v in old_venues:
      if (v.get_attributes()==venue.get_attributes()):
        raise Exception('Cannot create venue.  Entry allready exists.')
    # add venue
    db.session.add(venue)
    db.session.flush()
    print('venue_id: ', venue.id)
    g = form_data['genres']
    print('/n/n/n genres: ', g, '/n/n/n')
    # TODO: figure out how to make genres return as a list
    # for g in genres:
    #   genre = Genre(venue_id=venue.id, genre=g)
    #   db.session.add(genre)
    # commit changes
    genre = VenueGenre(venue.id, genre=g)
    venue_name = venue.name
    db.session.add(genre)
    db.session.commit()
  except Exception as e:
    successful_add=False
    print(f'The following error  occured while trying to create a venue: {e}')
    flash(f"Venue venue_name could not be created due to the following exception: {e}.")
    db.session.rollback()

  finally:
    db.session.commit()
    db.session.close()
    if successful_add:
      flash(f'Venue {venue_name}was successfully listed!')
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()

  # TODO  
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():

  artists=Artist.query.all()

  data = []
  for artist in artists:
    artist_data = {}
    artist_data['id'] = artist.id
    artist_data['name'] = artist.name
    data.append(artist_data)

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  
  response = {}
  search_term = search_term=request.form.get('search_term', '')
  if search_term:
    print(f'search_term: {search_term}')
    search_term = search_term.lower()
    artists =  Artist.query.all()
    data = []
    count = 0
    for artist in artists:
      artist_name = artist.name.lower()
      
      if search_term in artist_name:
        match = {}
        match['id'] = artist.id
        match['name'] = artist.name
        match['num_upcoming_shows'] = len(get_artist_shows(artist.id, period='upcomming'))
        data.append(match)
        count += 1
    
    response['count'] = count
    response['data'] = data

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  
  artist = Artist.query.get(artist_id)
  past_shows = get_artist_shows(artist_id, period='past')
  print('\n\n\n past_shows: ', past_shows, '\n\n\n')
  upcomming_shows = get_artist_shows(artist_id, period='upcomming')

  ps= []
  for show in past_shows:
    s={}
    s["venue_id"] = show.venue_id
    s["venue_name"] = show.venue.name
    s["venue_image_link"] = show.venue.image_link 
    s["start_time"] = str(show.start_time)
    ps.append(s)
  
  us=[]
  for show in upcomming_shows:
    s={}
    s["venue_id"] = show.venue_id
    s["venue_name"] = show.venue.name
    s["venue_image_link"] = show.venue.image_link 
    s["start_time"] = str(show.start_time)
    us.append(s)

  ps_count = len(past_shows)
  us_count = len(upcomming_shows)

  # "id": 5,                                                                                                                "name": "Matt Quevedo",
  # "genres": ["Jazz"],
  # "city": "New York",
  # "state": "NY",
  # "phone": "300-400-5000",
  # "facebook_link": "https://www.facebook.com/mattquevedo923251523",
  # "seeking_venue": False,
  # "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  # "past_shows": [{
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "start_time": "2019-06-15T23:00:00.000Z"
  # }],

  genres = [g.genre for g in artist.genres]

  data = {
  "id": artist.id,
  "genres": genres,
  "name": artist.name, 
  "city": artist.city,
  "state": artist.state,
  "phone": artist.phone,
  "seeking_venue": artist.seeking_venue,
  "image_link": artist.image_link,
  "past_shows": ps,
  "upcoming_shows": us,
  "past_shows_count": ps_count,
  "upcoming_shows_count": us_count
  }

  if artist.seeking_description != '':
    data['seeking_description'] = artist.seeking_description

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  # TODO: populate form with fields from artist with ID <artist_id>
  a = Artist.query.get(artist_id)
  ag = ArtistGenre.query.get(ArtistGenre.artist_id==artist_id)
  artist = a.__dict__
  artist['genres'] = [g.genre for g in ag]

  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  data = request.form.to_dict()
  try:
    a = Artist.query.get(artist_id)
    a.name = data['name']
    #artist.genres = data['genres']
    a.city = data['city']
    a.state = data['state']
    a.phone = data['phone']
    a.website = data['website']
    a.facebook_link = data['facebook_link']
    a.seeking_venue = data['seeking_venue']
    a.seeking_description = data['seeking_description']
    a.image_link = data['image_link']

    ArtistGenre.query.get(ArtistGenre.artist_id==artist_id).delete()
    for g in data['genres']:
      genre = ArtistGenre(artist_id=artist.id, genre=g)
      db.add(genre)

    artist = a.__dict__
    artist['genres'] = data['genres']

    db.commit()
  except:
    db.rollback()
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # venue={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  # }

  v = Venue.query.get(venue_id)
  vg = VenueGenre.query.filter(VenueGenre.venue_id==venue_id).all()
  venue = v.__dict__
  venue['genres'] = [g.genre for g in vg]

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  data = request.form.to_dict()
  print(f'data: {data}')
  edit_successful = True
  try:
    v = Venue.query.get(venue_id)
    v.name = data['name']
    v.address = data['address']
    v.city = data['city']
    v.state = data['state']
    v.phone = data['phone']
    #v.website = data['website']
    v.facebook_link = data['facebook_link']
    #v.seeking_talent = data['seeking_talent']
    #v.seeking_description = data['seeking_description']
    #v.image_link = data['image_link']

    VenueGenre.query.filter(VenueGenre.venue_id==venue_id).delete()
    # TODO: get list of genres from form
    # for g in data['genres']:
    #   genre = VenueGenre(venue_id=venue_id, genre=g)
    #   db.session.add(genre)
    genre = VenueGenre(venue_id=venue_id, genre=data['genres'])
    db.session.add(genre)

    db.session.commit()
  except Exception as e:
    print(f'The following error occured while trying to edit venue: {e}')
    edit_successful = False
    db.session.rollback()
  finally:
    db.session.close()

  if edit_successful:
    flash('Venue edited')
  else:
    flash('Error occured while editing venue')
  
  return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  data = request.form.to_dict() 
  #print('\n\n\n\ artist form fields ', data.keys(), '\n\n\n')
  artist_added = True
  try:
    name = data['name']
    city = data['city'] 
    state =data['state']
    phone = data['phone']
    #image_link = data['image_link']
    facebook_link = data['facebook_link']
    # seeking_venue = 
    # seeking_description =
    # image_link =
    artist = Artist(name=name, city=city, state=state, phone=phone, facebook_link=facebook_link)
    db.session.add(artist)
    db.session.flush()

    g = data['genres']
    artist_name = artist.name
    ag = ArtistGenre(artist_id=artist.id, genre=g)
    db.session.add(ag)
    db.session.commit()
  except Exception as e:
    print(f'The following exception occured while trying to add an artist: {e}')
    artist_added = False
    db.session.rollback
  finally: 
    db.session.close()
  # on successful db insert, flash success
  if artist_added:
    flash(f'Artist {artist_name} was successfully listed!')
  else:
    flash(f"Error occurred while rtrying to add artist {artist_name}!")
  
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------
@app.route('/shows')
def shows():
  upcomming_shows = Show.query.filter(Show.start_time > datetime.datetime.now()).all()
  data = []

  for show in upcomming_shows:
    s = {
    "venue_id": show.venue.id,
    "venue_name": show.venue.name,
    "artist_id": show.artist.id,
    "artist_name": show.artist.name,
    "artist_image_link": show.artist.image_link,
    "start_time": str(show.start_time)
    }
    data.append(s)

  return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  data = request.form.to_dict()
  show_successful = True
  try:
    show = Show(venue_id=data['venue_id'], artist_id=data['artist_id'], start_time=data['start_time'])
    db.session.add(show)
    db.session.commit()
  except Exception as e: 
    print(f'The following exception occurred whiletrying to create a show: {e}')
    show_successful = False
    db.session.rollback()
  finally:
    db.session.close()

  # on successful db insert, flash success
  if show_successful:
    flash('Show was successfully listed!')
  else:
    flash('Error occured while creating show!')
  
  return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

def insert_venues_data():
  '''Function that inserts venues data
  Args:
    None
  Returns:
    None
  '''

  data1={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    "past_shows": [{
      "artist_id": 5,
      "artist_name": "Matt Quevedo",
      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [{
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 1,
    "upcoming_shows_count": 1,
  }

  venue_data = [data1, data2, data3]

  for data in venue_data:
    id = data['id']
    name = data['name']
    city = data['city']
    state = data['state']
    address = data['address']
    phone = data['phone']

    if 'website' in data:
      website = data['website']
    else:
      website = ''

    image_link = data['image_link']
    facebook_link = data['facebook_link']
    seeking_talent = data['seeking_talent']

    if 'seeking_description' in data:
      seeking_description = data['seeking_description']
    else:
      seeking_description = ''

    image_link = data['image_link']

    venue = Venue(id=id, name=name, city=city, state=state, address=address, phone=phone, website=website, image_link=image_link, 
      facebook_link=facebook_link, seeking_talent=seeking_talent, seeking_description=seeking_description)

    db.session.add(venue)
    db.session.commit()

    genres = data['genres']
    for g in genres:
      genre = VenueGenre(venue_id=id, genre=g)
      db.session.add(genre)
  
  db.session.commit()
  db.session.close()

def insert_artist_data():
  '''Function that inserts artist data
  Args:
    None
  Returns:
    None
  '''

  data1={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "past_shows": [{
      "venue_id": 1,
      "venue_name": "The Musical Hop",
      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 5,
    "name": "Matt Quevedo",
    "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "past_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 6,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "facebook_link":'',
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "past_shows": [],
    "upcoming_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 0,
    "upcoming_shows_count": 3,
  }
  artist_data = [data1, data2, data3]

  for data in artist_data:
    id = data['id']
    name = data['name']
    city = data['city']
    state = data['state']
    phone = data['phone']
    image_link = data['image_link']
    facebook_link = data['facebook_link']
    seeking_venue = data['seeking_venue']
    if 'seeking_description' in data:
      seeking_description = data['seeking_description']
    else:
      seeking_description = ''
    image_link = data['image_link']
  
    artist = Artist(id=id, name=name, city=city, state=state, phone=phone, image_link=image_link, 
      facebook_link=facebook_link, seeking_venue=seeking_venue, seeking_description=seeking_description, )
    db.session.add(artist)

    genres = data['genres']
    for g in genres:
      genre = ArtistGenre(artist_id=id, genre=g)
      db.session.add(genre)


  db.session.commit()
  db.session.close()

def insert_shows_data():
  '''Function that inserts shows data
  Args:
    None
  Returns:
    None
  '''

  shows_data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]

  for data in shows_data:
    venue_id = data['venue_id']
    artist_id = data['artist_id']
    start_time = data['start_time']

    show = Show(venue_id=venue_id, artist_id=artist_id, start_time=start_time)
    db.session.add(show)

  db.session.commit()
  db.session.close()


def insert_data():
  '''Function to enter data into database
  Args:
    None
  Returns:
    None
  '''
  insert_venues_data()
  insert_artist_data()
  insert_shows_data()

  print('Initial Data Inserted')


def drop_data():
  Show.query.delete()
  VenueGenre.query.delete()
  Venue.query.delete()
  ArtistGenre.query.delete()
  Artist.query.delete()
  Show.query.delete()
  db.session.commit()
  db.session.close()


def print_db():
  venues = Venue.query.all()
  print('Venues: ', venues)
  artists = Artist.query.all()
  print('Artists: ', artists)
  shows = Show.query.all()
  print('Shows: ', shows)
  genres = Genre.query.all()
  print('genres: ', genres)
    


# Default port:
if __name__ == '__main__':
  drop_data()
  insert_data()
  #print_db()
  app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
