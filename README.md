# Hextech

A Python framework for accessing League of Legends esports data. 
This package uses data from [Leaguepedia](https://lol.gamepedia.com/) and Riot's [Data Dragon](https://developer.riotgames.com/docs/lol#data-dragon) API. It does not require the use of a Riot API key.

## Installation

With [pip](https://pypi.org/project/Hextech/):
`pip install hextech`

## Usage

Here is a basic example of using hextech to print all game results in LCK 2020 Summer split.

~~~
import hextech

tournament = hextech.getTournaments()["LKC 2020 Summer"]
matches = tournament.getMatches()
for match in matches:
	games = match.getGames()
	for game in games:
		print(game)
~~~

### Tournament Class

A league specific collection of matches within a specified time frame (e.g. LCK 2020 Summer).

#### Variables

~~~
name: str
startDate: str
league: str
~~~

#### Functions

~~~
getMatches() -> Dict[str -> [Match](#match class)]
~~~

### Match Class

A series of games between two teams. There could be one or multiple games in a match.

#### Variables

~~~
_uniqueMatch: str # for internal use
_uniqueGames: List[str] # for internal use

dateTime: str
teams: Tuple(str, str)
scores: Tuple(int, int)
~~~

#### Functions

~~~
getGames() -> List[[Game](#game class)]
~~~

### Game Class

#### Variables

~~~
_uniqueGame: str # for internal use

gameName: str
dateTime: str
duration: str
matchHistory: str # link to Riot's match history page for this game

winner: int # corresponding with the index (zero-based) of the winning team
teams: Tuple(str, str)
bans: Tuple(str, str)
scoreboard: [ 
	List[[Scoreline](#scoreline class)], 	# list of scorelines for team 1
	List[[Scoreline](#scoreline class)] 	# list of scorelines for team 2
] 											# each list has an index for each player from top -> support
~~~

### Scoreline Class

Represents the stats for a given player for a specific game.

#### Variables

~~~
_uniqueGame: str # for internal use
player: [Player](#player class)

role: str
champion: str

kills: int
deaths: int
assists: int
gold: int
cs: int

summonerSpells: str
items: str
runes: str
~~~

### Player Class

#### Variables

~~~
name: str
team: str
thumbnail: str # url to the player's thumbnail image
~~~

## Issue Reporting

If you find a bug, please open a new [issue](https://github.com/bujustin/hextech/issues).

## Disclaimer

Hextech isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.