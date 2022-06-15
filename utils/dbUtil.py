import databases
import sqlalchemy
from functools import lru_cache
import config
from model import metadata
#1. Using Pydantic to load .env configuration file
@lru_cache()
def setting():
    return config.Settings()

def database_pgsql_url_config():
    # return str(setting().DB_CONNECTION + "://" + setting().DB_USERNAME + ":" + setting().DB_PASSWORD + 
    #                 "@" + setting().DB_HOST + ":" + setting().DB_PORT + "/" + setting().DB_DATABASE())
    return "postgresql://postgres:thaothao123@localhost:5432/token"

database = databases.Database(database_pgsql_url_config())
engine = sqlalchemy.create_engine(database_pgsql_url_config())
metadata.create_all(engine)

#2.Using starlette to load .env configuration file
# def database_pgsql_url_config():
    