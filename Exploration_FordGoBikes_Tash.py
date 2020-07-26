#!/usr/bin/env python
# coding: utf-8

# # Analyzing Ford GoBikes System Data¶
# ## By Tash Bettridge 
# 
# ## Preliminary Wrangling
# 
# >Formerly known as Ford GoBike, renamed Lyft Bikes is a regional public bicycle sharing system in the San Francisco Bay Area, California.
# 
# ### Data
# 
# The data will be analysed from the following:
# 
# * 2019 FordGo Bike and Baywheels Tripdata
# 
# ### Process
# 
# The data wrangling steps that were involved in this project were:
# - Step 1. Assessing the Data 
# - Step 2. Preliminary Wrangling
# - Step 3. Cleaning data
# - Step 4. Univariate Exploration
# - Step 5. Multivariate Exploration
# 
# 

# ### Step 1. Assessing the Data 
# 
# Data Analysis, storing data and data visualization of the wrangled data
# 

# In[1]:


# import all packages and set plots to be embedded inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import glob
import os
import datetime
import matplotlib.ticker as tick
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


#Retrieve the datasets from the User directory 
path = r'C:\Users\tash_\Desktop\Udacity\dataset'


# In[3]:


# detect all of the files ending with a .csv name within a specific working directory
files = glob.glob(os.path.join(path, "*.csv"))


# In[4]:


#use the pd.concat() method to stack every dataframe one on top of another.
df = pd.concat((pd.read_csv(f) for f in files), ignore_index = False)


# In[5]:


#Save a Copy To Master File
df.to_csv('baywheels_master.csv', index = False)


# ### Step 2. Preliminary Wrangling

# In[6]:


# Read contents of Master File
df = pd.read_csv('baywheels_master.csv')


# In[7]:


# Showing the first five rows of the newly combined dataset
df.describe()


# In[8]:


#Retrieve the first 10 samples of the data
df.sample(10)


# In[9]:


df.info(null_counts = True)


# In[10]:


df.isnull().sum()


# In[11]:


# Check dataset for duplicated data
df.duplicated().sum()


# In[12]:


#check for NaN data types
df.isna().sum()


# ### Step 3. Cleaning Data 
# There are some missing values in the dataset, such as start_station_id, start_station_name, end_station_id, end_station_name, rental_access_method. For more information please see below:
# 
# * Start/end times are not in the timestamp format
# 
# #### The following columns are not in object format:
# * start_station_id
# * end_station_id
# * bike_id
# * user_type
# * rental_access_method
# 
# ### Quality 
# 
# > There are some missing values and this will be sorted by converting some of the columns to the appropriate data types.
# 

# In[13]:


# Save the original data set and create a copy 
df_cleaned = df.copy()


# ### Define
# Converting columns to the appropriate data types:
# * Start_time and end_time to the timestamp format
# * User type and rental_access_method for all to category format
# * Bike ID, start station ID, and end station ID to object format
# 

# ### Code 

# In[14]:


# Converting the format to datetime
df_cleaned.start_time = pd.to_datetime(df_cleaned.start_time)
df_cleaned.end_time = pd.to_datetime(df_cleaned.end_time)


# In[15]:


# Converting the user_type and rental_access_method to category format
df_cleaned.user_type = df_cleaned.user_type.astype('category')
df_cleaned.rental_access_method = df_cleaned.rental_access_method.astype('category')


# In[16]:


# Convertng the bike_id, start_station_id, and end_station_id to object
df_cleaned.bike_id = df_cleaned.bike_id.astype(str)
df_cleaned.start_station_id = df_cleaned.start_station_id.astype(str)
df_cleaned.end_station_id = df_cleaned.end_station_id.astype(str)


# ### Test

# In[17]:


df_cleaned.info(null_counts = True)


# ### Define
# > Add columns for the start month, day of the week, and hour, along with figuring out the trip duration in minutes so I can create visuals based on workable units

# ### Code 

# In[18]:


# Start time month (January - December)
df_cleaned['start_time_month'] = df_cleaned['start_time'].dt.strftime('%B')


# In[19]:


# Start time month (1-12)
df_cleaned['start_time_month_num'] = df_cleaned['start_time'].dt.month.astype(int)


# In[20]:


# Start time weekday
df_cleaned['start_time_weekday'] = df_cleaned['start_time'].dt.strftime('%a')


# In[21]:


# Start and end time hour
df_cleaned['start_time_hour'] = df_cleaned['start_time'].dt.hour
df_cleaned['end_time_hour'] = df_cleaned['end_time'].dt.hour


