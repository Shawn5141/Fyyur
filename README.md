This is the public repository for Udacity's Full-Stack Nanodegree program.


5 project demonstrate my skills of building Full-stack application includes

1. [Fyyur](https://github.com/Shawn5141/Full-stack-Nanodegree-Project/tree/master/projects/01_fyyur/starter_code) -
- A musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. By utilizing Flask, SQLAlchemy, Postgres database, I created functionality with end point that enable CRUD function for artisis list and venues lists.

Used tech stack:
- `SQLAlchemy` as ORM library of choice
- `PostgreSQL` as database
- `Python3` and `Flask` for server language and framework
- `Flask-Migrate` for creating and running schema migrations
- Frontend: HTML, CSS, and Javascript with Bootstrap 3 (mainly provided by Udacity Team)

Applied concepts:
- How to use Git Bash & Github as version control tool
- Configure local database and connect it to a web application
- Create Model Schemas with columns and relationships (1:1, 1:n and N:N)
- Use SQLAlchemy ORM with PostgreSQL to query, insert, edit & delete Data
- Use WTForms to encapsulate input forms in seperate file & to allow for custom validations
- Use Boostrap as a simple to use Front End Libary and Ajax to fetch flask routes
- Create SQL-like Queries, but without any SQL syntax, only using SQLAlchemy ORM
- How to clearly structurize a larger web application in different files & folders

2. [Trivia app](https://github.com/Shawn5141/Full-stack-Nanodegree-Project/tree/master/projects/02_trivia_api/starter) -
- Implement backend for udacity trivia app which allow user to display questions, delete questions, add questions, search for questions based on a text query string and lastly play the quiz game, randomizing either all questions or within a specific category.

Used tech stack:
- React Components as frontend (provided by Udacity Team)
- Python3 and Flask for server language and API development
- `cors` to handle access to the API
- `unittest` for automated testing of APIs
- `curl` to get responses from API
- `README.md` to document project setup & API endpoints

Applied concepts:
- using best-practice `PEP8-style` to design and structur code
- `test-driven-development (TDD)` to rapidly create highly tested & maintainable endpoints.
- directly test and make response to any endpoint out there with `curl`.
- implement `errorhandler` to format & design appropiate error messages to client
- becoming aware of the importance of extensive project documentation & testing.

3. [coffee_shop_full_stack](https://github.com/Shawn5141/Full-stack-Nanodegree-Project/tree/master/projects/03_coffee_shop_full_stack/starter_code) -
- Programmed a backedend application for udacity coffe shop application that utilized third-party validation for user which has different authorities toward application.
Display graphics representing the ratios of ingredients in each drink. 
- Allow public users to view drink names and graphics.
- Allow the shop baristas to see the recipe information.
- Allow the shop managers to create new drinks and edit existing drinks.
- Using 'Flask' and 'Auth0', created a Full-Stack App to let Users
login to Site & make actions according to their Role & Permission Sets.

Used tech stack:
- `Python3` & `Flask` for server language and API development 
- `SQLAlchemy` as ORM / `Sqlite` as database
- `Ionic` to serve and build the frontend (provided by Udacity Team)
- `Auth0` as external Authorization Service & permission creation
- `jose` JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTs.
- `postman` to automatize endpoint testing & verification of correct Authorization behaviour.


 4. [Server Deployment, Containerization and Testing](https://github.com/Shawn5141/FSND-Deploy-Flask-App-to-Kubernetes-Using-EKS).

Deployed a Flask API to a Kubernetes cluster using Docker, AWS EKS, CodePipeline, and CodeBuild.

(Application has been teared down after successfull review to avoid incurring additional costs)

Used tech stack:
- `Docker` for app containerization & image creation to ensure environment consistency across development and production server
- `AWS EKS` & `Kubernetes` as container orchestration service to allow for horizontal scaling
- `aswscli` to interact with AWS Cloud Services
- `ekscli` for EKS cluster creation
- `kubectl` to interact with kubernetes cluster & pods
- `CodePipeline` for Continuous Delivery (CD) & to watch Github Repo for changes
- `CodeBuild` for Continuous Integration (CI), together with `pytest` for automated testing before deployment

 5. [Capstone Project](https://github.com/Shawn5141/Full-stack-Nanodegree-Project/tree/master/projects/capstone)

- Database modeling with `postgres` & `sqlalchemy` (see `models.py`)
- API to performance CRUD Operations on database with `Flask` (see `app.py`)
- Automated testing with `Unittest` (see `test_app`)
- Authorization & Role based Authentification with `Auth0` (see `auth.py`)
- Deployment on `Heroku` (see `setup.sh`)



