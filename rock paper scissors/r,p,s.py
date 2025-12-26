from tkinter import *
from tkinter import colorchooser
import random
import time

global ai
ai = random.choice(["Rock", "Scissors", "Paper"])

window = Tk()
window.geometry("700x500")
window.config(bg="#1E1E2E")  # Deep modern navy background

rock_img = PhotoImage(file="Projects/rock paper scissors/Rock-Flat--Streamline-Fluent-Emoji.png")
paper_img = PhotoImage(file="Projects/rock paper scissors/Scroll--Streamline-Emoji (1).png")
scissors_img = PhotoImage(file="Projects/rock paper scissors/Scissors--Streamline-Kawaii-Emoji.png")
global scores
scores = 0

def color():
    global bg_color
    bg_color = colorchooser.askcolor()
    window.config(bg=bg_color[1])
    label_bg.config(bg=bg_color[1])

# Change Color button — warm golden theme
button_color = Button(window, text="Change Color", width=15, font=("QilkaBold", 10),
                      command=color, bg="#FFD166", activebackground="#FFE29A", relief="groove")
button_color.place(x=10, y=10)

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)

label_rock = Label(window, image=rock_img, padx=5, pady=5, bg="#1E1E2E")
label_rock.grid(row=0, column=0, pady=(200, 5))
label_paper = Label(window, image=paper_img, padx=5, pady=5, bg="#1E1E2E")
label_paper.grid(row=0, column=1, pady=(200, 5))
label_scissors = Label(window, image=scissors_img, bg="#1E1E2E")
label_scissors.grid(row=0, column=2, pady=(200, 5))

label_bg = Label(window, width=60, height=10, bg="#355070")  # Muted slate blue bg
label_bg.place(x=150, y=100)

label_scores = Label(window, text=f"Scores: {scores}", font=("QilkaBold", 25), fg="#FFD166", bg="#1E1E2E")
label_scores.place(x=270, y=10, anchor=NW)

def rock():
    user = "Rock"
    if user == ai:
        label_win = Label(window, text="Its a Draw", font=("QilkaBold", 35), fg="#06D6A0", bg="#1E1E2E")  # Mint green win text
        label_win.place(x=260, y=125, anchor=NW)
    elif ai == "Scissors":
        label_win = Label(window, text="You Win", font=("QilkaBold", 35), fg="#06D6A0", bg="#1E1E2E")  # Mint green win text
        label_win.place(x=260, y=125, anchor=NW)
        global scores
        scores += 1
    else:
        label_win = Label(window, text="You Lost", font=("QilkaBold", 35), fg="#EF476F", bg="#1E1E2E")
        label_win.place(x=260, y=125, anchor=NW)
        if scores > 0:
            scores -= 1

    Label(window, text=f"AI: {ai}", font=("QilkaBold", 20), fg="white", bg="#1E1E2E").place(x=155, y=210)
    Label(window, text=f"You: {user}", font=("QilkaBold", 20), fg="white", bg="#1E1E2E").place(x=437, y=210)
    button_rock.config(state=DISABLED)
    button_paper.config(state=DISABLED)
    button_scissors.config(state=DISABLED)
    global label_scores
    label_scores.config(text=f"Scores: {scores}")
    # Add "Play Again" button
    window.update()
    time.sleep(1)
    global play_again_btn
    play_again_btn = Button(window, text="Play Again", font=("QilkaBold", 15),
                                bg="#06D6A0", activebackground="#8BE9B3", command=reset)
    play_again_btn.place(x=290, y=450)

def scissors():
    user = "Scissors"
    if user == ai:
        label_win = Label(window, text="Its a Draw", font=("QilkaBold", 35), fg="#06D6A0", bg="#1E1E2E")  # Mint green win text
        label_win.place(x=260, y=125, anchor=NW)
    elif ai == "Paper":
        label_win = Label(window, text="You Win", font=("QilkaBold", 35), fg="#06D6A0", bg="#1E1E2E")  # Mint green win text
        label_win.place(x=260, y=125, anchor=NW)
        global scores
        scores += 1
    else:
        label_win = Label(window, text="You Lost", font=("QilkaBold", 35), fg="#EF476F", bg="#1E1E2E")
        label_win.place(x=260, y=125, anchor=NW)
        if scores > 0:
            scores -= 1

    Label(window, text=f"AI: {ai}", font=("QilkaBold", 20), fg="white", bg="#1E1E2E").place(x=155, y=210)
    Label(window, text=f"You: {user}", font=("QilkaBold", 20), fg="white", bg="#1E1E2E").place(x=388, y=210)
    button_rock.config(state=DISABLED)
    button_paper.config(state=DISABLED)
    button_scissors.config(state=DISABLED)
    global label_scores
    label_scores.config(text=f"Scores: {scores}")
    # Add "Play Again" button
    window.update()
    time.sleep(1)
    global play_again_btn
    play_again_btn = Button(window, text="Play Again", font=("QilkaBold", 15),
                                bg="#06D6A0", activebackground="#8BE9B3", command=reset)
    play_again_btn.place(x=290, y=450)

