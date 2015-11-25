# -*- coding: utf-8 -*-
# BY Tizian Pessel
# CONTACT mail@tizian.com.de
# LICENSE do not distribute
# VER 1
prog_version = "1.0.0"
# DATE 17.07.2015
# http://www.way2python.de/unsortiert/tkwidgetprint.py


import win32ui, win32print, win32con
import Image as Img
import ImageWin, ImageGrab
import MySQLdb as mdb
from Tkinter import *
import random, string
import tkMessageBox
import ConfigParser
import PIL.ImageTk
import tkFileDialog
import PIL.Image
import base64
import hashlib
import shutil
import ftplib
import urllib
import time
import sha
import ttk
import os


def mdb_error(e=False):
	if e == False:
		pass
	eno = str(e).split(",")[0].replace("(", "")
	if eno == "2003":
		tkMessageBox.showerror(title="CR_CONN_HOST_ERROR",
		message="Kann nicht zum MySQL-Server verbinden.")
		config_exit()
	else:
		tkMessageBox.showerror(title="ERROR",
		message="Undefinierter MDB Error: "+e)

def config_exit(NONE=[]):
	global root, con
	if con != "":
		con.close()
	root.destroy()
	os._exit(0)
	
def db_execute(sql):
	global con, cur, settings, account
	try:
		cur.execute(sql)
	except mdb.Error, e:
		print "MDB ERROR: ", e
	except mdb.Warning, e:
		print "MDB WARNING: ", e
	
	if sql.split(" ")[0].upper() != "SHOW":
		con.commit()
	# Logging
	#TODO: Logging ins Rechteabfragesystem einbauen.
	
def db(action="", arg1=False, arg2=False, arg3=False, arg4=False):
	global con, cur, settings, account
	if con == "":
		try:
			con = mdb.connect(settings["db_server"], settings["db_user"], settings["db_password"], settings["db_name"]);
		except mdb.Error as e:
			mdb_error(e)
		cur = con.cursor()
	#----
	do = action.split("|")[0]
	if len(action.split("|")) > 1:
		com = action.split("|")[1]
		columns = com.split("}")[0].split(" ")
		word = com.split("}")[1]
		text = " WHERE "
		for i in columns:
			text = text + " `"+i+"` LIKE '%"+word+"%' OR"
		filter = text[:-3]
		
	else:
		filter = False
	if do == "account_check":
		sql = "SELECT `password` FROM `user` WHERE `username`='" + arg1 + "'" #TODO: Passwort verschlüsseln
		db_execute(sql)
		fetch = cur.fetchall()
		if fetch == ():
			return False
		elif fetch[0][0] == arg2:
			return True
		else:
			return False
	elif do == "init_settings":
		sql = "SELECT * FROM `settings` WHERE 1"
		db_execute(sql)
		for i in cur.fetchall():
			settings[i[0]] = i[1]
		return True
	elif do == "get_user_name":
		sql = "SELECT `name` FROM `user` WHERE `ID`='" + arg1 + "'"
		db_execute(sql)
		fetch = cur.fetchone()
		if fetch == None:
			return ""
		else:
			return fetch[0]
	elif do == "get_user_username":
		sql = "SELECT `username` FROM `user` WHERE `ID`='" + arg1 + "'"
		db_execute(sql)
		return cur.fetchone()[0]
	elif do == "get_user_jobs":
		roles = db(action="get_user_roles", arg1=arg1)
		sql = "SELECT * FROM `jobs` WHERE "
		for r in roles:
			sql = sql + "`for_ID` LIKE '%{0}%' OR ".format(r)
		sql = sql[:-4] + ";"
		db_execute(sql)
		return cur.fetchall()
	elif do == "get_user":
		sql = "SELECT * FROM `user` WHERE `username`='" + arg1 + "'"
		db_execute(sql)
		return cur.fetchone()
	elif do == "get_users":
		sql = "SELECT `ID`,`username`,`name`,`imagefiletype`,`roles`,`created`,`created_by`, `usergroup` FROM `user`"
		if filter == False:
			db_execute(sql)
			return cur.fetchall()
		else:
			sql = sql + filter
			db_execute(sql)
			return cur.fetchall()
	elif do == "get_user_id":
		sql = "SELECT `ID` FROM `user` WHERE `username`='" + arg1 + "'"
		db_execute(sql)
		return cur.fetchone()[0]
	elif do == "get_roles_name":
		sql = "SELECT `rolename` FROM `roles` WHERE `ID`='" + arg1 + "'"
		db_execute(sql)
		return cur.fetchone()
	elif do == "get_roles":
		sql = "SELECT * FROM `roles` WHERE 1"
		db_execute(sql)
		return cur.fetchall()
	elif do == "get_user_roles":
		sql = "SELECT `roles` FROM `user` WHERE `ID`='" + arg1 + "'"
		db_execute(sql)
		return cur.fetchall()[0][0].replace(" ", "").split(",")
	elif do == "get_user_image":
		sql = "SELECT `image`,`imagefiletype` FROM `user` WHERE `ID`='{0}'".format(arg1)
		db_execute(sql)
		image = cur.fetchone()
		if image[0] == "":# Keine Datei in der DB
			return "./images/noavatar.png"
		file = "{0}.{1}".format(image[0], image[1])
		if os.path.isfile(file) == True:# Datei bereits geladen
			return "./images/cache/{0}".format(file)
		else: #Datei laden
			ftp_download(image)
			return "./images/cache/{0}".format(file)
	elif do == "get_nodes":
		sql = "SELECT `ID`, `name`,`adress`,`created`,`created_by`,`image`,`imagefiletype` FROM `nodes` WHERE 1;"
		db_execute(sql)
		return cur.fetchall()
	# SET section
	elif do == "set_image":
		max = {"user":(160, 160),
			"nodes":(300, 200)}
		arg1 = make_thumnail(arg1, (max[arg3][0], max[arg3][1]))
		hash, mime = ftp_upload(arg1)
		sql = "UPDATE `{3}` SET `image`='{0}', `imagefiletype`='{1}' WHERE `ID`='{2}'".format(hash, mime, arg2, arg3)
		db_execute(sql)
	elif do == "set_user_username":
		sql = "UPDATE `user` SET `username`='{0}' WHERE `ID`='{1}'".format(arg1, arg2)
		db_execute(sql)
		if arg2 == account[0]: #Logout bei ändern von eigenen Daten!
			tkMessageBox.showinfo(title="Hinweis", message="Änderung erfolgreich!\nAus Sicherheitsgründen werden Sie jetzt ausgeloggt!")
			account_logout()
		return cur.fetchone()
	elif do == "set_user_password" or do == "set_user_passwort":
		sql = "UPDATE `user` SET `password`='{0}' WHERE `ID`='{1}'".format(arg1, arg2)
		db_execute(sql)
		if arg2 == account[0]: #Logout bei ändern von eigenen Daten!
			tkMessageBox.showinfo(title="Hinweis", message="Änderung erfolgreich!\nAus Sicherheitsgründen werden Sie jetzt ausgeloggt!")
			account_logout()
		return cur.fetchone()
	elif do == "set_user_name":
		sql = "UPDATE `user` SET `name`='{0}' WHERE `ID`='{1}'".format(arg1, arg2)
		db_execute(sql)
		if arg2 == account[0]:
			tkMessageBox.showinfo(title="Hinweis", message="Änderung erfolgreich!\nAus Sicherheitsgründen werden Sie jetzt ausgeloggt!")
			account_logout()
		return cur.fetchone()
	elif do == "set_user_roles":
		if len(arg1) > 0:
			sql = "UPDATE `user` SET `roles`='"
			for i in arg1:
				sql = sql + i + ", "
			sql = sql[:-2] + "' WHERE `ID`='{0}'".format(arg2)
		else:
			sql = "UPDATE `user` SET `roles`='' WHERE `ID`='{0}'".format(arg2)
		db_execute(sql)
		if arg2 == account[0]: #Logout bei ändern von eigenen Daten!
			tkMessageBox.showinfo(title="Hinweis", message="Änderung erfolgreich!\nAus Sicherheitsgründen werden Sie jetzt ausgeloggt!")
			account_logout()
		return cur.fetchone()
	elif do == "set_job_mark":
		sql = "SELECT `done` FROM `jobs` WHERE `ID`='{0}';".format(arg1)
		db_execute(sql)
		sql = "UPDATE `jobs` SET `done` = '{0}' WHERE `ID` = '{1}';".format("0" if int(cur.fetchone()[0]) == 1 else "1", arg1)
		db_execute(sql)
	# INSERT section
	elif do == "insert_user":
		sql = "INSERT INTO `user` (`ID`, `username`, `password`, `name`, `image`, `imagefiletype`, `roles`, `created`, `created_by`) VALUES (NULL, '{username}', '{pw}', '{name}', NULL, '', '', CURRENT_TIMESTAMP, '{by}');".format(**arg1)
		db_execute(sql)
		return
	elif do == "insert_job":
		sql = "INSERT INTO `eschaton`.`jobs` (`ID`, `name`, `description`, `priority`, `for_ID`, `done`, `created`, `created_by`) VALUES (NULL, '{name}', '{desc}', '{prio}', '{for}', '0', CURRENT_TIMESTAMP, '{by}');".format(**arg1)
		db_execute(sql)
		return
	# DELETE section
	elif do == "delete_user":
		sql = "INSERT INTO `user_deleted` SELECT*, CURRENT_TIME(), '{0}' FROM `user` WHERE `ID`='{1}'".format(account[0], arg1)
		db_execute(sql)
		sql = "DELETE FROM `user` WHERE `ID`='{0}';".format(arg1)
		db_execute(sql)
		if arg1 == account[0]: #Logout bei ändern von eigenen Daten!
			tkMessageBox.showinfo(title="Hinweis", message="Änderung erfolgreich!\nAus Sicherheitsgründen werden Sie jetzt ausgeloggt!")
			account_logout()
		return
	elif do == "delete_job":
		sql = "INSERT INTO `jobs_deleted` SELECT*, CURRENT_TIME(), '{0}' FROM `jobs` WHERE `ID`='{1}'".format(account[0], arg1)
		db_execute(sql)
		sql = "DELETE FROM `jobs` WHERE `ID`='{0}';".format(arg1)
		db_execute(sql)
		return
	elif do == "delete_user_image":
		sql = "UPDATE `user` SET `image`='', `imagefiletype`='' WHERE `ID`='{0}'".format(arg1)
		db_execute(sql)
		return
	else:
		return

