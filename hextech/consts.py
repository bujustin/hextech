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
Player data format (json)
{
    Team: "SeolHaeOne Prince"
    Role: "Bot"
    FileName: "SP Trigger 2020 Split 2.png"
    ID: "Trigger"
}
"""
PLAYERS_URL = """https://lol.gamepedia.com/api.php?action=cargoquery&format=json&limit=500
    &tables=Tournaments=T,TournamentPlayers=TP,PlayerImages=PI,PlayerRedirects=PR
    &fields=TP.Team,PR.ID,TP.Role,PI.FileName
    &where={}
    &join_on=T.OverviewPage=TP.OverviewPage,TP.Link=PI.Link,TP.Player=PR.AllName
    &order_by=PI.FileName DESC
    &group_by=TP.Player"""

"""
Params:
    Leaguepedia tournament name
Team data format (json)
{
    "Team1":"APK Prince",
    "TeamName":"SeolHaeOne Prince",
    "Short":"SP"
}
"""
TEAMS_URL = """https://lol.gamepedia.com/api.php?action=cargoquery&format=json&limit=500
    &tables=ScoreboardGames=SG,TeamRedirects=TR,Teams=T
    &fields=SG.Team1,TR._pageName=TeamName,T.Short
    &where={}
    &join_on=SG.Team1=TR.AllName,TR._pageName=T._pageName
    &group_by=SG.Team1"""

"""
Params:
    Leaguepedia tournament name
Match schedule data format (json)
{
    DateTime UTC    "2021-01-13 08:00:00"
    Team1   "Gen.G"
    Team2   "KT Rolster"
    BestOf  "3"
    Tab "Week 1"
    DateTime UTC__precision "0"
}
"""
MATCH_SCHEDULE_URL = """https://lol.gamepedia.com/api.php?action=cargoquery&format=json&limit=500
    &tables=MatchSchedule=MS
    &fields=MS.DateTime_UTC,MS.Team1,MS.Team2,MS.BestOf,MS.Tab
    &where={}
    &order_by=MS.DateTime_UTC ASC"""

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
    &where=NOT T.DateStart='' AND {}
    &join_on=L.League=T.League
    &order_by=T.DateStart DESC"""

"""
Params:
    Leaguepedia tournament name
Match data format (json)
{
    "DateTime UTC":"2020-08-07 13:13:00",
    "Patch":"10.15",
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
    &fields=SG.DateTime_UTC,SG.Patch,SG.Team1,SG.Team2,SG.Team1Score,SG.Team2Score,SG.UniqueGame
    &where={}
    &order_by=SG.DateTime_UTC DESC"""

"""
Params:
    Where clause filtering by SG.UniqueGame
Game data format (json)
{
    UniqueGame: "LCK/2020 Season/Spring Season/Scoreboards/Week 9_5_1"
    Gamename: "Game 1"
    DateTime UTC: "2020-04-16 09:10:00"
    Gamelength: "25:12"
    MatchHistory: "http://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT03/1351837?gameHash=8d4b64e0e36ce417"
    Winner: "1"
    Team1: "DragonX"
    Team2: "APK Prince"
    Team1Bans: "Illaoi,Trundle,Kalista,Miss Fortune,Ezreal"
    Team2Bans: "Sett,Varus,Senna,Nautilus,Volibear"
    Name: "ikssu"
    Team: "APK Prince"
    Role: "Top"
    Role Number: "1"
    Champion: "Ornn"
    Kills: "1"
    Deaths: "3"
    Assists: "2"
    Gold: "8284"
    CS: "203"
    TeamKills: "7"
    SummonerSpells: "Teleport,Flash"
    Items: "Refillable Potion,Null-Magic Mantle,Mercury's Treads,Doran's Shield,Infernal Mask,Forgefire Cape"
    KeystoneRune: "Unsealed Spellbook"
    FileName: "APK ikssu 2020 Split 1.png"
    DateTime UTC__precision: "0"
}
"""
GAMES_URL = """https://lol.gamepedia.com/api.php?action=cargoquery&format=json&limit=500
    &tables=ScoreboardGames=SG,ScoreboardPlayers=SP,PlayerImages=PI
    &fields=SG.UniqueGame,SG.Gamename,SG.DateTime_UTC,SG.Gamelength,SG.MatchHistory,
    SG.Winner,SG.Team1,SG.Team2,SG.Team1Bans,SG.Team2Bans,
    SP.Name,SP.Team,SP.Role,SP.Role_Number,SP.Champion,SP.Kills,SP.Deaths,SP.Assists,SP.Gold,SP.CS,SP.TeamKills,SP.SummonerSpells,SP.Items,SP.KeystoneRune,PI.FileName
    &where={}
    &join_on=SG.UniqueGame=SP.UniqueGame,SP.Link=PI.Link
    &order_by=SG.UniqueGame ASC,SP.Team,SP.Role_Number ASC
    &group_by=SG.UniqueGame,SP.Name"""

"""
Params:
    FileName provided in game data object
"""
LEAGUEPEDIA_THUMBNAIL_URL = "https://lol.gamepedia.com/Special:Redirect/file/{}"

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
