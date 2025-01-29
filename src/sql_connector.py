import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

try:
    mydb = mysql.connector.connect(
        host=os.getenv('host'),
        user=os.getenv('user'),
        password=os.getenv('password'),
        port=os.getenv('dbport'),
        database=os.getenv('database'),
        ssl_ca="ca-certificate.crt",
        ssl_disabled=False,
    )
    print("Conexión exitosa!")
except mysql.connector.Error as err:
    print(f"Error de conexión: {err}")

def createTable(tableName, df, dataIdType):
  tableNameLower = str(dataIdType) + str(tableName).lower()
  createTableIfNotExist(tableNameLower, df)

  cursor = mydb.cursor()

  cursor.execute(f"DELETE FROM {tableNameLower}")
  
  # Crear lista de columnas en base a las existentes en el df
  columns = df.columns.str.strip().tolist()
  placeholders = ", ".join(["%s"] * len(columns))
  columns_sql = ", ".join(f"`{col}`" for col in columns)
  
  sql = f"INSERT INTO {tableNameLower} ({columns_sql}) VALUES ({placeholders})"

  # Por cada fila ejecutar insert 
  for index, row in df.iterrows():
    val = tuple(
      row[column] if pd.notna(row[column]) else None
      for column in columns
    )

    cursor.execute(sql, val)
    mydb.commit()

def createTableIfNotExist(tableName, df):
  mycursor = mydb.cursor()

  columnas = []
  for column in df.columns.str.strip():  
      column_name = f"`{column}`"
      if pd.api.types.is_integer_dtype(df[column]):
          columnas.append(f"{column_name} INT")
      elif pd.api.types.is_float_dtype(df[column]):
          columnas.append(f"{column_name} FLOAT")
      elif pd.api.types.is_string_dtype(df[column]):
          columnas.append(f"{column_name} VARCHAR(255)")
      else:
          columnas.append(f"{column_name} TEXT")

  columns_sql = ", ".join(columnas)

  mycursor.execute(f"""
  CREATE TABLE IF NOT EXISTS {tableName} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        {columns_sql},
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
  );
  """)