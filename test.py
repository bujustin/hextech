import hextech

tournaments = hextech.getTournaments()
tournament = tournaments["LCK 2020 Summer"]
print(tournament)
matches = tournament.getMatches()
print(matches[0])
games = matches[0].getGames()
print(games[0])