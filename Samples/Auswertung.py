# -*- coding: cp1252 -*-
# BY Tizian Pessel
# CONTACT fidoro@hotmail.de
# LICENSE do not distribute
# VER 1
prog_version = "1"
# DATE 16.06.2015

import string

bands = ["Bandnamen nach ID", "GrooveExperience", "Gaffatapes", "TheTravelers", "Maniax", "Overexposed"]
text = """|46|1|3
|47|3|2
|48|5|1
|49|1|3
|50|3|2
|51|5|1
|52|2|3
|53|3|1
|54|4|2
"""

x = string.split(text, "\n")


n = 0
for i in x:
	if i == "":
		del x[n]
	n = n + 1
	
n = 0
y = []
while n < len(x):
	y.append([string.split(x[n], "|")[2], string.split(x[n], "|")[3]])
	n = n + 1
	
punkte = ["Punkte nach Band-ID", 0, 0, 0, 0, 0]
for i in y:
	id = int(i[0])
	points = int(i[1])
	punkte[id]= punkte[id] + points

g = "XXXXX"
n = 1
for i in g:
	print bands[n] + ": " + str(punkte[n]) + "Punkte"
	n = n + 1