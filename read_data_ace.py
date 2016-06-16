import numpy as np
import pickle
from datetime import datetime
from numpy.lib import recfunctions as rfn
def main():

    swics2hr_names=['year', 'day', 'hr', 'min', 'sec', 'fp_year', \
    'fp_doy', 'ACEepoch', 'nHe2', 'nHe2_err', 'vHe2', 'vthHe2', 'vHe2_err', \
    'vthHe2_err', 'qf_He', 'vC5', 'vthC5', 'vC5_err', 'vthC5_err', 'qf_C5',\
    'vO6', 'vthO6', 'vO6_err', 'vthO6_err', 'qf_O6', 'vFe10', 'vthFe10',\
    'vFe10_err', 'vthFe10_err', 'qf_Fe10', 'C6to4', 'C6to4_err', 'qf_C6to4',\
    'C6to5', 'C6to5_err', 'qf_C6to5', 'O7to6', 'O7to6_err', 'qf_O7to6', \
    'avqC', 'avqC_err', 'qf_avqC', 'avqO', 'avqO_err', 'qf_avqO', 'avqFe', \
    'avqFe_err', 'qf_avqFe', 'avqMg', 'avqMg_err', 'qf_avqMg', 'avqSi', \
    'avqSi_err', 'qf_avqSi', 'SW_type', 'FetoO', 'FetoO_err', 'qf_FetoO', \
    'HetoO', 'HetoO_err', 'qf_HetoO', 'CtoO', 'CtoO_err', 'qf_CtoO', \
    'NetoO', 'NetoO_err', 'qf_NetoO', 'MgtoO', 'MgtoO_err', 'qf_MgtoO', \
    'SitoO', 'SitoO_err', 'qf_SitoO']
    
    swics1hr_names=['year', 'day', 'hr', 'min', 'sec', 'fp_year', 'fp_doy', \
    'ACEepoch', 'nHe2', 'nHe2_err', 'vHe2', 'vthHe2', 'vHe2_err', 'vthHe2_err', \
    'qf_He', 'vC5', 'vthC5', 'vC5_err', 'vthC5_err', 'qf_C5', 'vO6', 'vthO6', \
    'vO6_err', 'vthO6_err', 'qf_O6', 'vFe10', 'vthFe10', 'vFe10_err', \
    'vthFe10_err', 'qf_Fe10', 'C6to4', 'C6to4_err', 'qf_C6to4', 'C6to5', \
    'C6to5_err', 'qf_C6to5', 'O7to6', 'O7to6_err', 'qf_O7to6', 'avqC', \
    'avqC_err', 'qf_avqC', 'avqO', 'avqO_err', 'qf_avqO', 'avqFe', \
    'avqFe_err', 'qf_avqFe', 'avqMg', 'avqMg_err', 'qf_avqMg', 'avqSi', \
    'avqSi_err', 'qf_avqSi', 'SW_type', 'FetoO', 'FetoO_err', 'qf_FetoO']
    
    swicsqdist_names=['year', 'day', 'hr', 'min', 'sec', 'fp_year', 'fp_doy', \
    'ACEepoch', 'qdistC1', 'qdistC2', 'qdistC3', 'qdistO1', 'qdistO2', \
    'qdistO3', 'qdistO4', 'qdistNe1', 'qdistNe2', 'qdistMg1', 'qdistMg2', \
    'qdistMg3', 'qdistMg4', 'qdistMg5', 'qdistMg6', 'qdistMg7', 'qdistSi1', \
    'qdistSi2',  'qdistSi3', 'qdistSi4', 'qdistSi5', 'qdistSi6', 'qdistSi7',
    'qdistFe1', 'qdistFe2', 'qdistFe3', 'qdistFe4', 'qdistFe5', 'qdistFe6', \
    'qdistFe7', 'qdistFe8', 'qdistFe9', 'qdistFe10', 'qdistFe11', 'qdistFe12', \
    'qdistFe13', 'qdistFe14', 'qdistFe15', 'qdistC_err1', 'qdistC_err2', \
    'qdistC_err3', 'qdistO_err1', 'qdistO_err2', 'qdistO_err3', 'qdistO_err4', \
    'qdistNe_err1', 'qdistNe_err2', 'qdistMg_err1', 'qdistMg_err2', 'qdistMg_err3', \
    'qdistMg_err4', 'qdistMg_err5', 'qdistMg_err6', 'qdistMg_err7', \
    'qdistSi_err1', 'qdistSi_err2', 'qdistSi_err3', 'qdistSi_err4', 'qdistSi_err5', \
    'qdistSi_err6', 'qdistSi_err7', 'qdistFe_err1', 'qdistFe_err2', 'qdistFe_err3', \
    'qdistFe_err4', 'qdistFe_err5', 'qdistFe_err6', 'qdistFe_err7', 'qdistFe_err8', \
    'qdistFe_err9', 'qdistFe_err10', 'qdistFe_err11', 'qdistFe_err12', 'qdistFe_err13', \
    'qdistFe_err14', 'qdistFe_err15', 'qf_qdistC1', 'qf_qdistC2', 'qf_qdistC3', \
    'qf_qdistO1', 'qf_qdistO2', 'qf_qdistO3', 'qf_qdistO4', 'qf_qdistNe1', \
    'qf_qdistNe2', 'qf_qdistMg1', 'qf_qdistMg2', 'qf_qdistMg3', 'qf_qdistMg4', \
    'qf_qdistMg5', 'qf_qdistMg6', 'qf_qdistMg7', 'qf_qdistSi1', 'qf_qdistSi2', \
    'qf_qdistSi3', 'qf_qdistSi4', 'qf_qdistSi5', 'qf_qdistSi6', 'qf_qdistSi7', \
    'qf_qdistFe1', 'qf_qdistFe2', 'qf_qdistFe3', 'qf_qdistFe4', 'qf_qdistFe5', \
    'qf_qdistFe6', 'qf_qdistFe7', 'qf_qdistFe8', 'qf_qdistFe9', 'qf_qdistFe10', \
    'qf_qdistFe11', 'qf_qdistFe12', 'qf_qdistFe13', 'qf_qdistFe14', 'qf_qdistFe15']
    
    magswepam_names=['year', 'day', 'hr', 'min', 'sec', 'fp_year', 'fp_doy', \
    'ACEepoch', 'Np', 'Tp', 'Alpha_ratio', 'Vp', 'V_rtn_r', 'V_rtn_t', \
    'V_rtn_n', 'V_gse_x', 'V_gse_y', 'V_gse_z', 'V_gsm_x', 'V_gsm_y', 'V_gsm_z', \
    'B_rtn_r', 'B_rtn_t', 'B_rtn_n', 'B_gse_x', 'B_gse_y', 'B_gse_z', 'B_gsm_x', \
    'B_gsm_y', 'B_gsm_z', 'Bmag', 'Lambda', 'Delta', 'dBrms', 'pos_gse_x', \
    'pos_gse_y', 'pos_gse_z', 'pos_gsm_x', 'pos_gsm_y', 'pos_gsm_z', 'pos_hs_x', \
    'pos_hs_y', 'pos_hs_z', 'MAG_pts']
    
    combined_names=['date', 'day', 'hr', 'min', 'sec', 'fp_year', 'fp_doy', \
    'ACEepoch', 'proton_density', 'proton_temp', 'He4toprotons', 'proton_speed', \
    'x_dot_RTN', 'y_dot_RTN', 'z_dot_RTN', 'x_dot_GSE', 'y_dot_GSE', 'z_dot_GSE', \
    'x_dot_GSM', 'y_dot_GSM', 'z_dot_GSM', 'SWEPAM_wt', 'nHe2', 'vHe2', 'vC5', \
    'vO6', 'vFe10', 'vthHe2', 'vthC5', 'vthO6', 'vthFe10', 'He_qual', 'C5_qual', \
    'O6_qual', 'Fe10_qual', 'C6to5', 'O7to6', 'avqC', 'avqO', 'avqFe', \
    'C6to5_qual', 'O7to6_qual', 'avqC_qual', 'avqO_qual', 'avqFe_qual', 'FetoO',\
    'FetoO_qual', 'Br', 'Bt', 'Bn', 'Bgse_x', 'Bgse_y', 'Bgse_z', 'Bgsm_x', \
    'Bgsm_y', 'Bgsm_z', 'Bmag', 'Lambda', 'Delta', 'dBrms', 'sigma_B', 'MAG_wt',\
    'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'unc_P1', 'unc_P2', 'unc_P3',\
    'unc_P4', 'unc_P5', 'unc_P6', 'unc_P7', 'unc_P8', 'DE1', 'DE2', 'DE3', 'DE4',\
    'unc_DE1', 'unc_DE2', 'unc_DE3', 'unc_DE4', 'W3', 'W4', 'W5', 'W6', 'W7', \
    'W8', 'unc_W3', 'unc_W4', 'unc_W5', 'unc_W6', 'unc_W7', 'unc_W8', 'E1p', \
    'E2p', 'E3p', 'E4p', 'FP5p', 'FP6p', 'FP7p', 'unc_E1p', 'unc_E2p', 'unc_E3p',\
    'unc_E4p', 'unc_FP5p', 'unc_FP6p', 'unc_FP7p', 'Z2', 'Z2A', 'Z3', 'Z4',\
    'unc_Z2', 'unc_Z2A', 'unc_Z3', 'unc_Z4', 'P1p', 'P2p', 'P3p', 'P4p', 'P5p',\
    'P6p', 'P7p', 'P8p', 'unc_P1p', 'unc_P2p', 'unc_P3p', 'unc_P4p', 'unc_P5p',\
    'unc_P6p', 'unc_P7p', 'unc_P8p', 'E1', 'E2', 'E3', 'E4', 'FP5', 'FP6', \
    'FP7', 'unc_E1', 'unc_E2', 'unc_E3', 'unc_E4', 'unc_FP5', 'unc_FP6', \
    'unc_FP7', 'EPAM_livetime', 'pos_gse_x', 'pos_gse_y', 'pos_gse_z', \
    'pos_gsm_x', 'pos_gsm_y', 'pos_gsm_z']

    data_file='C:\\Users\\alysha.reinard.SWPC\\Dropbox\\Work\\data\\ACE\\'
    data_file='/Users/alyshareinard/Dropbox/Work/data/ACE/'
    swics2hr=np.genfromtxt(data_file+'ACE_SWICS_Data_2hr_1998.txt', \
    skip_header=49, names=swics2hr_names)

    swics1hr=np.genfromtxt(data_file+'ACE_SWICS_Data_1hr_1998.txt', \
    skip_header=49, names=swics1hr_names)
    
    swicsqdist=np.genfromtxt(data_file+'ACE_SWICS_QdistData_1998.txt', \
    skip_header=51, names=swicsqdist_names)

    magswepam1min=np.genfromtxt(data_file+'ACE_MagSwepam_1998.txt', \
    skip_header=63, names=magswepam_names)

    combined1hr=np.genfromtxt(data_file+'ACE_combined1hr_1998.txt', \
    skip_header=116, names=combined_names)#, missing_values=9.9999e+03)

#
#    for each_year in range(1998,2012):
#        print("reading SWICS, year: ", each_year)
#        x=np.genfromtxt(data_file+'ACE_SWICS_Data_2hr_'+str(each_year)+'.txt', \
#        skip_header=49, names=swics2hr_names)
#        swics2hr=np.concatenate((swics2hr, x), axis=0)
#
#        
#        x=np.genfromtxt(data_file+'ACE_SWICS_Data_1hr_'+str(each_year)+'.txt', \
#        skip_header=49, names=swics1hr_names)
#        swics1hr=np.concatenate((swics1hr, x), axis=0)
#
#        x=np.genfromtxt(data_file+'ACE_SWICS_QdistData_'+str(each_year)+'.txt', \
#        skip_header=51, names=swicsqdist_names)
#        swicsqdist=np.concatenate((swicsqdist, x), axis=0)        
#
#    for each_year in range(1998, 2015):
#        print("reading MagSwepam, year: ", each_year)
#        x=np.genfromtxt(data_file+'ACE_MagSwepam_'+str(each_year)+'.txt', \
#        skip_header=63, names=magswepam_names)
#        magswepam1min=np.concatenate((magswepam1min, x), axis=0)   

    for each_year in range(1998, 2014): #2012 and 2013 are not formatted correctly
        print("reading combined, year: ", each_year)
        x=np.genfromtxt(data_file+'ACE_combined1hr_'+str(each_year)+'.txt', \
        skip_header=192, names=combined_names)
        combined1hr=np.concatenate((combined1hr, x), axis=0) 
        
    combined_date=[str(int(year))+"-"+str(int(doy))+"-"+str(int(hr))+"-"+str(int(minute)) for (year, doy, hr, minute) in \
    zip(combined1hr["date"], combined1hr["day"], combined1hr["hr"], \
    combined1hr["min"])]

#    print(combined_date)
    

 
    combined_datetime=[datetime.strptime(combined_date[i], "%Y-%j-%H-%M") \
       for i in range(len(combined_date))]
#    print(type(combined_datetime), type(combined_datetime[0]))
#    print(type(combined_date), type(combined_date[0]))
#    combined1hr_wdate=rfn.append_fields(combined1hr, names="datetime", data=combined_datetime, usemask=False)
    
           
    #TODO: insert datetime into combined1hr
 
#    filehandler=open('swics2hr.p', 'wb')
#    pickle.dump(swics2hr, filehandler)
#
#    filehandler=open('swics1hr.p', 'wb')
#    pickle.dump(swics1hr, filehandler)
#    
#    filehandler=open('swicsqdist.p', 'wb')
#    pickle.dump(swicsqdist, filehandler)
#
#    filehandler=open('magswepam1min.p', 'wb')
#    pickle.dump(magswepam1min, filehandler)
    
    filehandler=open('data/ACE_combined1hr_wdate.p', 'wb')
    combined1hr_wdates={"data":combined1hr, "datetime":combined_datetime}
    pickle.dump(combined1hr_wdates, filehandler)
        
main()