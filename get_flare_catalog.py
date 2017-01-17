import os
from datetime import datetime
import pickle
from urllib.request import urlopen
import pandas as pd
import numpy as np
import math

def create_datetime(ymd, hm):
    date=[]
    #unpack ymd and fix year

    for item, ihm in zip(ymd, hm):
#        print("len(date): ", len(date))
        if item=="  ":
            print("blank line")
            date.append(None)
            continue
        
        datestr=item.split()
        print(datestr)
        
        year=int(datestr[0])
        month=int(datestr[1])
        day=int(datestr[2])

        #fix two year dates without messing up 4 year dates
        if year<70: 
            year=year+2000
        elif  year<100: 
            year+=1900
        
        if math.isnan(ihm)==False:
            hour=math.floor(ihm/100)
            minute=math.floor(ihm-hour*100)

            #now check to see if the time is past 2400 and adjust
            if hour>=24:
                hour-=24
                day+=1
                [day, month, year]=check_daymonth(day, month, year)
            #print(day, month, year, hour, minute)
            try:
                date.append(datetime(year, month, day, hour, minute))
                #print(datetime(year, month, day, hour, minute))
            except:
                date.append(np.nan)
        else:
            date.append(np.nan)
    return date

def check_daymonth(day, month, year):
    if (day==32 or (day==31 and (month==9 or month==4 or
    month==6 or month==11)) or (day==30 and month==2) or
    (month==2 and day==29 and year % 4 ==0)):
#        print("month was: ", month)
#        print("day was: ", day)
        day=1
        month=month+1
#        print("month is: ", month)
#        print("day is: ", day)
    if month==13:
        year=year+1
        month=1
    return [day, month, year]
        
                
def download_flare_catalog():
    """ program to read in GOES h-alpha and x-ray flare information from web"""
    """ usage: [ha, xray]=get_flare_catalog; ha is a pandas dataframe"""
    """ ha['location'][300] prints the 300th location"""

    count=0
    for getyear in range(2000, 2015):  
        print("year: ", getyear)
        web_stem="http://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-features/solar-flares/x-rays/goes/xrs/"
        xray_webpage=web_stem+"goes-xrs-report_"+str(getyear)+".txt"
        web_stem="https://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-features/solar-flares/h-alpha/reports/kanzelhohe/halpha-flare-reports_kanz_"
        ha_webpage=web_stem+str(getyear)+".txt"
        print(xray_webpage)
        print(ha_webpage)
               
        names=["data code", "station code", "year", "month", "day", "init_ind", "init_time", "final_ind", "final_time", "peak_ind", 
               "peak_time", "location", "optical", "something", "xray_class", "xray_size", "station", "blank", "NOAA_AR", "etc"]
    
        widths=[2, 3, 2, 2, 2, 2, 4, 1, 4, 1, 4, 7, 3, 22, 1, 3, 8, 8, 6, 24]
        xray_df_year=pd.read_fwf(xray_webpage, widths=widths, header=None, names=names)#, parse_dates=[[2, 3, 4]])
        xray_df_year["year_month_day"]=[str(x)+" "+str(y)+" "+str(z) for x,y,z in zip(xray_df_year["year"], xray_df_year["month"], xray_df_year["day"])]
    #    print(temp[0:10])
    #    xray_df["year_month_day"]=[x+"-"+y+"-"+z for x,y,z in zip(xray_df[2], xray_df[3], xray_df[4])]
    
        #translates dates to datetime
    #    print(type(xray_df["year_month_day"]))
    #    print(xray_df["year_month_day"][0:10])
        xray_df_year["init_date"]=create_datetime(xray_df_year["year_month_day"], xray_df_year["init_time"])
        xray_df_year["peak_date"]=create_datetime(xray_df_year["year_month_day"], xray_df_year["peak_time"])
        xray_df_year["final_date"]=create_datetime(xray_df_year["year_month_day"], xray_df_year["final_time"])
    
        xray_df_year=xray_df_year[["init_date", "peak_date", "final_date", "location", "xray_class", "xray_size", "NOAA_AR"]]
           
          
        names=["data code", "station code", "year", "month", "day", "init_ind", "init_time", "final_ind", "final_time", "peak_ind", 
               "peak_time", "location", "data source", "something", "xray_class", "xray_size", "station", "optical", "int_flux", 
               "NOAA_AR", "CMP", "area", "intensity"]
        widths=[2, 3, 4, 2, 2, 2, 4, 1, 4, 1, 4, 7, 3, 22, 1, 3, 8, 8, 6, 5, 8, 8, 8]
        ha_df_year=pd.read_fwf(ha_webpage, widths=widths, header=None, names=names)#, parse_dates=[[2, 3, 4]])
    
        ha_df_year["year_month_day"]=[str(x)+" "+str(y)+" "+str(z) for x,y,z in zip(ha_df_year["year"], ha_df_year["month"], ha_df_year["day"])]
    
        #translates dates to datetime    
    
        ha_df_year["init_date"]=create_datetime(ha_df_year["year_month_day"], ha_df_year["init_time"])
        ha_df_year["peak_date"]=create_datetime(ha_df_year["year_month_day"], ha_df_year["peak_time"])
        ha_df_year["final_date"]=create_datetime(ha_df_year["year_month_day"], ha_df_year["final_time"])
    
        ha_df_year=ha_df_year[["init_date", "peak_date", "final_date", "location", "xray_class", "xray_size", "NOAA_AR"]]


        if count==0:
            ha_df=ha_df_year
            xray_df=xray_df_year
            count=1
        else:
            dfs=[ha_df, ha_df_year]
            ha_df=pd.concat(dfs)
            dfs=[xray_df, xray_df_year]
            xray_df=pd.concat(dfs)

    return (xray_df, ha_df)
    #xray_pd=pd.DataFrame(data, widths=widths, header=None, columns=names, parse_dates=[[2, 3, 4]])


