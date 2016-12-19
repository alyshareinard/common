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
import sys
from datetime import datetime
import os

def load_ar_locs():
    
    f=open(os.getcwd()+os.sep+'data'+os.sep+'ar_vals.p', 'rb')
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
        
    try:
        f=open('data/matched_ars_alldone.p', 'rb')
        matches=pickle.load(f)
    except:
        matches=match_ars(ar_vals)
    
    #now let's clean up the matches/pick the best ones
    overcount=0
    for match in matches:
        if len(match)>2:
            overcount+=1
    print(overcount)
    
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
    
    
def match_ars(ar_vals):
    
    try:
        f=open("data/good_ars_alldone.p", "rb")
        ars=pickle.load(f)
    except:
        dist_vs_time_auto(ar_indexes, ar_vals)    
#    f=open("data/good_ars_alldone.p", "rb")
#    ars=pickle.load(f)
    ar_indexes=[]
    ar_nums=[]
    ar_fits=[]
    times=[]
    EWs=[]
    NSs=[]
    init_time=datetime(1982, 1, 1, 0, 0)
    for ar in ars:
        #collect all the AR indexes in one list (instead of a list of lists)
        for val in ar:
            ar_indexes.append(val)
        time_vals=ar_vals["ar_date"][ar]
        time_diffs=[x-init_time for x in time_vals.values] #normalize to zero
        time_diffs=[x.total_seconds()/60./60/24. for x in time_diffs]
        EW_vals=ar_vals["EW"][ar]
        NS_vals=ar_vals["NS"][ar]
        times.append(time_diffs)
        EWs.append(EW_vals)
        NSs.append(NS_vals)
        fit, res, _, _, _=np.polyfit(time_diffs, EW_vals, 1, full=True)
#        fit_fn=np.poly1d(fit)
        ar_nums.append(ar_vals["noaa_spot_gn"][ar[0]])
        ar_fits.append(fit)
        
    EW_all=ar_vals["EW"][ar_indexes]
    time_all=ar_vals["ar_date"][ar_indexes]
    time_diffs_all=[x-init_time for x in time_all.values] #normalize to zero
    time_diffs_all=[x.total_seconds()/60./60/24. for x in time_diffs_all]
#    plt.plot(time_diffs_all, EW_all, 'yo')
#    plt.xlim(-35, 20)
#    plt.show()
    ar_matches=[]
    for ar in ars:

        this_ar=[ar_vals["noaa_spot_gn"][ar[0]]]
        time_vals=ar_vals["ar_date"][ar]
        time_diffs=[x-init_time for x in time_vals.values] #normalize to zero
        time_diffs=[x.total_seconds()/60./60/24. for x in time_diffs]
        EW_vals=ar_vals["EW"][ar]
        NS_vals=ar_vals["NS"][ar]
        fit, res, _, _, _=np.polyfit(time_diffs, EW_vals, 1, full=True)
        fit_fn=np.poly1d(fit)

#        plt.plot(time_diffs_all, EW_all, 'yo', time_diffs, fit_fn(time_diffs), '--k')
        #now shift
        #y=mx+b - > x=(y-b)/m where y = 270
        
        new_x=(270-fit[1])/fit[0]
        #y=mx+b -> b=y-mx
        new_int=-90-fit[0]*new_x
#        print(fit)
#        print("new x", new_x)
#        print("new int", new_int)
        new_fit=[fit[0], new_int]
#        print("new_fit", new_fit)
        new_fit_fn=np.poly1d(new_fit)
#        print(new_fit_fn)
#        plt.plot([-90, 90], new_fit_fn([-90, 90]), '--k')
#        plt.xlim(-25,0)
#        plt.ylim(-90, 90)
#        plt.show()  

        for index, val in enumerate(ar_fits):
#            print("val", val)
#            print("new_fit", new_fit)
            this_NS=np.mean(NS_vals)
            match_NS=np.mean(NSs[index])
            if val[1]>new_fit[1]-10 and val[1]<new_fit[1]+10 and this_NS<match_NS+10 and this_NS>match_NS-10:
                this_ar.append(ar_nums[index])
            
        if len(this_ar)>2:
            print("this_ar", this_ar)
            for ar in this_ar:
                index=ar_nums.index(ar)
                print("info for AR ", ar)                
#                print(times[index])
                print("EW: ", min(EWs[index]), max(EWs[index]))
#                print("this AR NS:", np.mean(NS_vals), max(NS_vals), min(NS_vals))
                print("NS: ", np.mean(NSs[index]), max(NSs[index]), min(NSs[index]))
                plt.plot(times[index], EWs[index], 'yo', times[index], new_fit_fn(times[index]), '--k')
                plt.show()
            print("Original AR: ", this_ar[0])
            second=input("which AR is a best match?")
            this_ar=[this_ar[0], int(second)]
            print("okay, replacing with ", this_ar)
            #TODO calculate the error based on each AR match    
