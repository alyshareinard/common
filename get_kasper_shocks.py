# -*- coding: utf-8 -*-
"""
Created on Fri May 27 16:02:38 2016

@author: alysha.reinard
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_kasper_shocks():
    web_stem="https://www.cfa.harvard.edu/shocks/wi_data/"
    f=open("kasper_wind_shocks.txt", 'w')
    for getyear in range(1995, 2017):
        webpage=web_stem+"wi_"+str(getyear)+".html"
        line="nothing read yet"
        #   try: 
        data=urlopen(webpage)
        soup=BeautifulSoup(data, "html.parser")
#        print(soup)
    
        text_only=soup.get_text()
#        print(text_only)
        count=0
        for link in soup.find_all("a"):
            print("link web address is", link)
        dates=False
        
        indexes=([n for n in range(len(text_only)) if text_only.find(str(getyear), n)==n])
#        start=text_only.find(str(getyear))
        count=0
        for line in indexes:
            if count==0:
                count=1 #first item is from menu
            else:      
                event=text_only[line:line+94].splitlines()
                event=[x for x in event if x]
                if event[0]!=event[1]:
    
#                    print(event)
                    for x in event:
                        f.write(x)
                        f.write(" ")
                    f.write("\n")
#        print(text_only[start])
#        print(text_only[start+1])
#        for item in text_only:
#            #if count<30:

#            if item==str(getyear) or dates==True:
#                print(item)
#                dates=True
#            if "Page" in item:
#                dates=False
             #   count+=1
#        data=data.decode('utf-8')
#        print(data)
    #        data=data.split("\n")

#        for line in data:
#            print(line)
    f.close()
get_kasper_shocks()