
import mysql.connector

try: 
    
    
    cnx = mysql.connector.connect(
    host="fuelforcastapi.azurewebsites.net",
    port="8000",
    user="Shamil",
    password="Bandara@123",
    database="fuelforcast"
) 

except mysql.connector.Error as err: 
    
        print("Something is wrong with your user name or password") 
else:
    print("good")
