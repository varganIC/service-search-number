FROM python:3.9.5

WORKDIR /code
ENV PYTHONPATH=/code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY .env .
