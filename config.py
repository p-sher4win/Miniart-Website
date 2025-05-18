import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    FLASK_APP = os.environ.get('FLASK_APP')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGO_PASS = os.environ.get('MONGO_PASS')
    MONGO_URI = f'mongodb+srv://sher4win:{MONGO_PASS}@cluster0.juusclj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'