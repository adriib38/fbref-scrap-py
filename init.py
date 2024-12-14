from utils import loadYaml
from classificationTable.scraper import extractTable, saveInBBDD as saveClassificationTableInBBDD
from statsTeams.scraper import extractStatsTeam, saveInBBDD as saveStatsTeamsInBBDD

def init():
    competitions = loadYaml("competitions.yaml")["leagues"]
    for comp in competitions:
        extractTable(comp)
        extractStatsTeam(comp)
        
        saveClassificationTableInBBDD(comp['name'])
        saveStatsTeamsInBBDD(comp['name'])
init()