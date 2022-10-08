# -*- coding: utf-8 -*-
"""
Created on Sun May 15 10:00:07 2022

@author: elbia
"""

import mysql.connector as sql
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

#3 paths for 3 analysis results. These Excel files are the Tableau Input
path1 = "C:/Users/elbia/Desktop/Estudios/data analytics/Case_1_Cyclist/analysis1.xlsx"
path2 = "C:/Users/elbia/Desktop/Estudios/data analytics/Case_1_Cyclist/analysis2.xlsx"
path3 = "C:/Users/elbia/Desktop/Estudios/data analytics/Case_1_Cyclist/analysis3.xlsx"


AVG_1=[]
Day_1=[]
AVG_2=[]
Day_2=[]


#SQL connnection and query
cnx = sql.connect(user='root', password='zxc123',
                              host='localhost',
                              database='case_1_cyclistic')


query = ("SELECT * " 
         "FROM cyclistic " 
         "WHERE started_at IS NOT NULL " 
#         "LIMIT 10000"
         ) 

df = pd.read_sql(query, cnx)


cnx.close()
#I close the connection once I get all the data required into a DataFrame


""" CSV entry if required 
#pathDB = "C:/Users/elbia/Desktop/Estudios/data analytics/Case_1_Cyclist/DB/202204-divvy-tripdata.csv"
#df = pd.read_csv(pathDB)
"""

#Transform the date into datetime format
df["ended_at"] = pd.to_datetime(df["ended_at"])
df["started_at"] = pd.to_datetime(df["started_at"])

#Obtain ride length
df["ride_length"] = df["ended_at"] - df["started_at"]


#Obtain the weekday: 0 -> Monday; 6 -> Sunday
df["weekday"] = df["started_at"].dt.weekday

#Create a DF with these columns
dfweekday = df[["started_at","weekday"]]

#Separate casual and member riders
dfcasual = df[df.member_casual == "casual"]
dfmember = df[df.member_casual == "member"]


#Pivot Tables for get amount of riders per type of rider
casualpivot = dfcasual.pivot_table(columns=['weekday'], aggfunc='size')
memberpivot = dfmember.pivot_table(columns=['weekday'], aggfunc='size')

#Conver to dataframe
casualpivot = casualpivot.to_frame()
memberpivot = memberpivot.to_frame()


#AVG per day
for i in range(0,7):
    dfcasualrange = dfcasual[dfcasual.weekday == i] #filter the casual DF by day of the week
    internalvar1 = dfcasualrange["ride_length"].mean() #obtain mean of length ride
    internalvar2 = internalvar1.total_seconds() #transform into total seconds
    AVG_1.append(internalvar2) #append to list
    Day_1.append(dfcasualrange.duplicated(["weekday"]).sum()) #append the sum of data points
    dfmemberrange = dfmember[dfmember.weekday == i] #same process for annual members
    internalvar3 = dfmemberrange["ride_length"].mean()
    internalvar4 = internalvar3.total_seconds()    
    AVG_2.append(internalvar4)
    Day_2.append(dfmemberrange.duplicated(["weekday"]).sum())


#Create dictionaries with the lists of averages and day 
#Casual and members % between days
dic = {"average":AVG_1,"day":Day_1}
dfanalysis1 = pd.DataFrame(dic,columns=["average","day"])
dic2 = {"average":AVG_2,"day":Day_2}
dfanalysis2 = pd.DataFrame(dic2,columns=["average","day"])

#Create dictionaries with the lists of both averages
#Average travel time per day
dic3 = {"Casual Riders":AVG_1,"Member Riders":AVG_2}
dfanalysis3 = pd.DataFrame(dic3,columns=["Casual Riders","Member Riders"])


#concat for casual and member average per day DF
dftemp = [dfanalysis1, dfanalysis2]
dfanalysisconcat = pd.concat(dftemp)

temppivot = [casualpivot,memberpivot]
concatpivot = pd.concat(temppivot)

#list of casual and members to add to both analysis results to be able to discern rider types
templist=["casual","casual","casual","casual","casual","casual","casual",
          "member","member","member","member","member","member","member"]
dfanalysisconcat["member_type"] = templist
concatpivot["member_type"] = templist


dfanalysis3.to_excel(path1) #Average travel time per day
dfanalysisconcat.to_excel(path2) #Casual and members % between days
concatpivot.to_excel(path3) #Amounts of travels registered

"""Graphs for a fast analysis
dfanalysis3.plot(kind='bar', 
                 title='Average per day',
                 xlabel=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
# Turn on the grid
plt.minorticks_on()
plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

plt.show()




fig, (ax1,ax2) = plt.subplots(1,2,figsize=(15,5)) #ax1,ax2 refer to your two pies
# 1,2 denotes 1 row, 2 columns - if you want to stack vertically, it would be 2,1

ax1.pie(dfanalysis1["day"],
        labels=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
        autopct='%.2f')
ax1.set_title('Casual Riders')


ax2.pie(dfanalysis2["day"],
        labels=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
        autopct='%.2f')
ax2.set_title("Member Riders")

plt.show()
"""







