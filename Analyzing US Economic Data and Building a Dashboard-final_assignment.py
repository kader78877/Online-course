# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 16:25:54 2019

@author: Abdelkader AB
"""

import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

from bokeh.io import push_notebook, output_file,show,output_notebook
from bokeh.layouts import row
from bokeh.plotting import figure





link = "https://en.wikipedia.org/wiki/Economy_of_the_United_States"
page = requests.get(link)
soup = BeautifulSoup(page.text,'html.parser')

allTable = soup.find_all('table')
table = allTable[1]

def parse_table(rawTable) :
    
    #get all column name
    allCol = rawTable.find_all('th')
    for i,ele in enumerate(allCol):
        allCol[i] = ele.get_text().strip()
    
    #get all data
    allData = rawTable.find_all('tr')
    dataTable = np.zeros((len(allData)-1,len(allCol)))
    
    for i in range(1,len(allData)):
        row = allData[i].find_all('td')
        for j in range(len(allCol)):
            txt = row[j].get_text().replace('−','-').replace(',','').replace('\xa0%','')
            txt = txt.replace('%','')
            txt = txt.strip()
            if j==0 :
                txt = int(txt)
            else:
                txt = float(txt)
            dataTable[i-1,j] = txt    
            
    df = pd.DataFrame(data=dataTable,columns = allCol)
    return df

df = parse_table(table)
df = df.sort_values(by='Year',ascending=True)
df = df.set_index('Year')

def make_dashboard(x,gdp_change,unemployment,title,file_name):
    output_file(file_name)
    output_notebook()
    p = figure(title = title,x_axis_label='year',y_axis_label='%')
    p.line(x.squeeze(),gdp_change.squeeze(),color="firebrick",line_width=4,legend="% GDP change")
    p.line(x.squeeze(),unemployment.squeeze(),line_width=4,legend="% unemployed")
    show(p)
    
x = df.index.values
gdpGrowth = df.loc[:,'GDP growth(real)']
unemployment = df.loc[:,'Unemployment (in percent)']
output_notebook()        
title = "Unemployment stats according to GDP"
file_name = "index.html"

make_dashboard(x,gdpGrowth,unemployment,title,file_name)
