import os
from datetime import datetime

def get_flare_catalog():
    """program to read in GOES h-alpha and x-ray flare information"""

    #define data file location
    data_dir=os.getcwd()+"\data"
    ha_file=data_dir+"\ha.txt"

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
    xray_class=[]
    xray_size=[]
    NOAA_AR=[]

    with open(ha_file, "r") as f:
        ha_all_data=f.readlines()

    init_missing=0
    final_missing=0
    peak_missing=0
    for line in ha_all_data:
        print(line)
        group_num.append(line[0:2])
        station_num.append(line[2:5])
        year=int(line[5:7])
        if year < 90:
            year=year+2000
        else:
            year=year+1900
        month=int(line[7:9])
        day=int(line[9:11])
        try:
            initial_hr=int(line[12:15])
            initial_min=int(line[15:17])
        except ValueError:
            init_missing+=1
#            print("No initial time for event on date year:%d, month: %d, day: %d" %(year, month, day))

        try:
            final_hr=int(line[17:20])
            final_min=int(line[20:23])
        except ValueError:
            final_missing+=1
#            print("No final time for event on date year:%d, month: %d, day: %d" %(year, month, day))

        try:
            peak_hr=int(line[22:25])
            peak_min=int(line[25:27])
        except ValueError:
            peak_missing+=1
#            print("No peak time for event on date year:%d, month: %d, day: %d" %(year, month, day))

        try:
            initial_time.append(datetime(year, month, day, initial_hr, initial_min))
        except ValueError:
            print("Initial date is not valid: year: %d, month:%d, day:%d, hour:%d, min:%d" % (year, month, day, initial_hr, initial_min))
            initial_time.append(None)
        except NameError:
            initial_time.append(None)

        try:
            final_time.append(datetime(year, month, day, final_hr, final_min))
        except ValueError:
            print("Final date is not valid: year: %d, month:%d, day:%d, hour:%d, min:%d" % (year, month, day, final_hr, final_min))
            final_time.append(None)
        except NameError:
            final_time.append(None)

        try:
            peak_time.append(datetime(year, month, day, peak_hr, peak_min))
        except ValueError:
            print("Peak date is not valid: year: %d, month:%d, day:%d, hour:%d, min:%d" % (year, month, day, peak_hr, peak_min))
            peak_time.append(None)
        except NameError:
            peak_time.append(None)

    print(len(group_num))
    print(len(initial_time))
    print(len(final_time))
    print(len(peak_time))
                            
                            
get_flare_catalog()
