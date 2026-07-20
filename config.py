import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "neurolearn-dev-secret-change-me")
    DATABASE_PATH = os.path.join(BASE_DIR, "database", "neurolearn.db")
    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"
