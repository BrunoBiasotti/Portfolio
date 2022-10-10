# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 15:34:33 2022

@author: elbia
"""

import numpy as np
import pandas as pd
import statistics
import matplotlib.pyplot as plt
import configparser

""" Data cleaning methodology 

Representativeness of the sample:
    Sample size over other factors. Don't use homogeneity to determine representativeness
    *For salaries, leave out those elements that do not exceed 0.05% of samples over the total
    
Salaries:
    Median gross salary.

Atypical values:
    Interquartile Range Method with a coefficient of 3.5 (Q3 - Q1)
    Eliminate those entries whose salary is less than half the minimum wage

Dollar exchange rate:
    Average intraday price of Bloomberg and median of the value of the day of
    the publication with a delta of 5 days
    
Experience:
    Junior: from 0 to 2 years
    Semi-Senior: from 2 years inclusive up to 5 years
    Senior: from 5 years inclusive

"""


""" First cleaning process - Data Types

Confirm that the salaries are in INT, that is, they are not NULL or STR

"""


def primera_limpieza(base_df):

    uno_df_dropped = pd.DataFrame() #output DF of removed lines
    uno_list = [] #Internal list stores index number
    
    base_df = base_df.reset_index() 
    uno_copia = base_df.copy() #Copy DF to iterate
    
    for index, row in uno_copia.iterrows(): 
        try:
            (int(row['Último salario mensual  o retiro BRUTO (en tu moneda local)']) and 
            int(row['Último salario mensual o retiro NETO (en tu moneda local)']))
        except:
            uno_list.append(index)
            base_df = base_df.drop(index)
    
    #If both values are not INT it will go to except
    #Append the index of the row and remove it from df
    
    uno_df_dropped = uno_copia[uno_copia["index"].isin(uno_list)]
    
    #Create a DF with removed index
    
    return[base_df,uno_df_dropped]


""" Second cleaning process - Outliers and IQR

Remove those outliers that may interfere with the calculation of the methodology

The first step is to eliminate those entries whose value is less than half of the minimum wage
Minimum salary = 47,850 ARS for August 2022 -> limit of 23,295 ARS

The second step is to eliminate according to the interquartile range with a coefficient of 3.5

"""


def iqr(iqr_df,in_col):
    
    iqr_list = []
    
    temp_list = iqr_df[in_col].tolist()

    for elem in temp_list:
        iqr_list.append(int(elem))

    iqr_q75,iqr_q25 = np.percentile(iqr_list, [75,25])

    iqr = iqr_q75 - iqr_q25

    iqr_limit = iqr*3.5

    iqr_limit_upper = iqr_q75 + iqr_limit
    iqr_limit_lower = iqr_q25 - iqr_limit

    return[iqr_limit_upper,iqr_limit_lower]

def segunda_limpieza(uno_df):
    dos_copia = uno_df.copy()
    dos_list=[]
    
    for index, row in dos_copia.iterrows():
        if int(row['Último salario mensual  o retiro BRUTO (en tu moneda local)']) > 23295:
            pass
        else:
           dos_list.append(index)
           uno_df = uno_df.drop(index)
    
    
    dos_df_dropped1 = dos_copia[dos_copia["index"].isin(dos_list)]
    
    
    
    #IQR
    
    dos_copia_iqr = uno_df.copy()
    dos_list_iqr = []
    
    dos_limits = iqr(uno_df,'Último salario mensual  o retiro BRUTO (en tu moneda local)')
    
    dos_iqr_upper = dos_limits[0]
    dos_iqr_lower = dos_limits[1]
    
    for index, row in dos_copia_iqr.iterrows():
        if (int(row['Último salario mensual  o retiro BRUTO (en tu moneda local)']) > dos_iqr_lower and 
            int(row['Último salario mensual  o retiro BRUTO (en tu moneda local)']) < dos_iqr_upper):
            pass
        else:
           dos_list_iqr.append(index)
           uno_df = uno_df.drop(index)
    
    dos_df_dropped2 = dos_copia_iqr[dos_copia_iqr["index"].isin(dos_list_iqr)]
    
    dos_df_out = uno_df.copy()
    
    return(dos_df_out,dos_df_dropped1,dos_df_dropped2)


""" Third cleaning process - Text not regulated in professions