# In[22]:


# Duration in seconds to duration in minutes
df_cleaned['duration_min'] = df_cleaned['duration_sec']/60
df_cleaned['duration_min'] = df_cleaned['duration_min'].astype(int)


# ### Test 

# In[23]:


df_cleaned.sample(3)


# ### Define
# 
# >Calculate the total distance traveled using the latitude and longitude in the data set

# ### Code

# In[24]:


import math
from math import radians, sin, cos, acos

def distance(origin, destination):

    lat1, long1 = origin
    lat2, long2 = destination
    radius = 6371 # this is in kms

    dlat = math.radians(lat2 - lat1)
    dlong = math.radians(long2 - long1)
    
    x = (math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlong / 2) * math.sin(dlong / 2))
    y = 2 * math.atan2(math.sqrt(x), math.sqrt(1 - x))
    z = radius * y

    return z


# In[25]:


# Using the calcuated math on the columns for latidue and longitude
df_cleaned['distance_km'] = df_cleaned.apply(lambda x: distance((x['start_station_latitude'], x['start_station_longitude']), (x['end_station_latitude'], x['end_station_longitude'])), axis=1)


# In[26]:


# Converting the kilometers to miles
df_cleaned['distance_miles'] = df_cleaned['distance_km'] * 0.621371


# ### Test

# In[27]:


df_cleaned.sample(5)


# ### Store Data

# In[28]:


df_cleaned.to_csv('baywheels_master_clean.csv', index = False)


# ### What is the structure of your dataset?
# 
# The FordGoBike and BayWheels Datasets provide a valuable collection of data to work with in order draw data findings and a conclusion. This notebook uses data collected from January 2019 which the organisation was still using the naming structure FordGoBike until May 2019 and then changed its naming structure December 2019. There have been some anomity changes in the dataset and can no longer be distinguish by gender. 
# 
# 
# > The dataset has 25000+ bike rides that had happened in 2019. 
# 
# ### The dataset contained features about:
# 
# * trip duration
# * start time/end time
# * stations: start/end station, name, geolocation (latitude/longitude)
# * anonymized customer data: The users are divided into two user types: Subscriber and Customer
# * rented bikes: bike_id 
# 
# 
# ### The following columns that were added in the data cleaning phase:
# 
# 
# * Start Time Month
# * Start Time Month Number
# * Start Time Day of the Week
# * Start Time Hour
# * Distance (km)
# * Distance (miles)
#   
# 
# ### What is/are the main feature(s) of interest in your dataset?
# 
# > I am interested in investigate the main features which include data that is related to the start time and end time of a ride. 
# 
# ### What features in the dataset do you think will help support your investigation into your feature(s) of interest?
# 
# > The features in the dataset that I think will ehance my investigation would be looking at the start times and end times as well as any related time-based information. 

# ## Step 4. Univariate Exploration
# 
# > In this section, investigate distributions of individual variables. If
# you see unusual points or outliers, take a deeper look to clean things up
# and prepare yourself to look at relationships between variables.

# In[28]:


#have a look at the dataset 
df_cleaned.start_time_month.describe()


# In[29]:


sin_color = sb.color_palette()[0]


# In[30]:


#Display monthly Ford Go Bike sharing system
graph = sb.catplot(data = df_cleaned, x = 'start_time_month', 
                   kind = 'count', color = sin_color, aspect = 1.8);
graph.set_axis_labels('Month', 'Number of Bike Trips'),
graph.fig.suptitle('Usage by Month',
                   y = 1.07, fontsize = 16, fontweight = 'bold');
graph.set_xticklabels(rotation=80)


# ### Observation 1:  Usage by Month
# 
# > In the Bay Area, July which is in Summer in the Northen Hemispher is the most popular time to use the Ford Go Bike sharing system. March is also the second most popular time to use the Ford Go Bike sharing system in the Bay Area. 
# 
# >While December which is Winter time in the Northern Hemisphere, is the least popular time to use the Ford Go Bike Sharing System. Therefore, there will be more bikes available due to the usuage of bikes not been used around the Christmas Holidays. 

# In[31]:


# Weekly usage of the Ford Go bike sharing system
weekday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
graph = sb.catplot(data=df_cleaned, x='start_time_weekday', 
                   kind='count', color = sin_color, order = weekday)
graph.set_axis_labels('Weekdays', 'Number of Bike Trips')
graph.fig.suptitle('Usage by Day of the Week ',
                   y=1.07, fontsize=16, fontweight='bold');
