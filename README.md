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

## Running with uvicorn
uvicorn was added to the requirements and can run the code Asyncronously.

```
uv run uvicorn core.asgi:application
```


