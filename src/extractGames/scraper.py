from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
from sql_connector import createTable

def extractGames(comp):
    print(f"Getting games - {comp}")

    url = comp.get("games", "games")
    
    req = requests.get(url).text
    soup = BeautifulSoup(req, "html.parser")
    
    data = soup.find_all("table")[0]

    columns = [th.get_text(strip=True) for th in data.find_all("tr")[0].find_all("th")]

    rows = []
    for tr in data.find("tbody").find_all("tr"):
        cells = [cell.get_text(strip=True) for cell in tr.find_all(["td", "th"])]
        rows.append(cells)

    df = pd.DataFrame(rows, columns=columns)
    df_filtered = df[
        df['Time'].notna() & (df['Time'] != '') & (df['Time'] != 'Time') &
        df['Home'].notna() & (df['Home'] != '')
    ]
    df_filtered = df_filtered.drop(columns=['Notes', 'Match Report'])
    #Si no es '' Cambiar , por . en Attendance
    df_filtered['Attendance'] = df_filtered['Attendance'].apply(lambda x: x.replace(",", ".") if x != '' else x)

    #Si existe la columna xG renombrarla a Home_xG y un segundo xG a Away_xG
    if 'xG' in df_filtered.columns:
        df_filtered.rename(columns={'xG': 'Home_xG'}, inplace=True)
    if 'xG.1' in df_filtered.columns:
        df_filtered.rename(columns={'xG.1': 'Away_xG'}, inplace=True)


    path = "results/games/" + comp.get('name', 'name') + ".csv"
    # df.rename(columns={'Pts/MP': 'Pts_MP', 'Last 5': 'Last_5', 'Top Team Scorer': 'Top_Team_Scorer', 'xGD/90': 'xGD_90'}, inplace=True)

    df_filtered.to_csv(path, index=False, encoding="utf-8", sep=";")
    
def saveInBBDD(comp):
    file_path = f"./results/games/{comp}.csv"
    df = pd.read_csv(file_path, sep=";")

    print("Saving results...")
    createTable(comp, df, "games_")

