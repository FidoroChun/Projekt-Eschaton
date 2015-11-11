import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect(("192.168.3.47", 50000))

f = open("./images/bin.png", "rb")
nachricht = f.readlines()
try:
	s.send("SEND.bin.png")
	for i in f:
		s.send(i)
	s.send("END")
finally: 
	s.close()