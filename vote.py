#!/usr/bin/python3

from votinggui import VotingApp
from collections import OrderedDict
import tkinter.messagebox as tkmb
import tkinter.tix as tk

import os, sys, time, pickle

class Struct(object):
    def __init__(self, dictionary):
        "makes dictionary members instance fields"
        self.__dict__.update(dictionary)

def hide_file(path):
    "makes a file superficially more difficult to mess with"
    if os.name == 'nt':#windows
        os.system('ATTRIB +R +S +H +I \"'+path+'\"')

def show_file(path):
    if os.name == 'nt':#windows
        os.system('ATTRIB -R -S -H \"'+path+'\"')

def safe_eval(path):
    return eval(path, {'__builtins__': None}, {'environ': os.environ})


parameterpath = os.path.join(".", "paramtest.dat")

if os.name == 'nt':
    os.chdir("C:")

app = tk.Tk()
app.iconify()#hide it, shouldn't be needed

#fetch paramaters
#
# votefilepath:		name of the file to save to
# requiredChoices:	number of candidates to select
# categories:		categories for voting
# hideVoteFile: 	True or False whether to superficially hide the vote file
# allowRunning:		whether or not to let the user run the program in the first place
# overwriteVote:        allows the user to overwrite the previous vote
#

try:
    with open(parameterpath, 'rb') as f:
        for i in range(3):#3 tries
            try:
                parameters = pickle.load(f)
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

#check parameters
for p in ("votefilepath", "requiredChoices", "categories", "hideVoteFile",
          "allowRunning"):
    if p not in parameters:
        print("could not find {0}".format(p), file=sys.stderr)
        tkmb.showerror("Parameter Error", "Downloaded invalid parameters!")
        app.destroy()
        sys.exit(1)

p = Struct(parameters)#allow for easier access

#evaluate the vote file path
parts = (safe_eval(i) for i in p.votefilepath)
p.votefilepath = os.path.join(*parts)
del parts


if not p.allowRunning:
    tkmb.showerror("Error", "Voting not allowed at this time!")
    app.destroy()
    sys.exit(1)

if len(p.categories) == 0:
    tkmb.showerror("Parameter Error", "Downloaded invalid parameters!")
    app.destroy()
    sys.exit(1)

#get rid of the temporary root window and make the voting GUI
app.destroy()
app = VotingApp(p.categories, p.requiredChoices)

if not p.overwriteVote:
    if os.path.exists(p.votefilepath):#check on network too to prevent people from just deleting files
        tkmb.showerror("Vote already exists",
                       "A vote has already been submitted by this account!")
        app.destroy()
        sys.exit(1)

app.mainloop()#destroys itself automatically

if len(app.votes) == 0:
    sys.exit(0)

root = tk.Tk()
root.iconify()

if not p.overwriteVote:
    if os.path.exists(p.votefilepath):#check on network too to prevent people from just deleting files
        tkmb.showerror("Vote already exists",
                       "A vote has already been submitted by this account!")
        app.destroy()
        sys.exit(1)

try:
    with open(p.votefilepath, 'wb') as f:
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

if p.hideVoteFile:
    hide_file(votefilepath)#don't do this for testing purposes
tkmb.showinfo("Success!", "Vote Written Successfully")
root.destroy()
sys.exit(0)
