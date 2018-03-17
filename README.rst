#######
briscas
#######

.. image:: https://img.shields.io/pypi/v/briscas.svg
    :target: https://pypi.python.org/pypi/briscas
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/l/briscas.svg
    :target: https://pypi.python.org/pypi/briscas

.. image:: https://img.shields.io/pypi/pyversions/briscas.svg
    :target: https://pypi.python.org/pypi/briscas

.. image:: https://codecov.io/gh/bcollazo/briscas/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/bcollazo/briscas

.. image:: https://travis-ci.org/bcollazo/briscas.svg?branch=master
    :target: https://travis-ci.org/bcollazo/briscas

Python library to model the briscas card game.

It provides:

* Simple models with the validation and business logic needed.
* A script to play the game from the terminal
* A 'Player' interface with the following implementations:
    * Random Player
        * Chooses a random card from their hand every time.
    * Local Player
        * Chooses the 'weakest' card that will win hand locally.
    * Smart Player
        * Like Local Player but uses information from the pile to
            add a probabilistic distribution of outcomes.
    * KNN Player
        * Machine Learning player that uses thousands of games as model.
    * (Work In Progress) ML Players
        * Features: Life, Hand, Cards in Graveyard, Turn (+ card in play?)
