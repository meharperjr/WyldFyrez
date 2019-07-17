#!/usr/bin/env python
# coding: utf-8

# # Team WyldFyrez
# ## Relation to fire and weather data
# 
# blah blah blah stuff

# In[3]:


#import dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[15]:


#requesting csv and reading in file
fire_csv = "Resources/fire_init.csv"

df_fire = pd.read_csv(fire_csv, low_memory=False, dtype={'STAT_CAUSE_DESCR': str,'State': str, 
                                                         'CONT_DATE':str, 'Discovery_Date': str, 
                                                         'FIRE_SIZE':float,'LATITUDE': float,'LONGITUDE':float})

df_fire.head(10)


# In[16]:


#Cleaning Data frame to remove unused columns
df_sub = df_fire[['OBJECTID','STAT_CAUSE_DESCR', 'STATE','FIRE_YEAR', 'CONT_DATE', 'DISCOVERY_DATE', 'FIRE_SIZE', 'LATITUDE', 'LONGITUDE']]
df_sub.head()


# In[17]:


#Dropping data that does not have complete data
# this ultimately removed nearly everything from years 1992 through 2004
df_dropna = df_sub.dropna(how="any")
df_dropna.count()


# In[18]:


# converting date fields into lists to support date format clean up
date_contained = df_dropna.CONT_DATE.tolist()
date_discovery = df_dropna.DISCOVERY_DATE.tolist()


# In[19]:


# cleaning up start date field by stripping out the timestamp
date_disc = pd.Series(date_discovery)
#datedisc_df =pd.DataFrame(date_disc)
#d2 = pd.to_datetime(date_disc[0])

start = date_disc.str.split(pat = "T", expand=True)
start_df = pd.DataFrame(start)

start_clean = start_df.rename(columns={ 0: "Date Discovery",1: "Time"})
start_clean['Date Discovery'] = pd.to_datetime(start_clean['Date Discovery'])

start_clean.head()


# In[20]:


# cleaning up contained date field by stripping out the timestamp
date_cont = pd.Series(date_contained)
#dateend_df =pd.DataFrame(date_cont)
#d1 = pd.to_datetime(date_cont[0])


end = date_cont.str.split(pat = "T", expand=True)
end_df = pd.DataFrame(end)

end_clean = end_df.rename(columns={ 0 : "Date Contained", 1: "Time"})

end_clean['Date Contained'] = pd.to_datetime(end_clean['Date Contained'])
end_clean.head()


# In[21]:


# creating a duration value showing how long each fire was burning

#df_clean['duration'] = end_clean['Date Contained'] - start_clean['Date Discovery']
#df_clean

duration = pd.Series(delta.days for delta in (end_clean['Date Contained'] - start_clean['Date Discovery']))


# In[22]:


# concatinating the multiple dataframes we've created above into 1
df_concat = pd.concat([df_dropna, start_clean, end_clean, duration],axis =1)
df_concat.count()


# In[23]:


# renaming our duration column
df_concat = df_concat.rename(columns= {0:"Duration"})


# In[24]:


# dropping unused columns again
df_clean = df_concat[['OBJECTID','STAT_CAUSE_DESCR', 'STATE', 'Date Discovery', 'Date Contained', 'FIRE_SIZE', 'LATITUDE', 'LONGITUDE','Duration']]
df_clean.head()


# In[25]:


# checking our totals
df_clean.count()


# In[27]:


# write out a final, cleaned csv file for our data set to use in our graphs and charts workbook
df_dropcln.to_csv("fire_clean.csv")

