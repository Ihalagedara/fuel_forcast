from typing import List
import databases
import sqlalchemy
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel
import os
import urllib


host_server = os.environ.get('host_server', 'localhost')
db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '8000')))
database_name = os.environ.get('database_name', 'fastapi')
db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'Shamil')))
db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', 'Bandara@123')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode','prefer')))
DATABASE_URL = 'mysql+pymysql://{}:{}@{}/{}?port={}?charset=utf8'.format(db_username, db_password, host_server, database_name, db_server_port)

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

fuel = sqlalchemy.Table(
    "fuel_forcast",
    metadata,
    sqlalchemy.Column("Site_ID", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("Site_Name", sqlalchemy.String),
    sqlalchemy.Column("Region", sqlalchemy.String),
    sqlalchemy.Column("New_Region", sqlalchemy.String),
    sqlalchemy.Column("Depot", sqlalchemy.String),
    sqlalchemy.Column("Tower_Category", sqlalchemy.String),
    sqlalchemy.Column("Energy_category", sqlalchemy.String),
    sqlalchemy.Column("Entity", sqlalchemy.String),
    sqlalchemy.Column("Site_category", sqlalchemy.String),
    sqlalchemy.Column("Rectification_Rank", sqlalchemy.String),
    sqlalchemy.Column("New_Rectification_Rank", sqlalchemy.String),
    sqlalchemy.Column("Site_Cabin_Type", sqlalchemy.String),
    sqlalchemy.Column("STBG_FTG_Status", sqlalchemy.String),
    sqlalchemy.Column("Gen_brand_1", sqlalchemy.String),
    sqlalchemy.Column("Gen_Capacity_1", sqlalchemy.String),
    sqlalchemy.Column("Gen_Brand_2", sqlalchemy.String),
    sqlalchemy.Column("Gen_Capacity_2", sqlalchemy.String),
    sqlalchemy.Column("Fuel_Tank_Capacity", sqlalchemy.String),
    sqlalchemy.Column("FuelConsumption_Fuel_consumption", sqlalchemy.String),
    sqlalchemy.Column("FuelFilled1_Date", sqlalchemy.String),
    sqlalchemy.Column("FuelFilled1_Filled_Fuel_Qty_L", sqlalchemy.String),
    sqlalchemy.Column("RunningHr_TotalGenRunning", sqlalchemy.String),
    sqlalchemy.Column("RegionaUpdate_STBG_FTG_Status", sqlalchemy.String),
    sqlalchemy.Column("Remaining_Fuel_Quantity", sqlalchemy.String),
    sqlalchemy.Column("Required_Fuel_Amount_for_Next_5_Day", sqlalchemy.String),
    sqlalchemy.Column("Next_Filling_Date", sqlalchemy.String),
    sqlalchemy.Column("Remark", sqlalchemy.String),
    sqlalchemy.Column("RegionaUpdate_STBG_FTG_Status2", sqlalchemy.String),

)

engine = sqlalchemy.create_engine(
    #DATABASE_URL, connect_args={"check_same_thread": False}
    DATABASE_URL, pool_size=3, max_overflow=0
)
metadata.create_all(engine)


class Fuel(BaseModel):
    Site_ID: str
    Site_Name: str
    Region: str
    New_Region: str
    Depot: str
    Tower_Category: str 
    Energy_category: str
    Entity: str
    Site_category: str
    Rectification_Rank: str
    New_Rectification_Rank: str
    Site_Cabin_Type: str
    STBG_FTG_Status: str
    Gen_brand_1: str
    Gen_Capacity_1: str
    Gen_Brand_2: str
    Gen_Capacity_2: str
    Fuel_Tank_Capacity: str
    FuelConsumption_Fuel_consumption: str
    FuelFilled1_Date: str
    FuelFilled1_Filled_Fuel_Qty_L: str
    RunningHr_TotalGenRunning: str
    RegionaUpdate_STBG_FTG_Status: str
    Remaining_Fuel_Quantity: str
    Required_Fuel_Amount_for_Next_5_Day: str
    Next_Filling_Date: str
    Remark: str
    RegionaUpdate_STBG_FTG_Status2: str

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
