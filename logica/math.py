# All game logic lives here.
# main.py only calls run_game().

import minimax
import alphabeta
import tree_display
import time
from config import (
    AI_SEARCH_DEPTH,
    START_NUMBER_MIN, START_NUMBER_MAX,
    WIN_THRESHOLD,
    PENALTY_DIVISORS, PENALTY_AMOUNT,
)


# Input helpers

def _get_start_number():
    while True:
        try:
            n = int(input(f"Enter starting number ({START_NUMBER_MIN} to {START_NUMBER_MAX}): "))
            if START_NUMBER_MIN <= n <= START_NUMBER_MAX:
                return n
            print(f"Must be between {START_NUMBER_MIN} and {START_NUMBER_MAX}.")
        except ValueError:
            print("Enter an integer.")


def _get_mode():
    print("\n1 - Two players")
    print("2 - vs Computer")
    while True:
        choice = input("Choose (1 or 2): ").strip()
        if choice in ("1", "2"):
            return int(choice)
        print("Enter 1 or 2.")


def _get_algorithm():
    print("\n1 - Minimax")
    print("2 - Alpha-Beta pruning")
    while True:
        choice = input("Choose algorithm (1 or 2): ").strip()
        if choice in ("1", "2"):
            return int(choice)
        print("Enter 1 or 2.")


def _get_multiplier(player_name, number):
    while True:
        try:
            m = int(input(f"{player_name}, multiply {number} by (2 or 3): "))
            if m in (2, 3):
                return m
            print("Enter 2 or 3.")
        except ValueError:
            print("Enter 2 or 3.")


# Game logic

def apply_move(number, multiplier, prev_was_even, inverted):
    """Apply one move and return (result, score_change, next_inverted, log)."""
    result = number * multiplier
    log = []
    next_inverted = False

    parity = "even" if result % 2 == 0 else "odd"
    if not inverted:
        score_change = 1 if result % 2 == 0 else -1
        log.append(f"  {number} x{multiplier} = {result} ({parity}) -> {'+1' if score_change > 0 else '-1'}")
    else:
        score_change = 1 if result % 2 != 0 else -1
        log.append(f"  {number} x{multiplier} = {result} ({parity}) [INVERTED] -> {'+1' if score_change > 0 else '-1'}")

    if result % 2 == 0 and prev_was_even:
        result -= 1
        next_inverted = True
        log.append(f"  Two even in a row -> number reduced to {result}, next player rules INVERTED")
        if any(result % d == 0 for d in PENALTY_DIVISORS):
            score_change -= PENALTY_AMOUNT
            log.append(f"  {result} divisible by {' or '.join(str(d) for d in PENALTY_DIVISORS)} -> current player -{PENALTY_AMOUNT}")

    return result, score_change, next_inverted, log


def _determine_winner(scores):
    if scores[0] < scores[1]:
        return 1
    elif scores[1] < scores[0]:
        return 0
    return None

# def _determine_winner(scores):
#     if scores[0] < scores[1]:
#         return 1
#     elif scores[1] < scores[0]:
#         return 0
#     return None


# Main game loop

