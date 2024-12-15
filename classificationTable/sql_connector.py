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
  cursor.execute(f"DELETE FROM {tableName}")

  sql = f"""
  INSERT INTO {tableName} 
  (Rk, Squad, MP, W, D, L, GF, GA, GD, Pts, Pts_MP, xG, xGA, xGD, xGD_90, Last_5, Attendance, Top_Team_Scorer, Goalkeeper, Notes) 
  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
  """

  for index, row in df.iterrows():
    val = tuple(
      row[column] if pd.notna(row[column]) else None
      for column in [
        "Rk",
        "Squad",
        "MP",
        "W",
        "D",
        "L",
        "GF",
        "GA",
        "GD",
        "Pts",
        "Pts_MP",
        "xG",
        "xGA",
        "xGD",
        "xGD_90",
        "Last_5",
        "Attendance",
        "Top_Team_Scorer",
        "Goalkeeper",
      ]
    )

    val += ("none",) #Set none in val
    cursor.execute(sql, val)
    mydb.commit()

def createTableIfNotExist(tableName):
  mycursor = mydb.cursor()

  mycursor.execute(f"""
  CREATE TABLE IF NOT EXISTS {tableName} (
    Rk INT NOT NULL,
    Squad VARCHAR(255),
    MP INT,
    W INT,
    D INT,
    L INT,
    GF INT,
    GA INT,
    GD INT,
    Pts INT,
    Pts_MP FLOAT,
    xG FLOAT,
    xGA FLOAT,
    xGD FLOAT,
    xGD_90 FLOAT,
    Last_5 VARCHAR(255),
    Attendance VARCHAR(255),
    Top_Team_Scorer VARCHAR(255),
    Goalkeeper VARCHAR(255),
    Notes FLOAT
  );
  """)

