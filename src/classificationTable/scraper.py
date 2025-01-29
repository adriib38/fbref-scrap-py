from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
from sql_connector import createTable

def extractTable(comp):
    print(f"Getting table - {comp}")

    url = comp.get("link", "link")
    
    req = requests.get(url).text
    soup = BeautifulSoup(req, "html.parser")
    
    data = soup.find_all("table")[0]

    columns = [th.get_text(strip=True) for th in data.find_all("tr")[0].find_all("th")]

    rows = []
    for tr in data.find_all("tbody")[0].find_all("tr"):
        cells = []  
        for td in tr:
            tdText = td.get_text(strip=True)
            cells.append(tdText)

        rows.append(cells)

    df = pd.DataFrame(rows, columns=columns)
    df = df.drop(columns=["Notes"])
    path = "results/classification/" + comp.get('name', 'name') + ".csv"
    df.rename(columns={'Pts/MP': 'Pts_MP', 'Last 5': 'Last_5', 'Top Team Scorer': 'Top_Team_Scorer', 'xGD/90': 'xGD_90'}, inplace=True)

    df.to_csv(path, index=False, encoding="utf-8", sep=";")
    
def saveInBBDD(comp):
    file_path = f"./results/classification/{comp}.csv"
    df = pd.read_csv(file_path, sep=";")

    print("Saving results...")
    createTable(comp, df, "")

