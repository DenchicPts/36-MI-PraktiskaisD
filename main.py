from cProfile import label
from tkinter import *

CHOOSING_NUMBER = 0
INVALID_NUMBER = 0

root = Tk()
root.title("Spēle")

canvas = Canvas(root, width=200, height=20)
canvas.pack()

def two_players():
    label = Label(root, text="Choose a number between 5 and 15", font=("Arial", 12))
    label.pack(pady=15)

    spinbox = Spinbox(root, from_=5, to=15, width=5, font=("Arial", 15)) #, command=lambda: print(spinbox.get())
    spinbox.pack()  

    button = Button(root, text="Start Game", width=8, command=lambda: print(spinbox.get())) 
    button.pack(pady=10)    

def start_game(num):  
    # Check if number is valid
    invalid_num_label = Label(root, text="Invalid number", font=("Arial", 12), fg="red")
    if int(num) < 5 or int(num) > 15:
        global INVALID_NUMBER
        if INVALID_NUMBER:
            return
        INVALID_NUMBER = 1
        invalid_num_label.pack(pady=15)
        return
    
    INVALID_NUMBER = 0
    invalid_num_label.config(text="") # Remove invalid number label if it exists

    current_number_label = Label(root, text="Current number: " + str(num), font=("Arial", 12))
    current_number_label.pack(pady=15)

    player1_score_label = Label(root, text="Player 1: 0", font=("Arial", 12))
    player1_score_label.pack(pady=5)

    computer_score_label = Label(root, text="Computer: 0", font=("Arial", 12))
    computer_score_label.pack(pady=5)

    turn_label = Label(root, text="Turn: Player 1", font=("Arial", 12))
    turn_label.pack(pady=15)

    move_label = Label(root, text="Player 1, multiply by 2 or 3", font=("Arial", 12))
    move_label.pack(pady=5)

    choose_multiply_spinbox = Spinbox(root, values=(2, 3), width=5, font=("Arial", 15)) #, command=lambda: print(choose_multiply_spinbox.get())
    choose_multiply_spinbox.pack()

    button = Button(root, text="Make Move", width=10, command=lambda: print(choose_multiply_spinbox.get()))
    button.pack(pady=10)

    calc_label = Label(root, text=str(num) + " x " + str(choose_multiply_spinbox.get()) + " = " + str(int(num) * int(choose_multiply_spinbox.get())), font=("Arial", 12))
    calc_label.pack(pady=15)

def choose_number():    
    global CHOOSING_NUMBER
    if CHOOSING_NUMBER:
        return
    CHOOSING_NUMBER = 1

    label = Label(root, text="Choose a number between 5 and 15", font=("Arial", 12))
    label.pack(pady=15)

    spinbox = Spinbox(root, from_=5, to=15, width=5, font=("Arial", 15)) #, command=lambda: print(spinbox.get())
    spinbox.pack()  

    button = Button(root, text="Start Game", width=8, command=lambda: start_game(spinbox.get())) 
    button.pack(pady=10)

def vs_computer():
    label = Label(root, text="Choose algorithm:", font=("Arial", 12))
    label.pack(pady=15)

    button = Button(root, text="Minimax", width=10, command=choose_number)
    button.pack(pady=5)

    button = Button(root, text="Alpha-Beta", width=10, command=choose_number)
    button.pack(pady=5)


button = Button(root, text="Two Players", width=10, command=root.destroy)
button.pack(pady=10)

button = Button(root, text="vs Computer", width=10, command=vs_computer)
button.pack(pady=10)



# def start_game(selected_number):
#     # Šeit varētu ievietot spēles loģiku, kas tiks izpildīta pēc tam, kad spēlētājs izvēlēsies skaitli un nospiedīs "Start Game" pogu.
#     # canvas = Canvas(root, width=200, height=70)
#     # canvas.pack()
#     label = Label(root, text=f"Selected number: {selected_number}", font=("Arial", 12))
#     label.pack(pady=15)

# button = Button(root, text="Start Game", width=8, command=lambda: start_game(spinbox.get()))
# button.pack(pady=10)

# selected_number_label = Label(root, text=f"Selected number: {spinbox.get()}", font=("Arial", 12))
# selected_number_label.pack(pady=15)


root.mainloop()


# Spēles sākumā spēlētājs izvēlas skaitli diapazonā no 5 līdz 15, ar kuru sākas spēle.

# Spēles apraksts

# Spēles sākumā ir dots spēlētāja izvēlētais skaitlis. Abiem spēlētājiem ir 0 punkti.

# Spēlētāji veic gājienus pēc kārtas, reizinot pašreizējo skaitli ar 2 vai ar 3.

# Ja reizināšanas rezultātā iegūts pāra skaitlis, spēlētājs saņem 1 punktu.

# Ja iegūts nepāra skaitlis, spēlētājam tiek atņemts 1 punkts.


# Papildu noteikumi

# 1. Ja pēc gājiena skaitļa paritāte sakrīt ar iepriekšējā gājiena skaitļa paritāti
# (tas ir, divas reizes pēc kārtas iegūts pāra vai nepāra skaitlis), tad no iegūtā skaitļa tiek atņemts 1.

# 2. Ja pēc šīs atņemšanas iegūtais skaitlis dalās ar 5 vai ar 7 bez atlikuma, spēlētājam papildus tiek atņemti 2 punkti.

# Pēc visu noteikumu izpildes spēle turpinās ar jauno skaitli.

# Spēles beigas

# Spēle beidzas, kad iegūtais skaitlis kļūst lielāks vai vienāds ar 1000.

# Uzvar spēlētājs ar mazāko punktu skaitu.
# Ja punktu skaits ir vienāds, rezultāts ir neizšķirts.