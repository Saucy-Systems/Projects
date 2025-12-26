from tkinter import *
import random
from tkinter import colorchooser

colors = ["red", "blue", "green", "yellow", "orange","purple", "pink", "brown", "black", "white", "gold", "silver", "beige"]

def check():
    answer=entry.get().strip().lower()
    if answer==text_color:
        print("nice")
        new_word()
        entry.delete(0,END)
    else:
        print("try again")
        new_word()


def bg_color():
    background = colorchooser.askcolor()
    window.config(bg=background[1])
def lb_color():
    lb_background = colorchooser.askcolor()
    label.config(bg=lb_background[1])
def new_word():
    global text_color
    text_color=random.choice(colors)
    label.config(text=random.choice(colors),fg=text_color)

window = Tk()
window.geometry("500x500")

entry = Entry(window, font=("Impact",15),bg="cyan")
entry.place(x=140,y=400)
button1= Button(window,text="Sumbit",command=check)
button1.place(x=140,y=430)
label= Label(window,font=("bangers",45,"bold"),height=2,width=8,bg="grey")
label.place(x=120,y=100)
button2= Button(window,text="bg color",command=bg_color)
button2.place(x=10,y=10)
button3= Button(window,text="label color",command=lb_color)
button3.place(x=80,y=10)

new_word()

#def win():
  #  win= Tk()
 #   win.mainloop() #window inside window
#win()
#def sc():
# window.after(2000,new_word)
# window.after(5000,sc) automatically runs new word function. time is in milliseconds

#sc()


    
window.mainloop()