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

Objects of the following classes are meant to be read-only; they are automatically instantiated by methods such as tournament.getMatches() and match.getGames().

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
getGames(retrieveImages: bool) -> List[<a href="https://github.com/bujustin/hextech#game-class">Game</a>] 
</pre>

`retrieveImages` is false by default. If `retrieveImages` is true, the `assets` variable in the <a href="https://github.com/bujustin/hextech#scoreline-class">Scoreline</a> objects get populated by data from the data dragon api.

### Game Class

#### Variables

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

The scoreboard variable contains [Scoreline](#scoreline-class) variables for each role on each team. The list is indexed such that scoreboard[0] and scoreboard[1] correspond to team 1 and 2 respectively; and scoreboard[i][0] -> top ... scoreboard[i][4] -> support.

#### Functions

<pre>
getScoreline(teamIndex: int, roleIndex: int) -> <a href="https://github.com/bujustin/hextech#scoreline-class">Scoreline</a>
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

summonerSpells: List[str]
items: List[str]
runes: str

assets: Dict[str -> str] # dictonary mapping name of object (e.g. Blade of the Ruined King) to it's thumbnail url
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

## Changelog

### v1.0.2 - 8/10/2020

Added integration with Riot's Data Dragon api to retrieve champion, item, and summoner spell images.

## Disclaimer

Hextech isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.