#!/usr/bin/env python
# coding: utf-8

# ## 3: THIRD ALGORITHM - AT WHAT TIME WILL THEY SHOP?
# 
# Outcome (example):
# 1. input: Monday,Tuesday...
# 2. output: noon/morning/afternoon

# ### Import libraries 

# In[1]:


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
import random
import matplotlib.dates as mdates
from matplotlib.ticker import StrMethodFormatter
from matplotlib.pyplot import figure

class bcolors:
    WARNING = '\033[91m'
    BOLD = '\033[1m'
# ### Load and view data 

# In[2]:


# data for HH
df = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3.csv")
dataframe = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3.csv")

# data for different days vs stores
df_Mondays = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3_MoTime.csv")
df_Tuesdays = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3_TuTime.csv")
df_Wednesdays = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3_WeTime.csv")
df_Thursdays = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3_ThTime.csv")
df_Fridays = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3_FrTime.csv")
df_Saturdays = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3_SaTime.csv")
df_Sundays = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3_SuTime.csv")


    # Function to generate #visits per day of the week
from AlgorithmDAYS_HH3 import weekdays, dayofweek

    #Function to define the limits for total visits, days, same store and type per week
from AlgorithmCOUNTS_HH3 import CountTotalVisits, CountTotalDays, CountStoreName, CountTimePerDay, CountStoreType, CountTotalPerday, CountVisitsPerDay, CountTimingPerDay


# In[4]:

#create random samples for this day based on the assigned weights
def Monday(n):
    df_Monday = df_Mondays.sample(n=n, weights='weight', replace=True) 
    df_Monday = df_Monday.assign(day='Monday')
    del df_Monday['weight']
    return df_Monday

#create random samples for this day based on the assigned weights
def Tuesday(n):
    df_Tuesday = df_Tuesdays.sample(n=n, weights='weight', replace=True) 
    df_Tuesday = df_Tuesday.assign(day='Tuesday')
    del df_Tuesday['weight']
    return df_Tuesday

#create random samples for this day based on the assigned weights
def Wednesday(n):
    df_Wednesday = df_Wednesdays.sample(n=n, weights='weight', replace=True) 
    df_Wednesday = df_Wednesday.assign(day='Wednesday')
    del df_Wednesday['weight']
    return df_Wednesday

#create random samples for this day based on the assigned weights
def Thursday(n):
    df_Thursday = df_Thursdays.sample(n=n, weights='weight', replace=True) 
    df_Thursday = df_Thursday.assign(day='Thursday')
    del df_Thursday['weight']
    return df_Thursday

#create random samples for this day based on the assigned weights
def Friday(n):
    df_Friday = df_Fridays.sample(n=n, weights='weight', replace=True) 
    df_Friday = df_Friday.assign(day='Friday')
    del df_Friday['weight']
    return df_Friday

# #create random samples for this day based on the assigned weights
# def Saturday(n):
#     df_Saturday = df_Saturdays.sample(n=n, weights='weight', replace=True) 
#     df_Saturday = df_Saturday.assign(day='Saturday')
#     del df_Saturday['weight']
#     return df_Saturday

#create random samples for this day based on the assigned weights
def Sunday(n):
    df_Sunday = df_Sundays.sample(n=n, weights='weight', replace=True) 
    df_Sunday = df_Sunday.assign(day='Sunday')
    del df_Sunday['weight']
    return df_Sunday



def timeperday(dataframes):
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
        times = [Monday(mo), Tuesday(tu), Wednesday(we), Thursday(th), Friday(fr), Sunday(su)]
        # create one df for all visited stores + day of the week
        times = pd.concat(times)


        ### CHECKPOINT: range for visits/week and days/week

        # Check if the total STORE TYPES VISITED PER WEEK are within the normal range
        timecount = times[['time', 'day']]
        timecount = timecount.to_numpy()

        for timing, days in timecount:
            timeecount = times[times['time']==timing]['time'].count()
            counttimesperday = CountTimingPerDay(timing)
            mindaytimes = counttimesperday[0]
            maxdaytimes = counttimesperday[1]
            if mindaytimes <= timeecount <= maxdaytimes:
                restart = False
                return times
                break
            else:
                print(f"{bcolors.WARNING}{bcolors.BOLD} RERUN - Too few/many times per day")
                restart = True
                break