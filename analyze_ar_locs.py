# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 13:51:06 2016

@author: alysha.reinard
"""
import pickle

def analyze_ar_locs():
    f=open('../data/ar_vals.p', 'rb')
    ar_vals=pickle.load(f)
    location=ar_vals["loc"]
    NS=[]
    EW=[]
    
    for index, x in enumerate(location):
        if x !=None and len(x)==6:
            print("x", x)
            NS_val=int(x[1:3])
            EW_val=int(x[4:6])
            if x[0]=="S": NS_val=-NS_val
            if x[3]=="E": EW_val==-EW_val
        
            NS.append(NS_val)
            EW.append(EW_val)
        else:
            NS.append(None)
            EW.append(None)
            
#    print(location[0:20])
#    print(NS[0:20])
#    print(EW[0:20])
    
analyze_ar_locs()