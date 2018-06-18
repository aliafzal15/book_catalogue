import  os

SECRET_KEY = "$3@34"
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql+psycopg2://aliafzal:ali123@127.0.0.1:5432/catalogue')
SQLALCHEMY_TRACK_MODIFICATIONS = False
