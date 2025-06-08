# tread_media_backend

- Fastapi
- the application secrets are returned from .env.prod along with docker compose 

# python reqirements
- It is running on python 3.12, will update with 3.13 is stable
- Installed using poetry, for version control and ease of upgrading

# starting up the application
~~~bash
docker compose build
~~~
~~~bash
docker compose --env-file .env.prod -f docker-compose.yml up
~~~

# get up and running locally
- install poetry
curl -sSL https://install.python-poetry.org | python3 -
- copy the pyproject.toml needs to be there, so cd into the same folder the project is in and run the following
- sets the env in the same directory as the code
~~~bash
poetry config virtualenvs.in-project true
~~~
- install the requirements
~~~bash
poetry install --no-root
~~~

# environments requirements
- .env.prod
~~~bash
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DATABASE=db
POSTGRES_HOST=host of the db
POSTGRES_PORT=port
~~~