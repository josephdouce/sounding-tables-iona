# -*- coding: utf-8 -*-
"""
This is a sounding table program.

This program uses .csv files in the format 
Trim,value,value,... 
Sounding,contents,contents... 
Sounding,contents,contents... 

files named as Tank.csv in ./sounding_tables/

Created by Joseph Douce
"""
import os
import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_tk 
from datetime import datetime, date, time
import glob

#set working directory to current path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#import list of tanks from folder /sounding_tables/
tanks = glob.glob('./sounding_tables/*.csv')
      
#setup main_window
main_window = themed_tk.ThemedTk()
main_window.title("Sounding Tables")
#main_window.iconbitmap(default='./icon.ico')
main_window.set_theme('arc')

#global variables
sounding_table = {}
trimtable = ["Trim","-0.9","-0.6","-0.3","0","0.3","0.6"]
soundings = {}
contents = {}
previous_values = {}
previous_values_update = {}
date_and_time = {}
trim = tk.StringVar()

#global widget varibales
i=0
for tank in tanks:
    soundings[i] = tk.StringVar()
    date_and_time[i] = tk.StringVar()
    contents[i] = tk.StringVar()
    i=i+1


#slice the path and .csv fom the tank names        
def slice_tanks():
    for i, _ in enumerate(tanks):
        tanks[i] = tanks[i][18:-4]

#make the widgets
def make_widgets():

    #headings
    trim_frame = ttk.Frame(main_window)
    trim_frame.pack()

    #trim label
    trim_label = ttk.Label(trim_frame)
    trim_label["text"] = "Trim"
    trim_label["width"] = 20
    trim_label.pack(side="left")
    
    #trim select
    trim_select = ttk.Combobox(trim_frame)
    trim_select["width"] = 20
    trim_select["textvariable"] = trim
    trim_select["values"] = trimtable
    trim_select.pack(side="left")
    trim_select.current(3)

    sounding_frame = ttk.Frame(main_window)
    sounding_frame.pack()
    
    column_one = ttk.Frame(sounding_frame)
    column_one.pack(side="left")

    column_spacer = ttk.Frame(sounding_frame)
    column_spacer["width"] = 10
    column_spacer.pack(side="left")

    column_two = ttk.Frame(sounding_frame)
    column_two.pack(side="left")

    column_spacer = ttk.Frame(sounding_frame)
    column_spacer["width"] = 10
    column_spacer.pack(side="left")

    column_three = ttk.Frame(sounding_frame)
    column_three.pack(side="left")

    column_spacer = ttk.Frame(sounding_frame)
    column_spacer["width"] = 10
    column_spacer.pack(side="left")

    column_four = ttk.Frame(sounding_frame)
    column_four.pack(side="left")
   
    #tank rows
    for i, _ in enumerate(tanks):

        if tanks[i][0:2] == "BW":
            column = column_two
        elif tanks[i][0:2] == "GW":
            column = column_two
        elif tanks[i][0:2] == "HW":
            column = column_two
        elif tanks[i][0:2] == "LO":
            column = column_three
        elif tanks[i][0:2] == "MG":
            column = column_three
        elif tanks[i][0:2] == "CL":
            column = column_three
        elif tanks[i][0:2] == "TW":
            column = column_one
        elif tanks[i][0:2] == "VO":
            column = column_four
        elif tanks[i][0:2] == "SL":
            column = column_four
        elif tanks[i][0:2] == "TR":
            column = column_four
        elif tanks[i][0:2] == "UN":
            column = column_four
        else:
            column = column_one
        
        if not tanks[i][:2] == tanks[i-1][:2]:
            type_frame = ttk.Frame(column)
            type_frame.pack()

            type_label = ttk.Label(type_frame)
            type_label["text"] = tanks[i].split(" ")[0]
            type_label.pack() 

        row_frame = ttk.Frame(column)
        row_frame.pack()

        tank_frame = ttk.Frame(row_frame)
        tank_frame.pack(side="left")

        result_frame = ttk.Frame(row_frame)
        result_frame.pack(side="right")

        #individual tank names
        tank_label = ttk.Label(tank_frame)
        tank_label["text"] = tanks[i]
        tank_label["width"] = 35
        tank_label.pack(side="left")

        #individual tank sounding boxes
        sounding_box = ttk.Entry(tank_frame)
        sounding_box["width"] = 5
        sounding_box["textvariable"] = soundings[i]
        sounding_box.pack(side="left")
        sounding_box.bind("<Return>", update_values)
        sounding_box.bind("<Tab>", update_values)

        #cm label
        cm_label = ttk.Label(tank_frame)
        cm_label["text"] = "cm"
        cm_label["width"] = 3
        cm_label.pack(side="left") 

        #spacer label
        spacer_label = ttk.Label(result_frame)
        spacer_label["text"] = ""
        spacer_label["width"] = 2
        spacer_label.pack(side="left")

        #value label
        value_label = ttk.Label(result_frame)
        value_label["textvariable"] = contents[i]
        value_label["width"] = 7
        value_label.pack(side="left")

        #m3 label
        m3_label = ttk.Label(result_frame)
        m3_label["text"] = "m3"
        m3_label["width"] = 3
        m3_label.pack(side="left")

        #datetime label
        date_time_label = ttk.Label(result_frame)
        date_time_label["textvariable"] = date_and_time[i]
        date_time_label.pack(side="left")

    exit_frame = ttk.Frame(main_window)
    exit_frame.pack()

    copyright_frame = ttk.Frame(main_window)
    copyright_frame.pack()

