# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 12:44:35 2016

@author: alysha.reinard
"""

from urllib.request import urlopen
from datetime import datetime
#import numpy as np
import pickle
from pandas import DataFrame

def read_ars():
    web_stem="http://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-features/sunspot-regions/usaf_mwl/"
    data_code=[] #data code: always 11 for sunspot data
    year=[]
    month=[]
    day=[]
    time=[] #UT time
    loc=[]
    mag_class=[]    #Mt Wilson magnetic classification
    max_mag=[]      #max magnetic field strength in group from MWIL
    mw_spot_gn=[]   #Mount wilson spot group number
    noaa_spot_gn=[] #NOAA/USAF sunspot group number after Aug 1982
    zurich=[]       #Zurich class of AR
    penumbra=[]     #penumbra class of AR
    compactness=[]  #compactness class of AR
    num_spots=[]    #number of spots
    long_extent=[]  #longitudinal extent in degrees
    area=[]         #Area in millions of solar hemisphere
    CM_pass_year=[] #Individual Central Meridian Passage year
    CM_pass_month=[] # " month
    CM_pass_day=[]  # " day
    RCM_pass_year=[] #Regional Central meridian passage year
    RCM_pass_month=[] # " month
    RCM_pass_day=[]  # " day
    stat_ser_num=[]  #station serial number
    qual=[]         #qual
    station=[]      #4 letter station abbreviation
    
    for getyear in range(1981, 2016):
        print(getyear)
        webpage=web_stem+"usaf_solar-region-reports_"+str(getyear)+".txt"
        line="nothing read yet"
#        try: 
        data=urlopen(webpage)
#        data=data.decode('utf-8')
#        print(data)
    #        data=data.split("\n")

        for line in data:
            line=line.decode('utf-8')
#            print(type(line))
#            print(line)
            data_code.append(line[0:2])
            year.append(str(line[2:4]))
            month.append(str(line[4:6]))
            day.append(str(line[6:8]))
            time.append(str(line[9:13]))
            loc.append(line[14:20])
            mag_class.append(line[20:24])
            max_mag.append(line[25:26])
            try:
                mw_spot_gn.append(int(line[27:32]))
            except:
                mw_spot_gn.append(None)
            try:
                noaa_spot_gn.append(int(line[33:38]))
            except:
                noaa_spot_gn.append(None)
            zurich.append(line[39:40])
            penumbra.append(line[40:41])
            compactness.append(line[41:42])
            try:
                num_spots.append(int(line[43:45]))
            except:
                num_spots.append(None)
            
            try:
                long_extent.append(int(line[46:48]))
            except:
                long_extent.append(None)
                
            try:
                area.append(int(line[48:52]))
            except:
                area.append(None)
            CM_pass_year.append(line[53:55])
            CM_pass_month.append(line[55:57])
            CM_pass_day.append(line[57:61])
            RCM_pass_year.append(line[62:64])
            RCM_pass_month.append(line[64:66])
            RCM_pass_day.append(line[66:70])
            stat_ser_num.append(line[71:73])
            try:
                qual.append(int(line[75:76]))
            except:
                qual.append(None)
            station.append(line[76:80])
            
#        except:
#            e=sys.exc_info()[0]
#            print("Error:: %s" %e)
#           print("problem reading: ", line)
#    print(qual)
#    print([(y+" "+m+" "+d+" "+t) for y, m, d, t in zip(year, month, day, time)])
    ar_date=[]
    print("length is:", len(year))
    for i in range(len(year)):
#        print(time[i])
        try:
            if int(time[i])>2400:
                time[i]=str(int(time[i])-2400)
                day[i]=str(int(day[i])+1)
#            print(year[i], month[i], day[i], time[i])
            ar_date.append(datetime.strptime(year[i]+" "+month[i]+" "+day[i]+" "+time[i], "%y %m %d %H%M"))
        except:
            ar_date.append(None)

    
    AR_vals=DataFrame(data=[ar_date, loc, mag_class, max_mag, mw_spot_gn, noaa_spot_gn, 
                     num_spots, zurich, compactness, penumbra, long_extent, area, qual])
    print(AR_vals.shape)
    AR_vals=AR_vals.transpose()
    print(AR_vals.shape) 
    
    cols=['ar_date', 'loc', 'mag_class', 'max_mag', 'mw_spot_gn', 
                         'noaa_spot_gn', 'num_spots', 'zurich', 'compactness', 
                         'penumbra', 'long_extent', 'area', 'qual']
    AR_vals.columns=cols                     

#    print(AR_vals.dtype)
#    AR_vals.dtype.names=('ar_date', 'loc', 'mag_class', 'max_mag', 'mw_spot_gn', 
#                         'noaa_spot_gn', 'num_spots', 'zurich', 'compactness', 
#                         'penumbra', 'long_extent', 'area', 'qual')
    filehandler=open('../data/ar_vals.p', 'wb')
    pickle.dump(AR_vals, filehandler)

    
read_ars()