graph.set_xticklabels(rotation=80);


# ### Observation 2:  Usage by Month
# 
# In 2019, Monday through Friday has heavy usage in hiring bikes from the Ford Go Bike sharing system in the Bay Area. 
# The usage drops significantly on the weekend where Saturday and Sunday. The data suggests that the Ford Go Bike sharing system is mainly used during the week. 

# In[32]:


#Hourly usage of the Ford Go bike sharing system
graph = sb.catplot(data = df_cleaned, x='start_time_hour', 
                   kind='count', color = sin_color, aspect = 1.7)
graph.set_axis_labels('Hours', 'Number of Bike Rides')
graph.fig.suptitle('Usage by Hour', y=1.07, fontsize=16, fontweight='bold');
graph.set_xticklabels(rotation=80);


# ### Observation 3: Usage by Hour 
# 
# > In 2019, the most popular times to ride bikes would during 0700-0900 and from 1600-1900. 
# The highest usage time was at 0800 in the morning and at 1700 in the afternoon. 
# The least used time of the bikes was at 0300. 

# In[33]:


#Convert duration to minutes instead of seconds 
df_cleaned['duration_min'] = df_cleaned['duration_sec']/60
df_cleaned.info()


# In[34]:


#finding the distribution 
df_cleaned.duration_min.describe()


# In[35]:


#Display the FordGoBike Trip Duration in Seconds 
bin_edges = np.arange(0, 4000, 70)
plt.hist(data = df_cleaned, x = 'duration_sec', bins = bin_edges);
plt.title("Trip Duration in Seconds", 
          y=1.07, fontsize=16, fontweight='bold')
plt.xlabel('Duration in Seconds')
plt.ylabel('Number of Bike Trips');
graph.set_xticklabels(rotation=80);


# In[36]:


#Finding the distribution
df_cleaned.duration_min.describe(percentiles = [.95])
df_cleaned.duration_min.describe()


# In[37]:


#Find out the average trip
df_cleaned.duration_min.mean()


# In[38]:


# Display the duration bike rides in minutes 
bin_edges = np.arange(0, 45, 1)
ticks = [0, 5, 10, 15, 20, 25, 30,  35, 40, 45]
labels = ['{}'.format(val) for val in ticks]
plt.hist(data = df_cleaned, x = 'duration_min', 
         bins = bin_edges, rwidth = 0.6);
plt.title("Trip Duration in Minutes", y=1.05, 
          fontsize=16, fontweight='bold')
plt.xlabel('Duration in Minutes')
plt.xticks(ticks, labels)
plt.ylabel('Number of Bike Trips');
graph.set_xticklabels(rotation=80);


# ### Observation 4: Duration of Bike Trips
# 
# > In 2019, the average duration of bike trips was under 13.46 minutes. 
# 

# In[39]:


df_cleaned.distance_miles.describe()


# In[40]:


df_cleaned.distance_miles.mean()


# In[41]:


bin_edges = np.arange(0, 5, 1)
plt.hist(data = df_cleaned, x = 'distance_miles',
         bins = bin_edges);
plt.title("Trip Distance in Miles", y=1.07, 
          fontsize=16, fontweight='bold')
plt.xlabel('Distance in Miles')
plt.ylabel('Number of Bike Trips');
graph.set_xticklabels(rotation=80);


# ### Observation 5: Distance in Miles 
# > In 2019, the mean of the distance traveled in miles was at 1.347 miles. 
# 

# In[42]:


# Plotting start station id distribution.
bin_edges = np.arange(0, 45, 1)
ticks = [0, 5, 10, 15, 20, 25, 30,  35, 40, 45]
labels = ['{}'.format(val) for val in ticks]
plt.hist(data = df_cleaned, x = 'start_station_id', 
         bins = bin_edges, rwidth = 0.6);
plt.title("Distribution of Start Stations", y=1.05, 
          fontsize=16, fontweight='bold')
plt.xlabel('Start Station')
plt.xticks(ticks, labels)
plt.ylabel('Number of Stations');
graph.set_xticklabels(rotation=80);


     


# In[43]:


# Plotting end station id distribution.
bin_edges = np.arange(0, 45, 1)
ticks = [0, 5, 10, 15, 20, 25, 30,  35, 40, 45]
labels = ['{}'.format(val) for val in ticks]
plt.hist(data = df_cleaned, x = 'end_station_id', 
         bins = bin_edges, rwidth = 0.6);
