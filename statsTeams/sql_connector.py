import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

try:
    mydb = mysql.connector.connect(
        host=os.getenv('host'),
        user=os.getenv('user'),
        port=os.getenv('dbport'),
        password=os.getenv('password'),
        database=os.getenv('database'),
        ssl_ca="ca-certificate.crt",
        ssl_disabled=False,
    )
    print("Conexión exitosa!")
except mysql.connector.Error as err:
    print(f"Error de conexión: {err}")

def createTable(tableName, df):
    createTableIfNotExist(tableName)

    cursor = mydb.cursor()
    tableNameLower = tableName.lower()
    cursor.execute(f"DELETE FROM statsTeam_{tableNameLower}")  # Limpia la tabla antes de insertar datos

    sql = f"""
    INSERT INTO statsTeam_{tableNameLower}
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
    tableNameLower = tableName.lower()
    
    mycursor.execute(f"""
    CREATE TABLE IF NOT EXISTS statsTeam_{tableNameLower} (
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
        created_at timestamp not null DEFAULT (CURRENT_timestamp),
        PRIMARY KEY (Squad)
    )
    """)
    print(f"Tabla {tableName} creada o ya existente.")
