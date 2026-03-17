from tkinter import *

root = Tk()
root.title("Spēle")

canvas = Canvas(root, width=200, height=20)
canvas.pack()

label = Label(root, text="Choose a number between 5 and 15", font=("Arial", 12))
label.pack(pady=15)

spinbox = Spinbox(root, from_=5, to=15, width=5, font=("Arial", 15)) #, command=lambda: print(spinbox.get())
spinbox.pack()

# def start_game(selected_number):
#     # Šeit varētu ievietot spēles loģiku, kas tiks izpildīta pēc tam, kad spēlētājs izvēlēsies skaitli un nospiedīs "Start Game" pogu.
#     # canvas = Canvas(root, width=200, height=70)
#     # canvas.pack()
#     label = Label(root, text=f"Selected number: {selected_number}", font=("Arial", 12))
#     label.pack(pady=15)

button = Button(root, text="Start Game", width=8, command=lambda: start_game(spinbox.get()))
button.pack(pady=10)

selected_number_label = Label(root, text=f"Selected number: {spinbox.get()}", font=("Arial", 12))
selected_number_label.pack(pady=15)


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