plt.title("Distribution of End Stations", y=1.05, 
          fontsize=16, fontweight='bold')
plt.xlabel('End Station')
plt.xticks(ticks, labels)
plt.ylabel('Number of Stations');
graph.set_xticklabels(rotation=80);


# ### Observation 6: Distribution of Start and End Stations
# 
# > In 2019, through observing the Start and End station usages. The same stations usage is more frequent as start stations and end stations. 
# 

# ### Talk about some of the relationships you observed in this part of the investigation. How did the feature(s) of interest vary with other features in the dataset?
# 
# > There were six observations that were made with the duration of the bike ride data. As the data was cleaned, through the data cleaning phase. The data visualisation of the duration of the bike ride and the distance helped to form a story. The trip duration takes a large amount of values and is concentrated.
# 
# 
# ### Did you observe any interesting relationships between the other features (not the main feature(s) of interest)?
# 
# > Looking at the cleaned dataset, in Observation 6: start station and end station which is plotted to do a comparison of bike sharers frequency in start and end station. 
# 

# ## Bivariate Exploration
# 
# > In this section, I investigate relationships between pairs of variables in the data.

# In[45]:


# Clean the User Type data for data visualisation
customer = df_cleaned.query('user_type == "Customer"')['bike_id'].count()
subscriber = df_cleaned.query('user_type == "Subscriber"')['bike_id'].count()
customer_prop = customer / df_cleaned['bike_id'].count()
subscriber_prop = subscriber / df_cleaned['bike_id'].count()


# In[46]:


# Plot a pie chart to compare the percentage of Customers vs Subscribers that are using the platform
plt.figure(figsize = [10, 5])
labels = ['Customer', 'Subscriber']
size = [customer_prop, subscriber_prop]
explode = (0, 0.3)
plt.pie(size, explode=explode, labels = labels, autopct='%1.1f%%', 
        shadow=True, startangle=90, textprops={'color':'white'})
plt.axis('equal')
plt.suptitle('Customers vs. Subscribers in Ford GoBikes Sharing', y=1.07,
             fontsize=16, fontweight='bold');


# ### Observation 1: Customers vs. Subscribers in Ford GoBikes Sharing
# 
# > In 2019, 80.6% of the user types in the Ford GoBikes sharing platform were Subscribers. 19.4% of the user types in the Ford GoBikes Sharing Platform were Customers. 
# 
# 

# In[47]:


# Plot Number of Custoners vs Subscribers in the Ford GoBike Sharing app. 
plt.figure(figsize = [10, 5])
graph = sb.countplot(data = df_cleaned, x = "user_type", 
                     order = df_cleaned.user_type.value_counts().index);
graph.set_xlabel('User Type');
graph.set_ylabel('Number of Bike Trips');
plt.suptitle('Customers vs. Subscribers in Ford GoBike Sharing System', 
             y=1.07, fontsize=16, fontweight='bold');


# ### Observation 2: Customers vs. Subscribers Usage in Ford GoBikes Sharing
# 
# > There are more than 200,000 Subscribers as displayed in the Customers vs. Subscribers in Ford GoBike Sharing System chart.

# In[48]:


# Plot comparison of usage between Customers vs Subscribersin 2019
plt.figure(figsize = [12, 5])
graph = sb.catplot(data=df_cleaned, x='start_time_month', 
                   col="user_type", kind='count', sharey = True, color = sin_color);
graph.set_axis_labels("Month", "Number of Bike Trips");
graph.set_titles("{col_name}");
graph.fig.suptitle('Customers vs. Subscribers in Ford GoBike Sharing System',
                   y=1.07, fontsize=16, fontweight='bold');
graph.set_xticklabels(rotation=80);


# ### Observation 3: Customers vs. Subscribers Usage in Ford GoBikes Sharing
# 
# > There are more than 200,000 Subscribers as displayed in the Customers vs. Subscribers in Ford GoBike Sharing System chart. 
# 
# Customers: The demand is high during December. However, the frequency is high betwen the months of July - October 2019.
# 
# Subscribers: The demand is highest in March 2019. THis is followed by July 2019 which is Summer time in the Bay Area and April which is Spring. 
# 
# 
# 

# In[50]:


plt.figure(figsize=(12, 5))
df_cleaned_user_week = df_cleaned.groupby(['start_time_weekday', 'user_type']).size().reset_index()
weekday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
ax = sb.pointplot(data=df_cleaned_user_week, x='start_time_weekday', 
                  y=0, hue = 'user_type', scale=.7, order = weekday);
