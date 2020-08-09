"""
Params:
    Where clause filtering by L.League_Short
Tournament data format (json)
{
    Name:"Worlds 2020"
    DateStart:"2020-09-25"
    League Short:"WCS"
    DateStart__precision:"1"
}
"""
TOURNAMENTS_URL = """https://lol.gamepedia.com/api.php?action=cargoquery&format=json&limit=500
    &tables=Leagues=L,Tournaments=T
    &fields=T.Name,T.DateStart,L.League_Short
    &where=NOT T.DateStart='' AND ({})
    &join_on=L.League=T.League
    &order_by=T.DateStart DESC"""

DEFAULT_LEAGUES = [
    "LCK",
    "EU LCS", "LEC",
    "LCS", "NA LCS",
    "LPL",
    "MSC", "MSI", "WCS", "RR"
]

"""
Params:
    Leaguepedia tournament name
Match data format (json)
{
    "DateTime UTC":"2020-08-07 13:13:00",
    "Team1":"KT Rolster",
    "Team2":"Hanwha Life Esports",
    "Team1Score":"2",
    "Team2Score":"1",
    "UniqueGame":"LCK/2020 Season/Summer Season/Scoreboards/Week 8_4_3",
    "DateTime UTC__precision":"0"
}
"""
MATCHES_URL = """https://lol.gamepedia.com/api.php?action=cargoquery&format=json&limit=500
    &tables=ScoreboardGames=SG
    &fields=SG.DateTime_UTC,SG.Team1,SG.Team2,SG.Team1Score,SG.Team2Score,SG.UniqueGame
    &where=SG.Tournament='{}'
    &order_by=SG.DateTime_UTC DESC"""

"""
Params:
    Where clause filtering by SG.UniqueGame
Game data format (json)
{
    "UniqueGame":"LCK/2020 Season/Summer Season/Scoreboards/Week 8_4_1",
    "Gamename":"Game 1",
    "DateTime UTC":"2020-08-07 11:20:00",
    "Gamelength":"32:18",
    "MatchHistory":"http://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/1413537?gameHash=5dd2b153945ea73e",
    "Winner":"2",
    "Team1":"KT Rolster",
    "Team2":"Hanwha Life Esports",
    "Team1Bans":"Galio,Kalista,Sett,Camille,Kennen",
    "Team2Bans":"Karma,Zoe,Jayce,Twisted Fate,LeBlanc",
    "Name":"CuVee",
    "Team":"Hanwha Life Esports",
    "Role":"Top",
    "Champion":"Gangplank",
    "Kills":"6",
    "Deaths":"1",
    "Assists":"5",
    "Gold":"16582",
    "CS":"311",
    "SummonerSpells":
    "Teleport,Flash",
    "Items":"Control Ward,Infinity Edge,Essence Reaver,Trinity Force,Boots of Swiftness,Sterak's Gage",
    "KeystoneRune":"Grasp of the Undying",
    "FileName":"GEN CuVee 2019 Split 2.png",
    "DateTime UTC__precision":"0"}
}
"""
GAMES_URL = """https://lol.gamepedia.com/api.php?action=cargoquery&format=json&limit=500
    &tables=ScoreboardGames=SG,ScoreboardPlayers=SP,PlayerImages=PI
    &fields=SG.UniqueGame,SG.Gamename,SG.DateTime_UTC,SG.Gamelength,SG.MatchHistory,
    SG.Winner,SG.Team1,SG.Team2,SG.Team1Bans,SG.Team2Bans,
    SP.Name,SP.Team,SP.Role,SP.Role_Number,SP.Champion,SP.Kills,SP.Deaths,SP.Assists,SP.Gold,SP.CS,SP.SummonerSpells,SP.Items,SP.KeystoneRune,PI.FileName
    &where={}
    &join_on=SG.UniqueGame=SP.UniqueGame,SP.Link=PI.Link
    &order_by=SG.UniqueGame ASC,SP.Team,SP.Role_Number ASC
    &group_by=SG.UniqueGame,SP.Name"""

"""
Params:
    FileName provided in game data object
"""
PLAYER_THUMBNAIL_URL = "https://lol.gamepedia.com/Special:Redirect/file/{}"

DDRAGON_VERSIONS_URL = "https://ddragon.leagueoflegends.com/api/versions.json"

"""
Params:
    Data dragon version number
    Champion name
"""
CHAMPION_THUMBNAIL_URL = "http://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}.png"

"""
Params:
    Data dragon version number
"""
ITEM_DATA_URL = "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/item.json"

"""
Params:
    Data dragon version number
    Item id
"""
ITEM_THUMBNAIL_URL = "http://ddragon.leagueoflegends.com/cdn/{}/img/item/{}.png"

"""
Params:
    Data dragon version number
    Summoner spell name
"""
SUMMONER_SPELL_THUMBNAIL_URL = "http://ddragon.leagueoflegends.com/cdn/{}/img/spell/Summoner{}.png"
