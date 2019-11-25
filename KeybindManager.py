# © Nicholai Fox Martinsen 2019.
# This computer code is licensed for use solely by the person to whom it is
# delivered and  may not be transferred, duplicated or reverse engineered, or decompiled.

from main import *
from tkinter import *
from tkinter import ttk
import win32api
import win32con
import PyHook3
import pythoncom
import ctypes
import time
from key import labeldisplay

global game
global keyvalue

wm = {0x020B: "MOUSE BUTTON", 0x0201: "LEFT CLICK", 0x0207: 'SCROLL CLICK', 0x0204: 'RIGHT CLICK', 0x020A: 'MOUSE WHEEL'}
gamelist = ['Apex Legends', 'PUBG', 'CS:GO']
listorder = ['ADS','Shoot','Melee','Reload', 'Move Forward', 'Move Backward', 'Move Left', 'Move Right', 'Jump','Crouch','Sprint','Interact','Fire Mode','Grenade','Heal','Inventory','Map', 'Weapon 1', 'Weapon 2', 'Weapon 3', 'Weapon 4','Next Weapon', 'Previous Weapon', 'Stow Weapons', 'Ping', 'Push-to-Talk', 'Chat']
buttonlist = []
sessionbinds = {'ADS':None,'Shoot':None,'Melee':None,'Reload':None,'Grenade':None, 'Move Forward':None, 'Move Backward':None, 'Move Left':None, 'Move Right':None, 'Jump':None,'Crouch':None,'Sprint':None,'Interact':None,'Heal':None,'Inventory':None,'Map':None, 'Ping':None, 'Weapon 1':None, 'Weapon 2':None, 'Weapon 3':None, 'Weapon 4':None, 'Next Weapon':None, 'Previous Weapon':None,'Stow Weapons':None, 'Push-to-Talk':None, 'Chat':None, 'Fire Mode':None}
# game = 'PUBG'
# print(list(x for x in keys.keys() if x != game))

#Next 5 functions all related to taking either mouse or keyboard input and turning that into a string
def press(*args):
    win32api.keybd_event(0x90, 0,0,0)
    time.sleep(.05)
    win32api.keybd_event(0x90,0 ,win32con.KEYEVENTF_KEYUP ,0)

#Takes mouse input and translates it into a user friendly string
def mouse_handler(msg, x, y, data, flags, time, hwnd, window_name):
    global keyvalue
    name = wm.get(msg, None)
    if name:
        xb = data >> 16
        if xb>0:
            keyvalue = (name + ' ' + str(xb + 3))
            ctypes.windll.user32.PostQuitMessage(0)
        else:
            keyvalue = (name)
            ctypes.windll.user32.PostQuitMessage(0)
    return True

def OnKeyboardEvent(event):
    global keyvalue
    keyvalue = event.Key
    ctypes.windll.user32.PostQuitMessage(0)
    ctypes.windll.user32.PostQuitMessage(0)
    return True

def readinput():
    try:
        hm = PyHook3.HookManager()
        hm.KeyDown = OnKeyboardEvent
        hm.HookKeyboard()
        PyHook3.cpyHook.cSetHook(PyHook3.HookConstants.WH_MOUSE_LL, mouse_handler)
        pythoncom.PumpMessages() #Continues to monitor for events until

    finally:
        PyHook3.cpyHook.cUnhook(PyHook3.HookConstants.WH_MOUSE_LL)
        PyHook3.cpyHook.cUnhook(PyHook3.HookConstants.WH_KEYBOARD_LL)

def press(*args):
    win32api.keybd_event(0x90, 0,0,0)
    time.sleep(.05)
    win32api.keybd_event(0x90,0 ,win32con.KEYEVENTF_KEYUP ,0)

def updatebinds(item):
    if win32api.GetKeyState(144) == 0: #enables numlock so input is accurately translated to game settings
        press()
    readinput()
    s = 'Escape', 'Lwin', 'Apps', 'Rwin' #doesn't allow these keys to be bound to game
    if keyvalue in s:
        return
    w.focus()
    k = translatekeylist(game)[keyvalue]
    changebind(k, item, game)
    buttonlist[listorder.index(item)].config(text=labeldisplay[reversekey(game)[getbind(item, game)]])

def checkpath(): #if the path for the settings file hasn't been set yet or is now invalid, this updates it
    try:
        file = open(getpath('settings')[game])
        file.close()
    except:
        updatepath(game)
    try:
        file = open(getpath('resolution')[game])
        file.close()
    except:
        updatepath(game)
    try:
        file = open(getpath('fov')[game])
        file.close()
    except:
        updatepath(game)

def updategame(event):
    global game
    global sessionbinds
    for item in sessionbinds:
        sessionbinds[item] = None
    game = gamelist[combo.current()]
    checkpath()
    r = getratio(game)
    fovorig.config(text=round(fovconversion(getfov(game), r, 1, game)))
    fovslider.config(from_=round(fovconversion(minfov[game], r, 1, game)), to=round(fovconversion(maxfov[game], r, 1, game)))
    fovinput.delete(0, END)
    fovinput.insert(0, (fovconversion(getfov(game), r, 1, game)))
    sensorig.config(text=getsens(game))
    sensgamecombo.config(values=list(x for x in keys.keys() if x != game))
    sensgamecombo.set('')
    senscombo.config(text='')
    sensbox.delete(0, END)
    for item in listorder:
        x = getbind(item, game)
        if x == None:
            buttonlist[listorder.index(item)].config(text='', state='disabled')
        elif x != None:
            buttonlist[listorder.index(item)].config(text=labeldisplay[reversekey(game)[x]], state='enabled')
            sessionbinds[item] = x