def ftp_upload(file):
	#ftp Create and Login
	ftp = ftplib.FTP("192.168.3.47")
	ftp.login("eschaton", "test123")
	#file
	mime = os.path.splitext(file)[1].replace(".", "")
	f = open(file, "rb")
	#gethash
	hash = hashlib.sha224(f.read()).hexdigest()
	#file
	f.close()
	f = open(file, "rb")
	#upload
	ftp.storbinary("STOR {0}".format(hash), f, 1024)
	f.close()
	return hash, mime
	
def ftp_download(file):
	if type(file) == vartype["str"]:
		file = file.split(".")
	#file=[filename, filetype]
	#ftp Create and Login
	ftp = ftplib.FTP("192.168.3.47")
	ftp.login("eschaton", "test123")
	#file
	f = open("./images/cache/{0}.{1}".format(file[0], file[1]), "wb")
	#download
	ftp.retrbinary("RETR {0}".format(file[0]), f.write)
	f.close()
	return

def clear_cache():
	shutil.rmtree("./images/cache", ignore_errors=True)
	os.makedirs("./images/cache")
def make_thumnail(infile, size):
	#Workaround, weil das fileobject von Image nicht geschlossen wird
	#temp_file = "./images/cache/{0}.cache".format(str(int(time.time())))
	outfile = "./images/cache/temp.jpg"
	if infile != outfile:
		im = Img.open(infile)
		im.thumbnail(size, Img.ANTIALIAS)
		im.save(outfile, "JPEG")
		#
		#
		f = open(outfile, "rb")
		hash = hashlib.sha224(f.read()).hexdigest()
		newname = outfile.replace("temp", hash)
		f.close()
		if os.path.isfile(newname) == True:# Datei bereits vorhanden
			os.remove(newname)
		os.rename(outfile, newname)
		return newname

def account_login(NONE=[]):
	global account, objects
	if db(action="account_check", arg1=objects[2].get(), arg2=objects[3].get()) == True:
		id = str(db(action="get_user_id", arg1=objects[2].get()))
		user_name = db(action="get_user_name", arg1=id)
		account = [id, objects[2].get(), user_name]
		root.title("Eschaton Client - {0}".format(user_name))
		tab_open_login()
	elif objects[2].get() == "" and objects[3].get() == "":
		pass
	else:
		tkMessageBox.showerror(title="Login Fehler", message="Kein Account konnte diesem Passwort zugeordnet werden.\nBitte überprüfen Sie Ihre Eingaben.")

def account_logout(NONE=[]):
	global account, objects
	account = [0, "", "", ""]
	tab_open_login()
	root.title("Eschaton Client - Kein Benutzer")
	tkMessageBox.showinfo(title="Logout", message="Sie wurden erfolgreich ausgeloggt!")

def init_vars():
	global tab_buttons, frames, geo, pad, tab_button_names, objects, active_tab, active_tab_widget, active_tab_name, con, account, tag, settings, vartype
	tab_button_names = [
	"Aufträge",
	"Lager",
	"Produkte",
	"Standorte",
	"Mitarbeiter",
	"Einstellungen",
	"Login"
	]
	objects = []
	active_tab = -1
	active_tab_widget = None
	active_tab_name = ""
	# id, username, readable_name
	account = [0, "", "", ""]
	con = ""
	tag = {}
	init_settings()
	#System
	vartype = {"str":"",
		"tuple":(0, 1),
		"list":[],
		"int":0,
		"float":1.0,
		"bool":True}

def init_settings(): 
	global settings
	settings = {
	"db_server":"192.168.3.47",
	"db_user":"root",
	"db_password":"test123",
	"db_name":"eschaton",
	"node_id":1,
	"sql_log_UPDATE":"0",
	"sql_log_INSERT":"0",
	"sql_log_DELETE":"0",
	"sql_log_SHOW":"0",
	"bg_color":"#FFFFFF",
	"bg_color_button":"#999999",
	"bg_color_list":"#AEAEAE",
	}
	
def init_window():
	global tab_buttons, frames, c, geo, settings, root, style
	#Styles
	style = ttk.Style()
	style.configure('TFrame', background=settings["bg_color"], relief="groove", borderwidth=5)
	style.configure('TLabelframe', background=settings["bg_color"], relief="raised", borderwidth=50)
	style.configure('TLabelframe.Label', background=settings["bg_color"], foreground="#000000")
	style.configure('TButton', relief="flat", borderwidth=0,
	background="#FFFFFF",
	activebackground="#FF0000",
	foreground="#00FF00",
	highlightbackground="#0000FF",
	highlightcolor="#F00F0F",
	overrelief="sunken"
	)
	root.configure(bg=settings["bg_color"])
	main_frame.config(bg=settings["bg_color"])
	button_frame.config(bg=settings["bg_color"])
	query_frame.config(bg=settings["bg_color"])
	for i in frames.keys():
		frames[i].config(bg=settings["bg_color"])
	hub.select(len(tab_button_names)-1) #Call Login Tab
	change_tab()
		
