#!/usr/bin/python3

import tkinter.tix as tk
from tkinter import ttk
import tkinter.messagebox as tkmb
from tkinter.constants import *
from scrolledlistbox import ScrolledListBox
import sys

class VotingFrame(ttk.Frame):
    def __init__(self, parent=None, people=(), reqchoices=3, *args, **kwargs):
        #super constructor
        tk.Frame.__init__(self, master=parent, *args, **kwargs)

        #setup instance vars
        self.candidates, self.selection = list(people), list()
        self.requiredChoices=reqchoices
        self.status = tk.StringVar()
        self.update_status()

        #create GUI widgets
        self.candidateLabel = tk.Label(self, text="Candidates")
##        self.configSelectFrame = tk.Frame(self)
        self.candidateList = tk.StringVar(value=tuple(self.candidates))
        self.candidateListbox = ScrolledListBox(self, padx=3, pady=3)
        self.candidateListbox.lb.config(selectmode=BROWSE,
                                        listvariable=self.candidateList)
        self.configSelect=tk.Button(self, text="Add", padx=3, pady=3,
                                 command=self.add_candidate)
        self.candidateListbox.lb.config(selectmode="single")

        self.pathLabel = tk.Label(self, text="Selection", padx=5, pady=3)
        self.chosenList = tk.StringVar(value=tuple(self.selection))
        self.chosenListbox = ScrolledListBox(self, padx=3, pady=3)
        self.chosenListbox.lb.config(listvariable=self.chosenList)
        self.increaseSelection = tk.Button(self, text="▲", padx=2,pady=2,
                                           command=self.increase_priority)
        self.decreaseSelection = tk.Button(self, text="▼", padx=2,pady=2,
                                           command=self.decrease_priority)
        self.candidateRemove = tk.Button(self, text="Remove", padx=3, pady=3,
                                    command=self.remove_candidate)

        self.statusLabel = tk.Label(self, textvariable=self.status)
##        self.saveChanges = tk.Button(self, text="Submit Vote", padx=3, pady=3,
##                                     command=lambda:tkmb.showwarning(
##                                         "Functionality Warning",
##                                         "voting not implemented"))

        self.candidateListbox.lb.bind("<<ListboxSelect>>", self.stupid_check)
        self.chosenListbox.lb.bind("<<ListboxSelect>>", self.stupid_check)
        #grid all the items to make them look nice
        self.candidateLabel.grid(row=0, column=0, sticky=NSEW)
        self.candidateListbox.grid(row=1, column=0, sticky=NSEW)
        self.configSelect.grid(row=2, column=0, sticky=NSEW)

        self.pathLabel.grid(row=0, column=1, columnspan=3, sticky=NSEW)
        self.chosenListbox.grid(row=1, column=1, columnspan=3, sticky=NSEW)
        self.increaseSelection.grid(row=2, column=1, sticky=NSEW)
        self.decreaseSelection.grid(row=2, column=2, sticky=NSEW)
        self.candidateRemove.grid(row=2, column=3, sticky=NSEW)


        self.statusLabel.grid(row=3, column=0, columnspan=3, sticky=(N,S,W))
##        self.saveChanges.grid(row=3, column=1, columnspan=3, sticky=NSEW)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        #set up everything
        self.stupid_check()

    def reload_listboxes(self, e=None):
        print("\treloading listboxes", file=sys.stderr)
        selectedCandidate = self.candidateListbox.selected()
        selectedChoice = self.chosenListbox.selected()


        self.candidateList.set(tuple(self.candidates))
        self.chosenList.set(tuple(self.selection))
        if selectedCandidate != None:
            if selectedCandidate >= len(self.candidates):
                self.stupid_check()
            else:
                self.candidateListbox.select(selectedCandidate)

        if selectedChoice != None:
            if selectedChoice >= len(self.selection):
                self.stupid_check()#will disable the add/ remove as appropriate
            else:
                self.chosenListbox.select(selectedChoice)
        print("\tdone reloading listboxes", file=sys.stderr)

    def update_status(self):
        remaining = self.requiredChoices - len(self.selection)
        if remaining == 0:
            self.status.set("All candidates chosen")
        else:
            self.status.set("{} candidates remaining".format(remaining))

    def add_candidate(self, e=None):
        candidateindex = self.candidateListbox.selected()
        self.selection.append(self.candidates.pop(candidateindex))
        self.update_status()
        self.stupid_check()

    def remove_candidate(self, e=None):
        candidateindex = self.chosenListbox.selected()
        self.candidates.append(self.selection.pop(candidateindex))
        self.update_status()
        self.stupid_check()

    def increase_priority(self, e=None):
        candidateindex = self.chosenListbox.selected()
        self.selection.insert(candidateindex-1,
                              self.selection.pop(candidateindex))
