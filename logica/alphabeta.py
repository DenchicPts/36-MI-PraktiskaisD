# Alpha-Beta pruning algorithm for AI decision making.
from logica.config import PENALTY_DIVISORS, PENALTY_AMOUNT, WIN_THRESHOLD


def _simulate(number, multiplier, prev_was_even, inverted):
    """
    Simulate one move: apply multiplier, compute score change and inversion.
    Triggers inversion and penalty if two consecutive even results occur.

    Args:
        number (int): Current game number.
        multiplier (int): Multiplier to apply (2 or 3).
        prev_was_even (bool): Whether the previous result was even.
        inverted (bool): Whether scoring direction is flipped.

    Returns:
        result (int): New number after the move.
        score_change (int): Score delta for the current player.
        next_inverted (bool): Whether inversion is active on the next turn.
    """
    result = number * multiplier
    is_even = result % 2 == 0

    raw_score = 1 if is_even else -1
    score_change = raw_score if not inverted else -raw_score

    next_inverted = False
    if is_even and prev_was_even:
        result -= 1
        next_inverted = True
        if any(result % d == 0 for d in PENALTY_DIVISORS):
            score_change -= PENALTY_AMOUNT

    return result, score_change, next_inverted


def _run(number, prev_was_even, inverted, scores, depth, max_depth, is_ai_turn, alpha, beta, tree_log, parent_id, stats):
    """
    Alpha-beta minimax: AI maximizes score difference, opponent minimizes it.
    Prunes branches when alpha >= beta. Stops at WIN_THRESHOLD or max_depth.
    Logs all nodes to tree_log.

    Args:
        number (int): Current game number.
        prev_was_even (bool): Whether the previous result was even.
        inverted (bool): Whether scoring is currently inverted.
        scores (list[int]): Current scores as [ai_score, opponent_score].
        depth (int): Current recursion depth.
        max_depth (int): Maximum search depth.
        is_ai_turn (bool): True if it is the AI's turn.
        alpha (int | None): Best score the AI can guarantee so far.
        beta (int | None): Best score the opponent can guarantee so far.
        tree_log (list[dict]): Shared log of all visited nodes.
        parent_id (int | None): Parent node index in tree_log.

    Returns:
        best_diff (int): Best achievable score difference.
        best_mult (int | None): Best multiplier (2 or 3), or None at terminal nodes.
    """
    if number >= WIN_THRESHOLD or depth == max_depth:
        stats["evaluated"] += 1
        return scores[0] - scores[1], None

    best_mult = None
    best_node_id = None

    for mult in (2, 3):
        result, sc, next_inv = _simulate(number, mult, prev_was_even, inverted)
        stats["generated"] += 1

        new_scores = scores[:]
        new_scores[0 if is_ai_turn else 1] += sc

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
            alpha, beta, tree_log, node_id, stats,
        )

        if is_ai_turn:
            if alpha is None or future_diff > alpha:
                alpha, best_mult, best_node_id = future_diff, mult, node_id
            if beta is not None and alpha >= beta:
                tree_log[-1]["pruned"] = True
                break
        else:
            if beta is None or future_diff < beta:
                beta, best_mult, best_node_id = future_diff, mult, node_id
            if alpha is not None and beta <= alpha:
                tree_log[-1]["pruned"] = True
                break

    if best_node_id is not None:
        tree_log[best_node_id]["chosen"] = True

    return (alpha if is_ai_turn else beta) or 0, best_mult


def pick(number, prev_was_even, inverted, ai_score, opp_score, tree_log, max_depth):
    """
    Entry point for the AI move. Returns the best multiplier (2 or 3).

    Args:
        number (int): Current game number.
        prev_was_even (bool): Whether the previous result was even.
        inverted (bool): Whether scoring is currently inverted.
        ai_score (int): Current AI score.
        opp_score (int): Current opponent score.
        tree_log (list[dict]): Log for the explored game tree.
        max_depth (int): Maximum search depth.

    Returns:
        int: Chosen multiplier (2 or 3).
    """
    stats = {"generated": 0, "evaluated": 0}
    _, best_mult = _run(number, prev_was_even, inverted, [ai_score, opp_score], 0, max_depth, True, None, None, tree_log, None, stats)
    return best_mult or 2, stats