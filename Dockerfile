FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install --only-upgrade -y libpq5

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/
ENV DBHOST=postgres
ENV DBPASSWORD=postgres_password
ENV DBUSER=postgres_user
ENV DBNAME=postgres_database
ENV PUBLIC_DOMAIN_URL="localhost"

# Run migrations
