# © Nicholai Fox Martinsen

from key import *
import math
import os
import win32api

def search(look):
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    for i in drives:
        for root, dirs, files in os.walk(i):
            if look in root:
                return(root)
                break

def updatepath(game):
    directory= {}
    with open('search\\search.txt', 'r') as file:
        for line in file: k, v = line.strip().split('=');directory[k.strip()] = v.strip()
    dir = search(directory[game])
    l = {}
    listy = ('settings', 'resolution', 'fov')
    for i in listy:
        with open('search\\name'+i+'.txt', 'r') as file:
            for line in file: k, v = line.strip().split('=');l[k.strip()] = v.strip()
            for root, dirs, files in os.walk(dir):
                if l[game] in files:
                    d = root +'\\'+ l[game]
                    break
            try:
                with open('paths\\'+i+'.txt', 'r') as file:
                    temp = file.read()
                    temp = temp+'\n'+game+'='+d
                    with open('paths\\' + i+'.txt', 'w+') as file:
                        file.write(temp)
            except:
                with open('paths\\' + i + '.txt', 'w+') as file:
                    file.write(game+'='+d)


def getpath(name):
    paths = {}
    with open('paths\\'+name+'.txt', 'r') as file:
        for line in file:k, v = line.strip().split('=');paths[k.strip()] = v.strip()
        return paths

def translatekeylist(game):
    keyboard = {}
    if ':' in game:
        game = game.replace(':', '')

    with open('keytranslations\\'+game+'.txt', 'r') as file:
        for line in file: k, v = line.strip().split(':');keyboard[k.strip()] = v.strip()
    return keyboard

def translateconfig(game):
    dic = {}
    if ':' in game:
        game = game.replace(':', '')

    with open('configtranslations\\'+game+'.txt', 'r') as file:
        for line in file: k, v = line.strip().split(':');dic[k.strip()] = v.strip()
    return dic

def reversekey(game):
    inv_map = {v: k for k, v in translatekeylist(game).items()}
    try: return inv_map
    except:
        return ''

def changebind(bind, name, game):
    x = bindlocation(translateconfig(game)[name], game)
    if x == -1:
        return
    with open(getpath('settings')[game], 'r') as file:
        old = file.read(x)
        # print(old)
        file.read(bindlen(translateconfig(game)[name], game))
        # if direction[game] <0:
        #     file.read(1)
        newfile = old + bind + file.read()
    with open(getpath('settings')[game], 'w') as file:
        file.write(newfile)

def bindlocation(term, game):
    with open(getpath('settings')[game], 'r') as file:
        text = file.read()
        x = text.find(term)
        if x==-1:
            return x
        x = x + offsets[game]
        if direction[game]<0:
            x = x - bindlen(term, game) - 1
            # print(bindlen(term))
            # print(x)
        elif direction[game] >0:
            x= x+len(term)
    return (x)

def bindlen(term, game):
    length = 0
    if game == "Apex Legends":
        stopkey = '"'
    elif game == 'PUBG':
        stopkey = ')'
    with open(getpath('settings')[game], 'r') as file:
        text = file.read()
        x = text.find(term) + offsets[game]
        # print(x)
        if direction[game] >0:
            x= x+len(term)
            length +=1
        elif direction[game] <0:
            x += -1
        with open(getpath('settings')[game], 'r') as file:
            while True:
                file.seek(0)
                x += direction[game]
                file.read(x)

                if file.read(1) == stopkey:
                    return length
                else:
                    # print(length)
                    length +=1

def getbind(term, game):
    try:
         t=translateconfig(game)[term]
    except:
        return
    x = bindlocation(t, game)
    if x == -1:
        return None
    bind = ''
    if game == "Apex Legends":
        stopkey = '"'
    elif game == 'PUBG':
        stopkey = ')'
    with open(getpath('settings')[game], 'r') as file:
        file.read(x)
        nextchar = file.read(1)
        while nextchar != stopkey:
            bind += nextchar
            nextchar = file.read(1)
        return bind

def fovlocation(game):
    with open(getpath('fov')[game], 'r') as file:
        z=file.read()
        try:
            if game == 'PUBG':
                x=z.rfind(translateconfig(game)['FOV'])
            else:
                x=z.find(translateconfig(game)['FOV'])
        except:
            return -1
        return x + fovoffset[game]

def getfov(game):
    fov = ''
    l = fovlocation(game)
    if l == -1:
        return
    with open(getpath('fov')[game], 'r') as file:
        file.read(l)
        digit = file.read(1)
        while digit in numberlist:
            fov += digit
            digit = file.read(1)
        return float(fov)

def fovconversion(value, ratio, dir, game):
    if game == 'Apex Legends':
        if dir == 1:
            v = hfov_vfov(value*70, 4/3)
            return vfov_hfov(v, ratio)
        elif dir == -1:
            v = hfov_vfov(value, ratio)
            return round(vfov_hfov(v, 4/3)/70,3)
    if game == 'PUBG':
        if ratio == 16/9:
            return value
        elif ratio > 16/9:
            if dir == 1:
                v = hfov_vfov(value, 16 / 9)
                return vfov_hfov(v, ratio)
            elif dir == -1:
                v = hfov_vfov(value, ratio)
                return round(vfov_hfov(v, 16 / 9), 3)


