import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
# get secrets stored as local bash environment variables
# export all variables you want access to eg.: ~$ export USERNAME=''user1'
user = os.environ['USERNAME']
pword = os.environ['PW']
db_name = os.environ['DB']

# DATABASE URL
SQLALCHEMY_DATABASE_URI = f'postgres://{user}:{pword}@localhost:5432/{db_name}'
