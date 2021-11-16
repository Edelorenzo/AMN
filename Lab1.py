# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 10:33:19 2021

@author: Eline
"""

import numpy as np
import numpy.linalg as linalg
import pandas as pd
import os
import matplotlib.pyplot as plt

cwd = os.getcwd()
path = cwd + '\\cat_exp1.xlsx'
df = pd.read_excel(path, 'exp1')
data_meas = np.array(df)
D = data_meas[:,0]


# #Debug - check variable content
# print(df)
# print(data_meas)

#Variables

P = 10**5 #Pa
R = 8.31446 #Gass constant
T = 303 #K
C_sin = 20 #mM
C_pin = 0
xO2_in = 0.21 #Volume percentage
xCO2_in = 0
N_in = 0.006 #m^3/h
F_in = data_meas[:,0]           #L/h
C_s = data_meas[:,1]            #mM
C_p = data_meas[:,2]            #mM
TOC = data_meas[:,3]            
xO2 = (data_meas[:,4])/100      #perunage
xCO2 = data_meas[:,5]


#Calculation of rates with mass balances
rs = F_in*(C_sin-C_s)           #mmol/h
rp = F_in*(C_pin-C_p)           #mmol/h
VO2 = N_in*(xO2_in-xO2)         #m^3/h
rCO2 = N_in*(xCO2_in-xCO2)      #mmol/h
rO2 = VO2*(((P)/(R*T))*1000)      #mmol/h

# Debug - check calculation output
print("rs is", rs)
print("rp is", rp)
print("rO2 is", rO2)
print("rCO2 is", rCO2)

#Carbon balance, Oxygen balance and elecron balance

Cbalance = ((6*rs)+(6*rp))
Obalance = ((2*rs)+(4*rp)+(2*rO2))
ebalance = ((26*rs)+(22*rp)+(-4*rO2))

print('the c-balance has a total recovery of', Cbalance)
print('the o-balance has a total recovery of', Obalance)
print('the e-balance has a total recovery of', ebalance)

#get element composition from excel
df = pd.read_excel(path, 'Element_matrix', index_col=[0])
Emat = np.array(df)

#bundel in the ones you need
Rin = np.vstack((rs, rp, rO2, rCO2))

#select columns for Ein and Eout
Ein = Emat[:, [0,2]]
Eout = Emat[:, [1, 3]]

gap = np.zeros( (2, D.size) )
rec = np.zeros( (2, D.size) )

for iD in range (D.size):
    igap =| Ein @ Rin[:,iD]-Eout @ Rout[:,iD]
    irec = 1 - igap / (Ein @ Rin[:,iD])
    
    gap[:,iD] = igap
    rec[:,iD] = irec

print(rec)
print(gap)
    

