# Resources for Hextech

## Leaguepedia resources

- [Cargo tables](https://lol.gamepedia.com/Special:CargoTables)
- [Querying cargo tables](https://www.mediawiki.org/wiki/Extension:Cargo/Querying_data)

## Data Dragon resources

- https://developer.riotgames.com/docs/lol#data-dragon

## [Build and deploy to PyPI](https://packaging.python.org/tutorials/packaging-projects/)

- Update version in `setup.py`

- Run setup

        python setup.py sdist bdist_wheel

- Deploy to pypi

        python -m twine upload --repository pypi dist/*
        python -m twine upload --repository pypi dist/<package_name>-<version>.tar.gz dist/<package_name>-<version>-py3-none-any.whl
