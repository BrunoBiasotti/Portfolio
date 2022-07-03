# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 17:05:24 2022

@author: elbia
"""

import pandas as pd
import statistics
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

path = "C:/Users/elbia/Desktop/Estudios/data analytics/Case_2_Salaries/Case_2_Salaries.csv"

base_df = pd.read_csv(path)


"""Code to get the job list

temp = pd.DataFrame(base_df["Trabajo de"])

d = temp.groupby("Trabajo de").filter(lambda x: len(x) > 10)

c = d.groupby("Trabajo de").count()

print(c)
print(type(c))

Architect
BI Analyst / Data Analyst
Business Analyst
Consultant
DBA
Data Engineer
Data Scientist
Designer
Developer
HelpDesk
Infosec
Manager / Director
Middleware
Networking
Product Manager
Project Manager
QA / Tester
Recruiter / HR
Sales / Pre-Sales
Scrum Master
SysAdmin / DevOps / SRE
Technical Leader
UX
VP / C-Level
"""


""" General Insights

contratos = ["Full-Time",
             "Part-Time",
             "Freelance"
            ]
profesiones = ["Architect",
               "BI Analyst / Data Analyst",
               "Business Analyst",
               "Consultant",
               "DBA",
               "Data Engineer",
               "Data Scientist",
               "Designer",
               "Developer",
               "HelpDesk",
               "Infosec",
               "Manager / Director",
               "Middleware",
               "Networking",
               "Product Manager",
               "Project Manager",
               "QA / Tester",
               "Recruiter / HR",
               "Sales / Pre-Sales",
               "Scrum Master",
               "SysAdmin / DevOps / SRE",
               "Technical Leader",
               "UX",
               "VP / C-Level"
            ]



for cont in contratos:
    graph_mean = []
    graph_mode = []
    graph_max = []
    graph_min = []
    df_FT = pd.DataFrame(base_df.loc[base_df["Tipo de contrato"] == cont])
    for prof in profesiones:
        df_FT2 = pd.DataFrame(df_FT.loc[df_FT["Trabajo de"] == prof])
        df_FT_AVG = df_FT2["Salario mensual o retiro BRUTO (en tu moneda local)"]
        AVG_list = df_FT_AVG.values.tolist()
        AVG_list_clean = []
        
        for elem in AVG_list:
            try:
                AVG_list_clean.append(int(elem))
            except:
                pass
        

        
        AVG_list_sort = [v for v in AVG_list_clean if v > 10000]
        AVG_list_sort.sort(reverse=True)

#        print(len(AVG_list_clean)-len(AVG_list_sort))

        try:
            mean_FT = statistics.mean(AVG_list_sort)
        except:
            mean_FT = 0
        try:
            mode_FT = statistics.mode(AVG_list_sort)
        except:
            mode_FT = 0
        try:
            max_FT = AVG_list_sort[0]
        except:
            max_FT = 0
        try:
            min_FT = AVG_list_sort[-1]
        except:
            min_FT = 0
        
        graph_mean.append(mean_FT)
        graph_mode.append(mode_FT)
        graph_max.append(max_FT)
        graph_min.append(min_FT)
        
        
            
    print(graph_mean)
    print(graph_mode)
    print(graph_max)
    print(graph_min)


    
    
    fig_1 = plt.figure(figsize = (20,30))
    plt.barh(profesiones,graph_mean)
    plt.title(cont+": Mean by Profession")
    
    fig_2 = plt.figure(figsize = (20,30))
    plt.barh(profesiones,graph_mode)
    plt.title(cont+": Mode by Profession")
    
    fig_3 = plt.figure(figsize = (20,30))
    plt.barh(profesiones,graph_max)
    plt.title(cont+": Max by Profession")
    
    fig_4 = plt.figure(figsize = (20,30))
    plt.barh(profesiones,graph_min)
    plt.title(cont+": Min by Profession")
    
    plt.show()
    """
    


""" Code to get years

d = df_dev_exp.groupby(["Años en el puesto actual"]).size()
print(d) #get all the years of experience
print(type(d))

Años en el puesto actual DEV
0.0     695
0.5       2
1.0     417
1.2       1
1.3       4
1.5      20
2.0     308
2.5       2
3.0     144
4.0      83
5.0      65
6.0      25
7.0      29
8.0      15
9.0       6
10.0     31
11.0      7
12.0      7
13.0      7
14.0      2
15.0     10
16.0      1
17.0      1
18.0      3
20.0      6
22.0      1
23.0      1
24.0      1
25.0      2
33.0      1

Años en el puesto actual DA
0.0     59
1.0     30
1.5      1
2.0     27
2.5      1
3.0      7
4.0      5
5.0      5
7.0      1
10.0     2
20.0     1
60.0     1

