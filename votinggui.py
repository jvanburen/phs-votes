#!/usr/bin/python3

import tkinter.ttk as tk
from tkinter import tix
import tkinter.messagebox as tkmb
from tkinter.constants import *
from votingframe import VotingFrame
from collections import OrderedDict

import time, sys

def test_tix():
    testbase = tk.Tk()
    testbase.tk.eval("package require Tix")
    testbase.destroy()
    del testbase

class VotingApp(tix.Tk):
    def __init__(self, categories=OrderedDict(), reqchoices=3):
        tix.Tk.__init__(self)
        self.title("Voting Program")
        self.categories = categories
        self.votingFrames = []
        self.votes = dict()
        self.reqchoices = reqchoices

        #set up widgets
        self.topStatus = tix.StringVar()
        self.topLabel = tk.Label(self, textvariable=self.topStatus)

        self.votingTabs = tk.Notebook(self)
        self.voteButton = tk.Button(self, text="Vote", state=DISABLED)
        self.voteButton['command'] = self.vote
        
##        self['bg'] = self.votingTabs['bg']
        self.votingTabs.grid(row=0, column=0, rowspan=3, columnspan=3,
                             padx=4, pady=4)
        
        #add tabs
        
        for name in self.categories.keys():
            self.create_voting_panel(self.votingTabs, name)
            
        self.update_idletasks()
        self.voteButton.grid(row=5, column=2, padx=4, pady=2)
        
        #set up
        self.protocol("WM_DELETE_WINDOW", self.confirm_exit)
        self.resizable(0, 0)
        
    def create_voting_panel(self, nb, name):

        frame = tk.Frame(nb)
        self.votingTabs.add(frame, text=name.title(), underline=0)
        window = VotingFrame(frame, people=self.categories[name],
                             reqchoices=self.reqchoices)
        window.grid()
        window.bind("<<Vote>>", self.check_votes)
        
        self.votingFrames.append(window)

    def check_votes(self, e=None):
        if all(map(lambda v: v.vote_ready(), self.votingFrames)):
            self.voteButton['state'] = NORMAL
        else:
            self.voteButton['state'] = DISABLED

    def vote(self, e=None):
        if not tkmb.askyesno("Vote?", "Is This Your Final Vote?"):
            return
        frames = tuple(self.categories.keys())
        for index, cat in enumerate(self.votingFrames):
            self.votes[frames[index]] = cat.selection
        tkmb.showinfo("Success!", "Vote created Successfully!")
        self.destroy()

    def confirm_exit(self, e=None):
        if tkmb.askokcancel(
            "Quit Without Voting?",
            "Do You Really Want to Quit Without Saving Your Vote?"):
            self.destroy()
            sys.exit(0)

if __name__ == '__main__':
    c = OrderedDict()#categories
    c['test1'] = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
    c['test2'] = ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O")

    app = VotingApp(c)
    app.mainloop()