#exit button 
    exit_button = ttk.Button(exit_frame)
    exit_button["text"] = "Exit"
    exit_button["command"] = main_window.destroy
    exit_button.pack(pady=5, side="left")

    copyright_label = ttk.Label(copyright_frame)
    copyright_label["text"] = "© Joseph Douce 2018"
    copyright_label.pack()

#generate sounding table from .csv file
def load_sounding_table(file):
    
    #parse each line and add to sounding_tables{}
    input_file=open(file, "r")
    contents = []
    while True:
         sounding_and_contents = input_file.readline()
         sounding_and_contents = sounding_and_contents[:-1]
         if not sounding_and_contents:
             break
         else:
             contents = sounding_and_contents.split(",")
             sounding_table[contents[0]] = contents
    input_file.close()

#write new values to output file            
def update_values(*args):
    #write values to file
    output_to_file()
    #update ui with new values
    load_values()

#update displayed values from input file
def load_values():
    input_file=open('./last_soundings.txt', "r")
    i=0
    while True:
         sounding_and_time = input_file.readline()
         sounding_and_time = sounding_and_time[:-1]
         if not sounding_and_time:
             break
         else:
             values = sounding_and_time.split(",")
             previous_values[i] = values
             #sounding
             soundings[i].set(previous_values[i][1])
             #datetime
             date_and_time[i].set(previous_values[i][2])
             load_sounding_table("sounding_tables/" + tanks[i] + ".csv")

             try:
                 #lookup values from table for even numbers
                 if (int(soundings[i].get()) % 2) == 0:
                     contents[i].set(sounding_table[soundings[i].get()][trimtable.index(trim.get())])
                 else:
                     #interpolate values for odd numbers
                     upper = int(soundings[i].get()) + 1
                     lower = int(soundings[i].get()) - 1
                     upper = sounding_table[str(upper)][trimtable.index(trim.get())]
                     lower = sounding_table[str(lower)][trimtable.index(trim.get())]
                     avg = round((float(upper) + float(lower)) / 2 , 2)
                     contents[i].set(avg)
             except:
                 #throw error for non integers
                 contents[i].set("ERR")
             i=i+1
    input_file.close()

def output_to_file(*args):
    output_file=open('./last_soundings.txt', 'w')
    for i, _ in enumerate(soundings):
        try:
            if soundings[i].get() == previous_values[i][1]:
                print(tanks[i] + ',' + previous_values[i][1] + ',' + previous_values[i][2], file=output_file)
            else:
                print(tanks[i] + ',' + soundings[i].get() + ',' + str(datetime.today())[5:-10], file=output_file)
        except:
            print(tanks[i] + ',' + "0" + ',' + str(datetime.today())[5:-10], file=output_file)
    output_file.close()
    
#trim tank names
slice_tanks()

#create widgets
make_widgets()

#load last soundings file
load_values()

#mainloop
main_window.mainloop()
