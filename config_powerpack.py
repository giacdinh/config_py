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
	sock.bind(('',1999))
	sock.settimeout(20.0) # end socket if nothing read for 20s
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
			uid.append(data)

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

window.title("PopwerPack Config Tools")
window.geometry('700x200');
#window.configure(bg='cyan')

#clientlist()
length = len(uip)
# First row
for i in range(length):
	lbl = Label(window, text=uid[i], bg="white")
	lbl.grid(column=0, row=i)
	lbl = Label(window, text=uip[i], bg="white")
	lbl.grid(column=1, row=i)
	if i == 0:
		lbl = Label(window, text='POWERPACK FUNCTIONAL OPTIONS', bg='powder blue')
		lbl.grid(column=2, row=i, columnspan = 7)
		continue

	btn = Button(window, text="FW Upgrade")
	btn.grid(column=2, row=i)
	btn = Button(window, text="Config Upgrade", command=lambda:configupdate(uip[i]))
	btn.grid(column=3, row=i)
	btn = Button(window, text="Get Config")
	btn.grid(column=4, row=i)
	btn = Button(window, text="Get Logs")
	btn.grid(column=5, row=i)
	btn = Button(window, text="Reboot")
	btn.grid(column=6, row=i)

def close_window(): 
    window.destroy()

data, address = getUDP()
button = Button (window, text = "Exit", bg='green2', command = close_window)
button.grid(column=0, row=3)

app = Menu()
window.mainloop()
#-------------------------------------
