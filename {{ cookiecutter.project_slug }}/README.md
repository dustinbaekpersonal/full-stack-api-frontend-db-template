# API and Frontend

This repository illustrates how to develop APIs and how web applications interact with APIs to retrieve data that user asked for.

For API backend service, we use FastAPI.
For frontend, we use Dash.
For database, we use PostgreSQL.


## :wrench: Developer set up

First clone the repo. In a terminal, navigate to a folder you want to clone the code to then run:

1. Clone the repo
```bash
$ git clone git@github.com:dustinbaekpersonal/python-api-frontend.git
```

2. Create virtual environment and activate
```bash
$ cd backend # or cd frontend
$ make uv-setup && source .venv/bin/activate
```

3. Install dependencies
```bash
$ make uv-dev
```

4. To run pre-commit,
```bash
$ pre-commit install
```

## :computer: Local run

To run the API and front end locally, you will need to have both running in two separate terminal tabs.

In the first tab let's get the API running.

```bash
$ cd backend/app
$ uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Uvicorn is ASGI web server implementation for python, and 'main:app' is calling an app object that we created within main.py file.
'--reload' enables the restart of the server after code changes. You can navigate to http://127.0.0.1:8000/docs in a browser to see the Swagger spec for the API.

Now open a new terminal tab (Ctrl/Command + T) and get the dash app running:

```bash
$ cd frontend/src
$ python -m main
```

You should then be able to view the front end application by navigating to http://localhost:8050/ in a browser.


## :steam_locomotive: Running Docker container using docker-compose

To emulate realistic environment, we will use docker containers for database and web servers.

Pre-requisite:
You need to install docker on your machine: https://docs.docker.com/engine/install/

1. Create docker images and run containers for the first time.
```bash
$ docker-compose up --build
```

2. To check what images are pulled/build
```bash
$ docker images
```

3. To check what images are running using docker-compose
```bash
$ docker-compose ps
```

4. To stop docker containers
```bash
$ docker-compose stop
```

5. To check docker networks
```bash
$ docker network ls
$ docker inspect network_name
```

6. To execute command in running container
```bash
$ docker exec -it container_name bash
$ exit
```

7. To run docker containers with logs
```bash
$ docker-compose logs -f -t
```


### Extra tips
1. psql command
```bash
$ psql -U postgres -d fastapi_db
```
