# briscas

Computer Players:
- Random Player
- Local Player (most points locally)
- OK Player (best move now s.t. good position in future)
- AI Training:
  - Run many games store them as JSON.
  - K-nearest neighbor (from prev games most winnings play)
  - Stochastic Gradient Descent
  - Features: Life, Hand, Cards in Graveyard, Turn (+ card in play?)

Design:
- Game: to_json()
- Player Interface: play
- Hand
- Card
- Deck Singleton.
