#!/usr/bin/python3

from votinggui import VotingApp
from collections import OrderedDict
import tkinter.messagebox as tkmb
import tkinter.tix as tk

import os, sys, time, pickle

def hide_file(path):
    "makes a file superficially more difficult to mess with"
    if os.name == 'nt':#windows
        os.system('ATTRIB +R +S +H +I \"'+path+'\"')

def show_file(path):
    if os.name == 'nt':#windows
        os.system('ATTRIB -R -S -H \"'+path+'\"')

os.chdir("C:")
votefilepath = os.path.join(os.environ["USERPROFILE"],"vote.dat")
requiredChoices=3
categoriesPath="categoriestest.dat"#just for now
categories = OrderedDict()
#create a temporary root window for any dialogs that may pop up
app = tk.Tk()
app.iconify()#hide it, shouldn't be needed

try:
    with open(categoriesPath, 'rb') as f:
        for i in range(3):#3 tries
            try:
                categories = pickle.load(f)
                break
            except (pickle.PickleError, IOError):
                print("error retrieving voting information...",
                      file=sys.stderr)
                time.sleep(1)
        else:
            tkmb.showerror("IO Error", "Error reading data from network!")
            app.destroy()
            sys.exit(1)
except IOError:
    tkmb.showerror("IO Error", "Could not retrieve the voting information")
    app.destroy()
    sys.exit(1)

if len(categories) == 0:
    #for testing purposes
    categories['test1'] = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
    categories['test2'] = ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O")

#get rid of the temporary root window and make the voting GUI
app.destroy()
app = VotingApp(categories)


if os.path.exists(votefilepath):#check on network too to prevent people from just deleting files
    tkmb.showerror("Vote already exists",
                   "A vote has already been submitted by this account!")
    app.destroy()
    sys.exit(1)

app.mainloop()

if len(app.votes) == 0:
    sys.exit(0)

root = tk.Tk()
root.iconify()

try:
    with open(votefilepath, 'wb') as f:
        for i in range(3):#3 tries
            try:
                pickle.dump(app.votes, f, pickle.HIGHEST_PROTOCOL)
                break
            except pickle.PickleError:
                print("error pickling info, retrying", file=sys.stderr)
                time.sleep(1)
        else:
            tkmb.showerror("IO Error", "Error writing file to disk!")
            root.destroy()
            sys.exit(1)
except:
    tkmb.showerror("IO Error", "Could not store the vote data")
    app.destroy()
    sys.exit(1)

#hide_file(votefilepath)#don't do this for testing purposes
tkmb.showinfo("Success!", "Vote written Successfully")
root.destroy()
sys.exit(0)






