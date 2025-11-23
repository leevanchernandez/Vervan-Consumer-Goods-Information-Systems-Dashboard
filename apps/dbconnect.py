import psycopg2
import pandas as pd
import hashlib

def getdblocation():
    db = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="12345678",
        port="5432",
        database="Vervan Sample Data"
    )
    
    return db
def modifyDB(sql, values):
    db = getdblocation()
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()
    db.close()
    
def getDataFromDB(sql, values, dfcolumns):
    db = getdblocation()
    cursor = db.cursor()
    cursor.execute(sql, values)
    rows = pd.DataFrame(cursor.fetchall(), columns=dfcolumns)
    db.close()
    return rows

