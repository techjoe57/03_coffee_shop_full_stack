# from crypto import methods
import os
from pdb import post_mortem
import sys
# from turtle import title
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)
db = SQLAlchemy(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES
'''
    GET /drinks endpoint
    A public endpoint that contains only the drink.short() data representation
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():

        all_drinks = Drink.query.all()
        if (len(all_drinks)==0):
            abort(404)
        drinks = [drink.short() for drink in all_drinks]
       
    
        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200



'''
    GET /drinks-detail endpoint
    It requires the 'get:drinks-detail' permission and contains the drink.long() data representation

'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-details')
def get_drinks_details(payload):
    all_drinks = Drink.query.all()
    if (len(all_drinks) == 0):
        abort(404)
    drinks = [drink.long() for drink in all_drinks]
    
    return jsonify({
        'success': True,
        'drinks': drinks
    }), 200


'''
    POST /drinks
    Creates a new row in the drinks table
    Requires the 'post:drinks' permission
    Contains the drink.long() data representation

'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_new_drinks(payload):
    post_request = request.get_json()
    title = post_request['title']
    recipe = json.dumps(post_request['recipe'])

    try:
        drink = Drink(title=title, recipe=recipe)
        drink.insert()

        return json.dumps({
            'success': True,
            'drinks': drink.long(),
        }), 200
    except:
        print(sys.exc_info())
        abort(422)

'''
    PATCH /drinks/<id> endpoint
       Requires the 'patch:drinks' permission to update the corresponding
       row for <id> in the existing model
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(payload, id):
    patch_request = request.get_json()

    drink = Drink.query.filter(Drink.id == id).one_or_none()

    # patch_request = request.get_json()

    if drink is None:
        abort(404)

    body = request.get_json()

    if 'title' in patch_request:
        drink.title = patch_request['title']
    if 'recipe' in patch_request:
        drink.recipe = json.dumps(patch_request['recipe'])
# 
        # drink.title = body.get('title')
        # drink.recipe = json.dumps(body.get('recipe',None))

    drink.update()
        # drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': [drink.long()] #for  drink in drinks]
    }), 200
  

'''
    DELETE /drinks/<id> endpoint
    Requires the 'delete:drinks' permission to delete the corresponding row for <id>
        
   '''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if drink is None:
        abort(404)

    try:
        drink.delete()

        return jsonify({
            'success': True,
            'deleted': drink.id,
        }), 200
    except:
        print(sys.exc_info())
        abort(422)



# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
