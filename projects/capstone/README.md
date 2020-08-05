# FSND: Capstone Project

## Content

1. [Motivation](#motivation)
2. [Start Project locally](#start-locally)
3. [API Documentation](#api)
4. []
<a name="motivation"></a>
## Motivations & Covered Topics

This is the last project of the `Udacity-Full-Stack-Nanodegree` Course.
It covers following technical topics in 1 app:

1. Database modeling with `postgres` & `sqlalchemy` (see `models.py`)
2. API to performance CRUD Operations on database with `Flask` (see `app.py`)
3. Automated testing with `Unittest` (see `test_app`)
4. Authorization & Role based Authentification with `Auth0` (see `auth.py`)
5. Deployment on `Heroku`

<a name="start-locally"></a>
## Start Project locally
Dependency Requirement: Python3 and postgres installed on machine.

To start to run the local developement,

1. Initialize and activate a virtualenv:
  ```bash
  $ virtualenv --no-site-packages env
  $ source env/scripts/activate
  ``` 

2. Install the dependencies:
```bash
$ pip install -r requirements.txt
```

3. Change some information in config.py inorder to connect to local database if you want to run it locally and use local database
```python
database_setup = {
    "database_name_production" : "capstone_local_test_db",
    "user_name" : "postgres", # default postgres user name
    "password" : "postgres", # if applicable. If no password, just type in None
    "port" : "localhost:5432" # default postgres port
}
```
 - Just change `user_name`, `password` and `port` to whatever you choose while installing postgres.

4. Create local postgres database named `capstone_local_test_db` 
```
sudo -u postgres createuser --superuser USER_NAME   # Created username if don't want to use postgres as default user
sudo -u postgres postgres psql password USER_NAME   # Set password
sudo -u  postgres createdb capstone_local_test_db

```

5. Set Auth0
If you only want to test the API (i.e. Project Reviewer), you can
simply take the existing bearer tokens in `config.py`.

If you already know your way around `Auth0`, just insert your data 
into `config.py` => auth0_config.

6. Run the development server:
```
python app.py
```

7. Test all 48 tests
```python
# If connect to heroku postgres, run this two command: 
#Because heroku has connection limit, so I seperated test.py into two files:
python test_movie_app.py
python test_action_app.py


# If connect to local postgres, urn this commned:
python test.py
```

## API Documentation
<a name="api"></a>

### Base URL

**http://flask-deploy-test2.herokuapp.com**

### Avaliable Endpoint

Here is a short table about which ressources exist and which method you can use on them.
```
                      Allowed Methods
   Endpoints    |  GET |  POST |  DELETE | PATCH  |
                |------|-------|---------|--------|
  /actors       |  [x] |  [x]  |   [x]   |   [x]  |   
  /movies       |  [x] |  [x]  |   [x]   |   [x]  |   
```

### Roles (Auth0):
They are 3 Roles with distinct permission sets:

Casting Assistant:
- GET /actors (view:actors): Can see all actors
- GET /movies (view:movies): Can see all movies

Casting Director (everything from Casting Assistant plus)
- POST /actors (create:actors): Can create new Actors
- PATCH /actors (edit:actors): Can edit existing Actors
- DELETE /actors (delete:actors): Can remove existing Actors from database
- PATCH /movies (edit:movies): Can edit existing Movies

Exectutive Dircector (everything from Casting Director plus)
- POST /movies (create:movies): Can create new Movies
- DELETE /movies (delete:movies): Can remove existing Motives from database

Before start to run, make suer you are in virtualenv and need to run following script to export jwt token into env
```
source setup.sh 
```

### How to work with each endpoint

Click on a link to directly get to the ressource.

1. [Actors](#actors)
   1. [GET /actors](#actors)
   2. [POST /actors](#post-actors)
   3. [DELETE /actors](#delete-actors)
   4. [PATCH /actors](#patch-actors)
2. [Movies](#movies)
   1. [GET /movies](#get-movies)
   2. [POST /movies](#post-movies)
   3. [DELETE /movies](#delete-movies)
   4. [PATCH /movies](#patch-movies)

# <a name="actors"></a>
### Actors

# <a name="get-actors"></a>
### 1. GET /actors
- Fetches a list of dictionaries of examples in which the keys are the ids with all available fields
- Request Arguments: **None**
- Request Headers: **None**
- Requires permission: `get:actors`
- Allowed Role: PRODUCER, DIRECTOR and ASSISTANT
- Returns: 
  1. List of dict of actors with following fields:
      - **integer** `id`
      - **string** `name`
      - **string** `gender`
      - **integer** `age`
  2. **boolean** `success`
```bash
$ curl  http://flask-deploy-test2.herokuapp.com/actors -H 'Accept: application/json' -H "Authorization: Bearer ${PRODUCER}"
$ curl  http://flask-deploy-test2.herokuapp.com/actors -H 'Accept: application/json' -H "Authorization: Bearer ${DIRECTOR}"
$ curl  http://flask-deploy-test2.herokuapp.com/actors -H 'Accept: application/json' -H "Authorization: Bearer ${ASSISTANT}"
```

#### Example response
```
{"success": true, 
  "actors": [{"id": 1, "name": "Christy", "age": 22, "gender": "Female"}]
}
```

#### Errors
If you try fetch a page which does not have any actors, you will encounter an error which looks like this:
```
$ curl  http://flask-deploy-test2.herokuapp.com/actors -H 'Accept: application/json' -H "Authorization: Bearer ${PRODUCER}"
```
will return
```
{
  "error": 404,
  "message": "Not_found",
  "success": false
}
```

# <a name="post-actors"></a>
### 2. POST /actors
- Post actor with name, gender and age into database
- Request Arguments: actors name and gender
- Request Headers: "Authorization: Bearer ${PRODUCER}" or "Authorization: Bearer ${DIRECTOR}"
- Requires permission: `post:actors`
- Allowed Role: PRODUCER, DIRECTOR 
- Returns: 
  1. List of dict of actors with following fields:
      - **integer** `id`
      - **string** `name`
      - **string** `gender`
      - **integer** `age`
  2. **boolean** `success`
```bash
$ curl -X POST -H 'Content-Type: application/json' -H "Authorization: Bearer ${PRODUCER}" --data '{"name":"Tom Hank","age":68,"gender":"male"}' http://flask-deploy-test2.herokuapp.com/actors
$ curl -X POST -H 'Content-Type: application/json' -H "Authorization: Bearer ${DIRECTOR}" --data '{"name":"Tom Hank","age":68,"gender":"male"}' http://flask-deploy-test2.herokuapp.com/actors
```

#### Example response
```
{
	"actor":[{"age":68,"gender":"male","id":8,"name":"Tom Hank"}],
	"success":true
}
```

#### Errors
If post an Actor with already existing field values will result in an 422 error:
```
{
	"success": False,
	"error": 422,
	"message": "unprocessable"
}
```


# <a name="patch-actors"></a>
### 3. PATCH /actors
- Edit actor with name, gender and age into database
- Request Arguments: "Authorization: Bearer ${PRODUCER}" or "Authorization: Bearer ${DIRECTOR}"
- Request Headers: actors name and gender
- Requires permission: `patch:actors`
- Allowed Role: PRODUCER, DIRECTOR 
- Returns: 
  1. List of dict of actors with following fields:
      - **integer** `id`
      - **string** `name`
      - **string** `gender`
      - **integer** `age`
  2. **boolean** `success`
```bash
$ curl -X PATCH -H 'Content-Type: application/json' -H "Authorization: Bearer ${PRODUCER}" --data '{"name":"Tom Hank","age":30,"gender":"male"}' http://flask-deploy-test2.herokuapp.com/actors/2

$ curl -X PATCH -H 'Content-Type: application/json' -H "Authorization: Bearer ${DIRECTOR}" --data '{"name":"Tom Hank","age":30,"gender":"male"}' http://flask-deploy-test2.herokuapp.com/actors/2
```
#### Example response
```
{
	"actor":[{"age":30,"gender":"male","id":2,"name":"Tom Hank"}],
	"success":true
}

```

#### Errors
If you try to update an actor with an invalid id it will throw an 404error:
```
$ curl -X PATCH -H 'Content-Type: application/json' -H "Authorization: Bearer ${PRODUCER}" --data '{"name":"Tom Hank","age":30,"gender":"male"}' http://flask-deploy-test2.herokuapp.com/actors/125
```
will return
````
{
  "error": 404,
  "message": "not found",
  "success": false
}
````
Additionally, trying to update an Actor with already existing field values will result in an 422 error:
```
{
	"success": False,
	"error": 422,
	"message": "unprocessable"
}
```


# <a name="delete-actors"></a>
### 4. DELETE /actors
- delete actor with name, gender and age into database
- Request Arguments: "Authorization: Bearer ${PRODUCER}" or "Authorization: Bearer ${DIRECTOR}"
- Request Headers: actor's name and gender
- Requires permission: `delete:actors`
- Allowed Role: PRODUCER, DIRECTOR 
- Returns: 
  1. List of dict of actors with following fields:
      - **integer** `id`
      - **string** `name`
      - **string** `gender`
      - **integer** `age`
  2. **boolean** `success`
```bash
$ curl -X DELETE -H 'Content-Type: application/json' -H "Authorization: Bearer ${PRODUCER}"  http://flask-deploy-test2.herokuapp.com/actors/1


$ curl -X DELETE -H 'Content-Type: application/json' -H "Authorization: Bearer ${DIRECTOR}"  http://flask-deploy-test2.herokuapp.com/actors/1

```

#### Example response
```
{
	"delete":1,
	"success":true
}

```

#### Errors
If you try to delete actor with an invalid id, it will throw an 422error:
```
$ curl -X DELETE -H 'Content-Type: application/json' -H "Authorization: Bearer ${PRODUCER}"  http://flask-deploy-test2.herokuapp.com/actors/100

```
will return
```
{
	"success": False,
	"error": 422,
	"message": "unprocessable"
}
```


# <a name="movies"></a>
### Movies

# <a name="get-movies"></a>
### 1. GET /movies
- Fetches a list of dictionaries of examples in which the keys are the ids with all available fields
- Request Arguments: **None**
- Request Headers: **None**
- Requires permission: `get:movies`
- Allowed Role: PRODUCER, DIRECTOR and ASSISTANT
- Returns: 
  1. List of dict of movies with following fields:
      - **integer** `id`
      - **string** `title`
      - **Date** `release_date`
  2. **boolean** `success`
```bash
$ curl  http://flask-deploy-test2.herokuapp.com/movies -H 'Accept: application/json' -H "Authorization: Bearer ${PRODUCER}"
$ curl  http://flask-deploy-test2.herokuapp.com/movies -H 'Accept: application/json' -H "Authorization: Bearer ${DIRECTOR}"
$ curl  http://flask-deploy-test2.herokuapp.com/movies -H 'Accept: application/json' -H "Authorization: Bearer ${ASSISTANT}"
```
#### Example response
```
{
	"success": true, 
	"movies": [{"id": 1, "title": "The Great Escape", "release_date": "2020-08-04T00:00:00"}, {"id": 3, "title": "Talent", "release_date": "2020-08-12T00:00:00"}]
}

```

#### Errors
If database  does not have any movies, you will encounter an error which looks like this:
```
$ curl  http://flask-deploy-test2.herokuapp.com/movies -H 'Accept: application/json' -H "Authorization: Bearer ${PRODUCER}"
```
will return
```
{
  "error": 404,
  "message": "Not_found",
  "success": false
}
```


# <a name="post-movies"></a>
### 2. POST /movies
- Post actor with name, gender and age into database
- Request Arguments: movies title and release-date
- Request Headers: "Authorization: Bearer ${PRODUCER}"
- Requires permission: `post:movies`
- Allowed Role: PRODUCER 
- Returns: 
  1. List of dict of actors with following fields:
      - **integer** `id`
      - **string** `title`
      - **Date** `release_date`
  2. **boolean** `success`
```bash
$ curl -H 'Content-Type: application/json' -H "Authorization: Bearer ${PRODUCER}" --data '{"title":"Talent","release_date":"2020-08-04"}'  -X POST http://flask-deploy-test2.herokuapp.com/movies
```

#### Example response
```
{
	"movie":[{"id":4,"release_date":"2020-08-04T00:00:00","title":"Talent"}],
	"success":true}   

```

#### Errors
If post an movies with already existing field values will result in an 422 error:
```
{
	"success": False,
	"error": 422,
	"message": "unprocessable"
}
```

# <a name="patch-movies"></a>
### 3. PATCH /movies
- Edit actor with name, gender and age into database
- Request Arguments: "Authorization: Bearer ${PRODUCER}" or "Authorization: Bearer ${DIRECTOR}"
- Request Headers: movies name and gender
- Requires permission: `patch:movies`
- Allowed Role: PRODUCER, DIRECTOR 
- Returns: 
  1. List of dict of movies with following fields:
     - **integer** `id`
      - **string** `title`
      - **Date** `release_date`
  2. **boolean** `success`
```bash
$ curl -H 'Content-Type: application/json' -H "Authorization: Bearer ${PRODUCER}" --data '{"title":"Talent","release_date":"2020-08-04"}'  -X PATCH http://flask-deploy-test2.herokuapp.com/movies/4

$ curl -H 'Content-Type: application/json' -H "Authorization: Bearer ${DIRECTOR}" --data '{"title":"Talent","release_date":"2020-08-04"}'  -X PATCH http://flask-deploy-test2.herokuapp.com/movies/4
```
#### Example response
```
{
	"movie":[{"id":4,"release_date":"2020-08-04T00:00:00","title":"Talent"}],
	"success":true
}   
```

#### Errors
If you try to update an movie with an invalid id it will throw an 404error:
```
$ curl -H 'Content-Type: application/json' -H "Authorization: Bearer ${PRODUCER}" --data '{"title":"Talent","release_date":"2020-08-04"}'  -X POST http://flask-deploy-test2.herokuapp.com/movies/100
```
will return
````
{
  "error": 404,
  "message": "not found",
  "success": false
}
````
Additionally, trying to update an Actor with already existing field values will result in an 422 error:
```
{
	"success": False,
	"error": 422,
	"message": "unprocessable"
}
```


# <a name="delete-movies"></a>
### 4. DELETE /movies
- delete actor with name, gender and age into database
- Request Arguments: "Authorization: Bearer ${PRODUCER}" 
- Request Headers: actor's name and gender
- Requires permission: `delete:movies`
- Allowed Role: PRODUCER, DIRECTOR 
- Returns: 
  1. List of dict of movies with following fields:
      - **integer** `id`
      - **string** `title`
      - **Date** `release_date`
  2. **boolean** `success`
```bash
$ curl -X DELETE -H 'Content-Type: application/json' -H "Authorization: Bearer ${PRODUCER}"  http://flask-deploy-test2.herokuapp.com/movies/1
$ curl -X DELETE -H 'Content-Type: application/json' -H "Authorization: Bearer ${DIRECTOR}"  http://flask-deploy-test2.herokuapp.com/movies/1
```
#### Example response
```
{
	"delete":1,
	"success":true
}
```
#### Errors
If you try to delete movies with an invalid id, it will throw an 422error:
```
$ curl -X DELETE -H 'Content-Type: application/json' -H "Authorization: Bearer ${PRODUCER}"  http://flask-deploy-test2.herokuapp.com/movies/100

```
will return
```
{
	"success": False,
	"error": 422,
	"message": "unprocessable"
}
```


### Auth0
If you create your own Auth account and configure setting correctly by create 3 user assigned with Producer, Director and Assistant role which follow above permission.
You can use following http address to login and remove login session to login different account

Login Page:
https://fsnd5141.us.auth0.com/authorize?audience=capstone&response_type=token&client_id=B3TZ2WUxfLCQmvd98tmShMYDIS4a4m6D&redirect_uri=http://flask-deploy-test2.herokuapp.com

Remove login session: 
https://fsnd5141.us.auth0.com/v2/logout



### Authors
Shou-En Hsiao is in charged of capstone Api in this folder. All other files are contributed by Udacity- Full Stack Web Developer Nanodegree.