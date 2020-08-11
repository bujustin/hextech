import unittest
import hextech


class TestSum(unittest.TestCase):

    def testHextech(self):
        tournaments = hextech.getTournaments()
        self.assertTrue(len(tournaments) > 0)

        tournament = tournaments["LCK 2020 Spring"]
        self.assertIsInstance(tournament, hextech.Tournament)

        matches = tournament.getMatches()
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