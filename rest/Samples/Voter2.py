# -*- coding: cp1252 -*-
# BY Tizian Pessel
# CONTACT fidoro@hotmail.de
# LICENSE do not distribute
# VER 1
prog_version = "1"
# DATE 16.06.2015

from PIL import Image, ImageTk
from Tkinter import *
import tkMessageBox
import urllib
import sys

override = False
first_start = 1
#api_key = "rQ5lAYC8CmfzBA1RmkdPvfVza19aP1Oci4emR2cDNK6kwO5ltbGpgS84mHgQF2F"
api_key = "H6yvGNtUZce5HiYqTdyC8Rf3bz5isMgSFS4DongHCGKk2PfWBXRBtXpY8gyV5dy"

def vote_action():
	global votes, e, root, api_key
	code = e.get()
	if code == "":
		tkMessageBox.showinfo(title="Fehler", message="Der Code ist ungueltig (kein Code)")
		return
	if len(code) != 8:
		tkMessageBox.showinfo(title="Fehler", message="Der Code ist ungueltig (nicht 8-stellig)")
		return
	for i in code:
		try:
			int(i)
		except:
			tkMessageBox.showinfo(title="Fehler", message="Der Code ist ungueltig (nicht numerisch)")
			return
	# Check Code
	anfrage = "http://elt.tizian.com.de/index.php?api_key=" + api_key + "&action=check_code&code=" + code
	try:
		x = urllib.urlopen(anfrage)
	except:
		tkMessageBox.showinfo(title="Fehler", message="Keine Internetverbindung. Probier es noch einmal :)")
		return
	x = x.readlines()
	try:
		if x[0] == "1":
			tkMessageBox.showinfo(title="Fehler", message="Der Code wurde bereits benutzt!")
		elif x[0] == "0":
			# Vote
			anfrage = "http://elt.tizian.com.de/index.php?api_key=" + api_key + "&action=vote&code=" + code + "&id_band_" + str(votes[0]) + "=3&id_band_" + str(votes[1]) + "=2&id_band_" + str(votes[2]) + "=1"
			try:
				x = urllib.urlopen(anfrage)
			except:
				tkMessageBox.showinfo(title="Fehler", message="Keine Internetverbindung. Probier es noch einmal :)")
				return
			x = x.readlines()
			if x[0] == "true":
				text_ = "Erfolgreich gevotet. Folgender Code wurde entwertet: " + code
				tkMessageBox.showinfo(title="Erfolg!", message=text_)
			elif x[0] == "false":
				tkMessageBox.showinfo(title="Fehler", message="Nice try, sucker! :D\n(" + x[0] + ")") 
			else:
				mes = "[vote] Es ist ein unbekannter Fehler bem Check deines Codes aufgetreten! (" + x[0] + ")"
				tkMessageBox.showerror(title="Fehler", message=mes)
		else:
			mes = "[check] Es ist ein unbekannter Fehler bem Check deines Codes aufgetreten! (" + x[0] + ")"
			tkMessageBox.showerror(title="Fehler", message=mes)
	except: #Votesperre abfragen
		tkMessageBox.showinfo(title="Fehler", message="Das Voten wurde noch nicht freigegeben!")
		return

def init_entry():
	global root, e
	e.delete(0, END)

def init_variables():
	global votes, images, bands, first_start
	bands = ["Bandnamen nach ID", "GrooveExperience", "Gaffatapes", "TheTravelers", "Maniax", "Overexposed"]
	votes = [0, 0, 0]
	if first_start == 1:
		images = [PhotoImage(file="./1.gif"), PhotoImage(file="./2.gif"), PhotoImage(file="./3.gif"), PhotoImage(file="./4.gif"), PhotoImage(file="./5.gif")]
		first_start = 0

def init_labx():
	global labx, votes
	text_ = "'Entf' oder die Ruecktaste druecken um zurueckzusetzen!\n\n"
	
	text_ = text_ + "1. Platz: "
	if votes[0] != 0:
		text_ = text_ + bands[votes[0]]
	
	text_ = text_ + "\n2. Platz: "
	if votes[1] != 0:
		text_ = text_ + bands[votes[1]]
		
	text_ = text_ + "\n3. Platz: "
	if votes[2] != 0:
		text_ = text_ + bands[votes[2]]
		
	labx.config(text=text_)
	
	if votes[2] != 0:
		x = tkMessageBox.askyesno(title="Bestaetigen", message="Willst du jetzt sicher diese Bands voten?")
		if x == True:
			vote_action()
			init()
		else:
			init()
			
def init_buttons():
	global but1, but2, but3, but4, but5
	but1.config(state=NORMAL)
	but2.config(state=NORMAL)
	but3.config(state=NORMAL)
	but4.config(state=NORMAL)
	but5.config(state=NORMAL)
	
def init():
	init_variables()
	init_labx()
	init_entry()
	init_buttons()

def exit_handler():
	pass
	
def button_1():
	global votes, but1
	x = 1
	if votes[0] == 0:
		votes[0] = x
		but1.config(state=DISABLED)
	elif votes[1] == 0:
		votes[1] = x
		but1.config(state=DISABLED)
	elif votes[2] == 0:
		votes[2] = x
		but1.config(state=DISABLED)
	else:
		tkMessageBox.showerror(title="Fehler!", message="Du kannst nur drei Bands voten!")
	init_labx()
	