def resetsession():
    for item in listorder:
        if sessionbinds[item] != None:
            changebind(sessionbinds[item], item, game)
            buttonlist[listorder.index(item)].config(text=labeldisplay[reversekey(game)[getbind(item, game)]], state='enabled')

def clearbind(item):
    changebind('', item, game)
    buttonlist[listorder.index(item)].config(text=getbind(item, game))

def ttk_slider_callback(value):
    fovinput.delete(0, END)
    fovinput.insert(0,(round(float(value))))

def callback(sv):
    y=0
    r = getratio(game)
    if fovconversion(minfov[game], r, 1, game) >= 100:
        y=11
    else: y=10
    try:
        x = float(sv.get())
        if x>=round(fovconversion(minfov[game], r, 1, game)):
            fovslider.set(x)
        elif x>=y:
            fovslider.set(round(fovconversion(minfov[game], r, 1, game)))
        else:
            return
    except: return

def updatefov():
    changefov(fovconversion(float(sv.get()), getratio(game),-1,game),game)
    fovorig.config(text=round(fovconversion(getfov(game), getratio(game), 1, game)))

def updatesensgame(event):
    x= (list(x for x in keys.keys() if x != game))
    senscombo.config(text=getsens(x[sensgamecombo.current()]))

def convertsens():
    x = (list(x for x in keys.keys() if x != game))
    sensbox.delete(0, END)
    sensbox.insert(0, sens_equation(getsens(x[sensgamecombo.current()]), 0, x[sensgamecombo.current()], game))



w = Tk()
s = ttk.Style()
s.theme_use('clam')
i = -1

# img = PhotoImage(file = 'ratio.png')

w.title('Keybind Manager')

gameframe = ttk.LabelFrame(w, text='Games:', height=3000)
gameframe.grid(row=1, column=1, sticky='news')
combo = ttk.Combobox(gameframe, values= list(x for x in keys.keys()))
combo.grid(row=1, column=1)
combo.bind("<<ComboboxSelected>>", updategame)
game = combo.current()
resetbutton = ttk.Button(gameframe, text='Reset session', command=resetsession, width=20)
resetbutton.grid(row=1, column=2)

sensitivityframe = ttk.LabelFrame(w, text='Sensitivity Settings')
sensitivityframe.grid(row=2, column=1, sticky='nswe')

sv = StringVar()
sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
fovlabel = ttk.Label(sensitivityframe, text='FOV')
fovorigl = ttk.Label(sensitivityframe, text='Current FOV:')
fovorig = ttk.Label(sensitivityframe)
fovorigl.grid(column=1, row=1)
fovorig.grid(column=2, row=1)


fovslider = ttk.Scale(sensitivityframe, command=ttk_slider_callback)
fovlabel.grid(column=1, row=2)
fovslider.grid(column=2, row=2)

fovinput = Entry(sensitivityframe,textvariable=sv, width=5)
fovinput.grid(column=4, row=2)
fovupdate = ttk.Button(sensitivityframe, text='Update FOV value', command= updatefov)
fovupdate.grid(column=5, row =2)

sensgamelabel = ttk.Label(sensitivityframe, text ='Convert sens from:')
sensgamecombo= ttk.Combobox(sensitivityframe, values=[])
sensgamecombo.bind("<<ComboboxSelected>>", updatesensgame)
senscombo = ttk.Label(sensitivityframe)
senscombo.grid(row=1, column=9)
sensgamelabel.grid(column=7, row=1)
sensgamecombo.grid(column=8, row=1)


sensbox = ttk.Entry(sensitivityframe, width=10)
sensbox.grid(column=10, row=2)
sensorig = ttk.Label(sensitivityframe)
sensorig.grid(column=8, row=2)
sensorigl = ttk.Label(sensitivityframe, text ='Current Game Sensitivity:')
sensorigl.grid(column=7, row=2)
sensboxlabel = ttk.Label(sensitivityframe, text='Sensitivity:')
sensboxlabel.grid(column=9, row=2)

convertsensbutton = ttk.Button(sensitivityframe, text='Convert!', command=convertsens)
convertsensbutton.grid(column=10, row=1)

bindframe = ttk.LabelFrame(w, text="Keybinds")
bindframe.grid(row=8, column=1)

for item in listorder:
    if listorder.index(item) % 4 == 0:
        i+=2
    label = ttk.Label(bindframe, text=item + ': ')
    label.grid(row=listorder.index(item)%4 +1, column=int(i))
    if game == -1:
        button = ttk.Button(bindframe, text='', command=lambda x=item: updatebinds(x), width=20, state='disabled')
        button.bind('<Button-3>', lambda event, name=item: clearbind(name))
        button.grid(row=listorder.index(item) % 4 + 1, column=int(i + 1))

    elif getbind(item, game) != None:
        button = ttk.Button(bindframe, text=labeldisplay[reversekey(game)[getbind(item, game)]], command=lambda x=item: updatebinds(x), width=20)
        button.bind('<Button-3>', lambda event, name = item: clearbind(name))
        button.grid(row=listorder.index(item)%4 +1, column=int(i+1))
    else:
        button = ttk.Button(bindframe, text='', command=lambda x=item: updatebinds(x), width=20,state = 'disabled')
        button.bind('<Button-3>', lambda event, name=item: clearbind(event, name))
        button.grid(row=listorder.index(item) % 4 + 1, column=int(i + 1))
    buttonlist.append(button)

# buildapex()
# buildpubg()

w.mainloop()
