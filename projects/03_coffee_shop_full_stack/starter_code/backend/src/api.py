import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
#db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_drinks():

    #drinks  = [drink.short() for drink in Drink.query.all()]
    try:
        drinks  = [drink.short() for drink in Drink.query.all()]
        return json.dumps({
            "success": True, 
            "drinks": drinks
            })
    except:
        abort(404)
'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    print(jwt)
    print(Drink.query.all())
    try:

        return json.dumps({
            'success':
            True,
            'drinks': [drink.short() for drink in Drink.query.all()]
        }), 200
    except:
        abort(401)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks',methods=["POST"])
@requires_auth('post:drinks')
def create_drinks(jwt):
  
    try:
        new_drink = request.get_json()

        title = json.loads(request.data.decode('utf-8'))['title']
        if title == '':
            abort(400)

        drink = Drink(
            title=new_drink.get('title'),
            recipe=json.dumps(new_drink.get('recipe'))
        )
        print("before insert",json.dumps(new_drink.get('recipe')))
        drink.insert()
        print("drink long",[drink.long()])
        return jsonify({    
            'success': True,
            'drinks': [drink.long()]
        }), 200

    except exc.SQLAlchemyError as e:
        print("post error ",e)
        abort(422)
    except Exception as error:
        raise AuthError({
                'code': '401',
                'description': 'unable to post.'
            }, 401)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drinks_id>',methods=["PATCH"])
@requires_auth('patch:drinks')
def update_drink(jwt,drinks_id):
    
    drink=Drink.query.get(drinks_id)
    if not drink:
        abort(404)
    update = request.get_json()

    title = update.get('title')
    recipe= update.get('recipe')
    
    try:
        drink.title = title
        drink.recipe =json.dumps(recipe) 
        drink.update()
        return jsonify({"success": True,
                        "drinks": [drink.long()]})
    except exc.SQLAlchemyError as e:
        print(e)
        abort(422)
    except Exception as error:
        print(error)
        raise AuthError({
                'code': '401',
                'description': 'unable to patch.'
            }, 401)
'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<int:drinks_id>',methods=["DELETE"])
@requires_auth('delete:drinks')
def delete_drink(jwt,drinks_id):
    
    drink=Drink.query.get(drinks_id)
    if not drink:
        abort(404)

    try:
      
        drink.delete()
        return jsonify({"success": True,
                        "delete": drinks_id})
    except exc.SQLAlchemyError as e:
        print(e)
        abort(422)
    except Exception as error:
        print(error)
        abort(500)
## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''

@app.errorhandler(404)
def Not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "Not_found"
                    }), 404


@app.errorhandler(500)
def Internal_Server_Error(error):
    return jsonify({
                    "success": False, 
                    "error": 500,
                    "message": "Internal Server Error"
                    }), 500

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''

@app.errorhandler(AuthError)
def Internal_Server_Error(AuthError):
    return jsonify({
                    "success": False, 
                    "error": 401,
                    "message": "AuthError"
                    }), 401