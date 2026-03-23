# AI configuration
# How many moves ahead the computer looks.
AI_SEARCH_DEPTH = 3

# Score the computer is trying to maximise: own_score - opponent_score.
# Positive = AI wants higher difference; negative = AI plays defensively.
AI_SCORE_WEIGHT = 1

# Game rules
# Number range the player can choose at game start.
START_NUMBER_MIN = 5
START_NUMBER_MAX = 15

# The game ends when the current number reaches or exceeds this value.
WIN_THRESHOLD = 1000

# Extra penalty applied when Rule 1 reduces the number to a
# value divisible by one of these divisors.
PENALTY_DIVISORS = (5, 7)
PENALTY_AMOUNT = 2

# Output
# File where the AI decision tree is saved after each vs-Computer game.
TREE_OUTPUT_FILE = "../tree_output.txt"
