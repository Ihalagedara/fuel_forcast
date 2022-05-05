
import databases
import sqlalchemy
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel
import os
import urllib

#DATABASE_URL = "sqlite:///./test.db"

host_server = os.environ.get('host_server', 'localhost')
db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '5432')))
database_name = os.environ.get('database_name', 'fastapi')
db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'postgres')))
db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', 'secret')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode','prefer')))
DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server, db_server_port, database_name, ssl_mode)

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()



app = FastAPI(title="REST API using FastAPI PostgreSQL Async EndPoints")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(GZipMiddleware)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()



app = FastAPI()


@app.get("/")
async def first():
    return {"Hello" : "Test"}


@app.get("/getdata",response_model=List[Fuel], status_code = status.HTTP_200_OK)
async def filter_fuel_less_30(skip: int = 0, take: int = 20):
    query = fuel.select().offset(skip).limit(take)

    return database.fetch_all(query)

@app.get("/filter_less_100")
async def filter_fuel_less_100():
    

    return {"Hello" : "Test2"}


@app.get("/filter_less_200")
async def filter_fuel_less_200():
    

    return {"Hello" : "Test3"}

@app.get("/site/{Site_id}")
async def get_site(Site_id:str):
    

    return {"Hello" : "Test4"}
