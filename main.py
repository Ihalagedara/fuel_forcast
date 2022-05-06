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


app = FastAPI()



@app.get("/")
def less30():
    count =0
    for i in range(len(row)):
        if row[i][23]<50:
            count = count+1
            i=i+1
        else:
            i=i+1


    return count


    
    

@app.get("/first")
async def first():
    return row[0][2]


