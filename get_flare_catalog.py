import os
from datetime import datetime

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
        

                
def get_flare_catalog():
    """ program to read in GOES h-alpha and x-ray flare information"""
    """ usage: [ha, xray]=get_flare_catalog; ha is a dict"""
    """ ha['location'][300] prints the 300th location"""
    """ keys are ha.keys() -- station_num, group_num, initial_time, final_time"""
    """ peak_time, optical_importance, optical_brightness, xray_class, """
    """ xray_size, NOAA_AR """

    #define data file location
    data_dir=os.getcwd()+"/data"
    data_dir="/Users/alyshareinard/Documents/python/common/data"
    ha_file=data_dir+"/ha.txt"
    xray_file=data_dir+"/xray.txt"

    #Fill in H-alpha values
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

    with open(ha_file, "r") as f:
        ha_all_data=f.readlines()

    init_missing=0
    final_missing=0
    peak_missing=0
    for line in ha_all_data:
        group_num.append(line[0:2])
        station_num.append(line[2:4])
        year=int(line[5:7])
        if year < 90:
            year=year+2000
        else:
            year=year+1900
        peak_year=initial_year=final_year=year
        peak_month=initial_month=final_month=month=int(line[7:9])
        peak_day=initial_day=final_day=day=int(line[9:11])

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
        
    ha_flares={'group_num':group_num, 'station_num':station_num,
               'initial_time':initial_time, 'final_time':final_time,
               'peak_time':peak_time, 'location':location,
               'optical_importance':optical_importance, 'optical_brightness':optical_brightness,
               'xray_class':xray_class, 'xray_size':xray_size, "NOAA_AR":NOAA_AR}






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

    with open(xray_file, "r") as f:
        xray_all_data=f.readlines()

    init_missing=0
    final_missing=0
    peak_missing=0
    for line in xray_all_data:
#        print("line", line)
        group_num.append(line[0:2])
        station_num.append(line[2:4])
        year=int(line[5:7])
        if year < 90:
            year=year+2000
        else:
            year=year+1900
        peak_year=initial_year=final_year=year
        peak_month=initial_month=final_month=month=int(line[7:9])
        peak_day=initial_day=final_day=day=int(line[9:11])

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

    return [ha_flares, xray_flares]
                            
get_flare_catalog()
