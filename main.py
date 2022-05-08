from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import pyodbc


server = 'shamil.database.windows.net'
database = 'fuelforcast'
username = 'Shamil'
password = 'Bandara@123'   
driver= '{ODBC Driver 17 for SQL Server}'

with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT TOP (1000) * FROM [dbo].[Fuel-Forecast-CNR]")
        row = cursor.fetchall()
        #print(row[0][23])

keys = ["Site_ID","Site_Name","Region","New_Region","Depot","Tower_Category","Energy_category","Entity","Site_category","Rectification_Rank","New_Rectification_Rank","Site_Cabin_Type","STBG_FTG_Status","Gen_brand_1","Gen_Capacity_1","Gen_Brand_2","Gen_Capacity_2","Fuel_Tank_Capacity","FuelConsumption_Fuel_consumption","FuelFilled1_Date","FuelFilled1_Filled_Fuel_Qty_L","RunningHr_TotalGenRunning","RegionaUpdate_STBG_FTG_Status","Remaining_Fuel_Quantity","Required_Fuel_Amount_for_Next_5_Day","Next_Filling_Date","Remark","RegionaUpdate_STBG_FTG_Status2"]



class details(BaseModel):
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


app = FastAPI()


@app.get("/")
async def first():
    return {"Data":"Base"}


@app.get("/less30")
async def less30():
    count =0
    for i in range(len(row)):
        if row[i][23]<=30:
            count = count+1
            i=i+1
        else:
            i=i+1
    return count


@app.get("/less100")
async def less100():
    count =0
    for i in range(len(row)):
        if row[i][23]>30 & row[i][23]<=100:
            count = count+1
            i=i+1
        else:
            i=i+1
    return count


@app.get("/other")
async def other():
    count =0
    for i in range(len(row)):
        if row[i][23]>100:
            count = count+1
            i=i+1
        else:
            i=i+1
    return count


@app.get("/site/{siteId}")
async def site(siteId):
    details = []
    for i in range(len(row)):
        if str(row[i][0]) == str(siteId):
            break
        else:
            i=i+1

    for j in range(28):
        if str(row[i][j])=="":
            details.append("N/A")
        else:
            details[keys[j]] = str(row[i][j]) 
    
    return JSONResponse(details)

@app.get("/details/{type}")
async def det(type):
    if type == "urgent":
        list1 = []
        list2 = []
        for i in range(len(row)):
            if row[i][23]<=30:
                list1.append(row[i][0])
                list1.append(row[i][1])
                list1.append(row[i][8])
                list1.append(row[i][10])
                i=i+1
            else:
                i=i+1
            list2.append(list1)

    elif type == "critical":
        list1 = {}
        list2 = {}
        for i in range(len(row)):
            if row[i][23]>30 & row[i][23]<=100:
                list1["SIte_ID"] = str(row[i][0])
                list1["Site_Name"] = str(row[i][1])
                list1["Site_catogary"] = str(row[i][8])
                list1["Rank"] = str(row[i][10])
                list2["site"+1] = list1
                i=i+1
            else:
                i=i+1
            

    elif type == "other":
        list1 = []
        list2 = []
        for i in range(len(row)):
            if row[i][23]>100:
                list1.append(row[i][0])
                list1.append(row[i][1])
                list1.append(row[i][8])
                list1.append(row[i][10])
                i=i+1
            else:
                i=i+1
            list2.append(list1)

    return list2