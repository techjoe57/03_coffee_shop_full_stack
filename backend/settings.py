from os import environ
from dotenv import load_dotenv
#use pip install python-dotenv instead of pip install dotenv

load_dotenv()
#AUTH0 
AUTH0_DOMAIN = environ.get("AUTH0_DOMAIN")
ALGORITHMS = environ.get("ALGORITHMS")
API_AUDIENCE = environ.get("API_AUDIENCE")