I do a cleaning that is not established in the methodology which only includes 
those entries whose profession has more than 3 repetitions

"""

def tercera_limpieza(dos_df):
    
    tres_df_dropped = pd.DataFrame()
    tres_df_out = pd.DataFrame()
    
    tres_df_temp = pd.DataFrame(dos_df["Trabajo de"])
    
    tres_filter = tres_df_temp.groupby("Trabajo de").filter(lambda x: len(x) > 3)
    #Remove professions with less than 3 repetitions   
    tres_count = tres_filter.groupby("Trabajo de").count()
    
    tres_list = tres_count.index.tolist()
    
    tres_df_dropped = dos_df[dos_df["Trabajo de"].isin(tres_list) == False]
    tres_df_out = dos_df[dos_df["Trabajo de"].isin(tres_list) == True]    

    return(tres_df_out,tres_df_dropped,tres_list)



#Main code


config = configparser.RawConfigParser()
configFilePath = 'config.ini'
config.read(configFilePath)

ingresoDB = str(config.get('paths','ingresoDB'))
salarioSTR = str(config.get('paths','salarioSTR'))
valorAtipico = str(config.get('paths','valorAtipico'))
valorIQR = str(config.get('paths','valorIQR'))
profesionAtipico = str(config.get('paths','profesionAtipico'))
pathLimpio = str(config.get('paths','pathLimpio'))
analisis1 = str(config.get('paths','analisis1'))
analisis2 = str(config.get('paths','analisis2'))

sysarmy_df = pd.read_csv(ingresoDB)

df_primero = primera_limpieza(sysarmy_df)

df_sucio_1 = df_primero[1]

df_segundo = segunda_limpieza(df_primero[0])

df_sucio_2 = df_segundo[1]
df_sucio_3 = df_segundo[2]

df_tercero = tercera_limpieza(df_segundo[0])

df_sucio_4 = df_tercero[1]
profesiones = df_tercero[2]
limpio = df_tercero[0]

df_sucio_1.to_excel(salarioSTR)
df_sucio_2.to_excel(valorAtipico)
df_sucio_3.to_excel(valorIQR)
df_sucio_4.to_excel(profesionAtipico)
limpio.to_excel(pathLimpio)


""""Analysis - Salary per experience and role """

"""

final = []

for prof in profesiones:
    
    df_filtro = pd.DataFrame(limpio.loc[limpio["Trabajo de"] == prof])
    df_Median = df_filtro[["Último salario mensual  o retiro BRUTO (en tu moneda local)","Años de experiencia"]]
    
    jr = []
    ssr = []
    sr = []
    
    for index, row in df_Median.iterrows():
        if int(row['Años de experiencia']) < 2:
            jr.append(int(row['Último salario mensual  o retiro BRUTO (en tu moneda local)']))
        elif int(row['Años de experiencia']) >= 2 and int(row['Años de experiencia']) < 5:
            ssr.append(int(row['Último salario mensual  o retiro BRUTO (en tu moneda local)']))
        elif int(row['Años de experiencia']) >= 5:
            sr.append(int(row['Último salario mensual  o retiro BRUTO (en tu moneda local)']))    
    
    try:
        jr_median = statistics.median(jr)
    except:
        jr_median = 0
    try:
        ssr_median = statistics.median(ssr)
    except:
        ssr_median = 0
    try:
        sr_median = statistics.median(sr)
    except:
        sr_median = 0
    
    
    dic_temp_1 = {"jr":jr_median,"ssr":ssr_median,"sr":sr_median}
    dic_temp_2 = {prof:dic_temp_1}
    final.append(dic_temp_2)

"""

""" Graph for a fast analysis

graph_barh = pd.DataFrame()
new_index=['sr','ssr','jr']

x=0
for elem in final: 
    dtframe_concat = pd.DataFrame(final[x])
    dtframe_concat = dtframe_concat.reindex(new_index)
    x += 1
    graph_barh = pd.concat([graph_barh,dtframe_concat], axis=1)

colores={'jr':'#674ea7','ssr':'#ea2f2f','sr':'#ffa500'}
graph_barh = graph_barh.transpose()
graph_barh.plot(kind="barh",figsize=(15,8),color=colores)

graph_barh.to_excel(analisis1)
"""


""" Analysis - Salary per experience and role """

