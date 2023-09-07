#!/usr/bin/env python
# coding: utf-8

# ## 1: FIRST ALGORITHM - ON WHAT DAYS WILL THEY SHOP?
# 
# 
# 1. build grid: when do/dont they shop, how many times, on which day...
# 2. define priliminaries for algorithm
# 3. define filters for algorithm
# 4. RUN algorithm 
# 
# 
# ----
# 
# 
# Outcome (example):
# 1. input: rows of dow shopped
# 2. output: 0,1,2,0,0,1,0

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



from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.tree import DecisionTreeClassifier, export_graphviz, plot_tree


# In[2]:


# importing the required function
from scipy.stats import chi2_contingency


# ### Load and view data 

# In[3]:


df = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3.csv")

# del df["HH"]
df.describe(include='all')


# In[4]:


# df.dtypes


# In[5]:


# use the corr function to display the correlation between all the features
data_corr = df.corr()
# data_corr


# # 1. WHAT DAY? -  New dataframe: grocery visits/day/week

# ### Is there a correlation between day (of week) and week?

# In[6]:


df_orders = df[['week', 'order_ID', 'store_name', 'storename_num', 'store_type', 'storetype_num','day', 'day_num', 'time', 'time_num', 'timestamp', 'times', 'dates', 'times_min', 'dates_days', 'order_amount', 'order_price']]
df_orders = df_orders.drop_duplicates()


# In[7]:


# Cross tabulation between DAY and WEEK
CrosstabResult=pd.crosstab(index=df_orders['week'],columns=df_orders['day'])


# In[8]:


CrosstabResult


# In[9]:


# Performing Chi-sq test
ChiSqResult = chi2_contingency(CrosstabResult)

# P-Value is the Probability of H0 being True
# If P-Value > 0.05 then only we Accept the assumption(H0)



# No correlations
# > Probably predictable, about the same days each week

# > Let's check even vs uneven weeks

# In[12]:


df = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3.csv")

df_orders = df[['week','order_ID', 'store_name', 'storename_num', 'store_type', 'storetype_num','day', 'day_num', 'time', 'time_num', 'timestamp', 'times', 'dates', 'times_min', 'dates_days', 'order_amount', 'order_price']]
df_orders = df_orders.drop_duplicates()


# In[13]:


#Let's try grouping per even and uneven weeks
df_orders['week'] = df_orders['week'].replace([1, 3, 5, 7], 1)
df_orders['week'] = df_orders['week'].replace([2, 4, 6, 8], 2)


# In[14]:


# Cross tabulation between DAY and WEEK
CrosstabResult=pd.crosstab(index=df_orders['week'],columns=df_orders['day'])
CrosstabResult


# In[15]:


# Performing Chi-sq test
ChiSqResult = chi2_contingency(CrosstabResult)

# P-Value is the Probability of H0 being True
# If P-Value > 0.05 then only we Accept the assumption(H0)



# Not significant!
# > Even weeks are not different from uneven weeks

# Are the first 4 weeks different from the last 4?

# In[16]:


df = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3.csv")

df_orders = df[['week','order_ID', 'store_name', 'storename_num', 'store_type', 'storetype_num','day', 'day_num', 'time', 'time_num', 'timestamp', 'times', 'dates', 'times_min', 'dates_days', 'order_amount', 'order_price']]
df_orders = df_orders.drop_duplicates()


# In[17]:


# group per period 1 and 2
df_orders['week'] = df_orders['week'].replace([1, 2, 3, 4], 1)
df_orders['week'] = df_orders['week'].replace([5, 6, 7, 8], 2)


# In[18]:


# Cross tabulation between DAY and WEEK
CrosstabResult=pd.crosstab(index=df_orders['week'],columns=df_orders['day'])
CrosstabResult


# In[19]:


# Performing Chi-sq test
ChiSqResult = chi2_contingency(CrosstabResult)

# P-Value is the Probability of H0 being True
# If P-Value > 0.05 then only we Accept the assumption(H0)



# The first period is NOT significantly different from the second period!

# ## 2. Build Algorithm to 'randomize' shopping days

# #### Grid for dow/week & descriptions

# In[20]:


df = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH3\df\df_HH3.csv")


# In[21]:


days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df['day'] = pd.Categorical(df['day'], categories=days, ordered=True)
df_dow = df.sort_values(by=['week','day'])

# grouping the variables for week, day and unique order id's
df_dow = df.groupby(['week', 'day'])['order_ID'].nunique()
df_dow = pd.DataFrame (df_dow)
df_dow.head()


# In[22]:


days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df['day'] = pd.Categorical(df['day'], categories=days, ordered=True)
df_dow = df.sort_values(by=['week','day'])

# grouping the variables for week, day and unique order id's
df_dow = df.groupby(['week', 'day'])['order_ID'].nunique()
df_dow = pd.DataFrame (df_dow)
df_dow.head()

# make grid for days vs. week
df_dowgrid1 = df_dow.groupby(['week', 'day'])['order_ID'].aggregate('first').unstack()
df_dowgrid1 = df_dowgrid1.reset_index()
df_dowgrid1.replace(0, np.nan, inplace=True)
df_dowgrid1

# second grid to generate extra variables
df_dowgrid2 = df_dowgrid1.copy()
del df_dowgrid2["week"]
# column for total grocery visits
df_dowgrid1['sum'] = df_dowgrid2.sum(axis=1)
# column for total days shopped
df_dowgrid1['ndays'] = df_dowgrid2.count(axis=1)
# column for median visits/week
df_dowgrid1['med'] = df_dowgrid2.median(numeric_only=True, axis=1)

df_dowgrid1 = df_dowgrid1.round(0)
del df_dowgrid1["week"]


# In[23]:


df_dowgrid1


# #### Generate randomized weeks

# In[24]:


def period():
    # split up df to first and second period
    df_period = df_dowgrid1

    df_period = df_period. replace(np. nan,0)
    
    return df_period


# In[25]:


period()


# In[26]:


# df_period.to_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH4\df\df_HH4_period1.csv", index = None, header=True)


# # CONCLUSION

# Data to build the algorithm:
# >  2. Number of visits per day (per week)
#     1. Assign weights to each day (based on times shopped on these days)
#     
#     
# We then have the first given:
# > 1. Week 9: HH2 will shop on <b>Monday/Tuesday/..., X times</b>