def run_game():
    print("=== NUMBER GAME ===")
    mode = _get_mode()

    algo = None
    algo_name = ""
    if mode == 2:
        algo_choice = _get_algorithm()
        if algo_choice == 1:
            algo = minimax
            algo_name = "Minimax"
        else:
            algo = alphabeta
            algo_name = "Alpha-Beta"

    number = _get_start_number()

    scores = [0, 0]
    prev_was_even = False
    inverted = False
    turn = 0
    names = ["Player 1", "Player 2" if mode == 1 else "Computer"]
    # Each computer turn gets its own tree: list of (move_number, tree_log)
    all_trees = []
    move_number = 0
    total_generated = 0
    total_evaluated = 0
    total_ai_time = 0.0

    while number < WIN_THRESHOLD:
        print(f"\n{'─' * 44}")
        print(f"Current number : {number}{' [YOUR RULES ARE INVERTED]' if inverted else ''}")
        print(f"{names[0]}: {scores[0]} pts  |  {names[1]}: {scores[1]} pts")
        print(f"Turn: {names[turn]}")

        if mode == 2 and turn == 1:
            move_number += 1
            turn_log = []
            start_time = time.perf_counter()
            mult, stats = algo.pick(number, prev_was_even, inverted, scores[1], scores[0], turn_log, AI_SEARCH_DEPTH)
            move_time = time.perf_counter() - start_time
            total_ai_time += move_time
            total_generated += stats["generated"]
            total_evaluated += stats["evaluated"]
            all_trees.append((move_number, number, turn_log))
            print(f"Computer picks: x{mult}")
            print(f"  Computer search nodes -> generated: {stats['generated']}, evaluated: {stats['evaluated']}")
            print(f"  Computer move time -> {move_time * 1000:.3f} ms")
        else:
            mult = _get_multiplier(names[turn], number)

        raw_result = number * mult
        result, sc, next_inverted, log = apply_move(number, mult, prev_was_even, inverted)

        for line in log:
            print(line)

        scores[turn] += sc
        print(f"  {names[turn]} total: {scores[turn]} pts")

        prev_was_even = raw_result % 2 == 0 and not next_inverted
        inverted = next_inverted
        number = result
        turn = 1 - turn

    print(f"\n{'=' * 44}")
    print(f"GAME OVER — final number: {number}")
    print(f"{names[0]}: {scores[0]} pts  |  {names[1]}: {scores[1]} pts")

    winner = _determine_winner(scores)
    if winner is None:
        print("Result: DRAW!")
    else:
        print(f"Winner: {names[winner]}!")

    if mode == 2:
        avg_ai_time = total_ai_time / move_number if move_number > 0 else 0.0
        print("Computer search totals:")
        print(f"  Generated nodes: {total_generated}")
        print(f"  Evaluated nodes: {total_evaluated}")
        print(f"  Average move time: {avg_ai_time * 1000:.3f} ms")

    if mode == 2 and all_trees:
        tree_display.print_all_trees(all_trees, algo_name)

        # Add this to the bottom of math.py, keeping everything else the same

class GameState:
    """Holds all mutable game state. Passed around instead of local variables."""
    def __init__(self, mode: int, algo_choice: int, number: int):
        from logica import minimax, alphabeta
        self.number = number
        self.mode = mode
        self.scores = [0, 0]
        self.prev_was_even = False
        self.inverted = False
        self.turn = 0
        self.names = ["Player 1", "Player 2" if mode == 1 else "Computer"]
        self.all_trees = []
        self.move_number = 0
        self.algo = minimax if algo_choice == 1 else alphabeta
        self.algo_name = "Minimax" if algo_choice == 1 else "Alpha-Beta"
        self.finished = False

    def is_computer_turn(self):
        return self.mode == 2 and self.turn == 1

    def apply(self, multiplier: int):
        """Apply a move and advance state. Returns the log lines."""
        raw = self.number * multiplier
        result, sc, next_inverted, log = apply_move(
            self.number, multiplier, self.prev_was_even, self.inverted
        )
        self.scores[self.turn] += sc
        self.prev_was_even = raw % 2 == 0 and not next_inverted
        self.inverted = next_inverted
        self.number = result
        self.turn = 1 - self.turn
        if self.number >= WIN_THRESHOLD:
            self.finished = True
        return log

    def computer_move(self):
        """Run the AI and return (multiplier, tree_log)."""
        self.move_number += 1
        turn_log = []
        mult = self.algo.pick(
            self.number, self.prev_was_even, self.inverted,
            self.scores[1], self.scores[0], turn_log, AI_SEARCH_DEPTH
        )
        self.all_trees.append((self.move_number, self.number, turn_log))
        return mult, turn_log

    def winner(self):
        return _determine_winner(self.scores)