# -*- coding: utf-8 -*-
"""

@author: Adrien Wehrlé, GEUS (Geological Survey of Denmark and Greenland)

Run sice.py using multiprocessing with the nb_cores available.
Multiprocessing is used over years if only one day per year, over days of the 
different years otherwise.  

"""

import os
import sys
import subprocess
import numpy as np
import multiprocessing
from multiprocessing import Pool

nb_cores=multiprocessing.cpu_count()

mosaic_root=(sys.argv)[1]
doys_years=(sys.argv)[2:]

doys=[]
[doys.append(np.int(i)) for i in doys_years if len(i)==3]
years=[]
[years.append(np.int(i)) for i in doys_years if len(i)==4]


def sicepy_multiprocessing(k):
    
    if len(doys)==1:
        date=subprocess.Popen('$(date -d "${'+years[k]+'}-01-01 +$(( 10#${'+doy+'}-1 ))\
                              days" "+%Y-%m-%d")')
    else:
        date=subprocess.Popen('$(date -d "${'+year+'}-01-01 +$(( 10#${'+doys[k]+'}-1 ))\
                              days" "+%Y-%m-%d")')
                              
    os.system('./sice.py ${'+mosaic_root+'}/${'+date+'}')

# one day: multiprocessing over years
if len(doys)==1: 
    
    doy=doys[0]
    if __name__ == '__main__':
        with Pool(nb_cores) as p:
            p.map(sicepy_multiprocessing, years) 

# two days: multiprocessing over days from day1 to day2.
elif len(doys)==2:
    
    for year in years:
        if __name__ == '__main__':
            with Pool(nb_cores) as p:
                p.map(sicepy_multiprocessing, list(range(doys[0],doys[1])))   

# more than two days: multiprocessing over days for selected dates.  
elif len(doys)>2:
    
    for year in years:
        if __name__ == '__main__':
            with Pool(nb_cores) as p:
                p.map(sicepy_multiprocessing, doys)
