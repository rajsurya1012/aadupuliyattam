# Bagh Chal - Game of Goats and Tigers

**Project by:** Raj Surya (rajen064@umn.edu)

## Description

Bagh Chal is a strategic two-player board game. The game is asymmetric, with one player controlling four tigers and the other controlling up to twenty goats. The tigers 'hunt' the goats while the goats attempt to block the tigers' movements. The game is played on a \(5 \times 5\) board, with pieces positioned at the intersections of the lines. A variation of this game is prevalent in Aruppukkotai, India, inspiring the development of an AI agent to play the game.

![Bagh Chal Board](https://cdn.mathpix.com/cropped/2024_09_13_4257841470e173eef080g-1.jpg?height=321&width=424&top_left_y=816&top_left_x=816)

**Figure 1:** Board of Bagh Chal [Source: Wikipedia]

### Rules for Tigers:
- Move to an adjacent free position along the lines.
- Capture goats during any move without waiting for all goats to be placed.
- Capture only one goat at a time.
- Jump over a goat in any direction if there is an open space.
- Cannot jump over another tiger.

### Rules for Goats:
- Cannot move until all goats are positioned on the board.
- Must leave the board when captured.
- Cannot jump over tigers or other goats.

The game ends when tigers capture five goats or goats block all tigers' movements.

## Literature Review

The game has limited study in game theory or AI contexts. The complete database of all positions consists of 88,260,972 entries. The placement phase involves a search with a game-tree complexity of about 10. Tigers generally have an advantage in the opening, but goats may catch up over time. No existing research on heuristics exists, so novel heuristics were developed for this implementation.

## Game Implementation

### Requirements:
- Python

### Agents:
1. **Human Agent:** Interactive play with user input for actions.
2. **Random Agent:** Chooses a random valid move.
3. **Alphabeta Agent:** Uses alpha-beta search with heuristics for optimal moves. Can use dynamic depth based on the game state.
4. **Monte Carlo Tree Search Agent:** Uses Monte Carlo search for optimal moves, with configurable iterations.

All agents require a parameter 'T' or 'G' to indicate playing as tigers or goats.

### Heuristic:
Factors include:
- Number of goats captured.
- Number of goats yet to be placed.
- Number of valid moves available.
- Number of tigers without valid moves.
- Number of goats safe from immediate capture.
- Number of goats vulnerable to capture.

The heuristic is a weighted sum of these factors, optimized through trials.

### Running the Game:
Choose two agents, assign roles, and run the game. No special instructions required.

## Results
| Sl. No | Agent playing as Tigers            | Agent playing as Goats             | Total Number of Matches | Number of wins by Tigers | Number of wins by Goats | Number of draws | Average time per match (seconds) |
|--------|------------------------------------|------------------------------------|-------------------------|--------------------------|-------------------------|----------------|----------------------------------|
| 1      | Human                              | Random                             | 10                      | 10                       | 0                       | 0              | NA                               |
| 2      | Random                             | Human                              | 10                      | 0                        | 10                      | 0              | NA                               |
| 3      | Random                             | Random                             | 100                     | 99                       | 1                       | 0              | 0.44                             |
| 4      | Random                             | Alphabeta Depth=4                  | 10                      | 0                        | 4                       | 6              | 5.62                             |
| 5      | Alphabeta Depth=4                  | Random                             | 10                      | 1                        | 0                       | 9              | 7.78                             |
| 6      | Alphabeta Depth=4                  | MonteCarlo Iterations=200          | 50                      | 5                        | 0                       | 45             | 13.47                            |
| 7      | MonteCarlo Iterations=200          | Alphabeta Dynamic Depth            | 50                      | 0                        | 23                      | 27             | 57.20                            |
| 8      | Alphabeta Depth=6                  | Random                             | 10                      | 9                        | 1                       | 1              | 79.24                            |
| 9      | Random                             | Alphabeta Depth=6                  | 10                      | 0                        | 9                       | 1              | 225.79                           |
| 10     | Alphabeta Dynamic Depth            | Random                             | 10                      | 10                       | 0                       | 0              | 40.35                            |
| 11     | Random                             | Alphabeta Dynamic Depth            | 10                      | 0                        | 9                       | 1              | 9.33                             |
| 12     | MonteCarlo Iterations=200          | Random                             | 10                      | 10                       | 0                       | 0              | 10.6                             |
| 13     | Random                             | MonteCarlo Iterations=200          | 10                      | 8                        | 0                       | 2              | 10.15                            |
| 14     | Random MonteCarlo Iterations=10000 |                                    | 1                       | 0                        | 0                       | 1              | 315.6                            |
| 15     | Human (Beginner)                   | Alphabeta Dynamic Depth            | 1                       | 0                        | 1                       | 0              | NA                               |
| 16     | Alphabeta Dynamic Depth            | Human (Beginner)                   | 1                       | 1                        | 0                       | 0              | NA                               |
| 17     | Human (Intermediate)               | Alphabeta Dynamic Depth            | 1                       | 0                        | 0                       | 1              | NA                               |
| 18     | Alphabeta Dynamic Depth            | Human (Intermediate)               | 1                       | 0                        | 0                       | 1              | NA                               |
| 19     | Human (Beginner)                   | Monte Carlo Iterations=200         | 1                       | 1                        | 0                       | 0              | NA                               |
| 20     | Monte Carlo Iterations=200         | Human (Beginner)                   | 1                       | 0                        | 1                       | 0              | NA                               |
## Analysis

- **Random Agent:** Performs better as tigers due to initial advantage.
- **Alphabeta Search:** Robust heuristics can beat beginners; depth of 6 recommended for good performance.
- **Monte Carlo Search:** Less effective due to asymmetry and reliance on random simulations.

## References
1. Lim Yew Jin and J. Nievergelt, "Computing Tigers and Goats", ICGA Journal, Sept 2004
2. Sakshi Agarwal and Hiroyuki Iida, "Analyzing Thousand-Year-Old Game: Tigers and Goat is Still Alive", Information Technology and Tourism, Oct 2018