def destroy_objects(classes=["all"], object=None):
	global objects, tag, frames
	if object != None:
		object.destroy()
		objects.pop(objects.index(object))
		tag.pop(object)
		for i in tag.keys():
			if tag[i] == object:
				tag.pop(i)
		return
	for j in classes:
		if j == "all":
			for i in objects:
				i.destroy()
				objects = []
			tag = {}
		if j == "mitarbeiter_treeview_entry":
			try:
				object = tag["mitarbeiter_edit_entry"]
				object.destroy()
				objects.pop(objects.index(object))
				tag.pop(object)
				for i in tag.keys():
					if tag[i] == object:
						tag.pop(i)
			except:
				pass
				
def treeview(instance=False, action=False, options=False):
	global settings, objects, tag, global_treeview_instance
	if instance == False and action != "create":
		print "Treeview(): Keine Instanz übergeben!"
		return
	if action == False:
		print "Treeview(): Keine Aktion übergeben!"
		return
	if options == False:
		print "Treeview(): Keine Optionen übergeben!"
		return
	o = options.copy()
	#---
	if action == "create":
		#Create Instance
		cols = []
		for i in o["columns"]:
			cols.append(i[0])
		if cols[0] != "#0" and cols[0] != "":
			print "Treeview(): Erste Spalte ist nicht als '#0' definiert!"
		cols_rest = cols
		cols_rest.pop(0)
		if o.has_key("selectmode") == True: #extended, browse, none
			sel = o["selectmode"]
		else:
			sel = "browse"
		tree = ttk.Treeview(o["parent"], height=o["height"], columns=(cols_rest), selectmode=sel)
		#Setting Columns
		for i in o["columns"]:
			tree.column(i[0], width=i[1])
			tree.heading(i[0], text=i[2])
		#Inserting Rows
		n = 0
		tree.tag_configure(0, background=settings["bg_color_list"])
		tree.tag_configure(1, background=settings["bg_color"])
		tree.tag_configure("no_edit", background="#FFFFFF", foreground=settings["bg_color_button"])
		tree.tag_configure("fg_red", foreground="#ee9090")
		tree.tag_configure("fg_green", foreground="#008844")
		for i in o["rows"]:
			if i[0] == "":
				iid = str(i[1])
				level = "parent"
			else:
				iid = None
				level = "child"
			vals = []
			first = 1
			for j in i[2]:
				if first == 1:
					first = 0
					continue
				vals.append(j)
			vals = tuple(vals)
			if len(i) > 4:
				op = i[4]
			else:
				op = True
			if iid != None:
				op = False
			#Tagging
			taggs = []
			if level == "parent":
				taggs.append(n)
				if n == 0:
					n = 1
				else:
					n = 0
			if len(i) > 3:
				for k in i[3]:
					taggs.append(k)
			taggs = tuple(taggs)
			if len(i) > 5:
				tree.insert(str(i[0]), "end", iid, text=i[2][0], values=vals, tags=taggs, open=op, image=i[5])
			else:
				tree.insert(str(i[0]), "end", iid, text=i[2][0], values=vals, tags=taggs, open=op)
		#Placing
		if o["manager"] == "grid":
			if o.has_key("row") == False:
				o.update({"row":1})
			if o.has_key("column") == False:
				o.update({"column":1})
			if o.has_key("columnspan") == False:
				o.update({"columnspan":1})
			if o.has_key("sticky") == False:
				o.update({"sticky":"NESW"})
			tree.grid(row=o["row"], column=o["column"], padx=4, pady=2, columnspan=o["columnspan"], sticky=o["sticky"])
		elif o["manager"] == "place":
			if o.has_key("x") == False:
				print "Treeview(): Als Manager wurde 'place' gewählt. Schlüssel 'x' wurde nicht übergeben!"
				return
			if o.has_key("y") == False:
				print "Treeview(): Als Manager wurde 'place' gewählt. Schlüssel 'y' wurde nicht übergeben!"
				return
			tree.place(x=o["x"], y=o["y"])
		else:
			tree.pack()
		#Filter
		if o["filter"] == True:
			if o.has_key("query_count") == False:
				print "Treeview(): Ein Filter wurde gewählt. Schlüssel 'query_count' wurde nicht übergeben!"
				return
			e = Entry(query_frame)
			e.grid(row=1, column=1, padx=4, pady=2, columnspan=1, sticky="W")
			objects.append(e)
			tag.update({"filter":e})
			
			b = Button(query_frame, padx=4, pady=2, text="Filtern", command=lambda: button_press(id="treeview_filter"))
			b.grid(row=1, column=2, padx=4, pady=2, columnspan=1, sticky="W")
			objects.append(b)
			
			s = ttk.Separator(query_frame,orient=VERTICAL)
			s.grid(row=1, column=3, padx=4, pady=2, columnspan=1, sticky="W")
			objects.append(s)
			
			l = Label(query_frame, bg=settings["bg_color"], padx=4, pady=2, text="Ergebnisse: "+str(o["query_count"]))
			l.grid(row=1, column=4, padx=4, pady=2, columnspan=1, sticky="W")
			objects.append(l)
		#Binds
		tree.bind("<Delete>", treeview_key_event_delete)
			
	#
	objects.append(tree)
	global_treeview_instance = tree
	return tree
	
def action_buttons(action=False, functions=False):
	global objects, settings, actionbutton
	if action == False:
		return
	if action == "create":
		actionbutton = {}
		# Standartbuttons
		if functions == False:
			functions = "AD"
		#Bilder
		act_buttons = {
			"img_file_add":"./images/plus.png",
			"img_file_rem":"./images/bin.png",
			"img_file_edit":"./images/pencil.png",
			"img_file_prin":"./images/printer.png",
			"img_file_mark":"./images/checkmark.png",
			"img_file_none":"./images/info.png"}
		n = 0
		for i in functions:
			i = i.upper()
			type = "none"
			n = n + 1
			if i == "A":
				type = "add"
			if i == "R" or i == "D":
				type = "rem"
			if i == "P":
				type = "prin"
			if i == "M" or i == "F":
				type = "mark"
			if i == "E":
				type = "edit"
			if i == "S":
				sep = ttk.Separator(button_frame, orient=VERTICAL)
				sep.grid(row=2, column=n, padx=0, pady=0, sticky="NS")
				objects.append(sep)
				continue
			root.update()
			image = PIL.ImageTk.PhotoImage(PIL.Image.open(act_buttons["img_file_{0}".format(type)]))
			but = Button(button_frame, image=image, bg=settings["bg_color"], text="action_{0}".format(type), relief=FLAT, width=80, height=45)
			but.image = image
			but.grid(row=2, column=n, padx=0, pady=0, sticky="NW")
			objects.append(but)
			actionbutton[type] = but
			del but
		return
		
def treeview_get_selection_info(event=False): #TODO: IndexError wenn man auf bereits vorhandenes entry klickt
	global tree
	if event == False:
		dict = {
			"id":tree.selection()[0],
			"text":tree.item(tree.selection()[0])["values"][0],
			"rowname":str(tree.item(tree.selection()[0])["text"]).split(":")[0].lower(),
			"index":tree.index(tree.selection()[0]),
			"parent":tree.parent(tree.selection()[0])} if len(tree.selection()) != 0 else False
	elif event == "Mitarbeiter":
		dict = {
			"id":tree.selection()[0],} if len(tree.selection()) != 0 else False
	else:
		dict = {
			"id":tree.selection()[0],
			"row":tree.identify_row(event.y),
			"column":tree.identify_column(event.x),
			"x":tree.bbox(tree.identify_row(event.y), tree.identify_column(event.x))[0],
			"y":tree.bbox(tree.identify_row(event.y), tree.identify_column(event.x))[1],
			"width":tree.bbox(tree.identify_row(event.y),tree.identify_column(event.x))[2],
			"text":tree.item(tree.selection()[0])["values"][0],
			"rowname":str(tree.item(tree.selection()[0])["text"]).split(":")[0].lower(),
			"index":tree.index(tree.selection()[0]),
			"parent":tree.parent(tree.selection()[0])} if len(tree.selection()) != 0 else False
	return dict
	

