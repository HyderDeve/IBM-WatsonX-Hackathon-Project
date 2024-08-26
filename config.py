import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    IBM_API_KEY = os.getenv("IBM_GRANITE_API_KEY")
    IBM_SERVICE_URL = os.getenv("IBM_GRANITE_SERVICE_URL")
    MONGO_URI = os.getenv("MONGO_URI")

config = Config()
