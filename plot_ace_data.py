# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 14:32:04 2016

@author: alyshareinard
"""
import matplotlib.pyplot as plt
import pickle
from datetime import datetime
import matplotlib.gridspec as gridspec

def plot_ace_data():
    f=open('data/ACE_combined1hr_wdate.p', 'rb')
    combined1hr_wdates=pickle.load(f)
    
    start_date=datetime(2008, 12, 17, 3, 0)
    end_date=datetime(2008, 12, 17, 14, 0)
    
    ACE_data=combined1hr_wdates["data"]
    ACE_dates=combined1hr_wdates["datetime"]
    print(ACE_data.dtype.names)
#    print(ACE_data['proton_speed'])
#    print(ACE_dates)
#    plt.figure(figsize = (4,1))
    gs1 = gridspec.GridSpec(4, 1)
    gs1.update(wspace=0.025, hspace=0.05) # set the spacing between axes. 


    plt.subplot(5,1,1) 
    plt.plot(ACE_dates, ACE_data['proton_speed'], 'o-')
    plt.xlim(start_date, end_date)
    plt.ylim(0, 600)
    plt.xticks([])    
    
    plt.subplot(5,1,2)
    plt.plot(ACE_dates, ACE_data['Bt'], 'o-')
    plt.xlim(start_date, end_date)
    plt.ylim(0, 10)
    plt.xticks([]) 
    
    plt.subplot(5,1,3)
    plt.plot(ACE_dates, ACE_data['Bgse_x'], 'o-')
    plt.xlim(start_date, end_date)
    plt.ylim(-10, 10)  
    plt.xticks([]) 

    plt.subplot(5,1,4)
    plt.plot(ACE_dates, ACE_data['Bgse_x'], 'o-')
    plt.xlim(start_date, end_date)
    plt.ylim(-10, 10)  
    plt.xticks([]) 

    plt.subplot(5,1,5)
    plt.plot(ACE_dates, ACE_data['Bgse_z'], 'o-')
    plt.xlim(start_date, end_date)
    plt.ylim(-10, 10) 
    

    plt.show()
    
plot_ace_data()
    
    