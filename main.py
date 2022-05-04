from typing import List
import databases
from fastapi import FastAPI
import os
import urllib


host_server = os.environ.get('host_server', 'localhost')
db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '8000')))
database_name = os.environ.get('database_name', 'fastapi')
db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'Shamil')))
db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', 'Bandara@123')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode','prefer')))
DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server, db_server_port, database_name, ssl_mode)

database = databases.Database(DATABASE_URL)



app = FastAPI()


@app.get("/")
async def first():
    return {"Hello" : "Test"}


@app.get("/filter_less_30")
async def filter_fuel_less_30():
    i = 0
    count = 0
    for i in range(len(database)):
        if database[i].Remaining_Fuel_Quantity <= 30:
            count = count+1

    return {"Hello" : "Test1"}

@app.get("/filter_less_100")
async def filter_fuel_less_100():
    i = 0
    count = 0
    for i in range(len(database)):
        if database[i].Remaining_Fuel_Quantity <= 100 & database[i].Remaining_Fuel_Quantity >30:
            count = count+1

    return {"Hello" : "Test2"}


@app.get("/filter_less_200")
async def filter_fuel_less_200():
    i = 0
    count = 0
    for i in range(len(database)):
        if database[i].Remaining_Fuel_Quantity <= 200 & database[i].Remaining_Fuel_Quantity >100:
            count = count+1

    return {"Hello" : "Test3"}

@app.get("/site/{Site_id}")
async def get_site(Site_id:str):
    i=0
    for i in range(len(database)):
        if database[i].Site_ID == Site_id:
            break


    return {"Hello" : "Test4"}