def entry_popup_button_image():
	global popup, popup_objects
	filepath = tkFileDialog.askopenfilename(parent=popup, filetypes=[("JPEG", ".jpg"), ("PNG", ".png"), ("GIF", ".gif")])
	if filepath != False:
		dateiname = filepath.split("/")[len(filepath.split("/"))-1]
		for i in popup_objects.keys():
			if i.split("_")[0] == "imagebutton":
				popup_objects[i].config(text=dateiname)
				popup_objects.update({"file_"+i.split("_")[1]:filepath})

def entry_popup_return(event):
	global popup_objects, popup_results, account, popup
	for i in popup_objects.keys():
		if i.split("_")[0] == "entry":
			popup_results.update({i.split("_")[1]:popup_objects[i].get()})
		elif i.split("_")[0] == "text":
			popup_results.update({i.split("_")[1]:popup_objects[i].get("1.0", END)})
		elif i.split("_")[0] == "file":
			if type(popup_objects[i]) != type(False):
				f = str(mdb.escape_string(open(popup_objects[i], "rb").read()))
				popup_results.update({i.split("_")[1]:popup_objects[i]})
		if i.split("_")[0] == "number":
			popup_results.update({i.split("_")[1]:popup_objects[i].get()})
		else:
			pass
	popup_results.update({"by":str(account[0])})
	#
	if tab_button_names[active_tab] == "Mitarbeiter":
			if popup_results["username"] != "" and popup_results["pw"] != "" and popup_results["name"] != "":
				db(action="insert_user", arg1=popup_results)
				if popup_results["photo"] != "":
					userid = db(action="get_user", arg1=popup_results["username"])[0]
					db(action="set_image", arg1=popup_results["photo"], arg2=userid, arg3="user")
					pass
			else:
				tkMessageBox.showerror(title="Fehler", message="Bitte füllen sie alle Angaben aus, die mit * gekennzeichnet sind!")
				popup.focus()
				return
			tab_open_mitarbeiter()
	elif tab_button_names[active_tab] == "Aufträge":
			if popup_results["name"] != "" and popup_results["prio"] != "" and popup_results["for"] != "":
				db(action="insert_job", arg1=popup_results)
			else:
				tkMessageBox.showerror(title="Fehler", message="Bitte füllen sie alle Angaben aus, die mit * gekennzeichnet sind!")
				popup.focus()
				return
			tab_open_auftraege()
	popup.destroy()
	return
	
def entry_popup_esc(event):
	global popup
	text = "Sind Sie sicher, dass Sie das Fenster schließen möchten?\nAlle nicht gespeicherten Änderungen gehen verloren!"
	if tkMessageBox.askyesno(title="Bitte bestätigen!", message=text) == True:
		popup.destroy()

def entry_popup(options=False):
	global settings, popup, root, popup_objects, popup_results
	if options == False:
		return popup_results
	else:
		o = options.copy()
	popup_objects = {}
	popup_results = {}
	#Toplevel window
	popup = Toplevel()
	popup.title("Eingabe")
	fpopup = Frame(popup, width=popup.winfo_width(), height=popup.winfo_height(), bg=settings["bg_color"])
	fpopup.pack()
	# Elements
	for i in o.keys():
		if i.split("_")[0] != "type":
			if o.has_key("type_"+i) == False:
				o.update({"type_"+i:"normal"})
	n = 0
	first = 0
	for i in o.keys():
		if i.split("_")[0] != "type" and i.split("_")[0] != "option":
			n = n + 1
			lab = Label(fpopup, bg=settings["bg_color"], text=o[i]+":")
			lab.grid(row=n, column=1, padx=20, pady=5, sticky="NW")
			#
			if o["type_"+i] == "password":
				e = Entry(fpopup, show="*", width=30)
				popup_objects.update({"entry_"+i:e})
			elif o["type_"+i] == "big":
				e = Text(fpopup, height=4, width=30, relief=SUNKEN)
				popup_objects.update({"text_"+i:e})
			elif o["type_"+i] == "image":
				e = Button(fpopup, text="Datei", command=entry_popup_button_image, bg=settings["bg_color"])
				popup_objects.update({"imagebutton_"+i:e})
				popup_objects.update({"file_"+i:False})
			elif o["type_"+i] == "slider":
				option = o["option_"+i].split("-")
				e = Scale(fpopup, from_=option[0], to=option[1], orient=HORIZONTAL,
				bg=settings["bg_color"], #weiß
				troughcolor=settings["bg_color_list"], #grau
				activebackground=settings["bg_color_button"], #grau
				highlightbackground=settings["bg_color"], #weiß
				)
				popup_objects.update({"number_"+i:e})
			else:
				e = Entry(fpopup, width=30)
				popup_objects.update({"entry_"+i:e})
			e.grid(row=n, column=2, padx=20, pady=5, sticky="NW")
			if first == 0:
				e.focus()
				first = 1
	but = Button(fpopup, text="   Fertig   ", command=lambda: entry_popup_return(event=False))
	but.grid(row=n+1, column=3, padx=20, pady=5, sticky="NW")
	hin = Label(fpopup, bg=settings["bg_color"], text="mit * gekennzeichnete Felder müssen ausgefüllt werden", fg=settings["bg_color_list"])
	hin.grid(row=n+1, column=1, padx=20, pady=5, columnspan=2, sticky="NW")
	#----------------------------
	#popup.bind("<Return>", entry_popup_return)
	popup.bind("<Escape>", entry_popup_esc)
	popup.grab_set()
	popup.mainloop()
	
def role_popup_refresh_lb():
	global popup, lb_server, lb_account, popup_id
	lb_server.delete(0, END)
	lb_account.delete(0, END)
	result =  db(action="get_user_roles", arg1=popup_id)
	notempty = False
	if len(result) > 0 and result[0] != "":
		notempty = True
		for i in result:
			lb_account.insert(END, "["+i+"] "+db(action="get_roles_name", arg1=i)[0])
	#
	result2 =  db(action="get_roles")
	cont = False
	for i in result2:
		if notempty == True:
			for j in result:
				if i[1] == db(action="get_roles_name", arg1=j)[0]:
					cont = True
			if cont == True:
				cont = False
				continue
		lb_server.insert(END, "["+str(i[0])+"] "+i[1])

def role_popup_exit(event=None):
	global popup
	popup.destroy()
	if tab_button_names[active_tab] == "Mitarbeiter":
		tab_open_mitarbeiter()
	
def role_popup_action(event=None):
	global popup, lb_server, lb_account, popup_id
	if event == None:
		return
	#
	if event == "left":
		if len(lb_account.curselection()) == 1:
			result = db(action="get_user_roles", arg1=popup_id)
			sel = lb_account.get(lb_account.curselection()).split(" ")[0].replace("[", "").replace("]", "")
			try:
				result.pop(result.index(sel))
			except ValueError:
				pass
			db(action="set_user_roles", arg1=result, arg2=popup_id)
	elif event == "right":
		if len(lb_server.curselection()) == 1:
			result = db(action="get_user_roles", arg1=popup_id)
			sel = lb_server.get(lb_server.curselection()).split(" ")[0].replace("[", "").replace("]", "")
			result.append(sel)
			while True:
				try:
					result.pop(result.index(""))
				except ValueError:
					break
			db(action="set_user_roles", arg1=result, arg2=popup_id)
	elif event == "ok":
		role_popup_exit()
	if event != "ok":
		role_popup_refresh_lb()

def role_popup_button_1(event):
	global popup, lb_server, lb_account
	if event.widget == lb_server:
		role_popup_action(event="right")
	elif event.widget == lb_account:
		role_popup_action(event="left")
	
