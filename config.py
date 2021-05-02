import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MONGO_URI = os.environ.get(
        'MONGODB_URI') or 'mongodb+srv://Alvin:R2y7sefqZJL9cXp0@cluster0.xhr3k.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    NEO4J_URI = 'bolt://3.86.16.126:7687'
    NEO4J_USER = 'neo4j'
    NEO4J_PASSWORD = 'discriminations-jar-shocks'
    CODEMIRROR_LANGUAGES = ['javascript']
    CODEMIRROR_THEME = 'material-ocean'

# waitress-serve --listen=localhost:8000 nosqlcleaner:app
# heroku ps:scale web=1
