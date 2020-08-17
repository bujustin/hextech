import re
import json
import requests

from .consts import *
from . import ddragon


def getTeams(tournamentName):
    pass

"""
Filters support equality operators (=, !=, >, <, >=, <=)
e.g. tournamentDate=">2019-08-21" returns all tournaments with dates greater than 2019-08-21

Filters can be either single values 
e.g. tournamentName="LCK 2020 Summer"
or iterables
e.g. tournamentLeague=["LCK", "LCS"]

For iterable filters, the type determines whether AND/OR will be applied
Lists will apply OR to filter elements
e.g. tournamentDate=["2019-08-21", ">2020-01-01"] will return tournaments with tournamentDate = 2019-08-21 OR tournamentDate > 2020-01-01
Tuples will apply AND to filter elements (this is useful for applying tournamentDate range filters)
e.g. tournamentDate=(">2019-08-21", "<=2019-12-01") will return tournaments with dates between 2019-08-21 AND 2019-12-01
"""

"""
Params:
    List[str] : list of leagues to get tournaments from (e.g. LCS, LCK)
Returns:
    Dict[str -> Tournament] : dictionary of tournament names mapped to tournament objects
"""
def getTournaments(tournamentLeague=DEFAULT_LEAGUES, tournamentName=None, tournamentDate=None):
    argsString = " AND ".join(filter(None, [
        _formatArgs(tournamentLeague, "L.League_Short"),
        _formatArgs(tournamentName, "T.Name"),
        _formatArgs(tournamentDate, "T.DateStart")
        ]))

    url = TOURNAMENTS_URL.format(argsString)
    tournamentsJson = requests.get(url).json()["cargoquery"]

    tournaments = {}
    for i in range(len(tournamentsJson)):
        tournamentJson = tournamentsJson[i]["title"]
        tournament = Tournament(tournamentJson["Name"])
        tournament.startDate = tournamentJson["DateStart"]
        tournament.league = tournamentJson["League Short"]
        tournaments[tournamentJson["Name"]] = tournament

    return tournaments

def getMatches(tournamentName=None, matchDate=None, matchPatch=None, matchTeam=None):
    argsString = " AND ".join(filter(None, [
        _formatArgs(tournamentName, "SG.Tournament"),
        _formatArgs(matchDate, "SG.DateTime_UTC"),
        _formatArgs(matchPatch, "SG.Patch")
        ]))

    url = MATCHES_URL.format(argsString)
    matchesJson = requests.get(url).json()["cargoquery"]

    matches = []
    uniqueMatchMap = {}
    for i in range(len(matchesJson)):
        matchJson = matchesJson[i]["title"]

        # apply team filter
        if isinstance(matchTeam, str):
            matchTeam = [matchTeam]
        if isinstance(matchTeam, list):
            if matchJson["Team1"] not in matchTeam and matchJson["Team2"] not in matchTeam:
                continue
        elif isinstance(matchTeam, tuple):
            if not set(matchTeam).issubset(set([matchJson["Team1"], matchJson["Team2"]])):
                continue
        
        uniqueMatch = matchJson["UniqueGame"][:-2]
        if uniqueMatch not in uniqueMatchMap:
            match = Match(uniqueMatch)
            match._uniqueGames.append(matchJson["UniqueGame"])
            match.dateTime = matchJson["DateTime UTC"]
            match.patch = matchJson["Patch"]
            match.teams = (matchJson["Team1"], matchJson["Team2"])
            match.scores = (int(matchJson["Team1Score"]), int(matchJson["Team2Score"]))

            matches.append(match)
            uniqueMatchMap[uniqueMatch] = match
        else:
            match = uniqueMatchMap[uniqueMatch]
            match._uniqueGames.append(matchJson["UniqueGame"])
            match.dateTime = matchJson["DateTime UTC"]

    return matches

