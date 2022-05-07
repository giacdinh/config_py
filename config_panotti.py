from tkinter import *
import urllib3 
import socket
import time
import threading
import os
import select
from tkinter import filedialog

uid = ["UNIT ID"]
uip = ["UNIT IP ADDRESS"]
################################## client list ######################################
def clientlist():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(('',2999))
	sock.settimeout(2.0) # end socket if nothing read for 20s
	k = 0
	timeout = time.time() + 30 # scan UPD for 30s set time out for scan loop
	#socket.settimeout(5.0)		# set 5s timeout for each socket listening
	while True:
		j = 0
		try:
			data, (address,portnum) = sock.recvfrom(1024)
		except socket.timeout:
			sock.close()
			return 0

		for i in uip:
			if i == address:
				j = 0
				break
			else:
				j = 1

		if j == 1:
			uip.append(address)
			uid.append(str(data))

		k += 1
		time.sleep(1)
		if k == 5 or time.time() > timeout:
			return 0	

	return 0

################################## get UPD ######################################
def getUDP():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(('',1999))
	data, (address,portnum) = sock.recvfrom(1024)
	return data,address

################################## start read ######################################
def startread(addressIP,btn):
	btn.configure(text="Reading ...", bg='orange')
	http = urllib3.PoolManager()
	r = http.request('HEAD', 'http://' + addressIP + ':2999/remotem_start_read.cgi?')
	r.release_conn()

################################## stop read ######################################
def stopread(addressIP,btn):
	btn.configure(text="Start Read", bg='powder blue')
	http = urllib3.PoolManager()
	r = http.request('HEAD', 'http://' + addressIP + ':2999/remotem_stop_read.cgi?')
	r.release_conn()

################################## config update ##################################
def configupdate(addressIP):
	http = urllib3.PoolManager()
	window.filename =  filedialog.askopenfilename(initialdir = "~/",title = "choose your file")
	with open(window.filename, 'rb') as configfile:
		data = configfile.read()
		r = http.request('HEADER', 'http://' + addressIP + ':2999/remotem_config_update.cgi?', 
			body = data,
			headers={'Content-Type': 'text/plain'} )
	r.release_conn()



#--------------------------------
window = Tk()

window.title("Panotti Config Tools")
window.geometry('900x400');
#window.configure(bg='cyan')

clientlist()
length = len(uip)
# First row
#for i in range(length):
for i in range(10) :
	if i < length:
		uidlabel = str(uid[i])
		uiplabel = str(uip[i])
	elif i >= length:
		uidlabel = str('                  ')
		uiplabel = str('                     ')

	lbl = Label(window, text=uidlabel, bg="white")
	lbl.grid(column=0, row=i)
	lbl = Label(window, text=uiplabel, bg="white")
	lbl.grid(column=1, row=i)
	if i == 0:
		lbl = Label(window, text='PANOTTI FUNCTIONAL OPTIONS', bg='powder blue')
		lbl.grid(column=2, row=i, columnspan = 7)
		continue
	elif i == 1:
		btn1 = Button(window, text="Start read", bg='powder blue', command=lambda:startread(uiplabel,btn1))
		btn1.grid(column=2, row=i)
		btn = Button(window, text="Stop read", command=lambda:stopread(uiplabel,btn1))
		btn.grid(column=3, row=i)
	elif i == 2:
		btn2 = Button(window, text="Start read", bg='powder blue', command=lambda:startread(uiplabel,btn2))
		btn2.grid(column=2, row=i)
		btn = Button(window, text="Stop read", command=lambda:stopread(uiplabel,btn2))
		btn.grid(column=3, row=i)
	elif i == 3:
		btn3 = Button(window, text="Start read", bg='powder blue', command=lambda:startread(uiplabel,btn3))
		btn3.grid(column=2, row=i)
		btn = Button(window, text="Stop read", command=lambda:stopread(uiplabel,btn3))
		btn.grid(column=3, row=i)
	elif i == 4:
		btn4 = Button(window, text="Start read", bg='powder blue', command=lambda:startread(uiplabel,btn4))
		btn4.grid(column=2, row=i)
		btn = Button(window, text="Stop read", command=lambda:stopread(uiplabel,btn4))
		btn.grid(column=3, row=i)
	elif i == 5:
		btn5 = Button(window, text="Start read", bg='powder blue', command=lambda:startread(uiplabel,btn5))
		btn5.grid(column=2, row=i)
		btn = Button(window, text="Stop read", command=lambda:stopread(uiplabel,btn5))
		btn.grid(column=3, row=i)
	elif i == 6:
		btn6 = Button(window, text="Start read", bg='powder blue', command=lambda:startread(uiplabel,btn6))
		btn6.grid(column=2, row=i)
		btn = Button(window, text="Stop read", command=lambda:stopread(uiplabel,btn6))
		btn.grid(column=3, row=i)
	elif i == 7:
		btn7 = Button(window, text="Start read", bg='powder blue', command=lambda:startread(uiplabel,btn7))
		btn7.grid(column=2, row=i)
		btn = Button(window, text="Stop read", command=lambda:stopread(uiplabel,btn7))
		btn.grid(column=3, row=i)
	elif i == 8:
		btn8 = Button(window, text="Start read", bg='powder blue', command=lambda:startread(uiplabel,btn8))
		btn8.grid(column=2, row=i)
		btn = Button(window, text="Stop read", command=lambda:stopread(uiplabel,btn8))
		btn.grid(column=3, row=i)
	elif i == 9:
		btn9 = Button(window, text="Start read", bg='powder blue', command=lambda:startread(uiplabel,btn9))
		btn9.grid(column=2, row=i)
		btn = Button(window, text="Stop read", command=lambda:stopread(uiplabel,btn9))
		btn.grid(column=3, row=i)

	btn = Button(window, text="FW Upgrade")
	btn.grid(column=4, row=i)
	btn = Button(window, text="Config Upgrade", command=lambda:configupdate(uiplabel))
	btn.grid(column=5, row=i)
	btn = Button(window, text="Get Config")
	btn.grid(column=6, row=i)
	btn = Button(window, text="Get Logs")
	btn.grid(column=7, row=i)
	btn = Button(window, text="Reboot")
	btn.grid(column=8, row=i)

def close_window(): 
    window.destroy()

data, address = getUDP()
button = Button (window, text = "Exit", bg='green2', command = close_window)
button.grid(column=0, row=10)

app = Menu()
window.mainloop()
#-------------------------------------