#                print("want to match:", new_fit)
#                print("this one?", val)
#                pauseit=input("Enter if not a match, 'y' to match, 'q' to break, 'qqq' to stop program")
#                if pauseit=='y':
#                    this_ar.append(ar_nums[index])
#                if pauseit=='q': 
#                    break
#                if pauseit=='qqq':
#                    sys.exit(0)
        ar_matches.append(this_ar)
    print("matches", ar_matches)
#        filehandler=open("data/matched_ars.p", "wb")
#        pickle.dump(ar_matches, filehandler)   
    filehandler=open("data/matched_ars_alldone.p", "wb")
    pickle.dump(ar_matches, filehandler)    
    return ar_matches        
        
def dist_vs_time_auto(ar_indexes, ar_vals):
    count_bad=0
    count_good=0
    good_ars=[]
    for ar in ar_indexes:   
        NS_vals=ar_vals["NS"][ar]
        time_vals=ar_vals["ar_date"][ar]
        print(time_vals)
        init_time=time_vals.values[0]
        time_diffs=[x-init_time for x in time_vals.values] #normalize to zero
        time_diffs=[x.total_seconds()/60./60/24. for x in time_diffs]
        mean_time=np.mean(time_diffs)
        
        mean_NS=np.mean(NS_vals)
        ar_temp=list(ar)
        print("mean NS", mean_NS)
        for index in ar:
#            print(time_diffs)
#            print(NS_vals)
#            print("index", index, "NS", ar_vals["NS"][index])#, time_diffs[index])
            time_diff=(ar_vals["ar_date"][index] - init_time)
            time_diff=time_diff.total_seconds()/60./60./24.
            if abs(ar_vals["NS"][index]-mean_NS)>8:
                ar_temp.remove(index)
                print("removing", index)
            elif abs(time_diff-mean_time)>15: 
                ar_temp.remove(index)
                print("removing date that doesn't match", index)
        ar=list(ar_temp)
        if len(ar)>10:
            EW_vals=ar_vals["EW"][ar]
            NS_vals=ar_vals["NS"][ar]
            time_vals=ar_vals["ar_date"][ar]
#            print(time_vals)
#            print(ar_vals["loc"][ar])
#            print(ar_vals["noaa_spot_gn"][ar])
    #        print(type(time_vals))
            init_time=time_vals.values[0]
            time_diffs=[x-init_time for x in time_vals.values] #normalize to zero
            time_diffs=[x.total_seconds()/60./60./24. for x in time_diffs]
            fit, res, _, _, _=np.polyfit(time_diffs, EW_vals, 1, full=True)
#            print(fit)
#            slopes.append(fit[0])
            fit_fn=np.poly1d(fit)
#            print(fit_fn)
#            print(math.sqrt(res)/len(ar))
        #    NS_sep=max(NS_vals)-min(NS_vals)
      
            
            #now check for and remove outliers

            exp_ew=[fit[0]*x+fit[1] for x in time_diffs]
 #           print(exp_ew)
            diff_ew=abs(EW_vals-exp_ew)
 #           print("diff", diff_ew)
            plt.plot(time_diffs, EW_vals, 'yo', time_diffs, fit_fn(time_diffs), '--k')
            plt.show()  
            
            ar_temp=list(ar)   
            val, idx = max((val, idx) for (idx, val) in enumerate(diff_ew))
 #           print(val, idx)
 #           pauseit=input("press enter")
 #           if pauseit=="q": break
            num_removed=0
            while val>5 and num_removed<(len(ar_temp)/3):
                num_removed+=1

#                if pauseit=="q": break
                del ar[idx]
                print("removed", val, idx)
                EW_vals=ar_vals["EW"][ar]
                time_vals=ar_vals["ar_date"][ar]
                init_time=time_vals.values[0]
                time_diffs=[x-init_time for x in time_vals.values] #normalize to zero
                time_diffs=[x.total_seconds()/60./60/24. for x in time_diffs]
                fit, res, _, _, _=np.polyfit(time_diffs, EW_vals, 1, full=True)
                exp_ew=[fit[0]*x+fit[1] for x in time_diffs]
                diff_ew=abs(EW_vals-exp_ew)
#                print(diff_ew)
                fit_fn=np.poly1d(fit)
                val, idx = max((val, idx) for (idx, val) in enumerate(diff_ew))
                plt.plot(time_diffs, EW_vals, 'yo', time_diffs, fit_fn(time_diffs), '--k')
                plt.show() 

            if num_removed<(len(ar_temp)/3) and len(ar)>5:
                good_ars.append(ar)
                count_good+=1
            else: count_bad+=1
    print("good / all", count_good/(count_good+count_bad))
    filehandler=open("data/good_ars_alldone.p", "wb")
    pickle.dump(good_ars, filehandler)
#                print("largest remaining error", val)
#                pauseit=input("press enter")
            
#            for index, ew in enumerate(EW_vals):
#                exp_ew=fit[0]*time_diffs[index]+fit[1]
#                diff_ew=ew-exp_ew
#                print("diff:", time_diffs[index], ew, diff_ew)
#                pauseit=input("press enter to continue")
            
            
            