def _getGames(uniqueGames, retrieveImages=False):
    url = GAMES_URL.format(_formatArgs(uniqueGames, "SG.UniqueGame"))
    gamesJson = requests.get(url).json()["cargoquery"]

    games = []
    gameMap = {}
    for i in range(len(gamesJson)):
        gameJson = gamesJson[i]["title"]

        uniqueGame = gameJson["UniqueGame"]
        if uniqueGame not in gameMap:
            game = Game(uniqueGame)
            game.gameName = gameJson["Gamename"]
            game.dateTime = gameJson["DateTime UTC"]
            game.duration = gameJson["Gamelength"]
            game.matchHistory = gameJson["MatchHistory"]

            game.winner = int(gameJson["Winner"]) - 1
            game.teams = (gameJson["Team1"], gameJson["Team2"])
            game.bans = (gameJson["Team1Bans"], gameJson["Team2Bans"])

            games.append(game)
            gameMap[uniqueGame] = game

        player = Player(gameJson["Name"], gameJson["Team"])
        player.thumbnail = PLAYER_THUMBNAIL_URL.format(gameJson["FileName"])

        scoreline = Scoreline(uniqueGame, player)
        scoreline.role = gameJson["Role"]
        scoreline.champion = gameJson["Champion"]
        scoreline.kills = int(gameJson["Kills"])
        scoreline.deaths = int(gameJson["Deaths"])
        scoreline.assists = int(gameJson["Assists"])
        scoreline.gold = int(gameJson["Gold"])
        scoreline.cs = int(gameJson["CS"])
        scoreline.summonerSpells = gameJson["SummonerSpells"].split(",")
        scoreline.items = gameJson["Items"].split(",")
        scoreline.runes = gameJson["KeystoneRune"]

        if retrieveImages:
            # retrieve images using data dragon api and populate assets field
            scoreline.assets = ddragon.getItemThumbnail(scoreline.items)
            scoreline.assets[scoreline.champion] = ddragon.getChampionThumbnail(scoreline.champion)
            for summonerSpell in scoreline.summonerSpells:
                scoreline.assets[summonerSpell] = ddragon.getSummonerSpellThumbnail(summonerSpell)

        game = gameMap[uniqueGame]
        gameIndex = game.teams.index(gameJson["Team"])
        roleIndex = int(gameJson["Role Number"]) - 1
        game.scoreboard[gameIndex][roleIndex] = scoreline

    return games

def _formatArgs(args, prefix):
    if args == None: return None
    delim = " OR "
    if isinstance(args, list): pass
    elif isinstance(args, tuple): delim = " AND "
    else: args = [args]

    def formatArg(arg):
        m = re.search("<=|>=|!=|<|>|=", arg)
        if m == None:
            return "{}='{}'".format(prefix, arg)
        else:
            i = m.span()[1]
            return "{}{}'{}'".format(prefix, arg[:i], arg[i:])

    return "(" + delim.join(formatArg(arg) for arg in args) + ")"

class Tournament:
    def __init__(self, name):
        self.name = name

        self.startDate = ""
        self.league = ""

    def __str__(self):
        return self.name

    def getMatches(self):
        return getMatches(tournamentName=self.name)

class Match:
    def __init__(self, _uniqueMatch):
        self._uniqueMatch = _uniqueMatch
        self._uniqueGames = []

        self.dateTime = None
        self.patch = None
        self.teams = (None, None)
        self.scores = (0, 0)

    def __str__(self):
        return """{} {} {}-{} {}\n""".format(
            self.dateTime.split(" ")[0], self.teams[0], self.scores[0], self.scores[1], self.teams[1])

    def getGames(self, retrieveImages=False):
        return _getGames(self._uniqueGames, retrieveImages)

class Game:
    def __init__(self, uniqueGame):
        self._uniqueGame = uniqueGame

        self.gameName = None
        self.dateTime = None
        self.duration = None
        self.matchHistory = None

        self.winner = 0
        self.teams = (None, None)
        self.bans = (None, None)
        self.scoreboard = [[None] * 5, [None] * 5]

    def __str__(self):
        return "\t{}: {} vs. {}\n\tWinner: {} in {}\n\t\t{}\n".format(
            self.gameName, self.teams[0], self.teams[1],
            self.teams[self.winner], self.duration,
            "\n\t\t".join([str(self.scoreboard[0][i])+"\t\t"+str(self.scoreboard[1][i]) for i in range(5)]))

    def getScoreline(self, teamIndex, roleIndex):
        return self.scoreboard[teamIndex][roleIndex]

class Scoreline:
    def __init__(self, uniqueGame, player):
        self._uniqueGame = uniqueGame
        self.player = player

        self.role = ""
        self.champion = ""

        self.kills = 0
        self.deaths = 0
        self.assists = 0
        self.gold = 0
        self.cs = 0

        self.summonerSpells = []
        self.items = []
        self.runes = ""
        
        self.assets = {}

    def __str__(self):
        return "{}\t{}\t{}-{}-{}".format(
            self.player, self.champion, self.kills, self.deaths, self.assists)

class Player:
    def __init__(self, name, team):
        self.name = name
        self.team = team
        self.thumbnail = None

    def __str__(self):
        return "{} {}".format(self.team, self.name)
