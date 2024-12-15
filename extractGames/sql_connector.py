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
  cursor.execute(f"DELETE FROM games_{tableName}")

  sql = f"""
  INSERT INTO games_{tableName} 
  (Wk,Day,Date,Time,Home,Home_xG,Away_xG,Score,Away,Attendance,Venue,Referee) 
  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
  """

  for index, row in df.iterrows():
    val = tuple(
      row[column] if pd.notna(row[column]) else None
      for column in [
        "Wk",
        "Day",
        "Date",
        "Time",
        "Home",
        "Home_xG",
        "Away_xG",
        "Score",
        "Away",
        "Attendance",
        "Venue",
        
      ]
    )

    val += ("none",) #Set none in val
    cursor.execute(sql, val)
    mydb.commit()

def createTableIfNotExist(tableName):
  mycursor = mydb.cursor()

  mycursor.execute(f"""
  CREATE TABLE IF NOT EXISTS games_{tableName} (
    Wk INT NOT NULL,
    Day VARCHAR(10) NOT NULL,
    Date DATE NOT NULL,
    Time TIME,
    Home VARCHAR(50) NOT NULL,
    Home_xG DECIMAL(3,1),
    Score VARCHAR(5),
    Away_xG DECIMAL(3,1),
    Away VARCHAR(50) NOT NULL,
    Attendance INT,
    Venue VARCHAR(100),
    Referee VARCHAR(50),
    created_at timestamp not null DEFAULT (CURRENT_timestamp)
  );
  """)

