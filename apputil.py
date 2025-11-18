import numpy as np
from IPython.display import clear_output
import time
import seaborn as sns
import matplotlib.pyplot as plt

def update_board(current_board):
    # Pad with zeros so edge cells treat out-of-bounds as dead
    padded = np.pad(current_board, 1, mode='constant')

    # Sum neighbors in the 3x3 window around each cell (excluding the cell itself)
    neighbor_count = (
        padded[:-2, :-2] + padded[:-2, 1:-1] + padded[:-2, 2:] +
        padded[1:-1, :-2] +                     padded[1:-1, 2:] +
        padded[2:, :-2]  + padded[2:, 1:-1]  + padded[2:, 2:]
    )

    # Apply Game of Life rules
    updated_board = (
        (neighbor_count == 3) |
        ((current_board == 1) & (neighbor_count == 2))
    ).astype(int)

    return updated_board


def show_game(game_board, n_steps=10, pause=0.5):
    """
    Show `n_steps` of Conway's Game of Life, given the `update_board` function.

    Parameters
    ----------
    game_board : numpy.ndarray
        A binary array representing the initial starting conditions for Conway's Game of Life. In this array, ` represents a "living" cell and 0 represents a "dead" cell.
    n_steps : int, optional
        Number of game steps to run through, by default 10
    pause : float, optional
        Number of seconds to wait between steps, by default 0.5
    """
    for step in range(n_steps):
        clear_output(wait=True)

        # update board
        game_board = update_board(game_board)

        # show board
        sns.heatmap(game_board, cmap='plasma', cbar=False, square=True)
        plt.title(f'Board State at Step {step + 1}')
        plt.show()

        # wait for the next step
        if step + 1 < n_steps:
            time.sleep(pause)


def play_game_recursive():
    """
    Play a fixed number of Conway's Game of Life steps on a random 10x10 board.

    Returns:
    numpy.ndarray
        The board state after the recursive simulation.
    """
    max_steps = 10
    start_board = np.random.randint(2, size=(10, 10))

    def recurse(board, remaining):
        if remaining == 0:
            return board
        return recurse(update_board(board), remaining - 1)

    return recurse(start_board, max_steps)


if __name__ == "__main__":
    # Simple demo: advance a random board a few steps and print the result.
    board = np.random.randint(2, size=(5, 5))
    print("Initial board:\n", board)
    for i in range(3):
        board = update_board(board)
        print(f"\nBoard after step {i + 1}:\n", board)
