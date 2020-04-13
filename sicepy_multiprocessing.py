# -*- coding: utf-8 -*-
"""

@author: Adrien Wehrlé, GEUS (Geological Survey of Denmark and Greenland)

Run sice.py using multiprocessing with the nb_cores available.
Multiprocessing is used over years if only one day per year, over days of the 
different years otherwise.  

"""

import os
import multiprocessing
from multiprocessing import Pool
import sys

mosaic_root=(sys.argv)[1]
doys_years=(sys.argv)[2:]

doys=[]
[doys.append(np.int(i)) for i in doys_years if len(i)==3]
years=[]
[years.append(np.int(i)) for i in doys_years if len(i)==4]

nb_cores=multiprocessing.cpu_count()


def sicepy_multiprocessing(k):
    
    if len(doys)==1:
        date=subprocess.Popen('$(date -d "${'+years[k]+'}-01-01 +$(( 10#${'+doy+'}-1 ))\
                              days" "+%Y-%m-%d")')
    else:
        date=subprocess.Popen('$(date -d "${'+year+'}-01-01 +$(( 10#${'+doys[k]+'}-1 ))\
                              days" "+%Y-%m-%d")')
                              
    os.system('./sice.py ${'+args.mosaic_root+'}/${'+date+'}')
    
if len(doys)==0: 
    
    doy=doys[0]
        if __name__ == '__main__':
            with Pool(nb_cores) as p:
                p.map(sicepy_multiprocessing, list(years)) 
                
else:
    
    for year in years:
        if __name__ == '__main__':
            with Pool(nb_cores) as p:
                p.map(sicepy_multiprocessing, list(range(doys[0],doys[1])))
