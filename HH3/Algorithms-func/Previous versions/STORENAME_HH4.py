#!/usr/bin/env python
# coding: utf-8

# ## 3: CORRELATIONS -WHERE WILL THEY SHOP?

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


df = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH4\df\df_HH4.csv")

# del df["HH"]
# df.describe(include='all')


# In[4]:


# use the corr function to display the correlation between all the features
data_corr = df.corr()
# data_corr


# In[5]:


# df_count = df[['order_ID','store_name', 'day']]
# df_count = df_count.drop_duplicates()
# df_count = df_count.drop(columns=['order_ID'])
# df_count.head()


# -
# # 1. Where?

# ## ALL ORDERS

# ### check correlation per store TYPE

# In[6]:


df_orders = df[['order_ID', 'store_name', 'storename_num', 'store_type', 'storetype_num','day', 'day_num', 'time', 'time_num', 'timestamp', 'times', 'dates', 'times_min', 'dates_days', 'order_amount', 'order_price']]
df_orders = df_orders.drop_duplicates()


# In[7]:


# Cross tabulation between DAY and STORE TYPE
CrosstabResult=pd.crosstab(index=df_orders['store_type'],columns=df_orders['day'])
CrosstabResult


# In[8]:


# Performing Chi-sq test
ChiSqResult = chi2_contingency(CrosstabResult)

# P-Value is the Probability of H0 being True
# If P-Value > 0.05 then only we Accept the assumption(H0)

print('The P-Value of the ChiSq Test is:', ChiSqResult[1])


# Not significant, let's get more specific:

# ### check correlation per store NAME

# In[9]:


# Cross tabulation between DAY and STORE NAME
CrosstabResult=pd.crosstab(index=df_orders['store_name'],columns=df_orders['day'])
CrosstabResult


# In[10]:


# Performing Chi-sq test
ChiSqResult = chi2_contingency(CrosstabResult)

# P-Value is the Probability of H0 being True
# If P-Value > 0.05 then only we Accept the assumption(H0)

print('The P-Value of the ChiSq Test is:', ChiSqResult[1])


# Not significant..

# ### check correlation per TIME

# In[9]:


# Cross tabulation between DAY and STORE NAME
CrosstabResult=pd.crosstab(index=df_orders['store_name'],columns=df_orders['time'])
CrosstabResult


# In[10]:


# Performing Chi-sq test
ChiSqResult = chi2_contingency(CrosstabResult)

# P-Value is the Probability of H0 being True
# If P-Value > 0.05 then only we Accept the assumption(H0)

print('The P-Value of the ChiSq Test is:', ChiSqResult[1])


# In[11]:


# Cross tabulation between DAY and STORE NAME
CrosstabResult=pd.crosstab(index=df_orders['store_type'],columns=df_orders['time'])
CrosstabResult


# In[12]:


# Performing Chi-sq test
ChiSqResult = chi2_contingency(CrosstabResult)

# P-Value is the Probability of H0 being True
# If P-Value > 0.05 then only we Accept the assumption(H0)

print('The P-Value of the ChiSq Test is:', ChiSqResult[1])


# Significant!
# > Once we know the time, we can derive the store type or vice-versa

# ### check correlation per TIME (continuous)

# In[27]:


# f_oneway() function takes the group data as input and 
# returns F-statistic and P-value
from scipy.stats import f_oneway
 
# Assumption(H0) is that day and times are NOT correlated
 
# Finds out the Prices data for each FuelType as a list
CategoryGroupLists=df_orders.groupby('store_type')['times_min'].apply(list)
 
# Performing the ANOVA test
# We reject the Assumption(H0) only when P-Value < 0.05
AnovaResults = f_oneway(*CategoryGroupLists)
print('P-Value for Anova is: ', AnovaResults[1])

figure(figsize=(15, 2), dpi=80)
plt.xticks(rotation=45, ha='right')

sns.scatterplot(data=df_orders, x='times_min', y='store_type')

# get the Pearson correlation between both variables
current_corr = round(AnovaResults[1], 2)

# give the graph a title and labels
plt.title(f"The Anova P-value between day & time = (r={current_corr})")

# call the graph (show function)
plt.grid(False)
plt.show()


# In[28]:


# f_oneway() function takes the group data as input and 
# returns F-statistic and P-value
from scipy.stats import f_oneway
 
# Assumption(H0) is that day and times are NOT correlated
 
# Finds out the Prices data for each FuelType as a list
CategoryGroupLists=df_orders.groupby('store_name')['times_min'].apply(list)
 
# Performing the ANOVA test
# We reject the Assumption(H0) only when P-Value < 0.05
AnovaResults = f_oneway(*CategoryGroupLists)
print('P-Value for Anova is: ', AnovaResults[1])

figure(figsize=(15, 2), dpi=80)
plt.xticks(rotation=45, ha='right')

sns.scatterplot(data=df_orders, x='times_min', y='store_name')

# get the Pearson correlation between both variables
current_corr = round(AnovaResults[1], 2)

# give the graph a title and labels
plt.title(f"The Anova P-value between day & time = (r={current_corr})")

# call the graph (show function)
plt.grid(False)
plt.show()


# # 1.3 New Dataframes to 'randomize' stores (weighted)

# In[13]:


df = pd.read_csv (r"C:\Users\20204113\OneDrive - TU Eindhoven\2_Research\1_Groceries\DATA\9th week - narrative (3rd attempt)\HH4\df\df_HH4.csv")


# In[16]:


stores = ['MCD', 'De Pers', 'Albert Heijn']
df['store_name'] = pd.Categorical(df['store_name'], categories=stores, ordered=True)
df_storename = df.sort_values(by=['week','store_name'])

# grouping the variables for week, store and unique order id's
df_storename = df.groupby(['week', 'store_name'])['order_ID'].nunique()
df_storename = pd.DataFrame (df_storename)
df_storename.head()

# make grid for stores vs. week
df_storename1 = df_storename.groupby(['week', 'store_name'])['order_ID'].aggregate('first').unstack()
df_storename1 = df_storename1.reset_index()
df_storename1.replace(0, np.nan, inplace=True)
df_storename1

# second grid to generate extra variables
df_storename2 = df_storename1.copy()
del df_storename2["week"]
# column for total grocery visits
df_storename1['sum'] = df_storename2.sum(axis=1)
# column for total days shopped
df_storename1['ndays'] = df_storename2.count(axis=1)
# column for median visits/week
df_storename1['med'] = df_storename2.median(numeric_only=True, axis=1)

df_storename1 = df_storename1.round(0)
del df_storename1["week"]


# In[18]:


df_storename1


# #### Generate randomized weeks

# In[19]:


def storename():
    # split up df to first and second period
    df_storename = df_storename1

    df_storename = df_storename. replace(np. nan,0)
    
    return df_storename


# In[20]:


storename()

