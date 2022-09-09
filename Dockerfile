FROM python:3.9-slim

LABEL org.opencontainers.image.source=https://github.com/polaris-foundation/polaris-url-api

ENV FLASK_APP dhos_url_api/autoapp.py

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN apt-get update \
    && apt-get install -y curl nano \
    && useradd -m app \
    && chown -R app:app /app \
    && pip install --upgrade pip poetry \
    && poetry config virtualenvs.create false \
    && poetry install -v --no-dev

COPY --chown=app . ./

USER app

EXPOSE 5000

CMD ["python", "-m", "dhos_url_api"]
