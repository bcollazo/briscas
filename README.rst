#######
briscas
#######

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
