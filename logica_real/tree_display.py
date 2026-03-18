# Tree rendering and file output.
# Used by game_math.py after a vs-Computer game.

from logica_real.config import TREE_OUTPUT_FILE


def _build_chosen_path(tree_log):
    children = {}
    for node in tree_log:
        pid = node["parent"]
        if pid not in children:
            children[pid] = []
        children[pid].append(node["id"])

    path_ids = set()

    def walk(node_id):
        path_ids.add(node_id)
        for kid_id in children.get(node_id, []):
            if tree_log[kid_id]["chosen"]:
                walk(kid_id)

    for root_id in children.get(None, []):
        if tree_log[root_id]["chosen"]:
            walk(root_id)

    return path_ids


def build_lines(tree_log):
    children = {}
    for node in tree_log:
        pid = node["parent"]
        if pid not in children:
            children[pid] = []
        children[pid].append(node["id"])

    path_ids = _build_chosen_path(tree_log)
    lines = []

    def draw(node_id, prefix, is_last):
        node = tree_log[node_id]
        connector = "└── " if is_last else "├── "
        if node_id in path_ids:
            marker = "*"
        elif node.get("pruned"):
            marker = "~"
        else:
            marker = " "
        turn = "AI " if node["is_ai"] else "OPP"
        lines.append(f"{prefix}{connector}[{turn}] {marker} {node['result']}")

        kids = children.get(node_id, [])
        for i, kid in enumerate(kids):
            extension = "    " if is_last else "│   "
            draw(kid, prefix + extension, i == len(kids) - 1)

    roots = children.get(None, [])
    for i, root_id in enumerate(roots):
        draw(root_id, "", i == len(roots) - 1)

    return lines


def print_all_trees(all_trees, algo_name):
    all_lines = []

    for move_num, from_number, tree_log in all_trees:
        header = f"Move {move_num}: Computer's turn (from {from_number})  [{algo_name}]"
        sep = "─" * len(header)
        lines = build_lines(tree_log)

        print(f"\n{sep}")
        print(header)
        print(f"  * chosen path   ~ pruned")
        print(sep)
        for line in lines:
            print(line)

        all_lines.append(f"\n{sep}")
        all_lines.append(header)
        all_lines.append(f"  * chosen path   ~ pruned")
        all_lines.append(sep)
        all_lines.extend(lines)

    _save_to_file(all_lines)


def _save_to_file(lines, filename=None):
    if filename is None:
        filename = TREE_OUTPUT_FILE
    with open(filename, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
    print(f"\n  All trees saved to: {filename}")