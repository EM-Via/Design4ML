#!/usr/bin/env python
# coding: utf-8

# ## 4: FOURTH ALGORITHM - FROM WHAT CATEGORIES?
# 
# Outcome (example):
# 1. input: DAY, TIME, STORE
# 2. output: CATEGORIES

# ### Import libraries 

# In[21]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import numpy as np
from random import sample
import random
class bcolors:
    WARNING = '\033[91m'
    BOLD = '\033[1m'


# In[2]:


# Function to generate #visits per day of the week
from AlgorithmDAYS_HH3 import weekdays, dayofweek

# Function to generate #visits per time
from AlgorithmTIMES_HH3 import Monday, Tuesday, Wednesday, Thursday, Friday, Sunday, timeperday

# Function to generate #visits per time
# from AlgorithmSTOREday_HH3 import MondayStore, TuesdayStore, WednesdayStore, ThursdayStore, FridayStore, SundayStore, storeperday

# ### Load and view data 

# In[3]:


df = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3.csv")


# In[4]:


df_orders = df[['order_ID', 'week', 'store_name', 'storename_num', 'store_type', 'storetype_num','day', 'day_num', 'time', 'time_num', 'timestamp', 'times', 'dates', 'times_min', 'dates_days', 'order_amount', 'order_price']]
df_orders = df_orders.drop_duplicates()


# # Function (store as option)

# In[5]:


def StoreAmount(storename):
    df_store = df[df['store_name'] == storename]
    df_store = df_store.groupby(['order_ID'])['amount'].sum()
    df_store = pd.DataFrame (df_store)
    df_store = df_store.reset_index()        
    min = df_store.min(axis=0)['amount']
    max = df_store.max(axis=0)['amount']
    return random.randint(min, max)


# In[6]:


def StoreCount(storename):
    df_store = df[df['store_name'] == storename]
    df_store = df_store.groupby(['order_ID'])['amount'].count()
    df_store = pd.DataFrame (df_store)
    df_store = df_store.reset_index()        
    min = df_store.min(axis=0)['amount']
    max = df_store.max(axis=0)['amount']
    return random.randint(min, max)


# # For the entire week

# In[7]:


def WeekAmount():
    df_amount = df_orders.groupby(['week'])['order_amount'].sum()
    df_amount = pd.DataFrame (df_amount)
    df_amount = df_amount.reset_index()

    min = df_amount.min(axis=0)['order_amount']
    max = df_amount.max(axis=0)['order_amount']
    return (min,max)



# In[9]:


def WeekCount():
    df_count = df.groupby(['week'])['amount'].count()
    df_count = pd.DataFrame (df_count)
    df_count = df_count.reset_index()

    min = df_count.min(axis=0)['amount']
    max = df_count.max(axis=0)['amount']
    return (min,max)



# # Per category

# In[11]:


def CatCount():
    df_count = df.groupby(['week'])['category'].nunique()
    df_count = pd.DataFrame (df_count)
    df_count = df_count.reset_index()

    min = df_count.min(axis=0)['category']
    max = df_count.max(axis=0)['category']
    return (min,max)


# ### Check the counts for each category

#  The sign. limits differed in the two periods, split the df up:

# In[13]:


# for entire period
def PerCatCount(category):
    data = {'week': [1,2,3,4,5,6,7,8]}
    weeks = pd.DataFrame(data)
    df_cat = df[df['category'] == category]
    df_cat = df_cat.groupby(['week'])['amount'].count()
    df_cat = pd.DataFrame (df_cat)
    df_cat = df_cat.reset_index() 
    df_cat = weeks.merge(df_cat, how='left').fillna(0)
    min = df_cat.min(axis=0)['amount']
    max = df_cat.max(axis=0)['amount']
    return (min, max)


# # Itemcounts per store type



# In[22]:

def countsperstore(dataframes):
    storetime = dataframes[['store_name','time']]
    
    restart = True 
    while restart:
        storecounts = []

        for store, time in storetime.itertuples(index=False):
            storecounts.append(StoreCount(store))

        dataframes['counts'] = storecounts

        # Check if the total STORES VISITED PER DAY are within the normal range
        for items in df['item_type']:
            week9count = dataframes['counts'].sum()
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
                return dataframes
                break