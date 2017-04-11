# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 10:04:14 2017

@author: thijs

 "While this isn't directly related to the problem, 
 tkinter isn't designed to have more than one instance of Tk. 
 If you want to create an additional window you should create an instance of Toplevel 
 – Bryan Oakley Mar 28 '14 at 12:37" (http://stackoverflow.com/questions/20012489/unboundlocalerror-local-variable-referenced-before-assignment)



"""

import re
import tkinter as gui
from tkinter import messagebox
from tkinter import *


class FirstGui:
    def __init__(self):
        self.mainwindow = gui.Tk()
        self.mainwindow.minsize(400,350)
        self.top_frame = gui.Frame(self.mainwindow)
        self.down_frame = gui.Frame(self.mainwindow)
        self.button = gui.Button(self.top_frame, text='Execute', command=self.files, width=9)
        
        self.label1 = gui.Label(self.top_frame, text='File')
        
        self.invoer = gui.Entry(self.top_frame, width = 40)

        self.radio_var = gui.IntVar()
        
        self.label2 = gui.Label(self.top_frame, text='Type of file:')
        
        self.rb1 = gui.Radiobutton(self.top_frame, text='Fasta', variable = self.radio_var, value=1)
        self.rb2 = gui.Radiobutton(self.top_frame, text='Genbank', variable = self.radio_var, value=2)
        
        scrollbar = gui.Scrollbar(self.down_frame)
        scrollbar.pack(side='right', fill='y')
                
        self.output_v = gui.Text(self.down_frame, wrap='word', yscrollcommand=scrollbar.set)
        self.output_v.pack()
        
        scrollbar.config(command=self.output_v.yview)
        
        self.next = gui.Button(self.mainwindow, text='Next', command=SecondGui, width = 8)
        
        self.empty = gui.Label(self.down_frame, text = ' ')
        
        self.top_frame.pack()
        self.down_frame.pack()
        
        self.next.pack()
        self.next.place(relx=1,x=-2,y=2,anchor=NE)
        
        self.label1.pack()
        self.invoer.pack()
        self.label2.pack()
        self.rb1.pack()
        self.rb2.pack()
        self.button.pack() 
        self.empty.pack()
        
        gui.mainloop()
        
        
    def files(self):
        number = int(self.radio_var.get())
        going = True
        if number == 1:
            try:
                bestand = open(self.invoer.get()+'.fasta').read()
            except FileNotFoundError:
                self.output_v.delete('1.0', END)
                self.output_v.insert(1.0,'File not found, please try again')
                
            origin = re.search('\n',bestand)
            begin = origin.end()
            string = bestand[begin:]
            
            step = string.replace(' ','').replace('\n','').replace('//','').replace('\r','')         # Verwijder alles behalve de getallen
            seq = re.sub(r'\d+', '', step)
            output = seq.upper()
            
        if number == 2:
            
            try:
                bestand = open(self.invoer.get()+'.gb').read()
            except FileNotFoundError:
                self.output_v.delete('1.0', END)
                self.output_v.insert(1.0,'File not found, please try again')
            
            origin = re.search('ORIGIN',bestand)
            begin = origin.end()
            string = bestand[begin:]
            
            step = string.replace(' ','').replace('\n','').replace('//','').replace('\r','')         # Verwijder alles behalve de getallen
            seq = re.sub(r'\d+', '', step)
            output = seq.upper()
            
        self.output_v.delete('1.0', END)
        self.output_v.insert(1.0,str(output))

   
    
class SecondGui:
    def __init__(self):
        self.main_window = gui.Toplevel() #gui.Tk() gewijzigd naar gui.Toplevel()
        self.main_window.minsize(400,350)
        self.top_frame = gui.Frame(self.main_window)
        self.down_frame = gui.Frame(self.main_window)
        self.my_button = gui.Button(self.top_frame, text='Execute',command=self.methode)
                
        self.label1 = gui.Label(self.top_frame, text='Name')
        self.label1.pack()
        
        self.org = gui.Entry(self.top_frame, width = 40)
        self.org.pack()
        
        self.label2 = gui.Label(self.top_frame, text='Sequence')
        self.label2.pack()
        
        self.invoer = gui.Entry(self.top_frame, width = 40)
        self.invoer.pack()  
        
        self.radio_var1 = gui.IntVar()
               
        self.rb1 = gui.Radiobutton(self.top_frame, text='Transcript', variable = self.radio_var1, value=1)
        self.rb2 = gui.Radiobutton(self.top_frame, text='Translate', variable = self.radio_var1, value=2)
       
        scrollbar = gui.Scrollbar(self.down_frame)
        scrollbar.pack(side='right', fill='y')
                
        self.output_v = gui.Text(self.down_frame, wrap='word', yscrollcommand=scrollbar.set)
        self.output_v.pack()
        
        scrollbar.config(command=self.output_v.yview)
                
        self.writin = gui.Button(self.down_frame, text='Write to file', command=self.writing)
                                 
        self.rb1.pack()
        self.rb2.pack()
        self.my_button.pack()
        self.top_frame.pack()
        self.down_frame.pack()
        self.writin.pack(side='right')
        #self.v_label.pack(expand=True)
        gui.mainloop()
        
        
    def methode(self):
        wat = self.org.get()
        tekst = self.invoer.get()
        number = int(self.radio_var1.get())
        seq = tekst.replace(' ','').replace('\n','')

        if len(seq) == (seq.count('A') + seq.count('T') + seq.count('C') + seq.count('G')):
            print('yes')
            DNA = True
        else:
            DNA = False
            ending = 'This is not a DNA sequence, only use DNA sequences please'
        
        if number == 1 and DNA:
            message = 'Transcripted DNA'
            sequentie = tekst
            ending = sequentie.replace('T','U')
            
        if number == 2 and DNA:
            message = 'Aminoacid sequence'
            sequentie = tekst
            sequentie = sequentie.upper()
            stop = False
            aug = re.search("ATG",sequentie)
            pos1 = aug.start()
            n = aug.start()
            
            while not stop:
                if "TGA" in sequentie[n:n+3]:
                    stop = True
                    coded = sequentie[pos1:n+3]
                elif "TAA" in sequentie[n:n+3]:
                    stop = True
                    coded = sequentie[pos1:n+3]
                elif "TAG" in sequentie[n:n+3]:
                    stop = True
                    coded = sequentie[pos1:n+3]
                else:
                    n+=3
            
            coded = coded.lower()
            coding = [ coded[start:start+3] for start in range(0, len(coded), 3) ]
            
            code = {'ttt': 'F', 'tct': 'S', 'tat': 'Y', 'tgt': 'C',
                    'ttc': 'F', 'tcc': 'S', 'tac': 'Y', 'tgc': 'C',
                    'tta': 'L', 'tca': 'S', 'taa': '*', 'tga': '*',
                    'ttg': 'L', 'tcg': 'S', 'tag': '*', 'tgg': 'W',
                    'ctt': 'L', 'cct': 'P', 'cat': 'H', 'cgt': 'R',
                    'ctc': 'L', 'ccc': 'P', 'cac': 'H', 'cgc': 'R',
                    'cta': 'L', 'cca': 'P', 'caa': 'Q', 'cga': 'R',
                    'ctg': 'L', 'ccg': 'P', 'cag': 'Q', 'cgg': 'R',
                    'att': 'I', 'act': 'T', 'aat': 'N', 'agt': 'S',
                    'atc': 'I', 'acc': 'T', 'aac': 'N', 'agc': 'S',
                    'ata': 'I', 'aca': 'T', 'aaa': 'K', 'aga': 'R',
                    'atg': 'M', 'acg': 'T', 'aag': 'K', 'agg': 'R', 
                    'gtt': 'V', 'gct': 'A', 'gat': 'D', 'ggt': 'G',
                    'gtc': 'V', 'gcc': 'A', 'gac': 'D', 'ggc': 'G',
                    'gta': 'V', 'gca': 'A', 'gaa': 'E', 'gga': 'G',
                    'gtg': 'V', 'gcg': 'A', 'gag': 'E', 'ggg': 'G'}
                
            ending = ''.join(str(code.get(coding, coding)) for coding in coding) 
                   
        self.output_v.delete('1.0', END)
        self.output_v.insert(1.0,str(ending))

    def writing(self):
        naam = str(self.org.get())
        file = open(naam+'.txt', 'w')
        writing = self.output_v.get(1.0, END)
        file.write(str(writing))
        file.close()
        
        
FirstGui()






















