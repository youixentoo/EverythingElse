# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 14:06:46 2017

@author: thijs

"""
import re
import tkinter as gui
from tkinter import *

class IRC_codes:
    def __init__(self):
        self.mainwindow = gui.Tk()
        self.mainwindow.minsize(350,400)
        self.leftframe = gui.Frame(self.mainwindow)
        self.rightframe = gui.Frame(self.mainwindow)
        
        self.button = gui.Button(self.leftframe, text='Execute', command=self.IRC, width=9)
        self.searching = gui.Button(self.rightframe, text='Search', command=self.Pep, width=9)
        
        #self.clear = gui.Button(self.rightframe, text='Clear', command=self.clear)
        
        self.file = gui.Label(self.leftframe, text='File')
        self.quest = gui.Label(self.rightframe, text='IRC code')
        
        self.entry = gui.Entry(self.leftframe, width=40)
        self.s_entry = gui.Entry(self.rightframe, width=40)
        
        #self.radio_var1 = gui.IntVar()
        
        #self.rb1 = gui.Radiobutton(self.midframe, text='IRC codes', variable = self.radio_var1, value=1)
        #self.rb2 = gui.Radiobutton(self.midframe, text='Peptide sequence', variable = self.radio_var1, value=2)
        
        self.output_I = gui.Text(self.leftframe, wrap='word')
        
        #scrollbar = gui.Scrollbar(self.rightframe)
        #scrollbar.pack(side='right', fill='y')
                
        #self.output_p = gui.Text(self.rightframe, wrap='word', yscrollcommand=scrollbar.set)
        self.output_p = gui.Text(self.rightframe, wrap='word')
        
        #scrollbar.config(command=self.output_p.yview)
        
        self.leftframe.pack(side='left')
        self.rightframe.pack(side='right')
        
        
        
        self.file.pack() #left
        self.entry.pack() #left
        self.button.pack() #left        
        self.output_I.pack() #left
        #self.rb1.pack()
        #self.rb2.pack()
        self.quest.pack()
        self.s_entry.pack() #right
        self.searching.pack() #right
        self.output_p.pack() #right
        #self.clear.pack()
        
        gui.mainloop()
    
    def Options(self):
        Option = int(self.radio_var1.get())
        IRC_list,Search_list = self.IRC()
        
        if Option == 1:
            self.IRC()
        if Option == 2:
            self.Pep(IRC_list,Search_list)
    
    
    def IRC(self):
        Error = False
        
        try:
            bestand = open(self.entry.get()+'.txt').readlines()
        except FileNotFoundError:
            self.output_I.delete(1.0, END)
            self.output_I.insert(1.0, 'File not found, try again')
            Error = True
        
        if Error != True:
            i = 0
            Peptides = []            
            Search_list = []
            IRC_list = []
            
            for x in bestand:
                if re.search('C.[DNEHQSTI]C.{4,6}[ST].{2}[WM][HR][RKENAMSLPGQT]', x) != None:
                    n = re.search('IRC_\d{1,20}', x)
                    IRC_list.append(x[n.start():n.end()])
                    Search_list.append(x)
        
            self.output_I.delete('1.0', END)
            self.output_I.insert(1.0,str(IRC_list))

            #print(IRC_list)
                
            for item in Search_list:
                if IRC_list[i] in item:
                    Tab = re.search('\tM[GALMFWKQESPVICYHRNDT]{1,}',item)
                    Seq = item[Tab.start():]
                    Seq = Seq.replace('\t','').replace('\n','')
                    Peptides.append(Seq)
                i += 1
                
            Combined = dict(zip(IRC_list,Peptides))
            
            return Combined
        

    def Pep(self):
        IRC_text = self.output_I.get(1.0, END)
        if len(IRC_text) != 0 or IRC_text != 'File not found, try again':
            question = self.s_entry.get()
            Combined = self.IRC()
            
            try:
                output = Combined.get(question)
            except AttributeError:
                self.output_p.delete(1.0, END)
                self.output_p.insert(1.0,'Please search all the IRC codes before submitting')
                
            try:
                self.output_p.delete(1.0, END)
                self.output_p.insert(1.0,str(output))
            except UnboundLocalError:
                self.output_p.delete(1.0, END)
                self.output_p.insert(1.0,'Please search all the IRC codes before submitting')
            
        else:
            self.output_p.delete(1.0, END)
            self.output_p.insert(1.0,'Please search all the IRC codes before submitting')
            
        
        

        
        
        

    #def clear(self):
     #   self.output.delete(1.0, END)


obj1 = IRC_codes()     
        #return IRC_list,Search_list
    
"""
def Pep(IRC,Search):
    x = 0
    Peptides = []
        
    for item in Search:
        if IRC[x] in item:
            Tab = re.search('\tM[GALMFWKQESPVICYHRNDT]{1,}',item)
            Seq = item[Tab.start():]
            Seq = Seq.replace('\t','').replace('\n','')
            Peptides.append(Seq)
        x += 1
    
    return Peptides
        
def Combine(IRC,PEP):
    Combined = dict(zip(IRC, PEP))
    return Combined












class Pep_codes(IRC_codes):
    def __init__(self,IRC):
        self.Bestand = IRC.bestand
        self.Codes = IRC.IRC_list
        
        self.mainwindow = gui.Toplevel()
        self.mainwindow.minsize(350,400)
        self.topframe = gui.Frame(self.mainwindow)
        self.downframe = gui.Frame(self.mainwindow)
        
        self.label1 = gui.Label(self.topframe, text='IRC:')
        
        self.entry = gui.Entry(self.topframe, width=40)
        
        self.button = gui.Button(self.topframe, text='Search', command=self.Pep)
"""


       