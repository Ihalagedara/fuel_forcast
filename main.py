from fastapi import FastAPI
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

details = {}


app = FastAPI()


@app.get("/")
async def first():
    return {"Data":"Base"}


@app.get("/less30")
async def less30():
    count =0
    for i in range(len(row)):
        if row[i][23]<=50:
            count = count+1
            i=i+1
        else:
            i=i+1
    return count


@app.get("/less100")
async def less100():
    count =0
    for i in range(len(row)):
        if row[i][23]>50 & row[i][23]<=100:
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
    for i in range(len(row)):
        if str(row[i][0]) == str(siteId):
            break
        else:
            i=i+1

    for j in range(28):
        if str(row[i][j])=="":
            details[ keys[j] == "N/A" ]
        else:
            details[keys[j]] = str(row[i][j]) 
    print(details)
    return details



