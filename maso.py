import tkinter as tk
import tty, sys, termios, os
import time
import os.path

def evaluate(event):
  name=entry.get()
  app = "feh -xFD 2.0 --auto-zoom --auto-rotate -F "
  fpath="/media/pi/PICTS/"
  absfile=fpath+name+".JPG"
  ppid = " & echo $! > /tmp/pid"
  if os.path.isfile(absfile):
    res.configure(text=absfile,font=("",40))
    cmd = app+absfile+ppid
    os.system(cmd)
    time.sleep(60)
    os.system("cat /tmp/pid | xargs sudo kill")
  else:
    res.configure(text="Xin chon lai ma so",font=("",40))


    
w = tk.Tk()
w.title("CHUA BINH AN")
tk.Label(w, text="MA SO:", font=("",40)).pack()
entry = tk.Entry(w,font=("",40))
entry.bind("<KP_Enter>", evaluate)
entry.pack()
res = tk.Label(w)
res.pack()
w.mainloop()
