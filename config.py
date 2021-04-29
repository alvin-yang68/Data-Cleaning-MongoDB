import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MONGO_URI = os.environ.get('MONGODB_URI')

# waitress-serve --listen=localhost:8000 nosqlcleaner:app
# heroku ps:scale web=1
