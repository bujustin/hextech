import json
import os.path
import requests

from .consts import *


DDRAGON_VERSION_FILENAME = "ddragon_version"
DDRAGON_ITEMS_FILENAME = "ddragon_items.json"

"""
Request from data dragon api to get latest version number and item json. Caches data locally
Return:
    str : latest data dragon version
"""
def _updateDDragonData():
    # check for latest version
    version = requests.get(DDRAGON_VERSIONS_URL).json()[0]
    with open(DDRAGON_VERSION_FILENAME, "w") as fh:
        fh.write(version)

    # update item data cache to latest version
    itemData = requests.get(ITEM_DATA_URL.format(version)).json()
    with open (DDRAGON_ITEMS_FILENAME, "w") as fh:
        json.dump(itemData, fh)

    return version

"""
Checks cache for data dragon version number. If cache doesn't exist call updateDDragon()
Return:
    str : data dragon version
"""
def _checkDDragonData():
    if os.path.isfile(DDRAGON_VERSION_FILENAME):
        with open(DDRAGON_VERSION_FILENAME, "r") as fh:
            version = fh.read()
    else:
        version = _updateDDragonData()

    return version

"""
Params:
    str : champion name
Returns:
    str : url of champion thumbnail
"""
def getChampionThumbnail(champion):
    # TODO: add override for Wukong -> MonkeyKing
    version = _checkDDragonData()
    return CHAMPION_THUMBNAIL_URL.format(version, champion)

"""
Params:
    List[str] : list of item names
Returns:
    Dict[str -> str] : dict that maps item name to item thumbnail url
"""
def getItemThumbnail(items):
    if os.path.isfile(DDRAGON_ITEMS_FILENAME):
        version = _checkDDragonData()
    else:
        version = _updateDDragonData()

    with open(DDRAGON_ITEMS_FILENAME, "r") as fh:
        itemsJson = json.load(fh)["data"]

        itemMap = dict.fromkeys(items)
        for itemId, itemData in itemsJson.items():
            itemName = itemData["name"]
            if itemName in itemMap:
                itemMap[itemName] = ITEM_THUMBNAIL_URL.format(version, itemId)

    return itemMap

"""
Params:
    str : summoner spell name
Returns:
    str : url of summoner spell thumbnail
"""
def getSummonerSpellThumbnail(summonerSpell):
    version = _checkDDragonData()
    return SUMMONER_SPELL_THUMBNAIL_URL.format(version, summonerSpell)