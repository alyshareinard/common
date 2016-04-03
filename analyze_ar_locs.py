# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 13:51:06 2016

@author: alysha.reinard
"""
import pickle
import numpy as np
import pdb
import matplotlib.pyplot as plt
import math

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
            if x[3]=="E": EW_val=-EW_val
        
            NS.append(NS_val)
            EW.append(EW_val)

        else:
            NS.append(None)
            EW.append(None)
    ar_vals["NS"]=NS
    ar_vals["EW"]=EW
    print(ar_vals["noaa_spot_gn"][0:20])
    try:
        f=open('data/ar_grouped.p', 'rb')
        ar_indexes=pickle.load(f, encoding='latin1')
#        ar_indexes=pickle.load(f)
        print("loaded file")
    except Exception as e:
        print(e)
        print("recalculating from scratch")
        ar_indexes=group_ars(ar_vals)
        
    dist_vs_time(ar_indexes, ar_vals)
#    try:
#        f=open('data/ar_moves.p')
#        movement_diff=pickle.load(f)
#    except:
#        movement_diff=map_ar_movement(ar_vals, ar_indexes)
#    time_diff=[x[1] for x in movement_diff]
#    NS_vel=[x[3]/(x[1].total_seconds()/60./60.) for x in movement_diff]
#    EW_vel=[x[4]/(x[1].total_seconds()/60./60.) for x in movement_diff]
#    NS_vel=NS_diff/time_diff
#    EW_vel=EW_diff/time_diff
    #TODO: put this in reasonable units -- also check degrees vs distance and if
    #it's different near limb
#    print("at end")
#    print(movement_diff[0:100])
#    print(NS_vel[0:100])
#    print(EW_vel[0:100])
#    return (NS_vel, EW_vel, movement_diff)
    
def dist_vs_time(ar_indexes, ar_vals):
    slopes=[]
    count_bad=0
    count_good=0
    good_ars=[]
    for ar in ar_indexes:
        if len(ar)>=5:
            EW_vals=ar_vals["EW"][ar]
            NS_vals=ar_vals["NS"][ar]
            time_vals=ar_vals["ar_date"][ar]
            print(EW_vals)
            print(time_vals)
            print(ar_vals["loc"][ar])
            print(ar_vals["noaa_spot_gn"][ar])
    #        print(type(time_vals))
            init_time=time_vals.values[0]
            time_diffs=[x-init_time for x in time_vals.values] #normalize to zero
            time_diffs=[x.total_seconds()/60./60 for x in time_diffs]
            fit, res, _, _, _=np.polyfit(time_diffs, EW_vals, 1, full=True)
            print(fit)
            slopes.append(fit[0])
            fit_fn=np.poly1d(fit)
            print(fit_fn)
            print(math.sqrt(res)/len(ar))
            plt.plot(time_diffs, EW_vals, 'yo', time_diffs, fit_fn(time_diffs), '--k')
            plt.show()
            if (math.sqrt(res)/len(ar)) > 1 or (fit[0]<0.4 or fit[0]>0.7): 
                pauseit=input("good enough (g), take out a couple point (t) or bad (b) (q) to break")                
                if pauseit=="q": break
                elif pauseit=="g": 
                    good_ars.append(ar)
                    count_good+=1
                elif pauseit=="t":
                    removeit=input("which points?")
                    done=False
                    
                    while done == False:
                        new_ar=list(ar)
                        badpoints=[]
                        for val in removeit.split(" "):
                            badpoints.append(int(val))
                        for index in sorted(badpoints, reverse=True):
                            del new_ar[index]
                        EW_vals=ar_vals["EW"][new_ar]
                        time_vals=ar_vals["ar_date"][new_ar]
                        init_time=time_vals.values[0]
                        time_diffs=[x-init_time for x in time_vals.values] #normalize to zero
                        time_diffs=[x.total_seconds()/60./60 for x in time_diffs]                       
                        fit, res, _, _, _=np.polyfit(time_diffs, EW_vals, 1, full=True)
                        slopes.pop()
                        slopes.append(fit[0])
                        fit_fn=np.poly1d(fit)
                        plt.plot(time_diffs, EW_vals, 'yo', time_diffs, fit_fn(time_diffs), '--k')
                        plt.show()
                        goodnow=input("good now (g), try again (t), no good -- give up (n)")
                        if goodnow=="g": 
                            count_good+=1
                            good_ars.append(ar)
                            done=True
                        if goodnow=="n":
                            count_bad+=1
                            slopes.pop()
            else:
                good_ars.append(ar)
                count_good+=1
    print("bad", count_bad)
    print("good", count_good)
    filehandler=open("data/good_ars.p", "wb")
    pickle.dump(good_ars, filehandler)
    
    plt.hist(slopes, bins=[.4, 0.425, 0.45, 0.475, .5, 0.525, 0.55, 0.575, .6, 0.625, 0.65, 0.675, .7])
    plt.show()
    
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
        if target not in done and target !=None:
            done.append(target)
 #           print(target)
            for index, noaa_spot in enumerate(ar_vals["noaa_spot_gn"]):
                if noaa_spot==target:
                    matching_index.append(index)
            target_index.append(matching_index)

    filehandler=open('data/ar_grouped.p', 'wb')
    pickle.dump(target_index, filehandler)
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
#            print("time through", time_through)
            if time_through==0:
                old_ar_num=ar_vals["noaa_spot_gn"][index]
                old_time=ar_vals["ar_date"][index]
                old_loc=ar_vals["loc"][index]
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
#                    print(time_diff)
                    if time_diff.total_seconds()<0 and EW_diff>0:
                        print(ar_set)
                        print("time diff is negative", time_diff)
                        print(ar_vals["ar_date"][index])
                        print(old_time)
                        print(index)
                        print(old_loc, loc)
                        print(NS_diff, old_NS)
                        print(EW_diff, old_EW)
                        print(old_ar_num)
                        print(ar_vals["ar_date"][ar_set])
                        pass
#                        pdb.set_trace()
                    saveit=[old_ar_num, time_diff, loc, NS_diff, EW_diff]
                    ar_movement_diff.append(saveit)
                except:
                    pass
#                    print("skipping None")
                old_loc=loc
                old_time=ar_vals["ar_date"][index]
                old_NS=ar_vals["NS"][index]
                old_EW=ar_vals["EW"][index]
                
    filehandler=open('data/ar_moves.p', 'wb')
    pickle.dump(ar_movement_diff, filehandler)
    return ar_movement_diff
                
            
        

    
load_ar_locs()
