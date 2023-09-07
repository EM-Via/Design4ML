#!/usr/bin/env python
# coding: utf-8

# # FUNCTIONS FOR THE GROCERY LISTS

# ### Import libraries 

# In[61]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import dataframe_image as dfi
from datetime import time
import matplotlib.dates as mdates
from matplotlib.ticker import StrMethodFormatter
from matplotlib.pyplot import figure
from random import sample

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 2)

class bcolors:
    WARNING = '\033[91m'
    BOLD = '\033[1m'


# In[62]:


# Function to generate #visits per day of the week
from AlgorithmDAYS_HH4 import weekdays
#Function to define the limits for total visits, days, same store and type per week
from AlgorithmCOUNTS_HH4 import CountTotalVisits, CountTotalDays, CountStoreName, CountTimePerDay, CountStoreType, CountTotalPerday, CountVisitsPerDay, CountTimingPerDay
# Function to generate #visits per time
from AlgorithmTIMES_HH4 import times
# Function to generate #visits per time
from AlgorithmSTOREday_HH4 import Storename
# Function to decide amounts per visit & per week
from AlgorithmAMOUNT_HH4 import StoreAmount, WeekAmount, StoreCount, WeekCount


# In[63]:


dataframe = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH4\df\df_HH4.csv")


# # Define variables - day/time/store

# ## Days & visits

# In[64]:


CountTotalVisits()


# In[65]:


CountTotalDays()


# In[70]:


i = 0

while i < 2:

    ### 1. What DAY?
    df = weekdays()

#         # identify counts for visits per weekday
#     mo = int(df["times"].values[0])
#     tu = int(df["times"].values[1])
#     we = int (df["times"].values[2])
#     th = int (df["times"].values[3])
#     fr = int (df["times"].values[4])
#     sa = int (df["times"].values[5])
#     su = int (df["times"].values[6])
    
        
        ### CHECKPOINT: range for visits/week and days/week
        
        # Check if the total GROCERY VISITS PER WEEK are within the normal range
    visitcount = df['times'].sum()
    totalvisits = CountTotalVisits()
    minvisits = totalvisits[0]
    maxvisits = totalvisits[1]
    if minvisits <= visitcount <= maxvisits:
        i= i+1
    else:
        i=0
        continue

        # Check if the total GROCERY DAYS PER WEEK are within the normal range
    dayscount = df['times'].nunique()
    totaldays = CountTotalDays()
    mindays = totaldays[0]
    maxdays = totaldays[1]
    if mindays <= dayscount <= maxdays:
        i = i+1
        n = df['times'].sum()
            ## lists from the columns
        df['times'] = df['times'].astype(int)
        timeslist = df.times.values.tolist()
        dayslist = df.day.values.tolist()
            ## times * days
        day = sum([[s] * n for s, n in zip(dayslist, timeslist)], [])
    else:
        i=0
        continue


# ## Assign TIME

# In[76]:


restart = True 

while restart:
    # define times for the amount of visits in this week
    df_timeslist = times(n)

    # create lists from the columns
    df_timeslist['times'] = df_timeslist['times'].astype(int)
    df_timeslist.dtypes
    timeslist = df_timeslist.times.values.tolist()
    timelist = df_timeslist.time.values.tolist()

    # create new dataframe for each day-time
    time = sum([[s] * n for s, n in zip(timelist, timeslist)], [])
    d = {'day':day,'time':time}
    df2 = pd.DataFrame(d, columns=['day','time'])

        # Check if the total STORE TYPES VISITED PER WEEK are within the normal range
    for days in dataframe['day']:
        timecount = df2[df2['day']==days]['day'].count()
        countdaytime = CountTimePerDay(days)
        mintimes = countdaytime[0]
        maxtimes = countdaytime[1]
        if timecount < mintimes:
            restart = True
            break # force restart
        elif maxtimes < timecount:
            restart = True
            break # force restart
        else:
            df3 = df2
            pass
            
        # Check if the total days and times match
    dayslist = df3.day.values.tolist()
    timing = df3.time.values.tolist()        
    for y in dayslist:
            if y == 'Monday':
                for x in timing:
                        if x == 'morning':
                            restart = True
                            break # force restart
                        elif x == 'afternoon':
                            restart = True
                            break # force restart
                        else:
                            pass 
            if y == 'Wednesday':
                for x in timing:
                        if x == 'afternoon':
                            restart = True
                            break # force restart
                        else:
                            pass                                    
            if y == 'Thursday':
                for x in timing:
                        if x == 'morning':
                            restart = True
                            break # force restart
                        else:
                            pass
            if y == 'Friday':
                for x in timing:
                        if x == 'morning':
                            restart = True
                            break # force restart
                        else:
                            pass
            if y == 'Sunday':
                for x in timing:
                        if x == 'morning':
                            restart = True
                            break # force restart
                        else:
                            df4 = df3
                            restart = False
                break


