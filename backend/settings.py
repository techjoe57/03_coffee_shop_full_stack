from os import environ

#AUTH0 
AUTH0_DOMAIN = environ.get("AUTH0_DOMAIN")
ALGORITHMS = environ.get("ALGORITHMS")
API_AUDIENCE = environ.get("API_AUDIENCE")