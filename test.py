import unittest
import hextech


class TestSum(unittest.TestCase):

    def testGetTournaments(self):
        tournaments = hextech.getTournaments()
        self.assertTrue(len(tournaments) > 0)

        tournament = tournaments["LCK 2020 Spring"]
        self.assertIsInstance(tournament, hextech.Tournament)
        
    def testGetMatches(self):
        matches = hextech.getMatches(tournamentName="LCK 2020 Spring", matchTeam="DragonX")
        self.assertTrue(len(matches) > 0)

        match = matches[0]
        self.assertIsInstance(match, hextech.Match)

    def testGetGames(self):
        matches = hextech.getMatches(tournamentName="LCK 2020 Spring")
        self.assertTrue(len(matches) > 0)

        match = matches[0]
        self.assertIsInstance(match, hextech.Match)

        games = match.getGames(retrieveImages=True)
        self.assertTrue(len(games) > 0)

        game = games[0]
        self.assertIsInstance(game, hextech.Game)

        scoreline = game.scoreboard[0][0]
        self.assertIsInstance(scoreline, hextech.Scoreline)
        self.assertTrue(len(scoreline.assets) > 0)

        player = scoreline.player
        self.assertIsInstance(player, hextech.Player)

    def testGetPlayers(self):
        players = hextech.getPlayers(tournamentName="LCK 2020 Spring", roleFilter=["Mid"])
        self.assertTrue(len(players) > 0)

        player = players[0]
        self.assertIsInstance(player, hextech.Player)
        self.assertEqual(player.role, "Mid")

    def testGetTeams(self):
        teams = hextech.getTeams(tournamentName="LCK 2020 Spring")
        self.assertEqual(len(teams), 10)

        team = teams[0]
        self.assertIsInstance(team, hextech.Team)

        teamsMap = hextech.getTeams(tournamentName="LCK 2020 Spring", isMapped=True)
        self.assertEqual(len(teamsMap), 10)
        self.assertEqual(teamsMap["APK Prince"]["short"], "SP")

    def testGetMatchSchedule(self):
        matchSchedule = hextech.getMatchSchedule(tournamentName="LCK 2020 Spring")

        matchScheduleMap = {}
        for scheduledMatch in matchSchedule:
            date, time = scheduledMatch["dateTime"].split()
            if date not in matchScheduleMap: matchScheduleMap[date] = {}

            for i in range(2):
                teamName = scheduledMatch["teams"][i]
                if teamName not in matchScheduleMap[date]: matchScheduleMap[date][teamName] = []
                matchScheduleMap[date][teamName].append(scheduledMatch["teams"][1-i])

        date = "2020-02-05"
        self.assertTrue(date in matchScheduleMap)

        team1 = "DAMWON Gaming"
        team2 = "T1"
        self.assertTrue(team1 in matchScheduleMap[date] and team2 in matchScheduleMap[date])
        self.assertTrue(team2 in matchScheduleMap[date][team1])

    """ ddragon.py tests """

    def testGetChampionThumbnail(self):
        aatroxThumbnail = hextech.getChampionThumbnail("Aatrox")
        self.assertIsInstance(aatroxThumbnail, str)

    def testGetItemThumbnail(self):
        items = "Blade of The Ruined King,Corrupting Potion,Broken Stopwatch,Mercury's Treads,Sterak's Gage,Trinity Force".split(",")
        itemThumbnails = hextech.getItemThumbnail(items)
        self.assertIsInstance(itemThumbnails["Trinity Force"], str)

    def testGetChampionThumbnail(self):
        flashThumbnail = hextech.getSummonerSpellThumbnail("Flash")
        self.assertIsInstance(flashThumbnail, str)

if __name__ == '__main__':
    unittest.main()