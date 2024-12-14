import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv('host'),
    user=os.getenv('user'),
    password=os.getenv('password'),
    database=os.getenv('database')
)

def createTable(tableName, df):
    createTableIfNotExist(tableName)

    cursor = mydb.cursor()
    cursor.execute(f"DELETE FROM statsTeam_{tableName}")  # Limpia la tabla antes de insertar datos

    sql = f"""
    INSERT INTO statsTeam_{tableName} 
    (Squad, Pl, Age, Poss, MP, Starts, Min, `90s`, Gls, Ast, G_plus_A) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        val = tuple(
            row[column] if pd.notna(row[column]) else None
            for column in [
                "Squad", "Pl", "Age", "Poss", "MP", "Starts", "Min", "90s", "Gls", "Ast", "G_plus_A"
            ]
        )
        cursor.execute(sql, val)
    mydb.commit()

def createTableIfNotExist(tableName):
    mycursor = mydb.cursor()

    # Crear la tabla si no existe con las columnas necesarias
    mycursor.execute(f"""
    CREATE TABLE IF NOT EXISTS statsTeam_{tableName} (
        Squad VARCHAR(255),
        Pl INT,
        Age FLOAT,
        Poss FLOAT,
        MP INT,
        Starts INT,
        Min INT,
        `90s` FLOAT,
        Gls INT,
        Ast INT,
        G_plus_A INT,
        created_at timestamp not null DEFAULT (CURRENT_timestamp)
    )
    """)
    print(f"Tabla {tableName} creada o ya existente.")