def role_popup(id):
	global account, popup, listbox, settings, lb_server, lb_account, popup_id
	popup_id = id
	#Toplevel Window
	popup = Tk()
	popup.protocol("WM_DELETE_WINDOW", role_popup_exit)
	popup.title("Rolleneditor")
	fpopup = Frame(popup, width=popup.winfo_width(), height=popup.winfo_height(), bg=settings["bg_color"])
	fpopup.pack()
	#Content
	lb_server = Listbox(fpopup, selectmode=SINGLE)
	lb_account = Listbox(fpopup, selectmode=SINGLE)
	left = Button(fpopup, text="<--", command=lambda: role_popup_action(event="left"))
	right = Button(fpopup, text="-->", command=lambda: role_popup_action(event="right"))
	ok = Button(fpopup, text="Ok", command=lambda: role_popup_action(event="ok"))
	lab = Label(fpopup, bg=settings["bg_color"], text=db(action="get_user_username", arg1=popup_id))
	sep = ttk.Separator(fpopup,orient=HORIZONTAL)
	lab2 = Label(fpopup, bg=settings["bg_color"], text="Achtung! Änderungen werden sofort übernommen.", fg=settings["bg_color_list"])
	#
	lb_server.grid(row=3, column=1, padx=20, pady=5, sticky="NESW", rowspan=4)
	lb_account.grid(row=3, column=3, padx=20, pady=5, sticky="NESW", rowspan=4)
	left.grid(row=4, column=2, padx=20, pady=5, sticky="EW")
	right.grid(row=3, column=2, padx=20, pady=5, sticky="EW")
	ok.grid(row=8, column=3, padx=20, pady=5, sticky="EW")
	lab.grid(row=2, column=3, padx=20, pady=5, sticky="NESW")
	sep.grid(row=7, column=1, padx=20, pady=5, sticky="NS")
	lab2.grid(row=1, column=1, padx=20, pady=5, sticky="NW", columnspan=3)
	# LB Contents
	role_popup_refresh_lb()
	#Main
	lb_server.bind("<Double-Button-1>", role_popup_button_1)
	lb_server.bind("<Return>", role_popup_button_1)
	lb_account.bind("<Double-Button-1>", role_popup_button_1)
	lb_account.bind("<Return>", role_popup_button_1)
	popup.bind("<F5>", lambda: role_popup_action(event="refresh"))
	popup.mainloop()

def detail_frame(options=False):
	global detail_frame_object, detail_frame_data, objects
	if options == False:
		detail_frame_object.destroy()
		detail_frame_object = None
		detail_frame_data = {}
		return True
	else:
		if "detail_frame_data" in globals():
			pass
		else:
			detail_frame_data = {}
		if len(detail_frame_data) == 0:
			detail_frame_data = {
				"width":512,
				"height":614,
				"row":1,
				"column":1
			}
		for i in options.keys():
			detail_frame_data.update({i:options[i]})
		dfd = detail_frame_data.copy()
	# Frame
	detail_frame_object = ttk.Labelframe(active_tab_widget, width=dfd["width"], height=dfd["height"], text=" Details ")
	detail_frame_object.grid(column=dfd["column"], row=dfd["row"])
	detail_frame_object.grid_propagate(False)
	#Elements
	row = 0
	keys = sorted(dfd.keys())
	for key in keys:
		if key.split("_")[0] == "field":
			if dfd[key][0] == "label":
				dfd[key+"__title"] = Label(detail_frame_object, text=dfd[key][1]+":", font="Arial 14", background='#FFFFFF')
				dfd[key+"__title"].grid(row=row+1, column=1, padx=10, pady=5, columnspan=2, sticky="NW")
				dfd[key+"__content"] = Label(detail_frame_object, text=dfd[key][2], font="Arial 10", background='#FFFFFF')
				dfd[key+"__content"].grid(row=row+2, column=1, padx=10, pady=5, columnspan=2, sticky="NW")
				row = row + 2
			elif dfd[key][0] == "title":
				dfd[key+"__title"] = Label(detail_frame_object, text=dfd[key][1], font="Arial 14", background='#FFFFFF')
				dfd[key+"__title"].grid(row=row+1, column=1, padx=10, pady=5, columnspan=2, sticky="NW")
				row = row + 1
			elif dfd[key][0] == "list":
				if dfd.has_key(key+"__listcount") == False:
					dfd[key+"__listcount"] = 0
					item_key = key+"__item_"+str(dfd[key+"__listcount"])
				dfd[item_key+"_0"] = Label(detail_frame_object, text=dfd[key][1]+":", font="Arial 10", background='#FFFFFF')
				dfd[item_key+"_1"] = Label(detail_frame_object, text=dfd[key][2], font="Arial 10", background='#FFFFFF')
				dfd[item_key+"_0"].grid(row=row+1, column=1, padx=10, pady=5, columnspan=1, sticky="NW")
				dfd[item_key+"_1"].grid(row=row+1, column=2, padx=10, pady=5, columnspan=1, sticky="NW")
				row = row + 1
			else:
				print "detail_frame_object(): Unknown fieldtype >{0}<".format(dfd[key][0])
	objects.append(detail_frame_object)
	
def print_widget__grabwidget(widget):
	# grabs widget and stores it as a file 
	x = widget.winfo_rootx()
	y = widget.winfo_rooty()
	w = widget.winfo_width()
	h = widget.winfo_height()
	return ImageGrab.grab((x, y, x+w, y+h))
	
def print_widget(widget):
	widget.update()
	widget.update_idletasks()
	image = print_widget__grabwidget(widget)
	image.save("./images/tmp.bmp")
	
	# Creates a Dib instance from grabbed file
	im = Img.open("./images./tmp.bmp")
	dib = ImageWin.Dib('RGB',im.size)
	dib.paste(im,None)
	imagesize = (im.size[0]*10, im.size[1]*10) 
	
	# Sends the dib to the windows standard printer
	printer = win32print.GetDefaultPrinter()
	tkMessageBox.showinfo(title="Druckvorgang eingereiht!",
		message="Der Auftrag wurde an den Drucker '{0}' gesendet!".format(printer))
	phandle = win32print.OpenPrinter(printer)
	dc = win32ui.CreateDC()
	dc.CreatePrinterDC()
	dc.StartDoc(im.filename)
	dc.StartPage()
	dib.draw(dc.GetHandleAttrib(), (0, 0) + imagesize)  # output size can be changed
	dc.EndPage()										# by modifying the im.size tuple										   
	dc.EndDoc()
	win32print.ClosePrinter(phandle)
	del dc
	del im
	os.unlink("./images/tmp.bmp")
	
def tfi(type=False, data=False):
	if type == "M.roles":
		roles = []
		for i in data.split(","):
			for j in i.split(" "):
				if len(j) > 0:
					roles.append(j[0])
		text=""
		for i in roles:
			rolename = db(action="get_roles_name", arg1=i)
			if rolename == None:
				continue
			text = text + rolename[0] + ", "
		text = text[:-2]
	elif type == "S.user":
		text = db(action="get_user_username", arg1=str(data))
	else:
		return ""
	return text

def button(event):
	pass
