# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 11:29:34 2016

@author: alyshareinard

Very basic -- so far just reads in GONG fits files and displays them
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from astropy.io import fits
from urllib.request import urlopen

def read_GONGfits():
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
    
read_GONGfits()