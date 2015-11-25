from distutils.core import setup
import py2exe
import os

dateiliste = ["config.ini",
	("images", [
		"./images/Eschaton.png",
		"./images/favicon.ico",
		"./images/bin.png",
		"./images/checkmark.png",
		"./images/info.png",
		"./images/noavatar.png",
		"./images/pencil.png",
		"./images/plus.png",
		"./images/printer.png"]
	)
]

#~ dateiliste = [(".", "config.ini"),
	#~ ("images", "./images/bin.png"),
	#~ ("images", "./images/checkmark.png"),
	#~ ("images", "./images/Eschaton.png"),
	#~ ("images", "./images/favicon.ico"),
	#~ ("images", "./images/info.png"),
	#~ ("images", "./images/noavatar.png"),
	#~ ("images", "./images/pencil.png"),
	#~ ("images", "./images/plus.png"),
	#~ ("images", "./images/printer.png")]


setup(
	windows = [{
		"script":"Eschaton.py",
		"icon_resources": [(1, "./images/favicon.ico")]}],
	data_files = dateiliste,
	zipfile = "./DLLs/Eschaton.dll",
	# Info
	name = "Eschaton",
	company_name = "Data Nova",
	version = "1.0.0",
	description = "Build to be simple!",
	author = "Tizian Pessel",
	copyright = "by Tizian Pessel",
	dest_base = "basetest",
	options = {
		"py2exe":{
			"optimize": 2,
			"excludes": ["email"],
			"dist_dir":"./exe",
			"bundle_files":3, #Geh nur so...
			"unbuffered":True,
		}
	}
)

os.remove("./exe/w9xpopen.exe")