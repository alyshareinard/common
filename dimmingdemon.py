# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 15:00:46 2016

@author: alyshareinard
"""


import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from astropy.io import fits
from urllib.request import urlopen

def read_dimmingdemon():
    web_stem="ftp://gong2.nso.edu/HA/haf/"
    webpage=web_stem+"201604/20160408/"+"20160211000014Mh.fits.fz"
    print("webpage:", webpage)
#    hdulist=fits.open("data/mrrpm010722dh5f.fits.gz")
#    hdulist=fits.open("data/20160211000014Mh.fits.fz")
    hdulist=fits.open(webpage)
    hdulist.info()
    print(hdulist[0].header)
    scidata=hdulist[1].data
    imgplot = plt.imshow(scidata, cmap="gray")#[0,:,:])
    plt.colorbar()
    hdulist.close()
    
read_dimmingdemon()