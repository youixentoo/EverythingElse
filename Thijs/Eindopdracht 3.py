# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 12:28:54 2017
Vanuit een multiple fasta bestand, een hydropatie grafiek maken.

@author: Thijs Weenink


#Note 1:
Bestand omzetten gehaald van https://cartwrightlab.wikispaces.com/File+Formatting#Remove%20Line%20Breaks%20from%20Sequences
Variabelen omgezet naar meer logische namen

#Note 2:
Gekopieerd en geplakt vanuit andere afvinkopdrachten en weektaken
Kan hierdoor overeenkomstig zijn bij andere mensen

#Note 3:
De rest van de code is zelf geschreven. Doordat ik mensen heb geholpen, kunnen er overeenkomsten zijn.
"""
import re
import numpy as np
import matplotlib.pyplot as plt
from Bio.SeqUtils import seq3
                                                            

try:

    def main():
        bestand()
        try:
            file = open('fixedprot.txt')                    # Bestand openen, gemaakt door bestand()
        except FileNotFoundError:
            print('File not found')
        
        
        Dictonairy_full, accessie_codes = get_proteins(file)
        Defensins = get_def(Dictonairy_full, accessie_codes)
        get_hydropathy(Defensins)
        
    
    def bestand(): #Note 1
        try:
            Original = open('prots.fa')
            Edited = open('fixedprot.txt','w')              # Openen 2e bestand voor plakken sequenties zonder enters
        except FileNotFoundError:
            print('File not found')
            
            
        line = Original.readline() 
         
        while line: 
            Edited.write(line)                              # Schrijf de regel in het bestand
            sequenceList = [] 
            line = Original.readline() 
            while line and not line.startswith('>'):        # While loop voor 1 of meer regels
                sequenceList.append(line.strip('\n')) 
                line = Original.readline()                  
            Edited.write('%s\n' % ''.join(sequenceList))    # Verwijderen van de \n uit de sequentie
            
        Original.close()
        Edited.close()   
        
       
    def get_proteins(bestand):
        acces = []
        sequence = []
        
        for line in bestand.readlines():
            accessie = re.search('\|.+\|',line)             # Zoeken van de accessiecode
            if accessie != None:                            # Alleen headers
                start = accessie.start()
                end = accessie.end()
                acces.append(line[start+1:end-1])           # Zonder de |
            else:
                sequence.append(line.replace('\n',''))
        print('Accessie codes: ',acces)
        #print(sequence)
                
        Combined = dict(zip(acces,sequence))
        #print(Combined)
        return Combined, acces
    
    
    def get_def(Dictonary,codes):                           # BioPython omdat ik dat had in plaats van het aanpassen van de dictionary
        patroon_true = []                                   # seq3() = BioPython, maakt van de 1 lettercode een 3 lettercode
        patroon_false = []
        codes_true = []
        codes_false =[]
        
        for code in codes:
            seq = Dictonary.get(code)
            defensin = re.search('C.C.{3,5}C.{7}G.C.{9}CC',seq)
            if defensin != None:
                #print('Deze sequentie bevat het consensus patroon\n',seq[defensin.start():defensin.end()])
                patroon_true.append(seq3(seq))
                codes_true.append(code)
                Dict_acc_pat_true = dict(zip(codes_true,patroon_true))
            else:
                #print('Deze sequentie bevat niet het consensus patroon')
                patroon_false.append(seq3(seq))
                codes_false.append(code)
                Dict_acc_pat_false = dict(zip(codes_false,patroon_false))
        
        #print(Dict_acc_pat_true)
        #print(Dict_acc_pat_false)
        
        return Dict_acc_pat_true                            # Dict_acc_pat_false niet omdat daar geen data in staat
    
        
    def get_hydropathy(Defensins):
        
        try:
            choice = input('Accessie code voor grafiek: ')
            
            hydropatie = {	"Ile":-0.528, 
                    		   "Leu":-0.342,
                    		   "Phe":-0.370,
                    		   "Val":-0.308,
                    		   "Met":-0.324,
                    		   "Pro":-0.322,
                    		   "Trp": -0.270,
                    		   "His": 2.029,
                    		   "Thr": 0.853,
                    		   "Glu": 3.173,
                    		   "Gln": 2.176,
                    		   "Cys": 0.081,
                    		   "Tyr": 1.677,
                    		   "Ala":-0.495,
                    		   "Ser": 0.936,
                    		   "Asn": 2.354,
                    		   "Asp": 9.573,
                    		   "Arg": 4.383,
                    		   "Gly": 0.386,
                    		   "Lys": 2.101
                    		  }
            
            sequentie = Defensins.get(choice)
            Acids = [ sequentie[start:start+3] for start in range(0, len(sequentie), 3) ]   #Note 2
            values = ' '.join(str(hydropatie.get(Acids, Acids)) for Acids in Acids)
            numbers = values.split(' ')
            
            #print(Acids,'\n')
            #print(values,'\n')
            #print(numbers)
            lengte = len(numbers)
            Hydros = []
            
            for x in numbers:
                Hydros.append(float(x))
            
            xs = range(lengte)
            ys = Hydros
            
            plt.figure(figsize=(13,7))
            plt.plot(xs, ys, color='gray')
            plt.ylabel('Hydropatie waardes')
            plt.xlabel('Aminozuur nummer')
            plt.title(choice)
            
            plt.fill_between(xs, 0, ys, where=np.asarray(ys) > 0, color='green', interpolate=True)    
            plt.fill_between(xs, 0, ys, where=np.asarray(ys) <= 0, color='red', interpolate=True)
            
            plt.gcf()
            plt.savefig(choice+'.png')
        
        except TypeError:
            print('Invalid input')    
    
    
    main()

except KeyboardInterrupt:
    print('User interrupted')