#    for line in data:
#        print(line.decode('utf-8'))
    #print(xray_pd.head())



    #Fill in X-ray values
    #prepare lists for variables
    group_num=[]
    station_num=[]
    initial_time=[]
    final_time=[]
    peak_time=[]
    initial_indicator=[]
    final_indicator=[]
    peak_indicator=[]
    location=[]
    optical_importance=[]
    optical_brightness=[]
    xray_class=[]
    xray_size=[]
    NOAA_AR=[]


#    for getyear in range(1981, 2016):
    for getyear in range(2013, 2016):
 
        print(getyear)
        webpage=web_stem+"goes-xrs-report_"+str(getyear)+".txt"
        print(webpage)
        line="nothing read yet"
#        try: 
        data=urlopen(webpage)
#        data=data.decode('utf-8')
#        print(data)
    #        data=data.split("\n")
        init_missing=0
        final_missing=0
        peak_missing=0
        for line in data:
            line=line.decode('utf-8')  

            group_num.append(line[0:2])
            station_num.append(line[2:4])
            try:
                year=int(line[5:7])
            except:
                break
            if year < 70:
                year=year+2000
            else:
                year=year+1900
            peak_year=initial_year=final_year=year
            peak_month=initial_month=final_month=month=int(line[7:9])
            peak_day=initial_day=final_day=day=int(line[9:11])
    
            peak_year=create_datetime(ha_df["year_month_day"], line[13:17])
            initial_indicator.append(line[17])
            final_indicator.append(line[22])
            peak_indicator.append(line[27])
            location.append(line[28:34])
            optical_importance.append(line[34:35])
            optical_brightness.append(line[35:36])
            xray_class.append(line[59:60])
            xray_size.append(line[61:63])
            NOAA_AR.append(line[81:85])
            
            try:
                initial_hr=int(line[13:15])
                initial_min=int(line[15:17])
            except ValueError:
                init_missing+=1
    #            print("No initial time for event on date year:%d, month: %d, day: %d" %(year, month, day))
    
            try:
                final_hr=int(line[18:20])
                final_min=int(line[20:22])
            except ValueError:
                final_missing+=1
    #            print("No final time for event on date year:%d, month: %d, day: %d" %(year, month, day))
    
            try:
                peak_hr=int(line[23:25])
                peak_min=int(line[25:27])
            except ValueError:
                peak_missing+=1
    #            print("No peak time for event on date year:%d, month: %d, day: %d" %(year, month, day))
    
            try:
                if initial_hr==99:
                    initial_time.append(None)
                else:
                    if initial_hr>=24:
                        initial_hr=initial_hr-24
                        initial_day=initial_day+1
                    [initial_day, initial_month, initial_year]=check_daymonth(initial_day, initial_month, peak_year)
                    initial_time.append(datetime(initial_year, initial_month, initial_day, initial_hr, initial_min))
            except ValueError:
                print(line)
                print("Initial date is not valid: year: %d, month:%d, day:%d, hour:%d, min:%d" % (year, month, initial_day, initial_hr, initial_min))
                initial_time.append(None)
            except NameError:
                initial_time.append(None)
    
            try:
                if final_hr==99:
                    final_time.append(None)
                else:
                    final_day=day
                    if final_hr>=24:
                        final_hr=final_hr-24
                        final_day=final_day+1
                    [final_day, final_month, final_year]=check_daymonth(final_day, final_month, final_year)
                    final_time.append(datetime(final_year, final_month, final_day, final_hr, final_min))
            except ValueError:
                print(line)
                print("Final date is not valid: year: %d, month:%d, day:%d, hour:%d, min:%d" % (year, month, final_day, final_hr, final_min))
                final_time.append(None)
            except NameError:
                final_time.append(None)
    
            try:
                if peak_hr==99:
                    peak_time.append(None)
                else:
                    peak_day=day
                    if peak_hr>=24:
                        peak_hr=peak_hr-24
                        peak_day=peak_day+1
                    [peak_day, peak_month, peak_year]=check_daymonth(peak_day, peak_month, peak_year)
                    peak_time.append(datetime(peak_year, peak_month, peak_day, peak_hr, peak_min))
            except ValueError:
                print(line)
                print("Peak date is not valid: year: %d, month:%d, day:%d, hour:%d, min:%d" % (year, month, peak_day, peak_hr, peak_min))
                peak_time.append(None)
            except NameError:
                peak_time.append(None)
        
    xray_flares={'group_num':group_num, 'station_num':station_num,
               'initial_time':initial_time, 'final_time':final_time,
               'peak_time':peak_time, 'location':location,
               'optical_importance':optical_importance, 'optical_brightness':optical_brightness,
               'xray_class':xray_class, 'xray_size':xray_size, "NOAA_AR":NOAA_AR}

