#!/usr/bin/env python
# coding: utf-8

# ## 3: THIRD ALGORITHM - Where WILL THEY SHOP?

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


# ### Load and view data 

# In[2]:


# data for HH
df = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH4\df\df_HH4.csv")


# In[4]:


from STORENAME_HH4 import storename


# In[6]:


df_storename = storename()


# In[7]:


# Assign weights based on how the numbers per day are represented
df_MCD = pd.DataFrame(df_storename['MCD'])
df_MCD['weights'] = df_MCD.groupby(['MCD'])['MCD'].transform('count')
df_MCD = df_MCD.drop_duplicates()

df_DePers = pd.DataFrame(df_storename['De Pers'])
df_DePers['weights'] = df_DePers.groupby(['De Pers'])['De Pers'].transform('count')
df_DePers = df_DePers.drop_duplicates()

df_AH = pd.DataFrame(df_storename['Albert Heijn'])
df_AH['weights'] = df_AH.groupby(['Albert Heijn'])['Albert Heijn'].transform('count')
df_AH = df_AH.drop_duplicates()


# # 1. SELECT TIMES
# 

# In[9]:

#create random samples for each day based on the assigned weights
def storename(n):
    i = 0

    while i < 1:
        df_MCDs = df_MCD.sample(n=1, weights='weights') 
        df_MCDs = df_MCDs.rename(columns={"MCD": "times"})

        df_DePerss = df_DePers.sample(n=1, weights='weights')
        df_DePerss = df_DePerss.rename(columns={"De Pers": "times"})

        df_AHs = df_AH.sample(n=1, weights='weights')
        df_AHs = df_AHs.rename(columns={"Albert Heijn": "times"})

        #combine all random samplers and print the final (random) week9
        df_week9 = pd.concat([df_MCDs, df_DePerss, df_AHs])
        df_week9['store_name']=['MCD', 'De Pers', 'Albert Heijn']
        df_week9

        store9=[]
        for store in  df_week9['store_name']:
            store_9 = df.loc[df['store_name'] == store, 'store_type'].iloc[0]
            store9.append(store_9)

        df_week9['store_type'] = store9
        df_week9
            
        del df_week9['weights']
        if df_week9['times'].sum() == n:
            i= i+1
            return df_week9
        else:
            i=0
            continue


# In[11]:




