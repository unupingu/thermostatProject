# thermostatProject
# Copyright (C) 2020  Miquel Puig Gibert @miquipuig
 
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
if sys.version_info[0] < 3:
    PVERSION=2
else:
    PVERSION=3

# import tkinter
try:
    import tkinter as tk
    import tkinter.font as tkFont
    from tkinter import *
    from tkinter.ttk import *

except ImportError:
    from Tkinter import *
    import Tkinter as tk
    import tkFont

import time as time
import datetime
import threading
import random
#images
from PIL import Image, ImageTk
import numpy as np
import os, sys
from .dataService import ts
from . import *

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
#lineCollection
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

iteration=False

class ThermostatScreen:
 
    def __init__(self):
        
        self.root = tk.Tk()
        if(env=='production'):
            self.root.attributes("-fullscreen", True)
            self.root.config(cursor='none')
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-alpha", True)
        self.root.configure(background=bg)
        self.root.geometry("480x320") #Width x Height
        self.root.bind("<Escape>", quit)
        self.root.bind("x", quit)
        self.run(self.root)
        
    def mainloop(self):
        self.root.mainloop()
  
    def run(self, parent):

        if(PVERSION==2):
            self.gradeSymbol = u'\u00BA'
            self.gradeSymbol = self.gradeSymbol.encode('utf-8')
        else:
            self.gradeSymbol = '\u00BA'
        self.iteration=False
        #-------------    
        #   BUTTONS
        #-------------
        self.fnt1 = tkFont.Font(family='Digital-7 Mono', size=25, weight='normal')
        self.fnt1 = tkFont.Font(family='Digital-7 Mono', size=20 , weight='normal')
        # self.fnt1 = tkFont.Font(family='Arial', size=25)
        self.fnt2 = tkFont.Font( family='Garden Grown US', size=125, weight='normal')
        self.fnt3 = tkFont.Font( family='Arial', size=70, weight='bold')
        self.fnt4 = tkFont.Font( family='Calibri', size=20, weight='bold')      

        colorSymbolButton= tblue
        colorButton=bg
        self.style = Style() 
        self.style.configure('TButton', font = ('calibri', 20, 'bold'), borderwidth = '0')
        self.style.map('TButton', foreground = [('!disabled','!disabled','black')], background =[('!disabled',tblue)])
        
        # self.style.configure('TLabel', foreground="black", background="green")
        # self.powerBTN = tk.Button(root, text = 'Power', command=self.power, bd=0,highlightthickness=0, relief=tk.RIDGE,activebackground=tblue,bg=tblue,activeforeground=bg, fg=bg, font = self.fnt4)
        # self.powerBTN.grid(row = 0, column = 0 )
        self.plusBTN = tk.Button(parent, width=1, height=0, text ="+",bd=0,highlightthickness=0, relief=tk.RIDGE,activebackground=colorButton,bg=colorButton,activeforeground=colorSymbolButton, fg=colorSymbolButton, font = self.fnt3)
        #Seccion temperatura
        # self.plusBTN.place(relx=0.75, rely=0.23,anchor=tk.NW)
        # self.plusBTN.bind('<Button-1>',self.sumaD)
        # self.plusBTN.bind('<ButtonRelease-1>',self.sumaU)
        # self.lessBTN = tk.Button(parent, width=1, height=0, text ="-",bd=0,highlightthickness=0, relief=tk.RIDGE,activebackground=colorButton,bg=colorButton,activeforeground=colorSymbolButton, fg=colorSymbolButton, font = self.fnt3)
        # self.lessBTN.place(relx=0.25, rely=0.23,anchor=tk.NE)
        # self.lessBTN.bind('<Button-1>',self.restaD)
        # self.lessBTN.bind('<ButtonRelease-1>',self.restaU)      
        # self.tempLabel = tk.Label(text="%0.1f%s" % (ts.desiredT , self.gradeSymbol), font=self.fnt2, foreground='white',background=bg, anchor='e',width=5) 
        # self.tempLabel.place(relx=0.45, rely=0.48,anchor=tk.CENTER)
        
        #Hora y temperatura ambiente
        self.horaText = tk.StringVar()
        self.txt3 = tk.StringVar()
        self.horaText.set(time.strftime('%-I:%M:%S %p'))
        self.txt3.set("{0:0.0f}{1}C {2:0.1f}%".format(ts.temp,self.gradeSymbol,ts.humidity ))
        self.lecturesLabel = tk.Label(parent, textvariable=self.txt3, font=self.fnt1, foreground="white", background=bg, pady = 10)
        self.lecturesLabel.place(relx=0.03, rely=0.93, anchor=tk.W)
        self.horaLabel = tk.Label(parent, textvariable=self.horaText, font=self.fnt1, foreground="white", background=bg, pady = 10)
        self.horaLabel.place(relx=0.82, rely=0.93,anchor=tk.CENTER)
        #-----------
        #   ICONS
        #-----------
        self.pathname = os.path.dirname(sys.argv[0])
        self.fullpath = os.path.abspath(self.pathname)
        
        self.weather=Image.open(self.fullpath+IMG_WEATHER_PATH+ts.weatherIcon+'.png')
        self.weather= self.weather.resize((80, 80), Image.ANTIALIAS)
        self.weather = ImageTk.PhotoImage(self.weather)
        
        
        self.moon= Image.open(self.fullpath+IMG_PATH+'moon3.png')
        self.moon= self.moon.resize((100, 100), Image.ANTIALIAS)
        self.moon = ImageTk.PhotoImage(self.moon)
     
        self.sun= Image.open(self.fullpath+IMG_PATH+'sun2.png')
        self.sun= self.sun.resize((60, 60), Image.ANTIALIAS)
        self.sun = ImageTk.PhotoImage(self.sun)
        
        self.power= Image.open(self.fullpath+IMG_PATH+'power7.png') 
        self.power= self.power.resize((50, 50), Image.ANTIALIAS)
        
        self.eco= Image.open(self.fullpath+IMG_PATH+'eco1.png')
        self.eco= self.eco.resize((80, 80), Image.ANTIALIAS)
        self.eco = ImageTk.PhotoImage(self.eco)
 
        #BOTTOM CANVAS
        self.canvas = Canvas(parent, width=480, height=280, bg=bg, bd=0, highlightthickness=0, relief='ridge')
        self.canvas.place(relx=1, rely=0,anchor=tk.NE)    
            
        
        #DEFINE COLOR OF PICTURES
        # self.power = ImageTk.PhotoImage(self.power)
        self.power = self.power.convert('RGBA')
        self.dataPowerUp= np.array(self.power)
        self.dataPowerDown= np.array(self.power)
        red, green, blue, alpha = self.dataPowerUp.T
        red, green, blue, alpha = self.dataPowerDown.T
        self.defined_areas = (red == 0) & (blue == 0) & (green == 0)
        self.dataPowerUp[..., :-1][self.defined_areas.T] = (255, 241, 169)
        self.dataPowerDown[..., :-1][self.defined_areas.T] = (169, 183, 255)
        self.dataPowerUp = Image.fromarray(self.dataPowerUp)
        self.dataPowerDown = Image.fromarray(self.dataPowerDown)
        self.powerUp=ImageTk.PhotoImage(self.dataPowerUp)
        self.powerDown=ImageTk.PhotoImage(self.dataPowerDown)
        
        
        self.power=self.canvas.create_image(40, 35, image=self.powerDown)
        self.image=self.canvas.create_image(440, 35, image=self.sun)
        self.ecoImage=self.canvas.create_image(100, 80, image=self.eco)
        
        self.canvas.itemconfig(self.ecoImage, state = 'hidden')  
        
        #SELECTED TEMPERATURE
        self.tempText2=self.canvas.create_text(360,155,fill=twhite,font=self.fnt2,
                        text="%0.0fº" % (ts.desiredT%1*10 ), anchor='e')
        self.tempText1=self.canvas.create_text(265,155,fill=twhite,font=self.fnt2,
                        text="%i" % (ts.desiredT), anchor='e')
        
        
        self.ecoImage=self.canvas.create_image(110, 80, image=self.eco)
        #PLUS/MINUS BUTTON
        self.minusButton=self.canvas.create_text(110,130,fill=tblue,font=self.fnt3, text="-")
        self.plusButton=self.canvas.create_text(360,143,fill=tblue,font=self.fnt3, text="+")  
        self.canvas.tag_bind(self.minusButton, '<Button-1>', self.restaD)
        self.canvas.tag_bind(self.minusButton, '<ButtonRelease-1>', self.restaU)
        self.canvas.tag_bind(self.plusButton, '<Button-1>', self.sumaD)
        self.canvas.tag_bind(self.plusButton, '<ButtonRelease-1>', self.sumaU)
        
        #WEATHER INFO
        self.weatherIcon=self.canvas.create_image(180,35, image=self.weather, tag='weather')
        self.weatherText=self.canvas.create_text(210,30,fill=twhite,font=self.fnt1,text=str(ts.weatherTemp) + 'º ' + str(ts.weatherHumidity)+'%', tag='weather',anchor='w')
        # self.weatherText=self.canvas.create_text(270,30,fill=twhite,font=self.fnt1,text='HOLA', tag='weather')
        
        #TIME & LECTURES
        # self.timeText=self.canvas.create_text(475,300,fill=twhite,font=self.fnt1,text=time.strftime('%-I:%M:%S %p'), tag='time',anchor='e')
        # self.lecturesText=self.canvas.create_text(5,300,fill=twhite,font=self.fnt1,text="{0:0.0f}{1}C {2:0.1f}%".format(ts.temp,self.gradeSymbol,ts.humidity), tag='time',anchor='w')

        #POWER BUTTON
        if (ts.power==True):
            self.power=self.canvas.create_image(40, 35, image=self.powerUp)
        else:
            self.power=self.canvas.create_image(40, 35, image=self.powerDown)
        self.canvas.tag_bind(self.power, '<ButtonPress-1>', self.powerClick)
        self.canvas.tag_bind(self.image, '<ButtonPress-1>', self.moonSunClick)
         

        #-----------
        #  DIAGRAM
        #-----------
        t = np.arange(0, 3, .01)
        self.fig, self.ax = plt.subplots()        
        # fig.patch.set_alpha(0.5)
        #Diagram Size
        self.fig.set_size_inches(5, 0.87)
        self.fig.subplots_adjust(top=0.85) #adjust plot inside
        self.fig.subplots_adjust(bottom=0.02) #adjust plot inside
        self.fig.subplots_adjust(left=0.08) #adjust plot inside
        # self.fig.subplots_adjust(right=1.095) #adjust plot inside
        self.fig.subplots_adjust(right=0.9) #adjust plot inside
        self.fig.subplots_adjust(hspace=0) #adjust plot inside
        self.fig.patch.set_facecolor(bg) #color figura
        canvasFigure = FigureCanvasTkAgg(self.fig, master=parent)  # A tk.DrawingArea.        
        # canvasFigure.draw()
        canvasFigure.draw_idle()
        canvasFigure.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=2)
        canvasFigure.get_tk_widget().place(relx=0.5, rely=0.625,anchor=tk.N)

        #It need a semaphore like a atomic function -  concurrency problems
        # x=ts.th.extractHistoricData(0)
        # y=ts.th.extractHistoricData(1)
        # z=ts.th.extractHistoricData(2)

        data=ts.th.extractHistoricData([0,1,2])
        x=data[0]
        y=data[1]
        z=data[2]
        
        # x = [datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(12)]
        # y = [i+random.gauss(0,1) for i,_ in enumerate(x)]
        self.ax.plot(x,y,linewidth=2)
        self.ax.plot(x,z)
        
        # x = np.arange(100)
        # y = 10*np.sin(x / 50) +13
        # points = np.array([x, y]).T.reshape(-1, 1, 2)
        # segments = np.concatenate([points[:-1], points[1:]], axis=1)
        # norm = plt.Normalize(y.min(), y.max())
        # lc = LineCollection(segments, cmap='viridis', norm=norm)
        # lc.set_array(y)
        # lc.set_linewidth(2)
        # line = self.ax.add_collection(lc)
        
        # self.ax.set_xlim(x.min(), x.max()) #rango en x
        # self.ax.set_ylim(y.min(),y.max() +1 ) #rango en y
        # # ax.step(x, y + 2, 'red', label='pre (default)')
        # self.ax.plot(x, y -0.1*x, color='green', alpha=0.5)
        # ax.plot(x, y + 2,'C0o', color='red', alpha=0.5)
        # ax.step(x, y + 1, where='mid', label='mid')
        # ax.plot(x, y + 1, 'C1o', alpha=0.5)

        # ax.step(x, y, where='post', label='post')
        # ax.plot(x, y, 'C2o', alpha=0.5)
 
        #colors and borderse
        self.ax.set_facecolor(bg)     
        self.ax.axis('on') #border
        self.ax.spines['top'].set_color(bg)
        self.ax.spines['left'].set_color(bg)
        self.ax.spines['bottom'].set_color(bg)
        self.ax.spines['right'].set_color(bg)
        #xaxis conf
        self.ax.tick_params(axis='x', colors=tblue, labelsize=7, direction="in", pad= 1)
        self.ax.xaxis.tick_top()
        # ax.xaxis.get_major_ticks()
        #yaxis conf
        self.ax.yaxis.label.set_color(tblue)
        self.ax.tick_params(axis='y', colors=tblue, labelsize=7, direction="in", pad=2.5)
        # #colorbar config
        # cbar=self.fig.colorbar(line, ax=self.ax)
        # cbar.outline.set_edgecolor(bg)
        # cbar.ax.yaxis.set_tick_params(color=tblue, labelsize=7, direction="in", pad= 2)
        # cbytick_obj = plt.getp(cbar.ax.axes, 'yticklabels')
        # plt.setp(cbytick_obj, color=tblue)    
        # self.fig.patch.set_visible(True)    
        # #ax.legend(title='Parameter where:') #legend
        
        self.count=0
        self.canvas.after(500, self.refresh_canvas)
        
    def moonSunClick(self, event):
        global bg
        if(ts.moonSun=='sun'):
            ts.moonSun='moon'
            self.canvas.itemconfig(self.image, image = self.moon)
        else:
            ts.moonSun='sun' 
            self.canvas.itemconfig(self.image, image = self.sun)
        ts.dayNightLoadTemperature()
        self.refresh_tempLabel()
    
    def refreshEcoState(self):
        if(ts.ecoState()):
            self.canvas.itemconfig(self.ecoImage, state = 'normal')   

        else:           
            self.canvas.itemconfig(self.ecoImage, state = 'hidden')   

        
    def quit(self):
        root.destroy()
    def powerClick(self, event):
        ts.powerP()
        if (ts.power==True):
            self.canvas.itemconfig(self.power, image = self.powerUp)
        else:
            self.canvas.itemconfig(self.power, image = self.powerDown)

    def refresh_canvas(self):
        # self.txt2.set(time.strftime("%H:%M:%S"))
        self.horaText.set(time.strftime('%-I:%M:%S %p'))                
        # self.canvas.itemconfig(self.timeText,text=time.strftime('%-I:%M:%S %p'))

 
        if(ts.refreshDataListener):
            # self.canvas.itemconfig(self.lecturesText,text="{0:0.0f}{1}C {2:0.1f}%")
            self.txt3.set("{0:0.1f}{1}C {2:0.1f}%".format(ts.temp,self.gradeSymbol,ts.humidity))
            #DIAGRAM
            # ts.updateFake()
            # self.y.set_xdata(ts.historicData[0]) 
            
            data=ts.th.extractHistoricData([0,1,2])
            x=data[0]
            y=data[1]
            z=data[2]
  
            try:
                self.ax.clear()
                self.ax.plot(x,y,linewidth=3)
                self.ax.plot(x,z)
                self.fig.canvas.draw_idle()
            except Exception as ex:
                logger.error(ex)
            # self.fig.canvas.flush_events()
            self.count=0
            ts.refreshDataListener=False
            ts.refreshDesiredConf=True
            self.weather=Image.open(self.fullpath+IMG_WEATHER_PATH+ts.weatherIcon+'.png')
            self.weather= self.weather.resize((80, 80), Image.ANTIALIAS)
            self.weather = ImageTk.PhotoImage(self.weather)
            self.canvas.itemconfig(self.weatherIcon, image = self.weather)
            self.canvas.itemconfig(self.weatherText,text=str(ts.weatherTemp) + 'º ' + str(ts.weatherHumidity)+'%')
            
        if(ts.refreshDesiredConf):
            self.refresh_tempLabel_full()
        
        self.canvas.after(500, self.refresh_canvas)
        
    def refresh_tempLabel(self):
        # self.tempLabel.configure(text="%s%sC" % (str(np.around(ts.desiredT, decimals=1)) , self.gradeSymbol))
        # self.tempLabel.configure(text="%0.1f%s" % (ts.desiredT , self.gradeSymbol))
        self.canvas.itemconfig(self.tempText2,text="%0.0fº" % (ts.desiredT%1*10))
        self.canvas.itemconfig(self.tempText1,text="%i." % (ts.desiredT))

       
    def refresh_tempLabel_full(self):
        # self.tempLabel.configure(text="%s%sC" % (str(np.around(ts.desiredT, decimals=1)) , self.gradeSymbol))
        ts.startHeater()
        self.refresh_tempLabel()
        if (ts.started and ts.power):
            self.canvas.itemconfig(self.tempText2,fill=tred)
            self.canvas.itemconfig(self.tempText1,fill=tred)
        elif (ts.tAchieved and ts.power):
            self.canvas.itemconfig(self.tempText2,fill=tgreen)
            self.canvas.itemconfig(self.tempText1,fill=tgreen)
        else:
            self.canvas.itemconfig(self.tempText2,fill='white')
            self.canvas.itemconfig(self.tempText1,fill='white')
        ts.refreshDesiredConf=False
        self.refreshEcoState()
    
    def sumaW(self):
        sleepTime=0.400
        while(self.iteration==True):
            ts.increaseTemperature()
            time.sleep(sleepTime)
            sleepTime-=(sleepTime/10)
        # ts.startHeater()
    def restaW(self):
        sleepTime=0.400
        while(self.iteration==True):
            ts.decreaseTemperature()
            time.sleep(sleepTime)
            sleepTime-=(sleepTime/12)
        # ts.startHeater()
    def sumaD(self,event):
        self.iteration=True
        t = threading.Thread(target=self.sumaW, args=())
        t.daemon = True
        t.start()
    def sumaU(self,event):
        self.iteration=False
        
    def restaU(self,event):
        self.iteration=False
    def restaD(self,event):
        self.iteration=True
        t = threading.Thread(target=self.restaW, args=())
        t.daemon = True
        t.start()
