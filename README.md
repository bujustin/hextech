# Hextech

A Python framework for accessing League of Legends esports data. 
This package uses data from [Leaguepedia](https://lol.gamepedia.com/) and Riot's [Data Dragon](https://developer.riotgames.com/docs/lol#data-dragon) API. It does not require the use of a Riot API key.

## Installation

With [pip](https://pypi.org/project/Hextech/):

`pip install hextech`

## Usage

Here is a basic example of using hextech to print the winners of each game in LCK 2020 Summer split.

~~~
import hextech

tournament = hextech.getTournaments()["LKC 2020 Summer"]
matches = tournament.getMatches()
for match in matches:
	games = match.getGames()
	for game in games:
		print(game.teams[game.winner])
~~~

Objects of the following classes are meant to be read-only; they are automatically instantiated by methods such as tournament.getMatches() and match.getGames().

Note: All date times are in UTC

### Functions

The definitions of the framework's base functions. The functions take in parameters that act as filters for data selection. Some filters are required while others are optional. More detailed descriptions of the filters can be found in the source code.

Filters support equality operators (=, !=, >, <, >=, <=)
e.g. `tournamentDate=">2019-08-21"` returns all tournaments with dates greater than 2019-08-21

Filters can be either single values 
e.g. `tournamentName="LCK 2020 Summer"`
or iterables
e.g. `tournamentLeague=["LCK", "LCS"]`

For iterable filters (lists/tuples), the type determines whether AND/OR will be applied
Lists will apply OR to filter elements
e.g. `tournamentDate=["2019-08-21", ">2020-01-01"]` will return tournaments with tournamentDate = 2019-08-21 OR tournamentDate > 2020-01-01
Tuples will apply AND to filter elements (this is useful for applying tournamentDate range filters)
e.g. `tournamentDate=(">2019-08-21", "<=2019-12-01")` will return tournaments with dates between 2019-08-21 AND 2019-12-01

These functions are used by other classes 
e.g. `Tournament.getMatches()` calls the base `getMatches()` function with the filter `tournamentName`

<pre>
getPlayers(
	tournamentName: str/List[str]/Tuple(str) # required
	roleFilter: List[str] # optional
    thumbnailRedirect: Bool # optional
) -> List[<a href="https://github.com/bujustin/hextech#player-class">Player</a>]

getTeams(
	tournamentName: str/List[str]/Tuple(str) # required
	isMapped: Bool # optional
    thumbnailRedirect: Bool # optional
) -> List[str]

getMatchSchedule(
	tournamentName: str/List[str]/Tuple(str) # required
) -> List[Dict]

getTournaments(
	tournamentLeague: str/List[str]/Tuple(str), # optional (if not specified, use default leagues)
	tournamentName: str/List[str]/Tuple(str), # optional
	tournamentDate: str/List[str]/Tuple(str) # optional
) -> Dict[str -> <a href="https://github.com/bujustin/hextech#tournament-class">Tournament</a>]

getMatches(
	tournamentName: str/List[str]/Tuple(str), # optional
    matchDate: str/List[str]/Tuple(str) # optional
    matchPatch: str/List[str]/Tuple(str) # optional
    matchTeam: str/List[str]/Tuple(str) # optional
) -> List[<a href="https://github.com/bujustin/hextech#match-class">Match</a>]
</pre>

### Tournament Class

A league specific collection of matches within a specified time frame (e.g. LCK 2020 Summer).

<pre>
name: str
startDate: str # format yyyy-mm-dd
league: str

getMatches() -> Dict[str -> <a href="https://github.com/bujustin/hextech#match-class">Match</a>]
getTeams() -> List[str]
getPlayers() -> List[<a href="https://github.com/bujustin/hextech#player-class">Player</a>]
getMatchSchedule() -> List[Dict]
</pre>

### Match Class

A series of games between two teams. There could be one or multiple games in a match.

<pre>
_uniqueMatch: str # for internal use
_uniqueGames: List[str] # for internal use
dateTime: str # format yyyy-mm-dd hh:mm:ss
patch: str
teams: Tuple(str, str)
scores: Tuple(int, int)

getGames(retrieveImages: bool) -> List[<a href="https://github.com/bujustin/hextech#game-class">Game</a>] 
</pre>

`retrieveImages` is false by default. If `retrieveImages` is true, the `assets` variable in the <a href="https://github.com/bujustin/hextech#scoreline-class">Scoreline</a> objects get populated by data from the data dragon api.

### Game Class

<pre>
_uniqueGame: str # for internal use
gameName: str
dateTime: str # format yyyy-mm-dd hh:mm:ss
duration: str # format hh:mm
matchHistory: str # link to Riot's match history page for this game
winner: int # corresponding with the index (zero-based) of the winning team
teams: Tuple(str, str)
bans: Tuple(str, str)
scoreboard: [ 
	List[<a href="https://github.com/bujustin/hextech#scoreline-class">Scoreline</a>],
	List[<a href="https://github.com/bujustin/hextech#scoreline-class">Scoreline</a>]
] 

getScoreline(teamIndex: int, roleIndex: int) -> <a href="https://github.com/bujustin/hextech#scoreline-class">Scoreline</a>
</pre>

The scoreboard variable contains [Scoreline](#scoreline-class) variables for each role on each team. The list is indexed such that scoreboard[0] and scoreboard[1] correspond to team 1 and 2 respectively; and scoreboard[i][0] -> top ... scoreboard[i][4] -> support.

### Scoreline Class

Represents the stats for a given player for a specific game.

<pre>
_uniqueGame: str # for internal use
player: <a href="https://github.com/bujustin/hextech#player-class">Player</a>
role: str
champion: str
kills: int
deaths: int
assists: int
kp: float
gold: int
cs: int
summonerSpells: List[str]
items: List[str]
runes: str
assets: Dict[str -> str] # dictonary mapping name of object (e.g. Blade of the Ruined King) to it's thumbnail url
</pre>

### Player Class

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

### v1.0.4 - 10/2/2020

Added getTeams() and getPlayers() functionality.

### v1.0.5 - 11/12/2020

Added roleFilter and thumbnailRedirect parameters and functionality to getPlayers(). Added role field to player class.

### v1.0.8 - 11/25/2020

Added Team class. Modified getTeams() to return short name and thumbnail. Added isMapped and thumbnailRedirect parameters to getTeams().

### v1.0.10 - 12/5/2020

Modified getPlayers() to return player ID instead of player name (`Viper` vs `Viper (Park Do-hyeon)`).

### v1.0.11 - 1/17/2021

Added getMatchSchedule() functionality.

## Disclaimer

Hextech isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.