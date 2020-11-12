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

    def testGetTeams(self):
        teams = hextech.getTeams(tournamentName="LCK 2020 Spring")
        self.assertTrue(len(teams) == 10)

    def testGetPlayers(self):
        players = hextech.getPlayers(tournamentName="LCK 2020 Spring")
        self.assertTrue(len(players) > 0)

        player = players[0]
        self.assertIsInstance(player, hextech.Player)

    def testGetPlayersRedirect(self):
        players = hextech.getPlayers(tournamentName="LCK 2020 Spring", roleFilter=["Mid"], thumbnailRedirect=True)
        self.assertTrue(len(players) > 0)

        player = players[0]
        self.assertIsInstance(player, hextech.Player)
        self.assertTrue(player.role, "Mid")

    """ ddragon.py tests """

    def testGetChampionThumbnail(self):
        aatroxThumbnail = hextech.getChampionThumbnail("Aatrox")
        self.assertIsInstance(aatroxThumbnail, str)

    def testGetItemThumbnail(self):
        items = "Blade of the Ruined King,Corrupting Potion,Broken Stopwatch,Mercury's Treads,Sterak's Gage,Trinity Force".split(",")
        itemThumbnails = hextech.getItemThumbnail(items)
        self.assertIsInstance(itemThumbnails["Blade of the Ruined King"], str)

    def testGetChampionThumbnail(self):
        flashThumbnail = hextech.getSummonerSpellThumbnail("Flash")
        self.assertIsInstance(flashThumbnail, str)

if __name__ == '__main__':
    unittest.main()