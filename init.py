from utils import loadYaml
from scraper import extractTable, saveInBBDD

def init():
    competitions = loadYaml("competitions.yaml")["leagues"]
    for comp in competitions:
        extractTable(comp)

        saveInBBDD(comp['name'])

init()