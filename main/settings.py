import os
from dotenv import load_dotenv
load_dotenv()

SALT = os.getenv("SALT")
HOST_IP = os.getenv("HOST_IP")
PORT = os.getenv("PORT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_HOST = os.getenv("DATABASE_HOST")