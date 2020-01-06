"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any
import copy
import sys
sys.setrecursionlimit(1500)


class GameTree:
    """
    An object representing a game with its children
    being the possible gamestates this game could go to based
    on the possible moves

    game: Game
    score: int
    children: List[GameTree]
    """

    def __init__(self, game: Any):
        self.children = []
        self.score = None
        self.game = game


def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def recursive_helper(game: Any) -> Any:
    """
    Recursively return -1 * the scores for the best possible moves

    """
    if game.is_over(game.current_state):
        if game.is_winner('p2') or game.is_winner('p1'):
            return -1
        return 0
    else:
        moves = game.current_state.get_possible_moves()[:]
        games_list = []
        for move in moves:
            g = copy.deepcopy(game)
            s = g.current_state.make_move(move)
            g.current_state = s
            games_list.append(g)
        return max([-1 * recursive_helper(c) for c in games_list])


def recursive_minimax(game: Any) -> Any:
    """
    Recursively return the best possible move for game
    """
    moves_scores = []
    moves = game.current_state.get_possible_moves()

    for move in moves:
        g = copy.deepcopy(game)
        s = g.current_state.make_move(move)
        g.current_state = s

        moves_scores.append(-1*recursive_helper(g))
    return moves[moves_scores.index(max(moves_scores))]


def iterative_minimax(game: Any):
    """
    Return a move using the the iterative minimax strategy
    """
    moves_scores = []
    moves = game.current_state.get_possible_moves()

    for move in moves:
        g = copy.deepcopy(game)
        s = g.current_state.make_move(move)
        g.current_state = s

        moves_scores.append(-1*iterative_helper(g))

    return moves[moves_scores.index(max(moves_scores))]


def iterative_helper(game: Any) -> Any:
    """
    Return the scores of the states reachable from game

    """
    s = []
    gt = GameTree(game)
    s.append(gt)

    while gt.score is None:
        curr_game = s[len(s)-1]

        if curr_game.game.is_over(curr_game.game.current_state):
            if curr_game.game.is_winner('p2') or curr_game.game.is_winner('p1'):
                curr_game.score = -1
            else:
                curr_game.score = 0
            s.pop()

        elif curr_game.children == []:
            moves = curr_game.game.current_state.get_possible_moves()[:]
            s.append(curr_game)
            for move in moves:
                g = copy.deepcopy(curr_game.game)
                s1 = g.current_state.make_move(move)
                g.current_state = s1
                gt1 = GameTree(g)
                curr_game.children.append(gt1)
                s.append(gt1)

        else:
            curr_game.score = max([-1*g.score for g in curr_game.children])
            s.pop()

    return gt.score


def rough_outcome_strategy(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2  # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
