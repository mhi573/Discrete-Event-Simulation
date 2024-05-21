# -*- coding: utf-8 -*-
"""
Additing agent/consumer individual differences
to the coffee shop simultion

We develop the logic and code outside of the simulation
with the idea of later integrating the code into the simulation

Note that additional code will be added within the simulation
so that the case information may be retained for use outside
of the simulation. The process is similar to what was used
for the simulation event log.

Created on Thu May 27 14:56:20 2022

@author: tom miller
"""
import pandas as pd
import numpy as np

# set percentage of customers who are "rushed"
prushed = 50

mean_service_time = 2 # minutes (120 seconds)

# create data frame with case information
# caseid is case identifier used throughout simulation
# casetype "relaxed" or "rushed" is randomly assigned Bernoulli (prushed)
# qmax is maxiumum line length tolerated before balking
#     5 if "rushed"
#    10 if "relaxed"
# wmax is total expected wait time minutes tolerated before reneging
#     5 * mean service time minutes if "rushed"
#    10 * mean service time minutes if "relaxed"

# define empty data frame
caseinfo = pd.DataFrame(columns = ["caseid", "casetype", "qmax", "wmax"])

# add caseid with attributes to existing caseinfo data frame
def addcase (caseinfo, caseid):
    if np.random.binomial(1, prushed/100, size = 1)[0] == 1:
        casetype = "rushed"
        qmax = 5
        wmax = 5 * mean_service_time
    else:
        casetype = "relaxed" 
        qmax = 10
        wmax = 10 * mean_service_time               
    newcase = pd.DataFrame([[caseid, casetype, qmax, wmax]], 
                           columns = ["caseid", "casetype", "qmax", "wmax"])   
    return pd.concat([caseinfo, newcase])

for i in range(10):
    caseid = i
    caseinfo = addcase(caseinfo, caseid)    
        
print(caseinfo)

caseinfo.to_csv("caseinfo.csv", index = False)




