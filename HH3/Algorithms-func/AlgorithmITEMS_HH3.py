#!/usr/bin/env python
# coding: utf-8

# ## 4: FUNCTIONS FOR ITEMS PER TIME, STORENAME

# ### Import libraries 

# In[72]:

import pandas as pd
import numpy as np
from random import sample
class bcolors:
    WARNING = '\033[91m'
    BOLD = '\033[1m'


# ### Load and view data 

# In[73]:


    # Function to generate #visits per day of the week
from AlgorithmDAYS_HH3 import weekdays, dayofweek
    #Function to define the limits for total visits, days, same store and type per week
from AlgorithmCOUNTS_HH3 import CountTotalVisits, CountTotalDays, CountStoreName, CountTimePerDay, CountStoreType, CountTotalPerday, CountVisitsPerDay, CountTimingPerDay
    # Function to generate #visits per time
from AlgorithmTIMES_HH3 import Monday, Tuesday, Wednesday, Thursday, Friday, Sunday, timeperday
    # Function to generate #visits per time
from AlgorithmSTOREday_HH3 import MondayStore, TuesdayStore, WednesdayStore, ThursdayStore, FridayStore, SundayStore, storeperday
    # Function to decide amounts per visit & per week
from AlgorithmAMOUNT_HH3 import StoreAmount, WeekAmount, StoreCount, WeekCount, CatCount, PerCatCount, countsperstore


# In[74]:

df = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3.csv")


# In[85]:

def supermarket(dataframes, counts, storenamez):
        ## Create dataframes for each day they go shopping
    typedf = {}
    storetypes = dataframes.store_type.values.tolist()
    storenames = dataframes.store_name.values.tolist()           
    thisnamedf = {}
    storenamedf = {}
    for storetype in dataframes['store_type']:
            storeday = df[df['store_type'] == storetype]
            items = storeday[['item_type', 'item_name', 'time', 'store_type','store_name', 'amount', 'category']]
            typedf[storetype] = pd.DataFrame(items)
            typedf[storetype].drop_duplicates()        
    ## Split up the dataframes to store name for mon, tue, sat, sun
    if 'supermarket'in dataframes.values:
            for storename in storenames:
                thisnamedf = typedf['supermarket']
                storesdf = thisnamedf[thisnamedf['store_name'] == storename]
                items = storesdf[['item_type', 'item_name', 'store_type', 'store_name', 'amount', 'category']]
                storenamedf[storename] = pd.DataFrame(items)
                storenamedf[storename].drop_duplicates()                
    ## Sample the dataframes per day they go shopping
    if 'supermarket' in dataframes.values:
            grocerylist = dataframes[dataframes['store_type'] == 'supermarket']
            if 'supermarket' in dataframes.values:
                storenamedf[storenamez]= storenamedf[storenamez].drop_duplicates()
                return storenamedf[storenamez].sample(n=counts, replace=False)


# In[86]:

def bakery(dataframes, counts):
        ## Create dataframes for each day they go shopping
    typedf = {}
    for storetype in dataframes['store_type']:
            storeday = df[df['store_type'] == storetype]
            items = storeday[['item_type', 'item_name', 'store_type','store_name', 'amount', 'category']]
            typedf[storetype] = pd.DataFrame(items)
            typedf[storetype].drop_duplicates() 
    if 'bakery' in dataframes.values:
        grocerylist = dataframes[dataframes['store_type'] == 'bakery']
        if 'bakery' in dataframes.values:
            typedf['bakery'] = typedf['bakery'].drop_duplicates()
            return typedf['bakery'].sample(n=counts, replace=False)


# In[70]:

def petsupply(dataframes, counts):
        ## Create dataframes for each day they go shopping
    typedf = {}
    for storetype in dataframes['store_type']:
            storeday = df[df['store_type'] == storetype]
            items = storeday[['item_type', 'item_name', 'store_type','store_name', 'amount', 'category']]
            typedf[storetype] = pd.DataFrame(items)
            typedf[storetype].drop_duplicates() 
        ## sample dataframes per store type
    if 'pet supplies' in dataframes.values:
            grocerylist = dataframes[dataframes['store_type'] == 'pet supplies']
            if 'pet supplies' in dataframes.values:
                typedf['pet supplies'] = typedf['pet supplies'].drop_duplicates()
                return typedf['pet supplies'].sample(n=counts, replace=False)


### Get lists per store type for the weekplanning output

def supermarkets(dataframes, index):
    storesuper = dataframes[dataframes['store_type'] == 'supermarket']
    storesuper = storesuper[['store_name', 'store_type', 'counts', 'I']]
    storesuper = storesuper.to_numpy()
    s = {}
    supermarkets = pd.DataFrame(columns = ['item_type', 'item_name', 'amount', 'category'])
    for storename, storetype, counts, i in storesuper:
        s[i] = pd.DataFrame(supermarket(dataframes, counts, storename))     
    s[i] = s[index]
    return s[index]

def bakeries(dataframes, index):
    storebake = dataframes[dataframes['store_type'] == 'bakery']
    storebake = storebake[['store_type', 'counts', 'I']]
    storebake = storebake.to_numpy()
    ba = {}
    supermarkets = pd.DataFrame(columns = ['item_type', 'item_name', 'amount', 'category'])
    for storetype, counts, i in storebake:
        ba[i] = pd.DataFrame(bakery(dataframes, counts))     
    ba[i] = ba[index]
    return ba[index]

def petsupplies(dataframes, index):
    storepet = dataframes[dataframes['store_type'] == 'pet supplies']
    storepet = storepet[['store_type', 'counts', 'I']]
    storepet = storepet.to_numpy()
    p = {}
    supermarkets = pd.DataFrame(columns = ['item_type', 'item_name', 'amount', 'category'])
    for storetype, counts, i in storepet:
        p[i] = pd.DataFrame(petsupply(dataframes, counts))     
    p[i] = p[index]
    return p[index]