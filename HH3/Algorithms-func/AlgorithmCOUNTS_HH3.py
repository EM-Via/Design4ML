#!/usr/bin/env python
# coding: utf-8

# ## 2.2. CHECKPOINT: counts & intervals per week/stores

# ### Import libraries 

# In[16]:


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


# ### Load and view data 

# In[17]:


# data for HH
df = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3.csv")


# In[18]:


df_orders = df[['order_ID', 'week', 'store_name', 'storename_num', 'store_type', 'storetype_num','day', 'day_num', 'time', 'time_num', 'timestamp', 'times', 'dates', 'times_min', 'dates_days', 'order_amount', 'order_price']]
df_orders = df_orders.drop_duplicates()


# # Maximums per week

# In[19]:


def CountTotalVisits():
    Count = df_orders.groupby(['week'])['order_ID'].nunique()
    Count = pd.DataFrame (Count)
    Count = Count.reset_index()

    min = Count.min(axis=0,numeric_only=True)['order_ID']
    max = Count.max(axis=0,numeric_only=True)['order_ID']
    return min, max


# In[21]:


def CountTotalDays():
    Count = df_orders.groupby(['week'])['day'].nunique()
    Count = pd.DataFrame (Count)
    Count = Count.reset_index()

    min = Count.min(axis=0,numeric_only=True)['day']
    max = Count.max(axis=0,numeric_only=True)['day']
    return min, max


# In[22]:


def CountTotalPerday():
    Count = df_orders.groupby(['week', 'day'])['order_ID'].count()
    Count = pd.DataFrame (Count)
    Count = Count.reset_index()

    min = Count.min(axis=0,numeric_only=True)['order_ID']
    max = Count.max(axis=0,numeric_only=True)['order_ID']
    return min, max

# In[23]:


weeks = [1,2,3,4,5,6,7,8]
df_orders.loc[:, ('week')] = pd.Categorical(df_orders.loc[:, ('week')], categories=weeks)


# In[24]:

def CountVisitsPerDay(day):
    df_count = df_orders[df_orders['day']== day]

    Count = df_count.sort_values(by=['week'])
    Count = Count.groupby(['week'])['order_ID'].nunique()
    Count = pd.DataFrame (Count)
    Count = Count.reset_index()

    min = Count.min(axis=0,numeric_only=True)['order_ID']
    max = Count.max(axis=0,numeric_only=True)['order_ID']
    return min, max


def CountStoreName(store):
    df_count = df_orders[df_orders['store_name']== store]

    Count = df_count.sort_values(by=['week'])
    Count = Count.groupby(['week'])['order_ID'].nunique()
    Count = pd.DataFrame (Count)
    Count = Count.reset_index()

    min = Count.min(axis=0,numeric_only=True)['order_ID']
    max = Count.max(axis=0,numeric_only=True)['order_ID']
    return min, max

# In[27]:


def CountStoreType(store):
    df_count = df_orders[df_orders['store_type']== store]

    Count = df_count.sort_values(by=['week'])
    Count = Count.groupby(['week'])['order_ID'].nunique()
    Count = pd.DataFrame (Count)
    Count = Count.reset_index()

    min = Count.min(axis=0,numeric_only=True)['order_ID']
    max = Count.max(axis=0,numeric_only=True)['order_ID']
    return min, max


def CountTimePerDay(day):
    df_count = df_orders[df_orders['day']== day]

    Count = df_count.sort_values(by=['week'])
    Count = Count.groupby(['week'])['order_ID'].nunique()
    Count = pd.DataFrame (Count)
    Count = Count.reset_index()

    min = Count.min(axis=0,numeric_only=True)['order_ID']
    max = Count.max(axis=0,numeric_only=True)['order_ID']
    return min, max


def CountTimingPerDay(time):
    df_count = df_orders[df_orders['time']== time]
    Count = df_count.groupby(['week', 'day'])['order_ID'].count()
    Count = pd.DataFrame (Count)
    Count = Count.reset_index()

    min = Count.min(axis=0,numeric_only=True)['order_ID']
    max = Count.max(axis=0,numeric_only=True)['order_ID']
    return min, max


def CountTypePerStore(itemtype, storetype):
    df_type = df[df['store_type'] == storetype]
    count = int(df['order_ID'].nunique())
    data = {'order_ID': range(count)}
    orderID = pd.DataFrame(data)
    df_type = df_type[df_type['item_type'] == itemtype]
    df_type = df_type.groupby(['order_ID'])['amount'].count()
    df_type = pd.DataFrame (df_type)
    df_type = df_type.reset_index() 
    df_type = orderID.merge(df_type, how='left').fillna(0)
    min = df_type.min(axis=0)['amount']
    max = df_type.max(axis=0)['amount']
    return (min, max)
