import os
from tkinter import *
import csv
def addl2():
    addl2.x += 1
    srctext = src.get()
    destext = des.get() 
    spamwriter.writerow([addl2.x,destext,srctext])
    #l2 = Label(text = 'yo ').pack()
    return
addl2.x=0

def addl3():
    addl3.y += 1
    srctext = srci.get()
    destext = desi.get() 
    spamwriter2.writerow([addl3,destext,srctext])
    #l2 = Label(text = 'yo ').pack()
    return
addl3.y=0

def add_host():
    add_host.z += 1
    host = hst.get()
    spamwriter3.writerow([add_host.z,host])
    #l2 = Label(text = 'yo ').pack()
    return
add_host.z=0

def close_window(): 
    root.destroy()

root = Tk()
src = StringVar()
des = StringVar()
srci = StringVar()
desi = StringVar()
hst = StringVar()
csvfile = open('layer2.csv', 'w',newline = '')
spamwriter = csv.writer(csvfile)
spamwriter.writerow(['id']+['mac_0']+['mac_1'])

csvfile2 = open('layer3.csv', 'w',newline = '')
spamwriter2 = csv.writer(csvfile2)
spamwriter2.writerow(['id']+['ip_0']+['ip_1'])

csvfile3 = open('singlehost.csv', 'w',newline = '')
spamwriter3 = csv.writer(csvfile3)
spamwriter3.writerow(['id']+['ip'])    	

root.geometry('350x250')
header1 = Label(text = 'Layer 2', fg = 'blue').grid(row = 1,column = 2)
l1 = Label(text = 'Source: ').grid(row = 2,column = 1)
l2 = Label(text = 'Destination: ').grid(row = 3,column = 1)
mentry1 = Entry(textvariable = src).grid(row = 2,column = 2)
mentry2 = Entry(textvariable = des).grid(row = 3,column = 2)
b1 = Button(text = 'Add Rule', command = addl2).grid(row = 4,column = 1)

header2 = Label(text = 'Layer3', fg = 'blue').grid(row = 5,column = 2)
l3 = Label(text = 'Source: ').grid(row = 6,column = 1)
l4 = Label(text = 'Destination: ').grid(row = 7,column = 1)
mentry3 = Entry(textvariable = srci).grid(row = 6,column = 2)
mentry4 = Entry(textvariable = desi).grid(row = 7,column = 2)
b2 = Button(text = 'Add Rule', command = addl3).grid(row = 8,column = 1)

header3 = Label(text = 'Block single host', fg = 'blue').grid(row = 10,column = 2)
l3 = Label(text = 'Host: ').grid(row = 11,column = 1)
mentry5 = Entry(textvariable = hst).grid(row = 11,column = 2)
b3 = Button(text = 'Add Rule', command = add_host).grid(row = 12,column = 1)

b4 = Button(text = 'Done', command = close_window).grid(row = 13,column = 2)

root.mainloop()
csvfile.close()
csvfile2.close()
csvfile3.close()
os.chdir('/home/ankan/pox')
os.system("./pox.py forwarding.l2_learning misc.proj")