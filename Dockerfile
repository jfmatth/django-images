## Phsae 1 - builder

    # Chainguard python-dev has UV installed
    FROM cgr.dev/chainguard/python:latest-dev as builder
    # FROM python:alpine  as builder

    ENV LANG=C.UTF-8
    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1

    USER root

    # RUN apk --no-cache add uv

    # use /app generic folder
    WORKDIR /app

    # use python venv to bring in any necessary packages
    # RUN python -m venv /app/venv
    COPY pyproject.toml  .
    RUN uv sync 

## Phase 2 - execution

    # FROM python:alpine 
    FROM cgr.dev/chainguard/python

    WORKDIR /app

    ENV PYTHONUNBUFFERED=1
    ENV PATH="/app/.venv/bin:$PATH"

    # bring in the virtual environment / packages from the builder directory
    COPY --from=builder /app/.venv /app/.venv

    # copy application files to WORKDIR (/app)
    COPY manage.py /app
    COPY core/ /app/core
    COPY images/ /app/images
    COPY staticfiles /app/staticfiles
    COPY sqlite /app/sqlite

    EXPOSE 8000

    # run line for app
    ENTRYPOINT [ "uvicorn", "--host", "0.0.0.0", "core.asgi:application"]
