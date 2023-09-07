#!/usr/bin/env python
# coding: utf-8

# ## 1: FIRST ALGORITHM - ON WHAT DAYS WILL THEY SHOP?
# 
# Outcome (example):
# 1. input: Monday,Tuesday...
# 2. output: 0 times, 1 time, 2 times...

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
import matplotlib.dates as mdates
from matplotlib.ticker import StrMethodFormatter
from matplotlib.pyplot import figure
class bcolors:
    WARNING = '\033[91m'
    BOLD = '\033[1m'

# ### Load and view data 

# In[2]:


# # data for dow
# df_period1 = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH2\df\df_HH2_period1.csv")
# df_period2 = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH2\df\df_HH2_period2.csv")


# In[3]:


from DAYS_HH3weights import period
  #Function to define the limits for total visits, days, same store and type per week
from AlgorithmCOUNTS_HH3 import CountTotalVisits, CountTotalDays, CountStoreName, CountTimePerDay, CountStoreType, CountTotalPerday, CountVisitsPerDay, CountTimingPerDay


# In[4]:


df_period = period()

# In[5]:


# Assign weights based on how the numbers per day are represented
df_Mondays1 = pd.DataFrame(df_period['Monday'])
df_Mondays1['weights'] = df_Mondays1.groupby(['Monday'])['Monday'].transform('count')
df_Mondays1 = df_Mondays1.drop_duplicates()

df_Tuesdays1 = pd.DataFrame(df_period['Tuesday'])
df_Tuesdays1['weights'] = df_Tuesdays1.groupby(['Tuesday'])['Tuesday'].transform('count')
df_Tuesdays1 = df_Tuesdays1.drop_duplicates()

df_Wednesdays1 = pd.DataFrame(df_period['Wednesday'])
df_Wednesdays1['weights'] = df_Wednesdays1.groupby(['Wednesday'])['Wednesday'].transform('count')
df_Wednesdays1 = df_Wednesdays1.drop_duplicates()

df_Thursdays1 = pd.DataFrame(df_period['Thursday'])
df_Thursdays1['weights'] = df_Thursdays1.groupby(['Thursday'])['Thursday'].transform('count')
df_Thursdays1 = df_Thursdays1.drop_duplicates()

df_Fridays1 = pd.DataFrame(df_period['Friday'])
df_Fridays1['weights'] = df_Fridays1.groupby(['Friday'])['Friday'].transform('count')
df_Fridays1 = df_Fridays1.drop_duplicates()

df_Saturdays1 = pd.DataFrame(df_period['Saturday'])
df_Saturdays1['weights'] = df_Saturdays1.groupby(['Saturday'])['Saturday'].transform('count')
df_Saturdays1 = df_Saturdays1.drop_duplicates()

df_Sundays1 = pd.DataFrame(df_period['Sunday'])
df_Sundays1['weights'] = df_Sundays1.groupby(['Sunday'])['Sunday'].transform('count')
df_Sundays1 = df_Sundays1.drop_duplicates()


# In[6]:


df_Saturdays1


# # 1. SELECT DAYS OF THE WEEK


# In[10]:

#create random samples for each day based on the assigned weights
def weekdays():
    df_Monday = df_Mondays1.sample(n=1, weights='weights') 
    df_Monday = df_Monday.rename(columns={"Monday": "times"})

    df_Tuesday = df_Tuesdays1.sample(n=1, weights='weights')
    df_Tuesday = df_Tuesday.rename(columns={"Tuesday": "times"})

    df_Wednesday = df_Wednesdays1.sample(n=1, weights='weights')
    df_Wednesday = df_Wednesday.rename(columns={"Wednesday": "times"})

    df_Thursday = df_Thursdays1.sample(n=1, weights='weights')
    df_Thursday = df_Thursday.rename(columns={"Thursday": "times"})

    df_Friday = df_Fridays1.sample(n=1, weights='weights')
    df_Friday = df_Friday.rename(columns={"Friday": "times"})

    df_Saturday = df_Saturdays1.sample(n=1, weights='weights')
    df_Saturday = df_Saturday.rename(columns={"Saturday": "times"})

    df_Sunday = df_Sundays1.sample(n=1, weights='weights')
    df_Sunday = df_Sunday.rename(columns={"Sunday": "times"})

    #combine all random samplers and print the final (random) week9
    df_week9_beforeNY = pd.concat([df_Monday, df_Tuesday, df_Wednesday, df_Thursday, df_Friday,df_Saturday,df_Sunday])
    df_week9_beforeNY['day']=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    del df_week9_beforeNY['weights']
    return df_week9_beforeNY



def dayofweek():
    i = 0

    while i < 2:

        ### 1. What DAY?
        df = weekdays()

        ### CHECKPOINT: range for visits/week and days/week

            # Check if the total GROCERY VISITS PER WEEK are within the normal range
        visitcount = df['times'].sum()
        totalvisits = CountTotalVisits()
        minvisits = totalvisits[0]
        maxvisits = totalvisits[1]
        if minvisits <= visitcount <= maxvisits:
            i= i+1
        else:
            print(f"{bcolors.WARNING}{bcolors.BOLD} RERUN - Too few/many visits per week")
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
            return df
        else:
            print(f"{bcolors.WARNING}{bcolors.BOLD} RERUN - Too few/many days per week")
            i=0
            continue