def button_2():
	global votes, but2
	x = 2
	if votes[0] == 0:
		votes[0] = x
		but2.config(state=DISABLED)
	elif votes[1] == 0:
		votes[1] = x
		but2.config(state=DISABLED)
	elif votes[2] == 0:
		votes[2] = x
		but2.config(state=DISABLED)
	else:
		tkMessageBox.showerror(title="Fehler!", message="Du kannst nur drei Bands voten!")
	init_labx()
	
def button_3():
	global votes, but3
	x = 3
	if votes[0] == 0:
		votes[0] = x
		but3.config(state=DISABLED)
	elif votes[1] == 0:
		votes[1] = x
		but3.config(state=DISABLED)
	elif votes[2] == 0:
		votes[2] = x
		but3.config(state=DISABLED)
	else:
		tkMessageBox.showerror(title="Fehler!", message="Du kannst nur drei Bands voten!")
	init_labx()
	
def button_4():
	global votes, but4
	x = 4
	if votes[0] == 0:
		votes[0] = x
		but4.config(state=DISABLED)
	elif votes[1] == 0:
		votes[1] = x
		but4.config(state=DISABLED)
	elif votes[2] == 0:
		votes[2] = x
		but4.config(state=DISABLED)
	else:
		tkMessageBox.showerror(title="Fehler!", message="Du kannst nur drei Bands voten!")
	init_labx()
	
def button_5():
	global votes, but5
	x = 5
	if votes[0] == 0:
		votes[0] = x
		but5.config(state=DISABLED)
	elif votes[1] == 0:
		votes[1] = x
		but5.config(state=DISABLED)
	elif votes[2] == 0:
		votes[2] = x
		but5.config(state=DISABLED)
	else:
		tkMessageBox.showerror(title="Fehler!", message="Du kannst nur drei Bands voten!")
	init_labx()
	
def exit_make(NONE):
	global root
	root.destroy()
	sys.exit()

def main_frame():
	global root, c, images, labx, e, but1, but2, but3, but4, but5, override
	root = Tk()
	root.protocol("WM_DELETE_WINDOW", exit_handler)
	root.overrideredirect(override)
	geo = [root.winfo_screenwidth()+2, root.winfo_screenheight()+2]
	root.geometry(str(geo[0])+"x"+str(geo[1])+"+-2+-2")
	#c = Canvas(root, bg="#000000", width=geo[0], height=geo[1])
	#c.place(x=0, y=0)
	f1 = Frame(root, width=str(geo[0]), height=str(geo[1]/3))
	f2 = Frame(root, width=str(geo[0]), height=str((geo[1]/3)*2))
	f1.place(x=2, y=2)
	f2.place(x=2, y=(geo[1]/3))
	init_variables()
	#----------------------------
	pad = [20, 20] #\n2)Bands vom -ersten- bis zum -dritten- Platz anklicken um Punkte zu vergeben.\n3)Absenden. Bestätigung erfolgt!
	lab1 = Label(f1, text="1) Persoenlichen Code eingeben.", font="Courier_New 20", fg="#000000")
	lab2 = Label(f1, text="2) Bands vom -ersten- bis zum -dritten- Platz anklicken um Punkte zu vergeben.", font="Courier_New 20", fg="#000000")
	lab3 = Label(f1, text="3) Absenden. Bestaetigung erfolgt!", font="Courier_New 20", fg="#000000")
	e = Entry(f1, font="Courier_New 15")
	but1 = Button(f2, compound=TOP, image=images[0], text="GrooveExperience", command=button_1)
	but2 = Button(f2, compound=TOP, image=images[1], text="Gaffatapes", command=button_2)
	but3 = Button(f2, compound=TOP, image=images[2], text="The Travelers", command=button_3)
	but4 = Button(f2, compound=TOP, image=images[3], text="Maniax", command=button_4)
	but5 = Button(f2, compound=TOP, image=images[4], text="Overexposed", command=button_5)
	labx = Label(f2, text="", font="Courier_New 10", fg="#000000")
	init_labx()
	#
	lab1.grid(row=0, column=0, padx=pad[0], pady=pad[1], sticky="NW")
	lab2.grid(row=1, column=0, padx=pad[0], pady=pad[1], sticky="NW")
	lab3.grid(row=2, column=0, padx=pad[0], pady=pad[1], sticky="NW")
	e.grid(row=3, column=0, padx=pad[0], pady=pad[1], sticky="NW")
	e.focus()
	but1.grid(row=4, column=0, padx=pad[0], pady=pad[1], sticky="NW")
	but2.grid(row=5, column=0, padx=pad[0], pady=pad[1], sticky="NW")
	but3.grid(row=4, column=1, padx=pad[0], pady=pad[1], sticky="NW")
	but4.grid(row=5, column=1, padx=pad[0], pady=pad[1], sticky="NW")
	but5.grid(row=4, column=2, padx=pad[0], pady=pad[1], sticky="NW")
	labx.grid(row=5, column=2, padx=pad[0], pady=pad[1], sticky="NW")
	#----------------------------
	root.bind("a"+"f", exit_make)
	root.mainloop()
main_frame()