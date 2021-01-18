from . import leaguepedia


class Tournament:
    def __init__(self, name):
        self.name = name

        self.startDate = ""
        self.league = ""

    def __str__(self):
        return self.name

    def getMatches(self):
        return leaguepedia.getMatches(tournamentName=self.name)

    def getTeams(self, isMapped=False, thumbnailRedirect=False):
        return leaguepedia.getTeams(self.name, isMapped, thumbnailRedirect)

    def getPlayers(self, roleFilter=["Top", "Jungle", "Mid", "Bot", "Support"], thumbnailRedirect=False):
        return leaguepedia.getPlayers(self.name, roleFilter, thumbnailRedirect)

    def getMatchSchedule(self):
        return leaguepedia.getMatchSchedule(self.name)

class Match:
    def __init__(self, _uniqueMatch):
        self._uniqueMatch = _uniqueMatch
        self._uniqueGames = []

        self.dateTime = None
        self.patch = None
        self.teams = (None, None)
        self.scores = (0, 0)

    def __str__(self):
        return "{} {} {}-{} {}\n".format(
            self.dateTime.split(" ")[0], self.teams[0], self.scores[0], self.scores[1], self.teams[1])

    def getGames(self, retrieveImages=False):
        return leaguepedia._getGames(self._uniqueGames, retrieveImages)

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
        self.kp = 0
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
    def __init__(self, name, team, role):
        self.name = name
        self.team = team
        self.role = role
        self.thumbnail = None

    def __str__(self):
        return "{} {}".format(self.team, self.name)

class Team:
    def __init__(self, name, short):
        self.name = name
        self.short = short
        self.thumbnail = None

    def __str__(self):
        return self.short
