from utils import loadYaml
from classificationTable.scraper import extractTable, saveInBBDD as saveClassificationTableInBBDD
from statsTeams.scraper import extractStatsTeam, saveInBBDD as saveStatsTeamsInBBDD
from extractGames.scraper import extractGames, saveInBBDD as saveGamesInBBDD

def init():
    competitions = loadYaml("competitions.yaml")["leagues"]
    for comp in competitions:
        extractTable(comp)
        extractStatsTeam(comp)
        extractGames(comp)
        
        saveClassificationTableInBBDD(comp['name'])
        saveStatsTeamsInBBDD(comp['name'])
        saveGamesInBBDD(comp['name'])
init()