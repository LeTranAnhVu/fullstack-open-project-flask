# Fullstack open project with Flask

## Note
My application will have totally 3 repo. This repo is backend, the others are following:
* My frontend repo: https://github.com/LeTranAnhVu/fullstack-open-project-react
* My devops repo: https://github.com/LeTranAnhVu/fullstack-open-project-devops
    * it contains the docker stuff with two submodules are frontend repo and backend repo (this one)
Please check the table hours of every repo to sum up my total working hours for this project, or *you can find my total in devops repo*


## Hours Keeping
| Day | hours | work |
|:----:|:-----|:-----|
|9.7| 0.5 | init project |
|10.7 + 11.7| 12 | init server, create schema, database model, setup migrate feature restaurants, ImageRestaurant, Update media file , create api for seeding the data of given data to databse. api for curd restaurants, error handling|
|12.7| 8 | tag curd, refactor code, move to blueprint, add cors, refactor Image save logic|, connect to react app |
|12.7 + 13.7| 11 | optimize query with joined, migrate user table & order, make order api, refactor tojson function for models |
|13.7| 8 | research authentication with jwt in flask, appy it, make decorator for checkLogin |
|14.7| 5 | apply jwt exprired, testing api, add logic for login_require, choose method to guard the api |
|| 3 | Refactor pagination|
|15.7| 6 | add User, Admin, permission Role|
|| 6 | add basic permission role|
|16.7| 8 | hand-pn build validator for flask|
|22.7| 6 | add seed image for restaurant in api |
|23.7| 0.5 | add config |
|25.7| 1 | fix api |
|26.7| 9 | add user validator, create Order Get method, fix unstable bug due to mutable parameter in to_json()|
|| 2 | setup env|
|total| 86 |Please note that I also have frontend and devops working hours 


# Instruction:
## Packages:
* Flask==1.1.1
* Flask-SQLAlchemy==2.4.1
* Flask-Migrate==2.5.2
* blurhash-python==1.0.1
* PyMySQL==0.9.3
  
## SETUP VENV:
* Install virtualenv:
  * `pip/ pip3 install virtualenv` 
* create venv:
  * `virtualenv venv`
* Access env:
  * `source venv/bin/activate`
* Install exist packages:
  * (venv) `pip install -r requirement.txt`


## SETUP & CONFIG DATABASE:
* Create `.env` from `.env.example`

* Migrate database:
  * `export FLASK_APP="run.py"`
  * If `migrations` folder does not exist. Run `flask db init`
  * To migrate: 
    * `flask db migrate`
  * To write change to database:
    * `flask db upgrade`
  * To drop change to database:
    * `flask db downgrade`
  
## START SERVER:
* `gunicorn --bind 0.0.0.0:5000 --workers=3 --timeout=1200 wsgi:app`

## SEEDING:
* seed restaurant: /api/seed/restaurants
* seed image for restaurant(importance): /api/seed/image_for_restaurant
* seed user (username: admin, password: admin): /api/seed/users

  
## OTHER:
* Deaccess env:
  * (venv) `deactivate`
* Export package:
  * (venv) `pip freeze > requirement.txt`

