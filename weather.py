import requests
import os
import dotenv
from tkinter import *

dotenv.load_dotenv()
api_key = os.getenv("weather_api")
base_url = "http://api.weatherapi.com/v1/current.json"

def get(city):
    url= f"{base_url}?key={api_key}&q={city}"
    response=requests.get(url)
    if response.status_code == 200:
        global weather_data
        weather_data= response.json()
        global t
        t=IntVar()
        check_box1.config(state=ACTIVE,command=temp,onvalue=1,offvalue=0,variable=t)
        global h
        h=IntVar()
        check_box2.config(state=ACTIVE,command=hum,onvalue=1,offvalue=0,variable=h)
        global c
        c=IntVar()
        check_box3.config(state=ACTIVE,command=con,onvalue=1,offvalue=0,variable=c)
        global uv
        uv=IntVar()
        check_box4.config(state=ACTIVE,command=uv_index,onvalue=1,offvalue=0,variable=uv)
    else:
        label_error= Label(window,text="Error",font=("Arial",20,"bold"),fg="#ef4444",bg="#0f172a")
        label_error.place(x=400,y=340)
        window.after(2000,label_error.destroy) # Pass function reference (no parentheses) so it runs after the delay
        window.update()

def temp():
    if t.get()==1:
     global label_temp
     label_temp= Label(window,font=("Arial",20,"bold"),fg="#22c55e",bg="#0f172a",text=f"{weather_data['current']['temp_c']} C")
     label_temp.place(x=300,y=123)
    elif t.get()==0:
     label_temp.destroy()

def hum():
    if h.get()==1:
     global label_hum
     label_hum= Label(window,font=("Arial",20,"bold"),fg="#22c55e",bg="#0f172a",text=f"{weather_data['current']['humidity']} %")
     label_hum.place(x=300,y=173)
    elif h.get()==0:
     label_hum.destroy()

def con():
    if c.get()==1:
     global label_con
     label_con= Label(window,font=("Arial",20,"bold"),fg="#22c55e",bg="#0f172a",text=f"{weather_data['current']['condition']['text']}")
     label_con.place(x=300,y=223)
    elif c.get()==0:
     label_con.destroy()

def uv_index():
    if uv.get()==1:
     global label_uv
     label_uv= Label(window,font=("Arial",20,"bold"),fg="#22c55e",bg="#0f172a",text=f"Index: {weather_data['current']['uv']}")
     label_uv.place(x=300,y=273)
    elif uv.get()==0:
     label_uv.destroy()

def input():
    global city_name
    city_name= entry_label.get()
    get(city_name)
    try:
     label_con.destroy()
     label_hum.destroy()
     label_temp.destroy()
     label_uv.destroy()
    except:
     pass

window= Tk()
window.geometry("500x400")
window.configure(bg="#0f172a")

entry_label= Entry(window,font=("Arial",15),bg="#1e293b",fg="#e5e7eb",insertbackground="#e5e7eb")
entry_label.place(x=100,y=350)

button_1= Button(window,text="Submit",bg="#22c55e",fg="black",activebackground="#16a34a",activeforeground="black",relief=SUNKEN,command=input)
button_1.place(x=330,y=350)

label_1= Label(window, text="Weather App",font=("Arial",35,"bold"),fg="#22c55e",bg="#0f172a")
label_1.place(x=100,y=30)

check_box1= Checkbutton(window,text="Temperature",font=("Arial",20,"bold"),bg="#0f172a",fg="#e5e7eb",selectcolor="#1e293b",activebackground="#0f172a",activeforeground="#e5e7eb",state=DISABLED)
check_box1.place(x=50,y=120)

check_box2= Checkbutton(window,text="Humidity",font=("Arial",20,"bold"),bg="#0f172a",fg="#e5e7eb",selectcolor="#1e293b",activebackground="#0f172a",activeforeground="#e5e7eb",state=DISABLED)
check_box2.place(x=50,y=170)

check_box3= Checkbutton(window,text="Condition",font=("Arial",20,"bold"),bg="#0f172a",fg="#e5e7eb",selectcolor="#1e293b",activebackground="#0f172a",activeforeground="#e5e7eb",state=DISABLED)
check_box3.place(x=50,y=220)

check_box4= Checkbutton(window,text="UV Index",font=("Arial",20,"bold"),bg="#0f172a",fg="#e5e7eb",selectcolor="#1e293b",activebackground="#0f172a",activeforeground="#e5e7eb",state=DISABLED)
check_box4.place(x=50,y=270)

window.mainloop()
