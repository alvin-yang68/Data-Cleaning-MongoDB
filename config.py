import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MONGO_URI = 'mongodb+srv://Alvin:R2y7sefqZJL9cXp0@cluster0.xhr3k.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

# waitress-serve --listen=localhost:8000 nosqlcleaner:app
# heroku ps:scale web=1
