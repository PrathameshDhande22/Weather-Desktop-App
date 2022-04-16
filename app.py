import configparser
from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
import threading
import requests
import datetime
import pytz
from timezonefinder import TimezoneFinder

'''Author: prathamesh Dhande
If you find any error in this code then you can contact me prathameshdhande534@gmail.com'''  

class Weather(Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather App")
        self.geometry("800x480")
        self.iconbitmap(r"Images/weather_icon.ico")
        self.resizable(False,False)
        # self.__gui()
        threading.Thread(target=self.__gui).start()
        
    def __gui(self):
       # placing the black border for search
       self.img=Image.open(r"Images/black_border.png")
       self.resizeimg=self.img.resize((275,35))
       self.finalimg=ImageTk.PhotoImage(self.resizeimg)
       Label(image=self.finalimg).place(x=20,y=20)
       
       # creating the search button
       self.img1=Image.open(r"Images/search_btn.png")
       self.resizeim1=self.img1.resize((29,29))
       self.finalimg1=ImageTk.PhotoImage(self.resizeim1)
       self.b1=Button(image=self.finalimg1,bg="black",command=self.threading)
       self.b1.place(x=297,y=22)
       self.bind("<Return>",self.threading)
     
       # creating the search textbox
       self.search=StringVar()
       self.search_textbox=Entry(textvariable=self.search,font=("Segoe UI",14,'bold'),width=24,justify="center",relief="flat")
       self.search_textbox.place(x=25,y=25)

       # creating the current weather label to display the city name and city time
       Label(text="Current Weather :",font='Arial 14 bold',fg="red").place(x=590,y=7)

       # location image logo
       self.img2=Image.open(r'Images/location.png')
       self.resizeimg2=self.img2.resize((20,20))
       self.finalimg2=ImageTk.PhotoImage(self.resizeimg2)
       Label(image=self.finalimg2).place(x=595,y=36)

       # location label 
       self.location=Label(text='',font='Calibri 15')
       self.location.place(x=620,y=34)

       # time label for the searched city
       self.timelbl=Label(text="",font=("Cambria",16))
       self.timelbl.place(x=590,y=60)

       # creating the label for the logo according to main
       self.img3=Image.open(r"Icons/main.png")
       self.resizeimg3=self.img3.resize((200,190))
       self.finalimg3=ImageTk.PhotoImage(self.resizeimg3)
       self.icons=Label(image=self.finalimg3)
       self.icons.place(x=70,y=110)

       # creating the label to display the temperature
       self.temperature=Label(text="",font=("Cambria",75,'bold'))
       self.temperature.place(x=270,y=140)
       self.degree=Label(text="",font="Cambria 40 bold")
       self.degree.place(x=390,y=135)

       # feels like label and sunny or fog like labels
       self.feel=Label(text="",font=("Nirmala UI",16,"bold"))
       self.feel.place(x=280,y=245)
       
       # sunrise logo
       self.finalimg4=ImageTk.PhotoImage(image=Image.open(r"Images/sunrise.png").resize((40,40)))
       Label(image=self.finalimg4).place(x=560,y=150)
       self.sunrise=Label(text="Sunrise : ",font=("Segoe UI",14,'bold'))
       self.sunrise.place(x=603,y=155)

       #sunset logo
       self.finalimg5=ImageTk.PhotoImage(image=Image.open(r"Images/sunset.png").resize((40,30)))
       Label(image=self.finalimg5).place(x=560,y=215)
       self.sunset=Label(text="Sunset : ",font=("Segoe UI",14,'bold'))
       self.sunset.place(x=603,y=210)

       # bottom bar
       self.finalimg6=ImageTk.PhotoImage(image=Image.open(r'Images/bottom_bar.png').resize((770,70)))
       Label(image=self.finalimg6,bg='#00b7ff').place(x=5,y=330)

       # placing the labels
       Label(text="Humidity",font="Calibri 15 bold",bg='#00b7ff',fg='white').place(x=35,y=335)
       Label(text="Pressure",font="Calibri 15 bold",bg='#00b7ff',fg='white').place(x=210,y=335)
       Label(text="Description",font="Calibri 15 bold",bg='#00b7ff',fg='white').place(x=400,y=335)
       Label(text="Visibility",font="Calibri 15 bold",bg='#00b7ff',fg='white').place(x=600,y=335)

       # humidity label
       self.humidity=Label(text="",font=("Calibri",15,'bold'),bg='#00b7ff',fg='black')
       self.humidity.place(x=50,y=361)

       # pressure label
       self.pressure=Label(text="",font=("Calibri",15,'bold'),bg='#00b7ff',fg='black')
       self.pressure.place(x=203,y=361)

       # description label
       self.des=Label(text="",font=("Calibri",15,'bold'),bg='#00b7ff',fg='black')
       self.des.place(x=405,y=361)

       # visibility label
       self.vis=Label(text="",font=("Calibri",15,'bold'),bg='#00b7ff',fg='black')
       self.vis.place(x=610,y=361)

       # exit and reset button
       Button(text='Exit',font=("Georgia",16,"bold"),bg='orange',fg='black',width=7,relief='groove',command=self.exit).place(x=680,y=420)
       Button(text='Reset',font=("Georgia",16,"bold"),bg='orange',fg='black',width=7,relief='groove',activebackground="blue",activeforeground='white',command=self.clear).place(x=560,y=420)

    def __get_weather(self):
        try:
            # getting the weather information
            city=self.search.get()
            config_file=configparser.ConfigParser()
            config_file.read("config.ini")
            api=config_file['Openweather']['api']
            data=f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}'
            weather=requests.get(data).json()
            self.__set_information(weather=weather)

        except requests.exceptions.ConnectionError:
            messagebox.showwarning('Connect',"Connect to The internet")
        except:
            messagebox.showerror('Error',"Some Errored Occured\nTry again Later!")
        
    def __set_information(self,weather):
        # print(weather)
        if weather['cod']=='404' and weather['message']=='city not found':
            messagebox.showerror("Error","Entered City Not Found")
            self.search.set("")
        elif weather['cod']=='400' and weather['message']=='Nothing to geocode':
            messagebox.showinfo("Warning",'Enter The city name')
            self.search.set('')
        else:
            # getting time according to timezone
            lon=weather['coord']['lon']  # longitutde
            lat=weather['coord']['lat']  # latitude
            tf=TimezoneFinder()
            result=tf.timezone_at(lng=lon,lat=lat)
            home=pytz.timezone(result)
            local=datetime.datetime.now(home).strftime("%d/%m/%y  %I:%M %p")
            self.timelbl['text']=local
            self.des['text']=weather['weather'][0]['description']
            self.feel['text']=f"Feels Like {int(weather['main']['feels_like']-273)}° | {weather['weather'][0]['main']}"
            type=weather['weather'][0]['main']
            self.place_image(type)
            
            # sets the temperature and degree label
            temp=int(weather['main']['temp']-273)
            self.degree['text']="°C"
            if temp>=100:
                self.degree.place(x=450,y=135)
            elif temp<=9 and temp>=0:
                self.degree.place(x=340,y=135)
            elif temp<=99 and temp>=10:
                self.degree.place(x=390,y=135)
            elif temp<0 and temp>=-9:
                self.degree.place(x=358,y=135)
            elif temp<=-10 and temp>=-99:
                self.degree.place(x=419,y=135)
            self.temperature['text']=int(weather['main']['temp']-273)
            self.humidity['text']=weather['main']['humidity'],'%'
            self.pressure['text']=weather['main']['pressure'],'mBar'
            self.location.config(text=weather['name'])
            self.vis['text']=int(weather['visibility']/1000),'km'
            self.sunrise['text']=f"Sunrise : \n{datetime.datetime.fromtimestamp(int(weather['sys']['sunrise'])).strftime('%d/%m/%y  %I:%M %p')}"
            self.sunset['text']=f"Sunset : \n{datetime.datetime.fromtimestamp(int(weather['sys']['sunset'])).strftime('%d/%m/%y   %I:%M %p')}"

    def place_image(self,type):
        if type=="Clear":
            img="clear.png"
            self.set_image(img)
        elif type=="Clouds":
            img='clouds.png'
            self.set_image(img)
        elif type=="Rain":
            img='rain.png'
            self.set_image(img)
        elif type=='Haze':
            img='haze.png'
            self.set_image(img)
        else:
            img='main.png'
            self.set_image(img)
    
    def set_image(self,img):
       self.img3=Image.open(f"Icons/{img}")
       self.resizeimg3=self.img3.resize((190,190))
       self.finalimg3=ImageTk.PhotoImage(self.resizeimg3)
       self.icons=Label(image=self.finalimg3)
       self.icons.place(x=70,y=110)
    
    def clear(self):
        self.des.config(text="")
        self.vis.config(text="")
        self.pressure.config(text="")
        self.humidity.config(text="")
        self.sunset.config(text="Sunset :")
        self.sunrise.config(text="Sunrise :")
        self.feel.config(text="")
        self.degree.config(text="")
        self.temperature.config(text="")
        self.timelbl.config(text="")
        self.location.config(text="")
        self.search.set("")
        img='main.png'
        self.set_image(img)

    def exit(self):
        a=messagebox.askyesno('Confirmation',"Are You sure You Want To Exit !")
        if a==True:
            self.destroy()

    def threading(self,event=0):
        t1=threading.Thread(target=self.__get_weather)
        t1.start()



if __name__=="__main__":
    c=Weather()
    c.mainloop()