def button_press(id=False, arg=""):
	global objects, tag
	#
	if id == 1:
		account_login()
	elif id == 2:
		account_logout()
	elif id == "treeview_filter":
		if tab_button_names[active_tab] == "Mitarbeiter":
			text = tag["filter"].get()
			tab_open_mitarbeiter(db_request="get_users|username name ID imagefiletype created created_by}{0}".format(text))
	elif id == "action_add":
		if tab_button_names[active_tab] == "Mitarbeiter":
			dict = {
				"username":"Benutzername*",
				"name":"Name*",
				"pw":"Passwort*",
				"photo":"Foto",
				"type_pw":"password",
				"type_photo":"image",}
			entry_popup(options=dict)
		elif tab_button_names[active_tab] == "Aufträge":
			dict = {
				"name":"Name*",
				"desc":"Beschreibung*",
				"prio":"Priorität",
				"for":"Für",
				"type_desc":"big",
				"type_for":"pick_group",
				"type_prio":"slider",
				"option_prio":"1-10"}
			entry_popup(options=dict)
	elif id == "action_rem":
		if tab_button_names[active_tab] == "Mitarbeiter":
			sel = treeview_get_selection_info()
			if sel == False:
				return
			if sel["parent"] == "":
				if tkMessageBox.askyesno(title="Bitte bestätigen", message="Wollen Sie sicher die ausgewählten Elemente unwiederruflich löschen?") == True:
					db(action="delete_user", arg1=sel["id"])
					if account[0] != 0:
						tab_open_mitarbeiter()
			else:
				if sel["rowname"] == "bild":
					db(action="delete_user_image", arg1=account[0])
					tree.item(sel["id"], values=("Nein", ""))
		elif tab_button_names[active_tab] == "Aufträge":
			if job != False:
				ask = tkMessageBox.askyesnocancel(title="Wirklich Löschen?",
					message="Möchten Sie den Auftrag mit der id: '{0}' endgültig löschen?".format(job))
				if ask == True:
					db(action="delete_job", arg1=job)
					tab_open_auftraege()
	elif id == "action_prin":
		if tab_button_names[active_tab] == "Aufträge":
			if job_printable == True:
				print_widget(detail_frame_object)
			else:
				tkMessageBox.showinfo(title="Druckauftrag nicht abgeschlossen!",
					message="Bittw wählen Sie einen Auftrag zum drucken aus!")
	elif id == "action_edit":
		print "EDIT"
	elif id == "action_mark":
		if tab_button_names[active_tab] == "Aufträge":
			if job != False:
				db(action="set_job_mark", arg1=job)
				tab_open_auftraege()
	else:
		print "button_press(): Unbekannte ID: {0}".format(id)

#----------------------------------------------------------------------------------------
def check_tab_state():
	global active_tab, active_tab_widget, active_tab_title, frames, hub, objects
	n = 0
	while True:
		hub.tab(n, state=DISABLED if account[0] == 0 else NORMAL)
		n = n + 1
		if n == len(tab_button_names)-1:
			break
def change_tab(tab=None):
	global active_tab, active_tab_widget, active_tab_title, frames, hub, objects, main_frame
	destroy_objects()
	check_tab_state()
	if tab == None:
		active_tab = hub.index(hub.select())
		active_tab_widget = hub.select()
		active_tab_title =  tab_button_names[active_tab]
	else:
		active_tab = tab_button_names.index(tab)
		active_tab_widget = frames[tab]
		active_tab_title =  tab
		return
	# Call TabFunction
	if active_tab_title == "Aufträge":
		tab_open_auftraege()
	elif active_tab_title == "Lager":
		tab_open_lager()
	elif active_tab_title == "Produkte":
		tab_open_produkte()
	elif active_tab_title == "Standorte":
		tab_open_standorte()
	elif active_tab_title == "Mitarbeiter":
		tab_open_mitarbeiter()
	elif active_tab_title == "Einstellungen":
		tab_open_einstellungen()
	elif active_tab_title == "Login":
		tab_open_login()
	else:
		print "Change_tab: Kein passender Titel gefunden: "+active_tab_title
	
def tab_open_auftraege(db_request="get_user_jobs"):
	global frames, tab_buttons, objects, settings, jobs, job_printable, job
	change_tab(tab="Aufträge")
	#Frame 2  
	jobs = db(action=db_request, arg1=account[0])
	rows = []
	for i in jobs:
		rows.append( ( "", i[0], (i[0], i[3], i[6], "✔" if str(i[5]) == "1" else "✘", i[1]), ("fg_green" if str(i[5]) == "1" else "",) ) )
	dict = {
		"parent":active_tab_widget,
		"height":"30",
		"manager":"pack",
		"filter":True,
		"query_count":len(jobs),
		"columns":[("#0", 50, "ID"),
				("prio", 50, "Priorität"),
				("date", 150,"Datum"),
				("done", 50, "Erledigt"),
				("name", 362, "Name")],
		"rows":rows,
		"manager":"grid",
		"row":1,
		"column":1
	}
	tree = treeview(action="create", options=dict)
	# Frame 1
	action_buttons(action="create", functions="ADSMSP")
	# DetailFrame
	job_printable = False
	job = False
	dict = {
		"row":1,
		"column":2,
		"width":342,
		"field_1":("label", "Name", ""),
		"field_2":("label", "Beschreibung", ""),
		"field_3":("title", "Meta Informationen", ""),
		"field_4":("list", "ID", ""),
		"field_5":("list", "Priorität", ""),
		"field_6":("list", "Erledigt", ""),
		"field_7":("list", "Erstellt", ""),
		"field_8":("list", "Erstellt von", ""),
	}
	detail_frame(options=dict)
	#Actionbuttons deaktivieren
	actionbutton["rem"].config(state=DISABLED)
	actionbutton["prin"].config(state=DISABLED)
	actionbutton["mark"].config(state=DISABLED)
	
def tab_open_lager():
	change_tab(tab="Lager")
	#
	treeview()
	
def tab_open_produkte():
	change_tab(tab="Produkte")
	#
	pass
	
def tab_open_standorte():
	global job_printable, nodes, job
	change_tab(tab="Standorte")
	#
	nodes = db(action="get_nodes")
	rows = []
	for i in nodes:
		rows.append(  ( "", i[0], (i[0], i[1]) )  )
		rows.append(  ( i[0], "", ("ID:", i[0], ""), ("no_edit",) )  )
		rows.append(  ( i[0], "", ("Standort:", i[1], "") )  )
		rows.append(  ( i[0], "", ("Adresse:", i[2], "") )  )
		rows.append(  ( i[0], "", ("Logo/Bild:", "Ja" if i[5] != "" else "Nein", "") )  )
		rows.append(  ( i[0], "", ("Erstellt:", i[3], ""), ("no_edit",) )  )
		rows.append(  ( i[0], "", ("Erstellt von:", tfi("S.user", i[4]), ""), ("no_edit",) )  )
	dict = {
		"parent":active_tab_widget,
		"height":"30",
		"manager":"grid",
		"filter":True,
		"query_count":len(nodes),
		"columns":[("#0", 100, "ID"),
				("username", 200, "Standort")],
		"rows":rows
	}
	tree = treeview(action="create", options=dict)
	# Actionbuttons
	action_buttons(action="create", functions="ADSP")
	# Detailframe
	job_printable = False
	job = False
	dict = {
		"column":2,
		"width":704,
		"field_1":("image", "", ""),
		"field_2":("label", "Name", ""),
		"field_3":("label", "Adresse", ""),
		"field_4":("title", "Meta Informationen", ""),
		"field_4":("list", "ID", ""),
		"field_6":("list", "Bild", ""),
		"field_7":("list", "Erstellt", ""),
		"field_8":("list", "Erstellt von", ""),
	}
	detail_frame(options=dict)

def tab_open_mitarbeiter(db_request="get_users"):
	global objects, frames, tree, tag, settings
	change_tab(tab="Mitarbeiter")
	# Frame 2
	users = db(action=db_request)
	rows = []
	for i in users:
		rows.append(  ( "", i[0], (i[0], i[1], i[2]) )  )
		rows.append(  ( i[0], "", ("ID:", i[0], ""), ("no_edit",) )  )
		rows.append(  ( i[0], "", ("Username:", i[1], "") )  )
		rows.append(  ( i[0], "", ("Name:", i[2], "") )  )
		rows.append(  ( i[0], "", ("Rollen:", tfi("M.roles", i[4]), "") )  )
		rows.append(  ( i[0], "", ("Benutzergruppe:",i[7], ""), ("no_edit",) )  )
		rows.append(  ( i[0], "", ("Passwort:", "-", "") )  )
		rows.append(  ( i[0], "", ("Bild:", "Ja" if i[3] != "" else "Nein", "") )  )
		rows.append(  ( i[0], "", ("Erstellt:", i[5], ""), ("no_edit",) )  )
		rows.append(  ( i[0], "", ("Erstellt von:", tfi("S.user", i[6]), ""), ("no_edit",) )  )
	dict = {
		"parent":active_tab_widget,
		"height":"30",
		"manager":"pack",
		"filter":True,
		"query_count":len(users),
		"columns":[("#0", 340, "ID"),
				("username", 340, "Benutzername"),
				("name", 340, "Name")],
		"rows":rows,
		"row":1,
		"column":1
	}
	tree = treeview(action="create", options=dict)
	# Frame 1
	action_buttons(action="create")
	
