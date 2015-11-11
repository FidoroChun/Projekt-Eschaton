import PIL.Image
import PIL.ImageTk
import MySQLdb as mdb
from Tkinter import *
import random, string
import tkMessageBox
import ConfigParser
import tkFileDialog
import base64
import urllib
import time
import sha
import ttk
import os

def change(event):
	print "anderung"
	



f1 = Tk()
nb = ttk.Notebook(f1)

f2 = Frame(nb)
lab = Label(f2, text="klappt das?")
lab.pack()

f3 = Frame(nb)
lab2 = Label(f3, text="das auch?")
lab2.pack()


nb.add(f2, text="eins")
nb.add(f2, text="drei")
nb.add(f3, text="zwei")
nb.pack()
f1.bind("<<NotebookTabChanged>>", change)
f1.mainloop()