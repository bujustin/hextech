import hextech

# tournaments = hextech.getTournaments()
# tournament = tournaments["LCK 2020 Spring"]
# print(tournament)
# matches = tournament.getMatches()
# print(matches[0])
# games = matches[0].getGames()
# print(games[0])

"""
ddragon.py tests
"""

def testGetChampionThumbnail():
	assert hextech.getChampionThumbnail("Aatrox") == "http://ddragon.leagueoflegends.com/cdn/10.16.1/img/champion/Aatrox.png"

def testGetItemThumbnail():
	items = "Blade of the Ruined King,Corrupting Potion,Broken Stopwatch,Mercury's Treads,Sterak's Gage,Trinity Force".split(",")
	itemThumbnails = hextech.getItemThumbnail(items)

	assert itemThumbnails["Blade of the Ruined King"] == "http://ddragon.leagueoflegends.com/cdn/10.16.1/img/item/3153.png"
	assert itemThumbnails["Corrupting Potion"] == "http://ddragon.leagueoflegends.com/cdn/10.16.1/img/item/2033.png"
	assert itemThumbnails["Broken Stopwatch"] == "http://ddragon.leagueoflegends.com/cdn/10.16.1/img/item/2424.png"
	assert itemThumbnails["Mercury's Treads"] == "http://ddragon.leagueoflegends.com/cdn/10.16.1/img/item/3111.png"
	assert itemThumbnails["Sterak's Gage"] == "http://ddragon.leagueoflegends.com/cdn/10.16.1/img/item/3053.png"
	assert itemThumbnails["Trinity Force"] == "http://ddragon.leagueoflegends.com/cdn/10.16.1/img/item/3078.png"

testGetChampionThumbnail()
testGetItemThumbnail()