def tab_open_einstellungen():
	change_tab(tab="Einstellungen")
	#
	pass
	
def tab_open_login():
	global frames, tab_buttons, account, objects, settings, active_tab_widget
	change_tab(tab="Login")
	#Labelframe
	frame = ttk.Labelframe(active_tab_widget)
	frame.place(x=0, y=0)
	if account[0] != 0:
		user = db(action="get_user", arg1=account[1])
		#Labelframe
		frame.config(text=" Willkommen, {0}".format(user[3]))
		#Elements
		file = db(action="get_user_image", arg1=account[0])
		image = PIL.ImageTk.PhotoImage(PIL.Image.open(file))
		avatar = Label(frame, image=image, bg=settings["bg_color"])
		avatar.image = image
		objects.append(avatar)
		objects.append(Label(frame, bg=settings["bg_color"], font="Arial 12", text=user[1]))
		objects.append(Button(frame, width=12, font="Arial 12", text="Logout", bg=settings["bg_color"], command=lambda: button_press(id=2)))
		#
		objects[0].grid(row=1, column=1, sticky="WE", padx=4, pady=10)
		objects[1].grid(row=2, column=1, sticky="WE", padx=4, pady=10)
		objects[2].grid(row=3, column=1, sticky="WE", padx=4, pady=10)
	else:
		#Labelframe
		frame.config(text=" Anmeldung ")
		#Elements
		objects.append(Label(frame, bg=settings["bg_color"], padx=4, pady=5, font="Arial 12", text="Benutzer:"))
		objects.append(Label(frame, bg=settings["bg_color"], padx=4, pady=5, font="Arial 12", text="Passwort:"))
		objects.append(Entry(frame, font="Arial 12"))
		objects.append(Entry(frame, show="*", font="Arial 12"))
		objects.append(Button(frame, padx=4, pady=2, width=9, font="Arial 12", text="Login", bg=settings["bg_color"], command=lambda: button_press(id=1)))
		#
		objects[0].grid(row=1, column=1, sticky="NW")
		objects[1].grid(row=2, column=1, sticky="NW")
		objects[2].grid(row=1, column=2, sticky="NW")
		objects[2].focus()
		objects[3].grid(row=2, column=2, sticky="NW")
		objects[4].grid(row=3, column=2, columnspan=2, sticky="NE")
	#Labelframe
	objects.append(frame)
	root.update()
	frame.place(x=(geo[0]-frame.winfo_width())/2, y=((geo[1]*0.9)-frame.winfo_height())/2)
	
def event_key(event):
	global active_tab, tab_button_names
	#print event.keycode
	# 104=NUM_RETURN, 36=RETURN
	if event.keycode == 104 or event.keycode == 36 or event.keycode == 13:
		if tab_button_names[active_tab] == "Login":
			account_login()
			
def event_single_button_1(event):
	widget = event.widget
	parent = widget._nametowidget(widget.winfo_parent())
	widget_type = widget.winfo_class()
	if parent == button_frame and widget_type == "Button":
		widget_text = widget["text"]
		button_press(widget_text)
	
def event_tab_button_1(event):
	change_tab()

def treeview_key_event_delete(event):
	if tab_button_names[active_tab] == "Mitarbeiter":
		button_press(id="action_rem")
	
def treeview_entry_event_return(event):
	global tag
	if tab_button_names[active_tab] == "Mitarbeiter":
		text = event.widget.get()
		#
		db(action="set_user_"+tag[event.widget]["rowname"], arg1=text, arg2=tag[event.widget]["parent"])
		#
		if tag[event.widget]["rowname"] !=  "passwort":
			tree.item(tag[event.widget]["id"], values=(text, ""))
		else:
			tkMessageBox.showinfo(title="Passwort Erfolg", message="Das Passwort wurde erfolgreich geändert")
		destroy_objects(classes=["mitarbeiter_treeview_entry"])
	
	if tab_button_names[active_tab] == "Standorte":
		text = event.widget.get()
		#
		print tag[event.widget]["rowname"]
	
def treeview_entry_event_escape(event):
	global tag
	if tab_button_names[active_tab] == "Mitarbeiter":
		destroy_objects(classes=["mitarbeiter_treeview_entry"])
	elif tab_button_names[active_tab] == "Standorte":
		destroy_objects(classes=["mitarbeiter_treeview_entry"])
		
def event_double_button_1(event):
	global tree, active_tab, tab_button_names, root, frames, objects, tag, settings
	if tab_button_names[active_tab] == "Mitarbeiter":
		destroy_objects(classes=["mitarbeiter_treeview_entry"])
		sel = treeview_get_selection_info(event)
		if sel == False: #Nichts tun, wenn keine Auswahl getroffen (z.B. bei Klick auf Header)
			return
		if tree.parent(sel["row"]) == "": #Nichts tun, wenn parent
			return
		#
		if sel["column"] == "#0" or  sel["column"] == "#2": # Nichts tun, wenn != Datenspalte
			pass
		else:
			if sel["rowname"] == "username" or sel["rowname"] == "name" or sel["rowname"] == "passwort":
				e = Entry(active_tab_widget)
				if sel["rowname"] == "passwort":
					e.config(show="*")
				else:
					e.insert(0, sel["text"])
				e.place(x=sel["x"], y=sel["y"])
				e.focus()
				e.select_range(0, END)
				e.bind("<Return>", treeview_entry_event_return)
				e.bind("<Escape>", treeview_entry_event_escape)
				objects.append(e)
				tag.update({e:sel, "mitarbeiter_edit_entry":e})
			elif sel["rowname"] == "bild":
				filepath = tkFileDialog.askopenfilename(parent=root, filetypes=[("JPEG", ".jpg"), ("PNG", ".png"), ("GIF", ".gif")])
				if filepath != False:
					db(action="set_image", arg1=filepath, arg2=sel["parent"], arg3="user")
					tkMessageBox.showinfo(title="Upload erfolgreich",
						message="Das Benutzerbild wurde erfolgreich hochgeladen.")
			elif sel["rowname"] == "rollen":
				role_popup(id=sel["parent"])
	
	elif tab_button_names[active_tab] == "Standorte":
		destroy_objects(classes=["mitarbeiter_treeview_entry"])
		sel = treeview_get_selection_info(event)
		if sel == False: #Nichts tun, wenn keine Auswahl getroffen (z.B. bei Klick auf Header)
			return
		if tree.parent(sel["row"]) == "": #Nichts tun, wenn parent
			return
		#
		if sel["column"] == "#0" or  sel["column"] == "#2": # Nichts tun, wenn != Datenspalte
			pass
		else:
			if sel["rowname"] == "name" or sel["rowname"] == "adresse":
				e = Entry(active_tab_widget)
				e.insert(0, sel["text"])
				e.place(x=sel["x"], y=sel["y"])
				e.focus()
				e.select_range(0, END)
				e.bind("<Return>", treeview_entry_event_return)
				e.bind("<Escape>", treeview_entry_event_escape)
				objects.append(e)
				tag.update({e:sel, "standorte_edit_entry":e})
			elif sel["rowname"] == "logo/bild":
				filepath = tkFileDialog.askopenfilename(parent=root, filetypes=[("JPEG", ".jpg"), ("PNG", ".png"), ("GIF", ".gif")])
				if filepath != False:
					db(action="set_image", arg1=filepath, arg2=sel["parent"], arg3="nodes")
					tkMessageBox.showinfo(title="Upload erfolgreich",
						message="Das Standortbild wurde erfolgreich geändert.")
		