# ## Stores

# In[88]:


def storesfunc():
    dayslist = df4.day.values.tolist()
    timelist = df4.time.values.tolist()
    stores = pd.DataFrame(columns = ['store_name', 'store_type', 'time', 'day'])  
    n = len(dayslist)

    for i in range(n):
        days = dayslist[i]
        timing = timelist[i]
        item = Storename(days, timing)
        stores.append(item, ignore_index=True)


# In[89]:


storesfunc()

# ## Stores & time

# ## Define limits per week (amount)

# In[56]:


def countsfunc():
    storetime = stores[['store_name','time']]
    storetime
    restart = True 
    while restart:
        storecounts = []

        for store, time in storetime.itertuples(index=False):
            storecounts.append(StoreCount(store))

        stores['counts'] = storecounts

        # Check if the total STORES VISITED PER DAY are within the normal range
        for items in dataframe['item_type']:
            week9count = stores['counts'].sum()
            NormWeekCount = WeekCount()
            minWeekCount = NormWeekCount[0]
            maxWeekCount = NormWeekCount[1]
            if week9count < minWeekCount:
                print(f"{bcolors.WARNING}{bcolors.BOLD} RERUN - Too few items:", week9count)
                restart = True
                break # force restart
            elif maxWeekCount < week9count:
                print(f"{bcolors.WARNING}{bcolors.BOLD} RERUN - Too many items:", week9count)
                restart = True
                break # force restart
            else:
                restart = False
                return stores
                break


# In[57]:


countsfunc()


# # The Grocery Lists

# In[110]:


df = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH4\df\df_HH4.csv")


# In[111]:


## Split up the dataframes to store name for mon, tue, sat, sun
timings = stores.time.values.tolist()
storenames = stores.store_name.values.tolist()           
        
timingdf = {}
noonsdf = {}
afternoonsdf = {}
noonsdf = {}
eveningsdf = {}

for timing in stores['time']:
    storetime = df[df['time'] == timing]
    items = storetime[['item_type', 'item_name', 'time','store_name', 'amount']]
    timedf[timing] = pd.DataFrame(items)
    timedf[timing].drop_duplicates()
    
if 'noon' in stores.values:
    for storename  in storenames:
        timingdf = timedf['noon']
        storesdf = timingdf[timingdf['store_name'] == storename]
        items = storesdf[['item_type', 'item_name', 'time', 'store_name', 'amount']]
        noonsdf[storename] = pd.DataFrame(items)
        noonsdf[storename].drop_duplicates()

if 'afternoon'in stores.values:
    for storename  in storenames:
        timingdf = timedf['afternoon']
        storesdf = timingdf[timingdf['store_name'] == storename]
        items = storesdf[['item_type', 'item_name', 'time', 'store_name', 'amount']]
        afternoonsdf[storename] = pd.DataFrame(items)
        afternoonsdf[storename].drop_duplicates()

if 'evening'in stores.values:
    for storename  in storenames:
        timingdf = timedf['evening']
        storesdf = timingdf[timingdf['store_name'] == storename]
        items = storesdf[['item_type', 'item_name', 'time', 'store_name', 'amount']]
        eveningsdf[storename] = pd.DataFrame(items)
        eveningsdf[storename].drop_duplicates()

## Sample the dataframes per day they go shopping
dayamount = stores[['time', 'store_name', 'counts']]

def morning(counts):
    if 'morning' in dayamount.values:
            grocerylist = dayamount[dayamount['time'] == 'morning']
            if 'morning' in dayamount.values:
                typedf['morning'] = typedf['morning'].drop_duplicates()
                return typedf['morning'].sample(n=counts, replace=False)

def noon(counts):
    if 'noon' in dayamount.values:
            grocerylist = dayamount[dayamount['time'] == 'noon']
            storeslist = grocerylist.store_name.values.tolist()
            for storename in storeslist:
                if 'noon' in dayamount.values:
                    noonsdf[storename]= noonsdf[storename].drop_duplicates()
                    return noonsdf[storename].sample(n=counts, replace=True)
        
def afternoon(counts):        
    if 'afternoon' in dayamount.values:
            grocerylist = dayamount[dayamount['time'] == 'afternoon']
            storeslist = grocerylist.store_name.values.tolist()
            for storename in storeslist:
                if 'afternoon' in dayamount.values:
                    afternoonsdf[storename]= afternoonsdf[storename].drop_duplicates()
                    return afternoonsdf[storename].sample(n=counts, replace=True)

def evening(counts):                       
    if 'evening' in dayamount.values:
            grocerylist = dayamount[dayamount['time'] == 'evening']
            storeslist = grocerylist.store_name.values.tolist()
            for storename in storeslist:
                if 'evening' in dayamount.values:
                    eveningsdf[storename]= eveningsdf[storename].drop_duplicates()
                    return eveningsdf[storename].sample(n=counts, replace=True)


# In[112]:


noon(4)

