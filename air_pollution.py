
from tkinter import *
import requests

api_key="e021d86837e37e7c020dc4fbda895055ffa652f7"
base_url= "https://api.waqi.info/feed/"

def get(city):
    url=f"{base_url}{city}/?token={api_key}"
    response= requests.get(url)

    global data
    data= response.json()

    if response.status_code==200 and data["status"]=="error":
        label_error= Label(window,text="City not found. Please check the name.",font=("Arial",15),
                           bg="#020617",fg="#fca5a5")
        label_error.place(x=75,y=310)
        window.after(2000,label_error.destroy)

    elif response.status_code==429:
        label_error= Label(window,text="Too many Requests. Please Try again later.",font=("Arial",15),
                           bg="#020617",fg="#fca5a5")
        label_error.place(x=70,y=310)
        window.after(2000,label_error.destroy)

    elif response.status_code==500 or response.status_code==502:
        label_error= Label(window,text="Server unavailable. Try again later.",font=("Arial",15),
                           bg="#020617",fg="#fca5a5")
        label_error.place(x=75,y=310)
        window.after(2000,label_error.destroy)

    elif response.status_code==401:
        print("Invalid API key. Please check configuration")

    elif response.status_code==200 and data["status"]=="ok":
         result()
        
def result():
        
    global label_1
    label_1= Label(window,text=f"{data["data"]["aqi"]}",font=("Arial",20,"bold"),
                       bg="#020617",fg="#e5e7eb")
    label_1.place(x=135,y=100)

    if data["data"]["dominentpol"] == "pm25":
        pollutant="Fine particles"
    elif data["data"]["dominentpol"] == "pm10":
        pollutant="Coarse particles"
    elif data["data"]["dominentpol"] == "o3":
        pollutant="Ozone"
    elif data["data"]["dominentpol"] == "no2":
        pollutant="Nitrogen Dioxide"
    elif data["data"]["dominentpol"] == "so2":
        pollutant="Sulphur Dioxide"
    elif data["data"]["dominentpol"] == "co":
        pollutant="Carbon Monoxide"
    else:
        pollutant= data["data"]["dominentpol"]

    global label_2
    label_2= Label(window,text=f"{pollutant}",font=("Arial",20,"bold"),
                       bg="#020617",fg="#e5e7eb")
    label_2.place(x=275,y=150)

    global label_3
    global label_4

    if data["data"]["aqi"] <= 50:
        label_3= Label(window,text="Good",font=("Arial",20,"bold"),
                           bg="#020617",fg="#86efac")
        label_3.place(x=300,y=200)
        label_4= Label(window,text="Air quality is good.\nSafe for outdoor activities.",
                           font=("Arial",17,"bold"),justify=LEFT,wraplength=350, # It sets the maximum line width in pixels before Tkinter wraps text to the next line.
                           bg="#020617",fg="#e5e7eb")
        label_4.place(x=170,y=250)

    elif data["data"]["aqi"] > 50 and data["data"]["aqi"] <=100:
        label_3= Label(window,text="Moderate",font=("Arial",20,"bold"),
                           bg="#020617",fg="#fde68a")
        label_3.place(x=300,y=200)
        label_4= Label(window,text="Air quality is acceptable. Sensitive individuals should be cautious.",
                           justify=LEFT,wraplength=350,font=("Arial",17,"bold"),
                           bg="#020617",fg="#e5e7eb")
        label_4.place(x=170,y=250)

    elif data["data"]["aqi"] > 100 and data["data"]["aqi"] <=150:
        label_3= Label(window,text="Unhealthy for\nSensitive Group",font=("Arial",17,"bold"),
                           bg="#020617",fg="#fdba74")
        label_3.place(x=300,y=200)
        label_4= Label(window,text="Sensitive groups should limit outdoor exposure.",
                           justify=LEFT,wraplength=350,font=("Arial",17,"bold"),
                           bg="#020617",fg="#e5e7eb")
        label_4.place(x=170,y=250)

    elif data["data"]["aqi"] > 150 and data["data"]["aqi"] <=200:
        label_3= Label(window,text="Unhealthy",font=("Arial",20,"bold"),
                           bg="#020617",fg="#f87171")
        label_3.place(x=300,y=200)
        label_4= Label(window,text="Everyone should reduce outdoor exertion.",
                           justify=LEFT,wraplength=350,font=("Arial",17,"bold"),
                           bg="#020617",fg="#e5e7eb")
        label_4.place(x=170,y=250)

    elif data["data"]["aqi"] > 200 and data["data"]["aqi"] <=300:
        label_3= Label(window,text="Very Unhealthy",font=("Arial",20,"bold"),
                           bg="#020617",fg="#ef4444")
        label_3.place(x=300,y=200)
        label_4= Label(window,text="Avoid outdoor activities.",
                           justify=LEFT,wraplength=350,font=("Arial",17,"bold"),
                           bg="#020617",fg="#e5e7eb")
        label_4.place(x=170,y=250)

    else:
        label_3= Label(window,text="Hazardous",font=("Arial",20,"bold"),
                           bg="#020617",fg="#7f1d1d")
        label_3.place(x=300,y=200)
        label_4= Label(window,text="Health emergency. Stay indoors.",
                           justify=LEFT,wraplength=350,font=("Arial",17,"bold"),
                           bg="#020617",fg="#e5e7eb")
        label_4.place(x=170,y=250)

def check():
    city_name=entry_1.get()
    try:
     label_1.destroy()
     label_2.destroy()
     label_3.destroy()
     label_4.destroy()
    except:
        pass
    get(city_name)

window= Tk()
window.geometry("500x400")
window.config(bg="#020617")

entry_1= Entry(window,font=("Arial",15),bg="#1e293b",fg="#e5e7eb",
               insertbackground="#e5e7eb")
entry_1.place(x=120,y=350)

button_1= Button(window,text="Check",bg="#22d3ee",fg="#020617",
                 activebackground="#06b6d4",activeforeground="#020617",
                 command=check)
button_1.place(x=360,y=350)

label_main= Label(window,text="Check Air Pollution",font=("Arial",25,"bold"),
                  fg="#e5e7eb",bg="#020617")
label_main.place(x=100,y=10)

label_aqi= Label(window,text="AQI:",font=("Arial",20,"bold"),
                 bg="#020617",fg="#e5e7eb")
label_aqi.place(x=50,y=100)

label_pollutant= Label(window,text="Main Pollutant: ",font=("Arial",20,"bold"),
                       bg="#020617",fg="#e5e7eb")
label_pollutant.place(x=50,y=150)

label_level= Label(window,text="Air Quality Level:",font=("Arial",20,"bold"),
                   bg="#020617",fg="#e5e7eb")
label_level.place(x=50,y=200)

label_advice= Label(window,text="Advice:",font=("Arial",20,"bold"),
                    bg="#020617",fg="#e5e7eb")
label_advice.place(x=50,y=250)

window.mainloop()

# Read Me

'This app tells air pollution of available cities or their overall country.'

'Free api from aqicn is used.'
'Tkinter module is used to build GUI of this app. '

'I learned mapping ( process of converting values to strings ), so that user can have a '
'better understanding for there city.'

'Also learned some tkinter label functions such as wraplengh and justify.'
