# Eventeger API
Your Social Event Manager
Final Project at DCI by Hugo, Hila, Alex

## Our app is the result of joining two ideas:
- An app that brings together the logistic aspects of creating and managing a small event
- A social app that allows you to stay connected with your loved ones or remote networks

## Features: 
🏕 Creating group with a common passion, interest or connection<br>
👯‍♂️ Adding and removing members from the group<br>
🔐 Only admins are authorized to edit group details and add people to group<br>
💂 Set or remove admins<br>
📆 Creating events<br>
⛔️ Only members of the group are authorized to create and view events within the group<br>
📷 Uploading photos to the group with the option to like and comment on them<br>
🧭 Navigating to Event location via google maps<br>


https://user-images.githubusercontent.com/24811549/217003545-c70e8e2a-b67e-4cf3-8d70-c2a7b044aae5.mov


## Technologies and Methodologies: 
- Django RestFramework
- Swagger for better transperany with endpoints
- Docker for hosting DB 
- Postgres as ORM 


- Authentication to the API
- Role-based permissions to the app modules (Group-based authorization and role-based within the groups)
- CRUD operations for groups, events, users and photos 
- Automation of all processes to enable transparency and flow within the team, including Github actions for CI/CD, Flake8 and test-coverage reports (threshold 90%, currently standing on 97%)
- Test Driven Development approach to minimize pitfalls

## Under Construction:
- Chat 
- Inventory list with incremental search and quantities that auto-update
- To do list 
- Calendar
- Gmail sign in 
- Event Timeline
- Deploy to Google Cloud Platform 


## Run our project locally 
**Requirements:**
git installed<br>
python 3.8>.10<br>
django<br>
- Install python-venv packages:
`apt install python3.10-venv`<br>
Then you can install a virtual enviroment using the command line:<br>
`python3 -m venv .venv`<br>
- Activate the venv:
`. .venv/bin/activate`<br>
- Install the requirements of the project:
`pip install -r requirements.txt`<br>
**Install Docker:**
\[https://docs.docker.com/engine/install/ubuntu/\](https://docs.docker.com/engine/install/ubuntu/
- After installing Docker:
- create an image maping the localhost and the port 2022
`docker run -d --name <image_name> -p 127.0.0.1:2022:2022 -e POSTGRES_PASSWORD=postgres postgres`
- run the image:
`docker start <image_name_or_id>`<br>
- Go to the container and open posgresql:
`docker exec -it postgres bash psql -U postgres`
- Create a database called eventeger_db:
`postgres=# CREATE DATABASE eventeger_db;`
## Make migrations and run the server
After the database is set up with docker we need to make migrations and migrate by using the following commands:<br>
- Inside the directory of the project:
`python3 manage.py makemigrations && migrate`
- After all migrations are done we can run the server an look the endpoints in the documentation url http://127.0.0.1:8000/api/docs/
`python manage.py runserver`