def dist_vs_time(ar_indexes, ar_vals):

    count_bad=0
    count_good=0
    good_ars=[]
    for ar in ar_indexes:
        print(ar)


        NS_vals=ar_vals["NS"][ar]
        time_vals=ar_vals["ar_date"][ar]
        print(time_vals)
        init_time=time_vals.values[0]
        time_diffs=[x-init_time for x in time_vals.values] #normalize to zero
        time_diffs=[x.total_seconds()/60./60/24. for x in time_diffs]
        mean_time=np.mean(time_diffs)
        
        mean_NS=np.mean(NS_vals)
        ar_temp=list(ar)
        print("mean NS", mean_NS)
        for index in ar:
#            print(time_diffs)
#            print(NS_vals)
#            print("index", index, "NS", ar_vals["NS"][index])#, time_diffs[index])
            time_diff=(ar_vals["ar_date"][index] - init_time)
            time_diff=time_diff.total_seconds()/60./60.
            if abs(ar_vals["NS"][index]-mean_NS)>8:
                ar_temp.remove(index)
                print("removing", index)
            elif abs(time_diff-mean_time)>360:  #360 = 15 days
                ar_temp.remove(index)
                print("removing date that doesn't match", index)
        ar=list(ar_temp)
        if len(ar)>=5:
            EW_vals=ar_vals["EW"][ar]
            NS_vals=ar_vals["NS"][ar]
            time_vals=ar_vals["ar_date"][ar]
            print(time_vals)
            print(ar_vals["loc"][ar])
#            print(ar_vals["noaa_spot_gn"][ar])
    #        print(type(time_vals))
            init_time=time_vals.values[0]
            time_diffs=[x-init_time for x in time_vals.values] #normalize to zero
            time_diffs=[x.total_seconds()/60./60 for x in time_diffs]
            fit, res, _, _, _=np.polyfit(time_diffs, EW_vals, 1, full=True)
            print(fit)
#            slopes.append(fit[0])
            fit_fn=np.poly1d(fit)
            print(fit_fn)
            print(math.sqrt(res)/len(ar))
            NS_sep=max(NS_vals)-min(NS_vals)
            print("NS separation", NS_sep)
            plt.plot(time_diffs, EW_vals, 'yo', time_diffs, fit_fn(time_diffs), '--k')
            plt.show()
            if (math.sqrt(res)/len(ar)) > 1 or fit[0]<0.4 or fit[0]>0.7 or NS_sep>10: 
                pauseit=input("good enough (g), take out a couple point (t) or bad (b) (q) to break")                
                if pauseit=="q": break
                elif pauseit=="g": 
                    good_ars.append(ar)
                    count_good+=1
                elif pauseit=="b":
                    count_bad+=1
                elif pauseit=="t":
                    removeit=input("which points?")
                    done=False
                    
                    while done == False:
                        new_ar=list(ar)
                        badpoints=[]
                        if len(removeit)>0:
                            for val in removeit.split(" "):
                                try:
                                    badpoints.append(int(val))
                                except:
                                    print("that's not a number!")
                        for index in sorted(badpoints, reverse=True):
                            try:
                                new_ar.remove(index)
                            except:
                                print(index, "wasn't in the list")
                        EW_vals=ar_vals["EW"][new_ar]
                        NS_vals=ar_vals["NS"][new_ar]
                        time_vals=ar_vals["ar_date"][new_ar]
                        init_time=time_vals.values[0]
                        time_diffs=[x-init_time for x in time_vals.values] #normalize to zero
                        time_diffs=[x.total_seconds()/60./60 for x in time_diffs]                       
                        fit, res, _, _, _=np.polyfit(time_diffs, EW_vals, 1, full=True)

                        fit_fn=np.poly1d(fit)
                        print(fit_fn)
                        print(math.sqrt(res)/len(ar))
                        print("NS separation", max(NS_vals)-min(NS_vals))
                        plt.plot(time_diffs, EW_vals, 'yo', time_diffs, fit_fn(time_diffs), '--k')
                        plt.show()
                        goodnow=input("good now (g), try again (t), bad (b)")
                        if goodnow=="g": 
                            count_good+=1
                            good_ars.append(new_ar)
                            done=True
                        if goodnow=="b":
                            count_bad+=1
                            done=True
                        if goodnow=='t':
                            removeit=input("which points?")
            else:
                good_ars.append(ar)
                count_good+=1
                filehandler=open("data/good_ars.p", "wb")
                pickle.dump(good_ars, filehandler)
                print("good/all", count_good/(count_good+count_bad))
    print("bad", count_bad)
    print("good", count_good)
    filehandler=open("data/good_ars_alldone.p", "wb")
    pickle.dump(good_ars, filehandler)
    
#    plt.hist(slopes, bins=[.4, 0.425, 0.45, 0.475, .5, 0.525, 0.55, 0.575, .6, 0.625, 0.65, 0.675, .7])
#    plt.show()
    
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