#    filehandler=open('data/haflare_vals.p', 'wb')
#    pickle.dump(ha_flares, filehandler)
    data_dir="/Users/alyshareinard/Documents/python/common/data"

    filehandler=open(data_dir+'/xflare_vals.p', 'wb')
    pickle.dump(xray_flares, filehandler)
    ha_flares={"not yet implemented":"try get_flare_catalog_fromfile()"}
    return (ha_flares, xray_flares)

        
def get_flare_catalog_fromfile():
    """ program to read in GOES h-alpha and x-ray flare information from file"""
    """ usage: [ha, xray]=get_flare_catalog; ha is a dict"""
    """ ha['location'][300] prints the 300th location"""
    """ keys are ha.keys() -- station_num, group_num, initial_time, final_time"""
    """ peak_time, optical_importance, optical_brightness, xray_class, """
    """ xray_size, NOAA_AR """
    #define data file location
    data_dir=os.getcwd()+"/data"
#    data_dir="/Users/alyshareinard/Documents/python/common/data"
    ha_file=data_dir+"/ha.txt"
    xray_file=data_dir+"/xray.txt"

    #code eto read in halpha data
    names=["data code", "station code", "year", "month", "day", "init_ind", "init_time", "final_ind", "final_time", "peak_ind", 
           "peak_time", "location", "data source", "something", "xray_class", "xray_size", "station", "optical", "int_flux", 
           "NOAA_AR", "CMP", "area", "intensity"]

    widths=[2, 3, 2, 2, 2, 2, 4, 1, 4, 1, 4, 7, 3, 22, 1, 3, 8, 8, 6, 5, 8, 8, 8]

    ha_df=pd.read_fwf(ha_file, widths=widths, header=None, names=names, parse_dates=[[2, 3, 4]])
    #translates dates to datetime   
    ha_df["init_date"]=create_datetime(ha_df["year_month_day"], ha_df["init_time"])
    ha_df["peak_date"]=create_datetime(ha_df["year_month_day"], ha_df["peak_time"])
    ha_df["final_date"]=create_datetime(ha_df["year_month_day"], ha_df["final_time"])

    ha_df=ha_df[["init_date", "peak_date", "final_date", "location", "xray_class", "xray_size", "NOAA_AR"]]


    #code to read in xray data
    names=["data code", "station code", "year", "month", "day", "init_ind", "init_time", "final_ind", "final_time", "peak_ind", 
           "peak_time", "location", "optical", "something", "xray_class", "xray_size", "station", "blank", "NOAA_AR", "etc"]

    widths=[2, 3, 2, 2, 2, 2, 4, 1, 4, 1, 4, 7, 3, 22, 1, 3, 8, 8, 6, 24]

    xray_df=pd.read_fwf(xray_file, widths=widths, header=None, names=names, parse_dates=[[2, 3, 4]])
    #translates dates to datetime
    xray_df["init_date"]=create_datetime(xray_df["year_month_day"], xray_df["init_time"])
    xray_df["peak_date"]=create_datetime(xray_df["year_month_day"], xray_df["peak_time"])
    xray_df["final_date"]=create_datetime(xray_df["year_month_day"], xray_df["final_time"])

    xray_df=xray_df[["init_date", "peak_date", "final_date", "location", "xray_class", "xray_size", "NOAA_AR"]]
       

    return (xray_df, ha_df)

def get_flare_catalog():

    try:
        print("downloading")
        (xray, halpha)=download_flare_catalog()
    except:
        print("getting from file")
        (xray, halpha)=get_flare_catalog_fromfile()
    return (xray, halpha)
                            
get_flare_catalog()