##        self.chosenListbox.lb.activate(candidateindex-1)
        self.chosenListbox.inc_selection()

        self.stupid_check()

    def decrease_priority(self, e=None):
        candidateindex = self.chosenListbox.selected()
        self.selection.insert(candidateindex+1,
                              self.selection.pop(candidateindex))
##        self.chosenListbox.lb.activate(int(candidateindex)+1)
        self.chosenListbox.dec_selection()

        self.stupid_check()

    def stupid_check(self, e=None):
##        self.reload_listboxes()#why?
        print("chosenListboxSelection:", self.chosenListbox._selected())

        #check whether it's valid to add candidates
        if len(self.candidates) == 0 \
           or self.candidateListbox.selected()==None \
           or len(self.selection) >= self.requiredChoices:
            #disable adding to list if no more candidates allowed or none selected

            self.configSelect.config(state=DISABLED)
            if len(self.candidates) != 0:
                #allow the user to select someone
                self.candidateListbox.lb.config(state=NORMAL)
            else:
                self.candidateListbox.lb.config(state=DISABLED)
        else:
            #re-enable adding to list
            print("reenabling movement")
            self.configSelect.config(state=NORMAL)
            self.candidateListbox.lb.config(state=NORMAL)

        if len(self.selection) == 0\
           or self.chosenListbox.selected()==None:
            #disable deleting / moving
            self.candidateRemove.config(state=DISABLED)
            self.increaseSelection.config(state=DISABLED)
            self.decreaseSelection.config(state=DISABLED)
            if len(self.selection) != 0:
                #allow the user to select someone
                self.chosenListbox.lb.config(state=NORMAL)
            else:
                self.chosenListbox.lb.config(state=DISABLED)

        else:
            #re-enable deleting / moving
            self.chosenListbox.lb.config(state=NORMAL)

            self.candidateRemove.config(state=NORMAL)

            if self.chosenListbox.curselection() == ('0',):
                #can't move up, already at the top of the list
                self.increaseSelection.config(state=DISABLED)
            else:
                self.increaseSelection.config(state=NORMAL)

            if self.chosenListbox.selected() == len(self.selection)-1:
                #can't move down, already at the end of the list
                self.decreaseSelection.config(state=DISABLED)
            else:
                self.decreaseSelection.config(state=NORMAL)
                self.chosenListbox.update()
##            self.chosenListbox.focus_force()
##            self.chosenListbox.update_idletasks()
##        if len(self.selection) == self.requiredChoices:
##            self.saveChanges.config(state=NORMAL)
##        else:
##            self.saveChanges.config(state=DISABLED)

        self.reload_listboxes()
        self.update_idletasks()
        
        print("#"*50, file=sys.stderr)
        self.event_generate("<<Vote>>")

    def vote_ready(self):
        return len(self.selection) == self.requiredChoices

if __name__ == '__main__':
    app = tk.Tk()
    app.title("Voting Frame Test Window")
    f = VotingFrame(app, ("Candidate 0",
                          "Candidate 1",
                          "Candidate 2",
                          "Candidate 3",
                          "Candidate 4",
                          "Candidate 5",
                          "Candidate 6",
                          "Candidate 7",
                          "Candidate 8",
                          "Candidate 9"))
    f.pack()
    app.resizable(0, 0)
    app.mainloop()