"""




#Full-Time Developer and Data Analyst specific data
    

years= [0.0,           
        1.0,          
        2.0,          
        3.0,     
        4.0,      
        5.0,      
        6.0,      
        7.0,      
        8.0,      
        9.0,       
        10.0,     
        11.0,      
        12.0,      
        13.0,      
        14.0,      
        15.0,     
        16.0,      
        17.0,      
        18.0,      
        20.0,      
        ]


#Full-Time Dev
    


df_dev = pd.DataFrame(base_df.loc[(base_df["Tipo de contrato"] == "Full-Time") 
                                  & (base_df["Trabajo de"] == "Developer")
                                  ])

#print(df_dev)

df_dev_salary = pd.DataFrame(df_dev["Salario mensual o retiro BRUTO (en tu moneda local)"])
dev_list = df_dev_salary.values.tolist()
dev_list2 = []

for elem in dev_list:
    try:
        dev_list2.append(int(elem[0]))
    except:
        pass



dev_list_clean = [v for v in dev_list2 if v > 10000]
dev_list_clean.sort(reverse=True)


dev_AVG = statistics.mean(dev_list_clean)
dev_mode = statistics.mode(dev_list_clean)
dev_max = dev_list_clean[0]
dev_min = dev_list_clean[-1]

print(dev_AVG)
print(dev_mode)
print(dev_max)
print(dev_min)


df_dev_exp = pd.DataFrame(df_dev[[
    "Salario mensual o retiro BRUTO (en tu moneda local)",
    "Años en el puesto actual"]])



years_dict_dev = {}

for key in years:
    dev_df_years = pd.DataFrame(df_dev_exp.loc[df_dev_exp["Años en el puesto actual"] == key])
    dev_df_years_AVG = dev_df_years["Salario mensual o retiro BRUTO (en tu moneda local)"]
    dev_years_AVG_list = dev_df_years_AVG.values.tolist()
    dev_years_AVG_list_clean = []
    
    for elem in dev_years_AVG_list:
        try:
            dev_years_AVG_list_clean.append(int(elem))
        except:
            pass
     

    
    try:
        dev_years_AVG = statistics.mean(dev_years_AVG_list_clean)
    except:
        dev_years_AVG = 0
    
    
    years_dict_dev[key] = dev_years_AVG

print(years_dict_dev)




fig_dev = plt.figure(figsize = (15,5))
plt.bar(*zip(*years_dict_dev.items()))
plt.title("Full-Time Dev: AVG by years of experience")
plt.show()


"""



#Full-Time Data Analyst
    
"""

df_da = pd.DataFrame(base_df.loc[(base_df["Tipo de contrato"] == "Full-Time") 
                                  & (base_df["Trabajo de"] == "BI Analyst / Data Analyst")
                                  ])




df_da_salary = pd.DataFrame(df_da["Salario mensual o retiro BRUTO (en tu moneda local)"])
da_list = df_da_salary.values.tolist()
da_list2 = []

for elem in da_list:
    try:
        da_list2.append(int(elem[0]))
    except:
        pass



da_list_clean = [v for v in da_list2 if v > 10000]
da_list_clean.sort(reverse=True)


da_AVG = statistics.mean(da_list_clean)
da_mode = statistics.mode(da_list_clean)
da_max = da_list_clean[0]
da_min = da_list_clean[-1]

print(da_AVG)
print(da_mode)
print(da_max)
print(da_min)


df_da_exp = pd.DataFrame(df_da[[
    "Salario mensual o retiro BRUTO (en tu moneda local)",
    "Años en el puesto actual"]])


d = df_da_exp.groupby(["Años en el puesto actual"]).size()
print(d) #get all the years of experience
print(type(d))

years_dict_da = {}

for key in years:
    da_df_years = pd.DataFrame(df_da_exp.loc[df_da_exp["Años en el puesto actual"] == key])
    da_df_years_AVG = da_df_years["Salario mensual o retiro BRUTO (en tu moneda local)"]
    da_years_AVG_list = da_df_years_AVG.values.tolist()
    da_years_AVG_list_clean = []
    
    for elem in da_years_AVG_list:
        try:
            da_years_AVG_list_clean.append(int(elem))
        except:
            pass
    
    try:
        da_years_AVG = statistics.mean(da_years_AVG_list_clean)
    except:
        da_years_AVG = 0
    
#    print(years_AVG)
    
    years_dict_da[key] = da_years_AVG

print(years_dict_da)

fig_da = plt.figure(figsize = (15,5))
plt.bar(*zip(*years_dict_da.items()))
plt.title("Full-Time Data Analyst: AVG by years of experience")
plt.show()