def event_treeview_button_1(event):
	global tab_button_names, active_tab, tag, tree, job_printable, job
	if tab_button_names[active_tab] == "Mitarbeiter":
		destroy_objects(classes=["mitarbeiter_treeview_entry"])
	elif tab_button_names[active_tab] == "Aufträge":
		tree = event.widget
		sel = treeview_get_selection_info(event="Mitarbeiter")
		if sel == False: #Nichts tun, wenn keine Auswahl getroffen (z.B. bei Klick auf Header)
			return
		#info für actionbuttons(aktionen)
		job_printable = True
		#Setze Button zustände
		actionbutton["rem"].config(state=NORMAL)
		actionbutton["prin"].config(state=NORMAL)
		for i in jobs:
			if int(i[0]) == int(sel["id"]):
				#info für actionbuttons(aktionen)
				job = i[0]
				#Setze Button zustände
				if i[5] == "1":
					actionbutton["mark"].config(state=NORMAL)
					actionbutton["mark"].config(relief=SUNKEN)
				else:
					actionbutton["mark"].config(state=NORMAL)
				#Detailansicht erneuern
				dict = {
					"column":2,
					"width":342,
					"field_1":("label", "Name", ""),
					"field_2":("label", "Beschreibung", ""),
					"field_3":("title", "Meta Informationen", ""),
					"field_4":("list", "ID", ""),
					"field_5":("list", "Priorität", ""),
					"field_6":("list", "Erledigt", ""),
					"field_7":("list", "Erstellt", ""),
					"field_8":("list", "Erstellt von", ""),
				}
		detail_frame()
		detail_frame(options=dict)
	elif tab_button_names[active_tab] == "Standorte":
		tree = event.widget
		sel = treeview_get_selection_info(event="Mitarbeiter")
		if sel == False: #Nichts tun, wenn keine Auswahl getroffen (z.B. bei Klick auf Header)
			return
		#info für actionbuttons(aktionen)
		job_printable = True
		#Setze Button zustände
		actionbutton["rem"].config(state=NORMAL)
		actionbutton["prin"].config(state=NORMAL)
		for i in nodes:
			if str(i[0]) == str(sel["id"]):
				#info für actionbuttons(aktionen)
				job = i[0]
				#Detailansicht erneuern
				dict = {
					"column":2,
					"width":704,
					"field_1":("image", i[5], ""),
					"field_2":("label", "Name", i[1]),
					"field_3":("label", "Adresse", i[2]),
					"field_4":("title", "Meta Informationen", ""),
					"field_4":("list", "ID", i[0]),
					"field_6":("list", "Bild", "Ja" if i[5] != "" else "Nein"),
					"field_7":("list", "Erstellt", i[3]),
					"field_8":("list", "Erstellt von", tfi(type="S.user", data=i[4])),
				}
		detail_frame()
		detail_frame(options=dict)
	
def lc_lab(text_=""):
	global lab, lc
	text_ = "Überprüfe Abhängigkeiten: " + text_ + "..."
	lab.config(text=text_)
	lc.update()
	
def checkup():
	global lc, lab, con, cur
	if lc.state() != "normal":#Check verschieben, falls Fenster noch nicht offen ist.
		lc.after(1, checkup)
		return
	#
	lc_lab("Checke Verbindung zur Datenbank")
	try:
		con = mdb.connect(settings["db_server"], settings["db_user"], settings["db_password"], settings["db_name"]);
	except mdb.Error as e:
		mdb_error(e)
	cur = con.cursor()
	#
	needed_files = ["config.ini", "images/Eschaton.png", "images/favicon.ico", "images/plus.png", "images/bin.png", "images/pencil.png"]
	for i in needed_files:
		lc_lab("Finde datei: {0}".format(i))
		if os.path.isfile("./"+i) == False:
			tkMessageBox.showerror(title="Fehler",
			message="Datei {0} konnte nicht gefunden werden.\nEine Neuinstallation des Programms könnte den Fehler beheben.".format(i))
	lc_lab("Fertig!")
	#~ while True: #TODO: Wieder aktivieren
		#~ if (time.time()-start_time) > 2:
			#~ break
	lc.destroy()
	main_frame()
	
def none():
	pass

def loading_screen():
	global lc, lab, start_time
	start_time = time.time()
	# INIT
	init_settings()
	#---------------------------------
	lc = Tk()
	lc.attributes("-topmost", True)
	lc.protocol("WM_DELETE_WINDOW", none)
	lc.overrideredirect(True)
	lc.deiconify()
	lc.title("Eschaton Client")
	geo = [600, 400]
	pad = [20, 20]
	lc.geometry(str(geo[0])+"x"+str(geo[1])+"+"+str((lc.winfo_screenwidth()/2)-300)+"+"+str((lc.winfo_screenheight()/2)-200))
	#
	image = PIL.ImageTk.PhotoImage(PIL.Image.open("./images/Eschaton.png"), master=lc)
	add = Label(lc, image=image)
	add.image = image
	add.place(x=0, y=0)
	lab = Label(lc)
	lab.place(x=0, y=380)	
	#
	lc.after(2000, checkup)
	lc.mainloop()
	
def root_jump():
	global root
	if root.state() != "normal":
		root.after(1, root_jump)
		return
	root.attributes("-topmost", True)
	root.attributes("-topmost", False)
	root.focus()
	root.lift()
	root.deiconify()

def main_frame():
	global root, frames, geo, pad, settings, hub, main_frame, query_frame, button_frame
	#INIT
	init_vars()
	#-------------------------
	root = Tk()
	root.protocol("WM_DELETE_WINDOW", config_exit)
	root.overrideredirect(False)
	root.deiconify()
	
	#image = PIL.ImageTk.PhotoImage(PIL.Image.open("./images/Icon.png"), master=root)
	#root.tk.call('wm', 'iconphoto', root._w, image)
	root.iconbitmap("./images/favicon.ico")
	
	root.resizable(0, 0)
	root.title("Eschaton Client - Kein Benutzer")
	geo = [1024, 768]
	pad = [20, 20]
	root.geometry(str(geo[0])+"x"+str(geo[1]))
	#Frames
	main_frame = Frame(root, width=str(geo[0]), height=str(geo[1]-105))
	frames = {}
	#Notebook
	hub = ttk.Notebook(main_frame)
	hub.grid(row=1, column=1, sticky="")
	#Frames
	for i in tab_button_names:
		frames[i] = Frame(hub, width=str(geo[0]), height=str(geo[1]-105))
		hub.add(frames[i], text=i)
	button_frame = Frame(root, width=str(geo[0]), height="65")
	query_frame = Frame(root, width=str(geo[0]), height="40")
	#Frames Gridding
	main_frame.grid(row=1, column=1, padx=0, pady=0, sticky="NW")
	main_frame.grid_propagate(False)
	button_frame.grid(row=2, column=1, padx=0, pady=0, sticky="NW")
	button_frame.grid_propagate(False)
	query_frame.grid(row=3, column=1, padx=0, pady=0, sticky="NW")
	query_frame.grid_propagate(False)
	#INIT
	root_jump()
	db(action="init_settings")
	init_window()
	#----------------------------
	root.bind("<ButtonRelease-1>", event_single_button_1)
	root.bind("<Double-Button-1>", event_double_button_1)
	root.bind("<Key>", event_key)
	root.bind("<<TreeviewSelect>>", event_treeview_button_1)
	root.bind("<<NotebookTabChanged>>", event_tab_button_1)
	root.mainloop()
loading_screen()