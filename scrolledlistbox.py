#!/usr/bin/python3

import tkinter.tix as tk
from tkinter.constants import *
import sys

class ScrolledListBox(tk.Frame):
    currentinstance = 0
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        #set name for debugging
        self.name = "ScrolledListBox"+str(ScrolledListBox.currentinstance)
        ScrolledListBox.currentinstance += 1
        print("created:", self.name)

        self.scrollbar = tk.Scrollbar(self)
        self.lb = tk.Listbox(self, exportselection=0,
                             yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y, in_=self)
        self.lb.pack(fill=BOTH, expand=True, side=LEFT, in_=self)
        self.scrollbar.config(command=self.lb.yview)
        self.bind("<Up>", self.inc_selection)
        self.bind("<Down>", self.dec_selection)

    def inc_selection(self, e=None):

        print("Incrementing selection of", self.name)
        print("selection beforehand =", self._selected())
        selected = self._selected()
        if selected==None:
            return
        if selected == 0:
            return#can't move higher than 0

        self.select(selected-1)
        print("selection afterward =", self._selected())
        print("-"*20)
        if e:
            #if called by handler, cancel other events triggered
            return "break"

    def dec_selection(self, e=None):
        print("decrementing selection of", self.name)
        print("selection beforehand =", self._selected())
        selected = self._selected()
        if selected == None:
            return
        if selected == self.lb.size()-1:
            return#can't move lower if at bottom
        self.select(selected+1)
        print("selection afterward =", self._selected())
        print("-"*20)
        if e:#kill other events triggered by other handlers
            return "break"


    def selected(self):
        selection = self.lb.curselection()
        print("selection report for {0}:".format(self.name))
        print('selected:', selection)
        print("ACTIVE:", self.lb.index(ACTIVE))
        print("ANCHOR:", self.lb.index(ANCHOR))

        if len(selection) == 1:
            print('returning only curselection')
            print("-"*20)
            return int(selection[0])
        elif len(selection) > 1:
            print('returning ANCHOR')
            print("-"*20)
            return int(self.lb.index(ANCHOR))
        print('no value to return', file=sys.stderr)
        print("-"*20)

        return None
    def _selected(self):
        selection = self.lb.curselection()
        if len(selection) == 1:
            return int(selection[0])
        elif len(selection) > 1:
            return int(self.lb.index(ANCHOR))
        return None

    def select(self, index):
        print("selecting {0} in {1}".format(index, self.name))
        if index != None:
            self.lb.selection_clear(0, END)
            self.lb.selection_anchor(index)
            self.lb.selection_set(index)
            self.lb.activate(index)

            self.lb.see(index)
            print("success")
        else: print("failure", file=sys.stderr)
        print("-"*20)


    def __getattr__(self, name):
        if hasattr(self.lb, name):
            return getattr(self.lb, name)
        raise AttributeError

