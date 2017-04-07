import os
from datetime import datetime

def get_yashiro_catalog():
    """ program to read in yashiro CME catalog """

    data_dir=os.getcwd()+"/data"
    cme_file=data_dir+"/yashiro_all.txt"

    #prepare lists for CME values
    CME_date=[]
    CME_PA=[]
    CME_width=[]
    CME_lin_speed=[]
    CME_2Ospeed_init=[]
    CME_2Ospeed_final=[]
    CME_2Ospeed_20R=[]
    CME_accel=[]
    CME_mass=[]
    CME_ke=[]
    CME_mpa=[]
    CME_remarks=[]

    names=["ymd", "hour", "sep", "minute", "sep2", "sec", "PA", "width",
           "lin_speed", "20speed_init", "20speed_final", "20speed_20R", 
           "accel", "sep3", "mass", "sep4", "ke", "sep5", "mpa"]
    
    widths=[10, 4, 1, 2, 1, 2, 8, 8, 8, 8, 8, 6, 6, 1, 10, 1, 10, 1, 8]
    cmes=pd.read_fwf(cme_file, widths=widths, header=3, names=names)#, parse_dates=[[1]])
    date=[]
    for i in range(len(cmes["ymd"])):
        ymd=cmes["ymd"][i].split("/")

        date.append(datetime(int(ymd[0]), int(ymd[1]), int(ymd[2]), cmes["hour"][i], cmes["minute"][i]))#, cmes["sec"][i]))
    
    cmes["date"]=date
    return cmes

