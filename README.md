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

<pre>
getMatches() -> Dict[str -> <a href="https://github.com/bujustin/hextech#match-class">Match</a>]
</pre>

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

<pre>
getGames() -> List[<a href="https://github.com/bujustin/hextech#game-class">Game</a>]
</pre>

### Game Class

#### Variables

The scoreboard variable contains [Scoreline](#scoreline-class) variables for each role on each team. The list is indexed such that scoreboard[0] and scoreboard[1] correspond to team 1 and 2 respectively; and scoreboard[i][0] -> top ... scoreboard[i][4] -> support.

<pre>
_uniqueGame: str # for internal use

gameName: str
dateTime: str
duration: str
matchHistory: str # link to Riot's match history page for this game

winner: int # corresponding with the index (zero-based) of the winning team
teams: Tuple(str, str)
bans: Tuple(str, str)
scoreboard: [ 
	List[<a href="https://github.com/bujustin/hextech#scoreline-class">Scoreline</a>],
	List[<a href="https://github.com/bujustin/hextech#scoreline-class">Scoreline</a>]
] 
</pre>

### Scoreline Class

Represents the stats for a given player for a specific game.

#### Variables

<pre>
_uniqueGame: str # for internal use
player: <a href="https://github.com/bujustin/hextech#player-class">Player</a>

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
</pre>

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