plt.title('Customer vs. Subscribers Trends in the Ford GoBike Sharing', y=1.07, fontsize=16, fontweight='bold')
plt.xlabel('Weekdays')
plt.ylabel('Number of Bike Trips');
plt.grid()


# ### Observation 4: Customers vs. Subscribers Trends in the Ford GoBikes Sharing
#  
# In 2019, customers usage is quite low and consistant staying under 10,000 bike trips during the week. While Subscribers frequently used the the Ford GoBikes Sharing platform during Monday - Thursday with a drop of the number of bike trips on Friday and a significant drop through to Saturday and Sunday. 
# 

# ### Talk about some of the relationships you observed in this part of the investigation. How did the feature(s) of interest vary with other features in the dataset?
# 
# > The importance of including the user type to the data analysis revealed that there were some differences in the behaviour of the customers and subscribers using the Ford GoBikes Sharing platform. 
# 
# > The dataset highlights the usage trends between customers and subscribers. This suggests that Customers are casual users and the Subscribers are daily commuters that maybe working, studying etc. 
# 
# 
# ### Did you observe any interesting relationships between the other features (not the main feature(s) of interest)?
# 
# > Through Observation, there is a difference in usage between customers and subscribers. The popularity of using Ford GoBikes for Customers is usually in December and increases more on Saturday as opposed to Subscribers where it decreases significantly on Saturday and during the weekend. 
# > There were some limitations in this analysis, due to the anomity of customer data shighuch as gender. 

# ## Step 5. Multivariate Exploration
# 
# > In this section, I will clean the data further in order to investigate the duration of the Ford Go Bike data.
# 

# In[60]:


# Number of bike trips Customers vs. Subscriber Usage by Duration

plt.figure(figsize = [8, 5])
base_color = sb.color_palette()[1]
sb.boxplot(data = df, x = 'user_type', y = 'duration_sec', color = base_color)
plt.title('Customer vs. Subscribers Duration in Seconds', y=1.07, fontsize=16, fontweight='bold')
plt.xlabel('User Type')
plt.ylabel('Duration in sec')
plt.show()


# ### Obserevation 1:  Customers vs. Subscribers Ride Duration in Seconds
# 
# > In 2019, the graph above highlights that the values are vey widespread to see a box plot. In the next observation, will have a look at the box plot with the duration in minutes as opposed to seconds. 
# 

# In[61]:


data = df_cleaned.query('duration_min < 30')
x = sb.catplot(data=data, y='duration_min', 
               col="user_type", kind='box', color = sin_color)
x.set_titles(col_template = '{col_name}')
x.set_axis_labels("", "Duration in Minutes")
x.fig.suptitle('Duration in Minutes by User Type',
               y=1.05, fontsize=16, fontweight='bold');


# ### Obserevation 2:  Duration in Minutes by User Type 
# 
# > The Duration in Minutes by User Type plot highlights that Customers normally have longer trip durations. Customers normally ride between 8 minutes and 18 minutes. Subscriber trips are normally shorter and last anywhere between 5-13 minutes. 
# 

# ### Talk about some of the relationships you observed in this part of the investigation. Were there features that strengthened each other in terms of looking at your feature(s) of interest?
# 
# > Through further observation between Customer and Supplier behaviours, The Duration changes whether if it is noted down in seconds vs minutes.  
# ### Were there any interesting or surprising interactions between features?
# 
# > Through observation of the plot box if looking at Customer and Supplier duration in seconds. The box plot graph highlights that the values are vey widespread to see a box plot. By amending the duration from seconds to Minutes by the User Type highlights that Customers normally have longer trip durations. Customers normally ride between 8-18 minutes. Subscriber trips are normally shorter and last anywhere between 5-13 minutes
# 
# 

# # References
# 
# 1. How To Combine Multiple CSV Files In Python: https://sempioneer.com/python-for-seo/how-to-combine-multiple-csv-files-in-python/
# 2. FordGoBike Data Set: https://www.lyft.com/bikes/bay-wheels/system-data
# 3. Github: https://github.com/ijdev/Ford-GoBike-System-Data---Data-Analysis/blob/master/exploration_template.ipynb
# 4. Keggle: https://www.kaggle.com/chirag02/ford-gobike-data-analysis
# 5. seaborn catplot: https://seaborn.pydata.org/generated/seaborn.catplot.html
# 6. matplotlib Documentation: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.hist.html
# 
