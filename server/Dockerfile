FROM python:3.10-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --prefer-binary -r /code/requirements.txt

COPY ./app /code/app
COPY ./ml /code/ml

ARG PORT=8080
ENV PORT=$PORT
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
