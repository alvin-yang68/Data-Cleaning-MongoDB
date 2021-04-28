import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MONGO_URI = os.environ.get('DATABASE_URL') or 'mongodb://localhost:27017'

# waitress-serve --listen=localhost:8000 nosqlcleaner:app
