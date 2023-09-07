#!/usr/bin/env python
# coding: utf-8

# ## 2: SECOND ALGORITHM - WHERE WILL THEY SHOP?
# 
# Outcome (example):
# 1. input: Monday,Tuesday...
# 2. output: store name X,Y...

# ### Import libraries 

# In[2]:


# %matplotlib notebook
get_ipython().run_line_magic('matplotlib', 'inline')
#Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns
import dataframe_image as dfi
from datetime import time
import matplotlib.dates as mdates
from matplotlib.ticker import StrMethodFormatter
from matplotlib.pyplot import figure
class bcolors:
    WARNING = '\033[91m'
    BOLD = '\033[1m'
    
# ### Load and view data 

# In[3]:


# data for HH
dataframe = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3.csv")
df = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3.csv")


# data for different days vs stores
df_Monday = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3_Mo.csv")
df_Tuesday = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3_Tu.csv")
df_Wednesday = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3_We.csv")
df_Thursday = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3_Th.csv")
df_Friday = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3_Fr.csv")
df_Saturday = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3_Sa.csv")
df_Sunday = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3_Su.csv")


    # Function to generate #visits per day of the week
from AlgorithmDAYS_HH3 import weekdays, dayofweek

    #Function to define the limits for total visits, days, same store and type per week
from AlgorithmCOUNTS_HH3 import CountTotalVisits, CountTotalDays, CountStoreName, CountTimePerDay, CountStoreType, CountTotalPerday, CountVisitsPerDay, CountTimingPerDay
    
    # Function to generate #visits per time
from AlgorithmTIMES_HH3 import timeperday

    # Function to decide amounts per visit & per week
from AlgorithmAMOUNT_HH3 import StoreAmount, WeekAmount, StoreCount, WeekCount, CatCount, PerCatCount, countsperstore
# # 1. SELECT STORE NAME

# In[5]:

#create random samples for this day based on the assigned weights
def MondayStore(n):
    df_Mondays = df_Monday.sample(n=n, weights='weight', replace=True) 
    df_Mondays = df_Mondays.assign(day='Monday')
    del df_Mondays['weight']
    return df_Mondays

#create random samples for this day based on the assigned weights
def TuesdayStore(n):
    df_Tuesdays = df_Tuesday.sample(n=n, weights='weight', replace=True) 
    df_Tuesdays = df_Tuesdays.assign(day='Tuesday')
    del df_Tuesdays['weight']
    return df_Tuesdays

#create random samples for this day based on the assigned weights
def WednesdayStore(n):
    df_Wednesdays = df_Wednesday.sample(n=n, weights='weight', replace=True) 
    df_Wednesdays = df_Wednesdays.assign(day='Wednesday')
    del df_Wednesdays['weight']
    return df_Wednesdays

#create random samples for this day based on the assigned weights
def ThursdayStore(n):
    df_Thursdays = df_Thursday.sample(n=n, weights='weight', replace=True) 
    df_Thursdays = df_Thursdays.assign(day='Thursday')
    del df_Thursdays['weight']
    return df_Thursdays

#create random samples for this day based on the assigned weights
def FridayStore(n):
    df_Fridays = df_Friday.sample(n=n, weights='weight', replace=True) 
    df_Fridays = df_Fridays.assign(day='Friday')
    del df_Fridays['weight']
    return df_Fridays

#create random samples for this day based on the assigned weights
def SundayStore(n):
    df_Sundays = df_Sunday.sample(n=n, weights='weight', replace=True) 
    df_Sundays = df_Sundays.assign(day='Sunday')
    del df_Sundays['weight']
    return df_Sundays

    
 # New function for store per day
def storeperday(dataframes, dataframes2):
    restart = True

    while restart:
        
        ### 2. What STORE?
        # identify counts for visits per weekday
        mo = int(dataframes["times"].values[0])
        tu = int(dataframes["times"].values[1])
        we = int (dataframes["times"].values[2])
        th = int (dataframes["times"].values[3])
        fr = int (dataframes["times"].values[4])
        sa = int (dataframes["times"].values[5])
        su = int (dataframes["times"].values[6])

        # Generate store names for the [previously identified] shopping dags + corresponding store type
        df3 = [MondayStore(mo), TuesdayStore(tu), WednesdayStore(we), ThursdayStore(th), FridayStore(fr), SundayStore(su)]
        # create one df for all visited stores + day of the week
        df3 = pd.concat(df3)
        stores = pd.merge(df3, dataframes2, how="left", on="day")


        ### CHECKPOINT: range for visits/week and days/week

        # Check if the total STORE TYPES VISITED PER WEEK are within the normal range
        for storetype in stores['store_type']:
            typecount = stores[stores['store_type']==storetype]['store_type'].count()
            countstoretype = CountStoreType(storetype)
            minstoretype = countstoretype[0]
            maxstoretype = countstoretype[1]
            if minstoretype <= typecount <= maxstoretype:
                pass
            else:
                print(f"{bcolors.WARNING}{bcolors.BOLD} RERUN - Too few/many store type:", storetype)
                restart = True
                break

        # Check if the total STORE NAMES VISITED PER WEEK are within the normal range
        for storename in stores['store_name']:
            namecount = stores[stores['store_name']==storename]['store_name'].count()
            countstorename = CountStoreName(storename)
            minstorename = countstorename[0]
            maxstorename = countstorename[1]
            if minstorename <= namecount <= maxstorename:
                restart = False
                return stores
                break
            else:
                print(f"{bcolors.WARNING}{bcolors.BOLD} RERUN - Too few/many store name:", storename)
                restart = True
                break
