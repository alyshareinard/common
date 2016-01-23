import os
from datetime import datetime

def get_yashiro_catalog():
    """ program to read in yashiro CME catalog """

    data_dir=os.getcwd()+"\data"
    cme_file=data_dir+"\yashiro_all.txt"

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

    with open(cme_file, "r") as cme_all_data:
#        cme_all_data=f.readlines()
        next(cme_all_data)
        next(cme_all_data)
        next(cme_all_data)
        next(cme_all_data)
        
        for line in cme_all_data:
            
#            print(line)
            year=int(line[0:4])
            month=int(line[5:7])
            day=int(line[8:10])
            hour=int(line[12:14])
            minute=int(line[15:17])
            sec=int(line[18:20])
            CME_date.append(datetime(year, month, day, hour, minute, sec))
            CME_PA.append(line[24:27])
            CME_width.append(line[32:35])
            CME_lin_speed.append(line[37:42])
            CME_2Ospeed_init.append(line[45:49])
            CME_2Ospeed_final.append(line[52:56])
            CME_2Ospeed_20R.append(line[59:63])
            CME_accel.append(line[69:73])
            CME_mass.append(line[76:83])
            CME_ke.append(line[86:95])
            CME_mpa.append(line[98:102])
            CME_remarks.append(line[104:])
                
##            print("lin", CME_lin_speed[-1])
##            print("2O", CME_2Ospeed_init[-1])
##            print("final", CME_2Ospeed_final[-1])
##            print("20R", CME_2Ospeed_20R[-1])
##            print("accel", CME_accel[-1])
##            print("mass", CME_mass[-1])
##            print("ke", CME_ke[-1])
##            print("mpa", CME_mpa[-1])
##            print("remarks", CME_remarks[-1])

        yashiro_cmes={'date':CME_date, "PA":CME_PA, "width":CME_width,
                      "lin_speed":CME_lin_speed, "2Ospeed_init":CME_2Ospeed_init,
                      "2Ospeed_final":CME_2Ospeed_final, "2Ospeed_20R":CME_2Ospeed_20R,
                      "accel":CME_accel, "mass":CME_mass, "ke":CME_ke, "mpa":CME_mpa,
                      "remarks":CME_remarks}
        return yashiro_cmes
#get_yashiro_catalog()