def paper():
    user = "Paper"
    if user == ai:
        label_win = Label(window, text="Its a Draw", font=("QilkaBold", 35), fg="#06D6A0", bg="#1E1E2E")  # Mint green win text
        label_win.place(x=260, y=125, anchor=NW)
    elif ai == "Rock":
        label_win = Label(window, text="You Win", font=("QilkaBold", 35), fg="#06D6A0", bg="#1E1E2E")  # Mint green win text
        label_win.place(x=260, y=125, anchor=NW)
        global scores
        scores += 1
    else:
        label_win = Label(window, text="You Lost", font=("QilkaBold", 35), fg="#EF476F", bg="#1E1E2E")
        label_win.place(x=260, y=125, anchor=NW)
        if scores > 0:
            scores -= 1

    Label(window, text=f"AI: {ai}", font=("QilkaBold", 20), fg="white", bg="#1E1E2E").place(x=155, y=210)
    Label(window, text=f"You: {user}", font=("QilkaBold", 20), fg="white", bg="#1E1E2E").place(x=423, y=210)
    button_rock.config(state=DISABLED)
    button_paper.config(state=DISABLED)
    button_scissors.config(state=DISABLED)
    global label_scores
    label_scores.config(text=f"Scores: {scores}")
    # Add "Play Again" button
    window.update()
    time.sleep(1)
    global play_again_btn
    play_again_btn = Button(window, text="Play Again", font=("QilkaBold", 15),
                                bg="#06D6A0", activebackground="#8BE9B3", command=reset)
    play_again_btn.place(x=290, y=450)

def reset():
    play_again_btn.destroy()
    global ai
    ai = random.choice(["Rock", "Scissors", "Paper"])

    # Clear the text labels
    for widget in window.place_slaves():
        # Remove dynamically placed result labels (not the green bg)
        if isinstance(widget, Label) and widget not in [label_bg] and widget not in [label_scores]:
            widget.destroy()

    # Re-enable buttons
    button_rock.config(state=NORMAL)
    button_paper.config(state=(NORMAL))
    button_scissors.config(state=(NORMAL))

# === LEARNING NOTES ===
# isinstance(obj, Type) → checks if obj is of given type/class
# like isinstance(5,int) returns True
# widget.destroy() → deletes that widget from window
# widget.place_slaves() → returns list of all widgets placed inside using .place()
# widget.pack_slaves() / widget.grid_slaves() → same idea for pack/grid layouts
# Tk(), Frame(), Canvas(), Toplevel() → containers that can hold other widgets
# for w in parent.place_slaves(): → loop through all child widgets
# if isinstance(w, Label): → target only label widgets
# w.destroy() → safely remove them
# global ai → use global variable across functions
# random.choice(list) → pick random element (used for AI move)
# button.config(state=NORMAL) → re-enable button
# .place(x=?, y=?) → manually position widget
# .config(bg=..., fg=...) → change widget colors

# Buttons — rich orange-gold tone for energy and balance
button_rock = Button(window, text="Rock", font=("QilkaBold", 15), activebackground="#06D6A0",
                     bg="#FFD166", width=8, border=3, relief="solid", command=rock)
button_rock.grid(row=0, column=0, pady=(400, 5))

button_paper = Button(window, text="Paper", font=("QilkaBold", 15), activebackground="#06D6A0",
                      bg="#FFD166", width=8, border=3, relief="solid", command=paper)
button_paper.grid(row=0, column=1, pady=(400, 5))

button_scissors = Button(window, text="Scissors", font=("QilkaBold", 15), activebackground="#06D6A0",
                         bg="#FFD166", width=8, border=3, relief="solid", command=scissors)
button_scissors.grid(row=0, column=2, pady=(400, 5))

print(isinstance(5, int))
window.mainloop()
