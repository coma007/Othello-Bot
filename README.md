# Othello-Bot

This project is an implementation of the classic Othello/Reversi board game, where you can play against a computer bot that uses the minimax algorithm with alpha-beta pruning. The game features both a console mode and a graphical user interface (GUI) mode !

## Table of Contents
- [Game Rules](#game-rules)
  - [Starting Position](#starting-position)
  - [Gameplay](#gameplay)
  - [Ending the Game](#ending-the-game)
  - [Scoring](#scoring) 
- [Implementation](#implementation)
  - [Data Structures](#data-structures)
  - [Minimax Algorithm with Alpha-Beta Pruning](#minimax-algorithm-with-alpha-beta-pruning)
  - [Hashing Algorithms](#hashing-algorithms)
- [Installation](#installation)
- [Usage](#usage)
  - [Game Modes](#game-modes)


## Game Rules

Othello, also known as Reversi, is a classic board game played on an 8x8 grid. The game involves two players, one controlling black pieces and the other controlling white pieces. The objective is to have the most pieces of your color on the board when the game ends.

### Starting Position

The game starts with a central arrangement of four discs: two white and two black discs, placed diagonally to each other. The black player makes the first move.

### Gameplay

1. Players take turns placing their discs on the board.
2. A player can place a disc in a position that encloses the opponent's discs in a straight line (vertical, horizontal or diagonal). 
3. All opponent's discs between the newly placed disc and another disc of the player's color are flipped to the player's color.
4. A move is valid only if it results in at least one opponent's disc being flipped.
   
### Ending the Game

The game ends when:
- The entire board is filled with discs.
- Any player has no valid moves.

### Scoring

At the end of the game, the player with the most discs of their color on the board wins.

## Implementation

### Data Structures

This project employs a variety of data structures to effectively manage the game's logic and state:

#### Game Tree 

The **Game Tree** maps potential moves and game states during gameplay. Each node represents a game state, and edges depict possible moves. This structure is vital for implementing the minimax algorithm with alpha-beta pruning, helping the bot assess and select moves.

The **Limited Queue** works with a breadth-first search (BFS) algorithm to efficiently navigate the game tree. It controls node count in the queue, optimizing memory while traversing the tree in a breadth-first manner.


#### HashMap with Limited Buckets 

The **HashMap** stores and retrieves encountered game states. Utilizing a limited number of buckets placed in a **Dynamic Array**, each bucket contains game states for efficient storage and retrieval. The HashMap's buckets are implemented as **Map** data structures, holding key-value pairs for enhanced lookups and updates.

These structures work cohesively to manage game states effectively, streamline searches, optimize storage, and contribute to the minimax algorithm. Together, they form the heart of the project's algorithms, enhancing the Othello/Reversi gaming experience.

### Minimax Algorithm with Alpha-Beta Pruning

The bot uses the **minimax algorithm** with **alpha-beta pruning** for decision-making. This algorithm evaluates moves while considering the opponent's responses. By simulating move sequences, the bot assigns scores to outcomes, maximizing its score while minimizing the opponent's chances.

**Alpha-beta pruning** improves efficiency by removing suboptimal branches in the game tree. It maintains values, alpha and beta, to reduce nodes explored significantly.

The minimax algorithm adjusts its **depth** based on computation time and legal moves, balancing strategic depth with computational efficiency.

### Hashing Algorithms

This project incorporates two hashing algorithms: Zobrist hashing and key compression, both of which are pivotal for efficiently managing game states within the HashMap.

#### Zobrist Hashing

**Zobrist hashing** involves assigning a random value to each possible piece-color-field combination on the game board. The hash value of a game state is computed by XOR-ing these random values based on the pieces' colors and corresponding field values. This hash value serves as an intermediary representation of the game state.

#### Key Compression

After Zobrist hashing, the **key compression** process further refines the hash value. The Zobrist hash value is combined with predetermined constants, and the result undergoes modular arithmetic using a prime number. This outcome is then reduced modulo the capacity of the HashMap, ensuring that the hash value falls within the range of available buckets.

Together, these hashing algorithms contribute to optimizing the performance and memory utilization of the HashMap, enabling efficient storage and retrieval of game states.


## Installation

To run the Othello/Reversi game, follow these steps:
1. Clone the repository to your local machine:
   ```shell
   git clone https://github.com/coma007/Othello-Bot.git
   cd Othello-Bot
   ```
2. Ensure you have Python 3.x installed.
3. Install the necessary dependencies:
   ```shell
   pip install pygame
   ```


## Usage

Navigate to the project directory and run the main script:
```shell
python3 main.py
```
Select a game mode by entering the corresponding number when prompted. 


### Game Modes

You can choose between two game modes:
1. **Console Mode**: Play the game in the console interface. You'll be presented with the game board and prompted to input your move by selecting a position from the list of legal moves. The board and game state will be displayed after each move, along with the estimated time for the last move.
2. **GUI Mode**: Play the game using a graphical user interface. A game window will pop up where you can make your moves by clicking on the legal positions. The GUI also displays the current game board, results, and estimated time for each move. The console will mirror the game state and moves in real-time. A demo video showcasing this mode is available bellow.

https://github.com/coma007/Othello-Bot/assets/76025555/93349187-0172-4d7d-94e8-d306bb4cfadd

Please note that in both modes, the computer bot always plays as the white player, and the human player controls the black pieces.


## Happy Reversing !  🥏 🎮

