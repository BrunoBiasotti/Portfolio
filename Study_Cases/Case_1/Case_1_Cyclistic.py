# -*- coding: utf-8 -*-
"""
Created on Sun May 15 10:00:07 2022

@author: elbia
"""

import mysql.connector as sql
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

asd=[]
qwe=[]
asd2=[]
qwe2=[]

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



print(df)

df["ride_length"] = df["ended_at"] - df["started_at"]

print(df["ride_length"])

df["weekday"] = df["started_at"].dt.weekday

#0 Monday, 6 Sunday

print(df)

dfweekday = df[["started_at","weekday"]]
print(dfweekday)


dfcasual = df[df.member_casual == "casual\r"]
dfmember = df[df.member_casual == "member\r"]

print(dfcasual)
print(dfmember)

print(dfcasual["ride_length"].mean())
print(dfmember["ride_length"].mean())

print(dfcasual.pivot_table(columns=['weekday'], aggfunc='size'))
print(dfmember.pivot_table(columns=['weekday'], aggfunc='size'))

print("\n")

#media por día
for i in range(0,7):
    dfcasualrange = dfcasual[dfcasual.weekday == i]
    internalvar1 = dfcasualrange["ride_length"].mean()
    internalvar2 = internalvar1.total_seconds()
    asd.append(internalvar2)
    qwe.append(dfcasualrange.duplicated(["weekday"]).sum())
    dfmemberrange = dfmember[dfmember.weekday == i]
    internalvar3 = dfmemberrange["ride_length"].mean()
    internalvar4 = internalvar3.total_seconds()    
    asd2.append(internalvar4)
    qwe2.append(dfmemberrange.duplicated(["weekday"]).sum())




print("\n")
dic = {"average":asd,"day":qwe}
dfanalysis1 = pd.DataFrame(dic,columns=["average","day"])
print(dfanalysis1)

print("\n")
dic2 = {"average":asd2,"day":qwe2}
dfanalysis2 = pd.DataFrame(dic2,columns=["average","day"])
print(dfanalysis2)

print("\n")
dic3 = {"Casual Riders":asd,"Member Riders":asd2}
dfanalysis3 = pd.DataFrame(dic3,columns=["Casual Riders","Member Riders"])
print(dfanalysis3)



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









