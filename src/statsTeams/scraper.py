from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
from sql_connector import createTable

def extractStatsTeam(comp):
    print(f"Getting stats table - {comp}")

    url = comp.get("link", "link")
    
    req = requests.get(url).text
    soup = BeautifulSoup(req, "html.parser")
    
    data = soup.find_all("table")[2]
    columns = [th.get_text(strip=True) for th in data.find_all("tr")[1].find_all("th")[:11]]
    
    rows = []
    for tr in data.find("tbody").find_all("tr"):
        # cells = [td.get_text(strip=True) for td in tr.find_all("td", "th")[:11]]
        cells = [cell.get_text(strip=True) for cell in tr.find_all(["td", "th"])[:11]]

        if len(cells) == 11:
            rows.append(cells)

    df = pd.DataFrame(rows, columns=columns)
    #Cambiar , por . en Min
    df['Min'] = df['Min'].str.replace(",", ".").astype(float)
    path = "results/stats-table/" + comp.get('name', 'name') + ".csv"
    df.rename(columns={'# Pl': 'Pl','G+A': 'G_plus_A'}, inplace=True)

    df.to_csv(path, index=False, encoding="utf-8", sep=";")
    
def saveInBBDD(comp):
    file_path = f"./results/stats-table/{comp}.csv"
    df = pd.read_csv(file_path, sep=";")

    print("Saving results...")
    createTable(comp, df, "statsteam_")

