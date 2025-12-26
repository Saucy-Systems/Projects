from tkinter import *
from tkinter import colorchooser
import random
import time

def restart():
 
 def color():
    color_select= colorchooser.askcolor()
    window.config(bg=color_select[1])
    label1.config(bg=color_select[1])

 def check():
    try:
     if int(entry.get()) < num:
         labelhigh= Label(window, text="The Number is Higher",bg="orange",fg="black",font=("komika axis",13))
         labelhigh.place(x=325,y=420)
         window.update()
         time.sleep(1)
         labelhigh.destroy()
     elif int(entry.get()) > num:
         labellow= Label(window, text="The Number is Lower",bg="orange",fg="black",font=("komika axis",13))
         labellow.place(x=325,y=420)
         window.update()
         time.sleep(1)
         labellow.destroy()
     else:
         label3= Label(window, text="You Guessed it! \n ",bg="orange",fg="black",font=("komika axis",23))
         label3.place(x=297,y=220)
         labelwin= Label(window, text=str(num),bg="orange",fg="black",font=("komika axis",50))
         labelwin.place(x=380,y=310)
         for i in range(10):
            colors_list= colors = ["red","blue","green","yellow","purple","pink","brown","black","white","gray"
                                   ,"cyan","magenta","gold","silver","beige","maroon","navy","lime","teal"]
            labelwin.config(fg=random.choice(colors_list))
            window.update()
            time.sleep(1)

    except:
         label3= Label(window, text="Please Enter A String",bg="orange",fg="black",font=("komika axis",13))
         label3.place(x=325,y=420)
         window.update()
         time.sleep(1)
         label3.destroy()

 def set_range():
    global num
    try:
     start= int(entrystart.get())
     end= int(entryend.get())
     num= random.randint(start,end+1)
    except:
     labelerror= Label(window, text="PLease enter\n both numbers",bg="lime",fg="black",font=("komika axis",8))
     labelerror.place(x=650,y=130)
     window.update()
     time.sleep(1)
     labelerror.destroy()
       
 window = Tk()
 window.geometry("800x700")

 num= random.randint(1,100)

 button1 = Button(window, text="Change Background", width=20,activebackground="lime",command=color)
 button1.place(x=10,y=10)
 label= Label(window,bg="orange",height=20,width=50)
 label.place(x=250,y=150)
 label1= Label(window,text="Guess the Number",font=("Komika axis",30))
 label1.place(x=230,y=100)
 entry= Entry(window,bg="cyan",width= 15,font=("Komika Axis",20))
 entry.place(x=290,y=465)
 button2= Button(window,text="Check",font=("Impact",20),activebackground="cyan",width=20,command=check)
 button2.place(x=300,y=520)
 entrystart= Entry(window,bg="yellow",font=("Komika Axis",11))
 entrystart.place(x=580,y=20)
 entryend= Entry(window,bg="yellow",font=("Komika Axis",11))
 entryend.place(x=580,y=60)
 labelstart= Label(window,text="Starting Range",font=("Komika axis",15))
 labelstart.place(x=390,y=10)
 labelend= Label(window,text="Ending Range",font=("Komika axis",15))
 labelend.place(x=410,y=50)
 button3= Button(window,text="Set",width=5,font=("Arial",10),activebackground="cyan",command=set_range)
 button3.place(x=720,y=95)
 buttonq= Button(window,text="Quit",font=("Minecraft",15),activebackground="cyan",command=quit)
 buttonq.place(x=30,y=600)
 buttonagain= Button(window,text="Play Again",font=("Minecraft",15),fg="White",bg="lime",command=restart)
 buttonagain.place(x=100,y=600)
 window.mainloop()
restart()



