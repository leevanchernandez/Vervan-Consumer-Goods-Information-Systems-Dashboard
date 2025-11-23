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
def modifyDB(sql, values, return_id=False):
    db = getdblocation()
    cursor = db.cursor()
    cursor.execute(sql, values)
    
    if return_id:
        last_id = cursor.fetchone()[0]  # get RETURNING id
        db.commit()
        db.close()
        return last_id

    db.commit()
    db.close()


def getDataFromDB(sql, values, dfcolumns):
    # ARGUMENTS
    # sql -- sql query with placeholders (%s)
    # values -- values for the placeholders (list or tuple)
    # dfcolumns -- column names for the output

    db = getdblocation()
    cur = db.cursor()
    cur.execute(sql, values)
    rows = pd.DataFrame(cur.fetchall(), columns=dfcolumns)
    db.close()
    return rows

def hash_string(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()
