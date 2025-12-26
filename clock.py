from tkinter import *
from time import *

def update():
    label_time= strftime("%I:%M:%S %p")
    clock_label.config(text=label_time)
    date= strftime("%B %d, %Y")
    date_label.config(text=date)
    day= strftime("%A")
    day_label.config(text=day)
    window.after(1,update)

window= Tk()
window.geometry("500x500")
clock_label= Label(window,font=("Arial",50),bg="black",fg="red")
clock_label.pack()
date_label= Label(window,font=("Arial",30),fg="black")
date_label.pack()
day_label= Label(window,font=("Arial",35),fg="black")
day_label.pack()

update()

window.mainloop()