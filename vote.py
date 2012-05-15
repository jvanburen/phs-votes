#!/usr/bin/python3

from votinggui import VotingApp
from collections import OrderedDict
import tkinter.messagebox as tkmb
import tkinter.tix as tk

import os, sys, time, pickle
os.chdir("C:")
votefilepath = os.path.join(os.environ["USERPROFILE"],"vote.dat")
requiredChoices=3
categories = OrderedDict()
categories['test1'] = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
categories['test2'] = ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O")
#
#add categories here
#

def hide_file(path):
    "makes a file superficially more difficult to mess with"
    if os.name == 'nt':#windows
        os.system('ATTRIB +R +S +H +I \"'+path+'\"')

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

hide_file(votefilepath)
tkmb.showinfo("Success!", "Vote written Successfully")
root.destroy()
sys.exit(0)
    





