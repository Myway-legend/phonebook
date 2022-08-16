import os


# Create a DB_URI from the environment variables
user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']
database = os.environ['POSTGRES_DB']
port = os.environ['POSTGRES_PORT']
DATABASE_CONNECTION_URI = f'postgresql://{user}:{password}@{host}:{port}/{database}'
