import tkinter as tk
from tkinter import font as tkfont
from logica.math import GameState
from logica.config import WIN_THRESHOLD, START_NUMBER_MIN, START_NUMBER_MAX
from logica import tree_display 

# ── helpers ──────────────────────────────────────────────────────────────────

def clear(root):
    for w in root.winfo_children():
        w.destroy()

def make_title(root, text):
    tk.Label(root, text=text, font=("Georgia", 18, "bold"), pady=12).pack()

def make_label(root, text, font=("Arial", 12), **kw):
    return tk.Label(root, text=text, font=font, **kw)

def make_button(root, text, cmd, width=16):
    return tk.Button(root, text=text, command=cmd, width=width,
                     font=("Arial", 11), relief="groove", pady=4)
 
# ── screens ───────────────────────────────────────────────────────────────────

def screen_home(root):
    clear(root)
    make_title(root, "Number Game")
    make_label(root, "Choose game mode:").pack(pady=(10, 4))
    make_button(root, "Two Players",  lambda: screen_start(root, mode=1)).pack(pady=4)
    make_button(root, "vs Computer",  lambda: screen_algo(root)).pack(pady=4)

def screen_algo(root):
    clear(root)
    make_title(root, "Choose Algorithm")
    make_button(root, "Minimax",     lambda: screen_start(root, mode=2, algo=1)).pack(pady=4)
    make_button(root, "Alpha-Beta",  lambda: screen_start(root, mode=2, algo=2)).pack(pady=4)
    make_button(root, "← Back",      lambda: screen_home(root), width=8).pack(pady=(12, 0))

def screen_start(root, mode: int, algo: int = 0):
    clear(root)
    make_title(root, "Choose Starting Number")

    make_label(root, f"Pick a number ({START_NUMBER_MIN}–{START_NUMBER_MAX}):").pack(pady=(8, 4))
    spin = tk.Spinbox(root, from_=START_NUMBER_MIN, to=START_NUMBER_MAX,
                      width=5, font=("Arial", 14), justify="center")
    spin.pack()

    err = make_label(root, "", fg="red")
    err.pack()

    def on_start():
        try:
            n = int(spin.get())
        except ValueError:
            err.config(text="Enter a whole number.")
            return
        if not (START_NUMBER_MIN <= n <= START_NUMBER_MAX):
            err.config(text=f"Must be {START_NUMBER_MIN}–{START_NUMBER_MAX}.")
            return
        state = GameState(mode=mode, algo_choice=algo, number=n)
        screen_game(root, state)

    make_button(root, "Start Game", on_start).pack(pady=8)
    make_button(root, "← Back",
                lambda: screen_home(root) if mode == 1 else screen_algo(root),
                width=8).pack()

# ── game screen ───────────────────────────────────────────────────────────────

def screen_game(root, state: GameState):
    clear(root)

    # — status bar —
    num_var   = tk.StringVar()
    score_var = tk.StringVar()
    turn_var  = tk.StringVar()
    inv_var   = tk.StringVar()
    log_var   = tk.StringVar()

    tk.Label(root, textvariable=num_var,   font=("Arial", 20, "bold")).pack(pady=(12, 0))
    tk.Label(root, textvariable=inv_var,   font=("Arial", 10), fg="orange").pack()
    tk.Label(root, textvariable=score_var, font=("Arial", 12)).pack(pady=2)
    tk.Label(root, textvariable=turn_var,  font=("Arial", 12, "italic")).pack()

    tk.Frame(root, height=1, bg="#ccc").pack(fill="x", padx=20, pady=8)

    # — move log —
    log_frame = tk.Frame(root)
    log_frame.pack(padx=16, fill="x")
    tk.Label(log_frame, textvariable=log_var, font=("Courier", 10),
             justify="left", anchor="w", fg="#555").pack(fill="x")

    tk.Frame(root, height=1, bg="#ccc").pack(fill="x", padx=20, pady=8)

    # — move controls —
    ctrl = tk.Frame(root)
    ctrl.pack(pady=4)

    spin_label = tk.Label(ctrl, text="Multiply by:", font=("Arial", 11))
    spin_label.grid(row=0, column=0, padx=4)

    mult_spin = tk.Spinbox(ctrl, values=(2, 3), width=4,
                           font=("Arial", 13), justify="center", state="readonly")
    mult_spin.grid(row=0, column=1, padx=4)

    move_btn = tk.Button(ctrl, text="Make Move", font=("Arial", 11),
                         relief="groove", pady=3)
    move_btn.grid(row=0, column=2, padx=8)

    def refresh():
        num_var.set(f"Current number: {state.number}")
        score_var.set(f"{state.names[0]}: {state.scores[0]} pts  |  "
                      f"{state.names[1]}: {state.scores[1]} pts")
        turn_var.set(f"Turn: {state.names[state.turn]}")
        inv_var.set("⚠ Your rules are INVERTED" if state.inverted else "")

    def show_log(lines):
        log_var.set("\n".join(lines))

    def do_move(mult: int):
        log = state.apply(mult)
        show_log(log)
        if state.finished:
            # disable controls, show result after a short delay
            move_btn.config(state="disabled")
            mult_spin.config(state="disabled")
            root.after(900, lambda: screen_result(root, state))
            return
        refresh()
        # if it's now the computer's turn, schedule it
        if state.is_computer_turn():
            move_btn.config(state="disabled")
            mult_spin.config(state="disabled")
            root.after(600, computer_turn)

    def computer_turn():
        mult, _ = state.computer_move()
        show_log([f"Computer picks: ×{mult}"])
        do_move(mult)
        move_btn.config(state="normal")
        mult_spin.config(state="readonly")

    move_btn.config(command=lambda: do_move(int(mult_spin.get())))

    # hide controls on computer turn
    if state.is_computer_turn():
        spin_label.grid_remove()
        mult_spin.grid_remove()
        move_btn.config(text="Computer thinking…", state="disabled")
        root.after(600, computer_turn)

    refresh()

# ── result screen ─────────────────────────────────────────────────────────────

def screen_result(root, state: GameState):
    clear(root)
    make_title(root, "Game Over")

    make_label(root, f"Final number: {state.number}").pack(pady=4)
    make_label(root, f"{state.names[0]}: {state.scores[0]} pts  |  "
                     f"{state.names[1]}: {state.scores[1]} pts").pack(pady=4)

    w = state.winner()
    result_text = "It's a draw!" if w is None else f"{state.names[w]} wins!"
    make_label(root, result_text, font=("Arial", 14, "bold")).pack(pady=8)

    if state.mode == 2:
        avg_ai_time = state.total_ai_time / state.move_number if state.move_number > 0 else 0.0
        make_label(root, "Computer search totals:", font=("Arial", 12, "bold")).pack(pady=(6, 2))
        make_label(root, f"Generated nodes: {state.total_generated}").pack()
        make_label(root, f"Evaluated nodes: {state.total_evaluated}").pack()
        make_label(root, f"Average move time: {avg_ai_time * 1000:.3f} ms").pack(pady=(0, 6))

    if state.mode == 2 and state.all_trees:
        make_button(root, "Show AI Trees",
                    lambda: tree_display.print_all_trees(state.all_trees, state.algo_name)
                    ).pack(pady=4)

    make_button(root, "Play Again", lambda: screen_home(root)).pack(pady=4)

# ── entry point ───────────────────────────────────────────────────────────────

def launch():
    root = tk.Tk()
    root.title("Number Game")
    root.geometry("720x420")
    root.resizable(False, False)
    screen_home(root)
    root.mainloop()

if __name__ == "__main__":
    launch()
