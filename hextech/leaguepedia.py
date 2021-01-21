import re
import json
import requests
import sys

from . import ddragon
from .classes import *
from .consts import *


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

def getPlayers(tournamentName, roleFilter=["Top", "Jungle", "Mid", "Bot", "Support"], thumbnailRedirect=False):
    """
    Params:
        tournamentName: str/List[str]/Tuple(str) : filter by tournament names (e.g. LCK 2020 Spring)
        roleFilter: List[str] : (optional) list of player roles to include
        thumbnailRedirect: Bool : (optional) if true, get redirected url for player image
    Returns:
        List[Player] : list of players in tournament
    """
    argsString = _formatArgs(tournamentName, "T.Name")
    url = PLAYERS_URL.format(argsString)
    playersJson = requests.get(url).json()["cargoquery"]
    roles = set(roleFilter)
    
    players = []
    for i in range(len(playersJson)):
        playerJson = playersJson[i]["title"]
        if playerJson["Role"] not in roles:
            # filter roles
            continue
        player = Player(playerJson["ID"], playerJson["Team"], playerJson["Role"])
        player.thumbnail = LEAGUEPEDIA_THUMBNAIL_URL.format(playerJson["FileName"])
        if thumbnailRedirect:
            # get redirected (http 301) image
            try:
                redirect = requests.get(player.thumbnail)
                player.thumbnail = redirect.history[-1].headers["Location"].split("/revision", 1)[0]
                # print progress
                sys.stdout.write("\r")
                sys.stdout.write("getting player thumbnail {}/{}".format(i+1, len(playersJson)))
                sys.stdout.flush()
            except:
                continue
        players.append(player)
    return players

def getTeams(tournamentName, isMapped=False, thumbnailRedirect=False):
    """
    Params:
        tournamentName: str/List[str]/Tuple(str) : filter by tournament names (e.g. LCK 2020 Spring)
        isMapped: Bool : (optional) if true, instead return a dictionary with team names (as they were during the tournament) as the keys
        thumbnailRedirect: Bool : (optional) if true, get redirected url for team image
    Returns:
        List[Team]
    """
    argsString = _formatArgs(tournamentName, "SG.Tournament")
    url = TEAMS_URL.format(argsString)
    teamsJson = requests.get(url).json()["cargoquery"]

    teams = {} if isMapped else []
    for i in range(len(teamsJson)):
        teamJson = teamsJson[i]["title"]
        team = Team(teamJson["TeamName"], teamJson["Short"])
        team.thumbnail = LEAGUEPEDIA_THUMBNAIL_URL.format("_".join(teamJson["TeamName"].split()) + "logo_square.png")
        if thumbnailRedirect:
            # get redirected (http 301) image
            try:
                redirect = requests.get(team.thumbnail)
                team.thumbnail = redirect.history[-1].headers["Location"].split("/revision", 1)[0]
                # print progress
                sys.stdout.write("\r")
                sys.stdout.write("getting team thumbnail {}/{}".format(i+1, len(teamsJson)))
                sys.stdout.flush()
            except:
                continue
        if isMapped: teams[teamJson["Team1"]] = vars(team) 
        else: teams.append(team)
    return teams

def getMatchSchedule(tournamentName):
    """
    Params:
        tournamentName: str/List[str]/Tuple(str) : filter by tournament names (e.g. LCK 2020 Spring)
    Returns:
        List[Dict]
    """
    argsString = _formatArgs(tournamentName, "MS.ShownName")
    url = MATCH_SCHEDULE_URL.format(argsString)
    schedulesJson = requests.get(url).json()["cargoquery"]

    matchSchedule = []
    for i in range(len(schedulesJson)):
        scheduleJson = schedulesJson[i]["title"]
        matchSchedule.append({
            "dateTime": scheduleJson["DateTime UTC"],
            "teams": (scheduleJson["Team1"], scheduleJson["Team2"]),
            "bestOf": scheduleJson["BestOf"],
            "week": scheduleJson["Tab"]
        })

    return matchSchedule

def getTournaments(tournamentLeague=DEFAULT_LEAGUES, tournamentName=None, tournamentDate=None):
    """
    Params:
        tournamentLeague: str/List[str]/Tuple(str) : filter by leagues to get tournaments from (e.g. LCS, LCK)
        tournamentName: str/List[str]/Tuple(str) : filter by tournament names (e.g. LCK 2020 Spring)
        tournamentDate: str/List[str]/Tuple(str) : date in the format of yyyy-mm-dd
    Returns:
        Dict[str -> Tournament] : dictionary of tournament names mapped to tournament objects
    """
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
    """
    Params:
        tournamentName: str/List[str]/Tuple(str) : filter by tournament names (e.g. LCK 2020 Spring)
        matchDate: str/List[str]/Tuple(str) : date in the format of yyyy-mm-dd
        matchPatch: str/List[str]/Tuple(str) : game patch the match is played on (e.g. 10.15)
        matchTeam: str/List[str]/Tuple(str)
    Returns:
        List[Match]
    """
    argsString = " AND ".join(filter(None, [
        _formatArgs(tournamentName, "SG.Tournament"),
        _formatDateTimeArgs(matchDate, "SG.DateTime_UTC"),
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
    """
    Params:
        uniqueGames: List[str] : list of strings indicating games to retrieve
        retrieveImages: Bool : indicates whether to retrieve spells, items, runes images from data dragon
    Returns:
        List[Game] : list of game objects retrieved
    """
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

        player = Player(gameJson["Name"], gameJson["Team"], gameJson["Role"])
        player.thumbnail = LEAGUEPEDIA_THUMBNAIL_URL.format(gameJson["FileName"])

        scoreline = Scoreline(uniqueGame, player)
        scoreline.role = gameJson["Role"]
        scoreline.champion = gameJson["Champion"]
        scoreline.kills = int(gameJson["Kills"])
        scoreline.deaths = int(gameJson["Deaths"])
        scoreline.assists = int(gameJson["Assists"])
        scoreline.kp = (scoreline.kills + scoreline.assists) / float(gameJson["TeamKills"])
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
    """
    Params:
        args: str/List[str]/Tuple(str)
        prefix: str
    Returns:
        str : args formatted to be used for leaguepedia query
    """
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

def _formatDateTimeArgs(dateArgs, prefix):
    """
    Helper function to change date strings to datetime strings when formating args
    Params:
        dateArgs: str/List[str]/Tuple(str) : date args in the format of yyyy-mm-dd
        prefix: str
    Returns:
        str : date args in the format of yyyy-mm-dd hh:mm:ss
    """
    if dateArgs == None: return None
    delim = " OR "
    if isinstance(dateArgs, list): pass
    elif isinstance(dateArgs, tuple): delim = " AND "
    else: dateArgs = [dateArgs]

    def formatDateTimeArg(dateArg):
        m = re.search("<=|>=|!=|<|>|=", dateArg)
        if m == None or m.group(0) == "=":
            return "({0}>='{1} 00:00:00' AND {0}<='{1} 23:59:59')".format(prefix, dateArg)
        else:
            i = m.span()[1]
            return "{}{}'{} 00:00:00'".format(prefix, dateArg[:i], dateArg[i:])

    return "(" + delim.join(formatDateTimeArg(dateArg) for dateArg in dateArgs) + ")"