def hfov_vfov(hfov, ratio):
    vfov = 2*math.atan(math.tan(math.radians(hfov)/2)*1/ratio)
    return math.degrees(vfov)

def vfov_hfov(vfov, ratio):
    hfov = 2*math.atan(math.tan(math.radians(vfov)/2)*ratio)
    return math.degrees(hfov)

def changefov(value, game):
    fov = ''
    if value > maxfov[game]:
        value = maxfov[game]
    elif value < minfov[game]:
        value = minfov[game]
    with open(getpath('fov')[game], 'r') as file:
        temp=file.read(fovlocation(game))
        digit = file.read(1)
        while digit in numberlist:
            digit = file.read(1)

        temp = temp + str(value) +digit+ file.read()
        with open(getpath('fov')[game], 'w') as newfile:
            newfile.write(temp)

def getratio(game):
    w=''
    h=''
    resh = ''
    resw = ''
    with open(getpath('resolution')[game], 'r') as file:
        z=file.read()
        h=z.find(translateconfig(game)['RESH'])
        w=z.find(translateconfig(game)['RESW'])
    with open(getpath('resolution')[game], 'r') as file:
        file.read(h+resoffset[game]['h'])
        digit = file.read(1)
        while digit in numberlist:
            resh += digit
            digit = file.read(1)
    with open(getpath('resolution')[game], 'r') as file:
        file.read(w+resoffset[game]['w'])
        digit = file.read(1)
        while digit in numberlist:
            resw += digit
            digit = file.read(1)
    return float(resw)/float(resh)

def sens_equation(currentsens,mmx, game1, game2):
    fov1 = math.radians(fovconversion(getfov(game1),getratio(game1),1,game1))
    fov2 = math.radians(fovconversion(getfov(game2),getratio(game2),1,game2))
    mm = mmx/100
    if mm > 0:
        x1 = math.atan(mm * math.tan(fov1 / 2))
        x2 = math.atan(mm * math.tan(fov2 / 2))
    else:
        x1 = math.tan(fov1 / 2)
        x2 = math.tan(fov2 / 2)
    newsens = currentsens * (x2 / x1) * (fov1 / fov2)
    newsens = newsens * (yaw[game1]/yaw[game2])
    return newsens

def getsens(game):
    sens=''
    with open(getpath('settings')[game], 'r') as file:
        z=file.read()
        x = z.find(translateconfig(game)['SENS'])
        file.seek(0)
        file.read(x+(len(translateconfig(game)['SENS'])))
        digit = file.read(1)
        while digit not in numberlist:
            digit = file.read(1)
        while digit in numberlist:
            sens+=digit
            digit = file.read(1)
        return float(sens)



#Game specific code below:

# def buildapex():
#     x = 1
#     while x > 0:
#         with open(getpath('settings')['Apex Legends'], 'r') as file:
#             x = file.read().find('" 1')
#             if x != -1:
#                 file.seek(0)
#                 tempfile = file.read(x-1)
#                 file.read(4)
#                 tempfile = tempfile + file.read()
#                 with open(getpath('settings')['Apex Legends'], 'w') as file:
#                     file.write(tempfile)
#     with open(getpath('settings')['Apex Legends'], 'r') as file:
#         tempfile = file.read()
#         for i in bindinglines['Apex']:
#             if tempfile.find(i) == -1:
#                 tempfile = tempfile + bindinglines['Apex'][i] + '\n'
#         with open(getpath('settings')['Apex Legends'], 'w') as file:
#             file.write(tempfile)
#
# def buildpubg():
#     with open(getpath('settings')['PUBG'], 'r') as file:
#         tempfile = file.read()
#         file.seek(0)
#         x = tempfile.find('CustomInputSettins=(ActionKeyList=(')
#         newfile = file.read(x+35)
#         for i in bindinglines['Pubg']:
#             if 'AxisName=' not in i:
#                 if tempfile.find(i) == -1:
#                     print(i)
#                     newfile = newfile + bindinglines['Pubg'][i]
#         newfile = newfile + file.read()
#         with open(getpath('settings')['PUBG'], 'w') as file:
#             file.write(newfile)
#     with open(getpath('settings')['PUBG'], 'r') as file:
#         tempfile = file.read()
#         file.seek(0)
#         x = tempfile.find('AxisKeyList=(')
#         newfile = file.read(x + 13)
#         for i in bindinglines['Pubg']:
#             if 'AxisName=' in i:
#                 if tempfile.find(i) == -1:
#                     print(i)
#                     newfile = newfile + bindinglines['Pubg'][i]
#         newfile = newfile + file.read()
#         with open(getpath('settings')['PUBG'], 'w') as file:
#             file.write(newfile)
