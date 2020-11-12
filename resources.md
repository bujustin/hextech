# Resources for Hextech

## Leaguepedia resources

~~~
https://lol.gamepedia.com/Special:CargoTables/Tournaments
https://lol.gamepedia.com/Special:CargoTables/TournamentPlayers
https://lol.gamepedia.com/Special:CargoTables/ScoreboardPlayers
https://lol.gamepedia.com/Special:CargoTables/ScoreboardGames
https://lol.gamepedia.com/Special:CargoTables/MatchSchedule
https://lol.gamepedia.com/Special:CargoTables/MatchScheduleGame
https://lol.gamepedia.com/Special:CargoTables/PlayerImages
https://www.mediawiki.org/wiki/Extension:Cargo/Querying_data
~~~

## Data Dragon resources

~~~
https://developer.riotgames.com/docs/lol#data-dragon
~~~

## [Build and deploy to PyPI](https://packaging.python.org/tutorials/packaging-projects/)

- Update version in `setup.py`

- Run setup

        python setup.py sdist bdist_wheel

- Deploy to pypi

        python -m twine upload --repository pypi dist/*
