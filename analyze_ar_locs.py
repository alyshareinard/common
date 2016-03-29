# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 13:51:06 2016

@author: alysha.reinard
"""
import pickle

def load_ar_locs():
    f=open('data/ar_vals.p', 'rb')
    ar_vals=pickle.load(f)
    location=ar_vals["loc"]
    NS=[]
    EW=[]
    
    for index, x in enumerate(location):
        if x !=None and len(x)==6:
            #print("x", x)
            NS_val=int(x[1:3])
            EW_val=int(x[4:6])
            if x[0]=="S": NS_val=-NS_val
            if x[3]=="E": EW_val==-EW_val
        
            NS.append(NS_val)
            EW.append(EW_val)
        else:
            NS.append(None)
            EW.append(None)
    ar_vals["NS"]=NS
    ar_vals["EW"]=EW
    print(ar_vals["noaa_spot_gn"][0:20])
    ar_indexes=group_ars(ar_vals)
    movement_diff=map_ar_movement(ar_vals, ar_indexes)
    time_diff=[x[1] for x in movement_diff]
    NS_diff=[x[3] for x in movement_diff]
    EW_diff=[x[4] for x in movement_diff]
    NS_vel=NS_diff/time_diff
    EW_vel=EW_diff/time_diff
    print(NS_vel)
    
    
def group_ars(ar_vals):
#    print(len(ar_vals))
#    for index in range(len(ar_vals)):
    index=0
    target=ar_vals["noaa_spot_gn"][index]
#    print(target)
    target_index=[]
    done=[]
    for target in ar_vals["noaa_spot_gn"]:

        matching_index=[]
        if target not in done:
            done.append(target)
 #           print(target)
            for index, noaa_spot in enumerate(ar_vals["noaa_spot_gn"]):
                if noaa_spot==target:
                    matching_index.append(index)
            target_index.append(matching_index)

#    print(target_index)
#    print(ar_vals["loc"][target_index[1]])
    return target_index 

def map_ar_movement(ar_vals, ar_indexes):
    ar_movement_diff=[]
    for ar_set in ar_indexes:
        #for this I'm just going to take pairs of different measurements of the
        #same AR and save the AR number, time difference, starting location, NS motion, EW motion

        time_through=0
        for index in ar_set:
            if time_through==0:
                old_ar_num=ar_vals["noaa_spot_gn"][index]
                old_time=ar_vals["ar_date"][index]
                loc=ar_vals["loc"][index]
                old_NS=ar_vals["NS"][index]
                old_EW=ar_vals["EW"][index]
                time_through+=1
            else:
                if ar_vals["noaa_spot_gn"][index]!=old_ar_num:
                    print("not the same AR!")
                    break
                try:
                    loc=ar_vals["loc"][index]
                    time_diff=ar_vals["ar_date"][index]-old_time
                    NS_diff=ar_vals["NS"][index]-old_NS
                    EW_diff=ar_vals["EW"][index]-old_EW
                    saveit=[old_ar_num, time_diff, loc, NS_diff, EW_diff]
                    ar_movement_diff.append(saveit)
                except:
                    print("skipping None")
                old_time=ar_vals["ar_date"][index]
                old_NS=ar_vals["NS"][index]
                old_EW=ar_vals["EW"][index]
                
    return ar_movement_diff
                
            
        

    
load_ar_locs()
