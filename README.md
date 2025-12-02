# django-images

A simple image hosting application written in Django.

## Want to use this project?

- Fork/Clone

- Setup python environment with ```uv```
```sh
uv sync
```

- Database migration for Django
```sh
uv run manage.py migrate
```

- Collect static files
```sh
uv run manage.py collectstatic --noinput
```

- Run the server:
```sh
uv run manage.py runserver
```

## Development environments

### Running with uvicorn
uvicorn was added to the requirements and can run the code Asyncronously.

```
uv run uvicorn --reload core.asgi:application 
```

### Running with Podman

We run in a single pod with two volumes.  One for the DB and the other for mediafiles

- Setup environment for postgres and app
```
podman pod create -p 8000:8000 img
podman volume create img
podman volume create media
```
- Run postgres
```
podman run -d `
--name images-db `
--pod img `
--env-file ENV-dev `
-v img:/var/lib/postgresql/data/ `
postgres:17
```
- Build our images

The application and a django utility
```
podman build -f .\Dockerfile -t images:v1
podman build -f .\Dockerfile-utility -t imagesutil:v1
```

- Run the application, make sure it's in our pod ```img```
```
podman run --pod img --env-file ENV-dev -v media:/app/mediafiles images:v1
```

- Run some Django utility functions with the other container, like migrate to setup the DB tables
```
podman run --pod img --env-file ENV-dev imagesutil:v1 migrate
```