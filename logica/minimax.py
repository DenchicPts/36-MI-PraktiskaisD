# Minimax algorithm for AI decision making.

from config import PENALTY_DIVISORS, PENALTY_AMOUNT, WIN_THRESHOLD


def _simulate(number, multiplier, prev_was_even, inverted):
    result = number * multiplier
    next_inverted = False
    score_change = (1 if result % 2 == 0 else -1) if not inverted else (1 if result % 2 != 0 else -1)
    if result % 2 == 0 and prev_was_even:
        result -= 1
        next_inverted = True
        if any(result % d == 0 for d in PENALTY_DIVISORS):
            score_change -= PENALTY_AMOUNT
    return result, score_change, next_inverted


def _run(number, prev_was_even, inverted, scores, depth, max_depth, is_ai_turn, tree_log, parent_id):
    if number >= WIN_THRESHOLD or depth == max_depth:
        return scores[0] - scores[1], None

    best_diff = None
    best_mult = None
    best_node_id = None

    for mult in (2, 3):
        result, sc, next_inv = _simulate(number, mult, prev_was_even, inverted)
        new_scores = [scores[0] + (sc if is_ai_turn else 0),
                      scores[1] + (sc if not is_ai_turn else 0)]

        node_id = len(tree_log)
        tree_log.append({
            "id": node_id, "parent": parent_id,
            "result": result, "is_ai": is_ai_turn,
            "chosen": False, "pruned": False,
        })

        future_diff, _ = _run(
            result, result % 2 == 0 and not next_inv,
            next_inv, new_scores,
            depth + 1, max_depth, not is_ai_turn,
            tree_log, node_id
        )

        if is_ai_turn:
            if best_diff is None or future_diff > best_diff:
                best_diff, best_mult, best_node_id = future_diff, mult, node_id
        else:
            if best_diff is None or future_diff < best_diff:
                best_diff, best_mult, best_node_id = future_diff, mult, node_id

    if best_node_id is not None:
        tree_log[best_node_id]["chosen"] = True

    return best_diff, best_mult


def pick(number, prev_was_even, inverted, ai_score, opp_score, tree_log, max_depth):
    scores = [ai_score, opp_score]
    _, best_mult = _run(number, prev_was_even, inverted, scores, 0, max_depth, True, tree_log, None)
    return best_mult or 2