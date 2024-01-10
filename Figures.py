#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 14:47:49 2024

@author: xrixhon
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 10:52:57 2023

@author: xrixhon
"""

import rheia.POST_PROCESS.post_process as rheia_pp
import rheia.UQ.uncertainty_quantification as rheia_uq
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import plotly.io as pio
import numpy as np
import os, sys
from pathlib import Path
import pickle as pkl
import hashlib

pio.templates.default = 'simple_white'
pio.kaleido.scope.mathjax = None

pio.renderers.default = 'browser'

dir_to_save = '/Users/xrixhon/Documents/PhD_Thesis/Papers/5 - Nuke_vs_Mol/Images/'

def dict_color_full():
    categories = ['Sectors','Electricity','Heat_low_T','Heat_high_T','Mobility','Freight','Ammonia',
               'Methanol','HVC','Conversion','Storage','Storage','Storage_daily','Resources',
               'Infrastructure','Years_1','Years_2','Phases']
    color_dict_full = dict.fromkeys(categories)

    for c in categories:
        color_dict_full.update(dict_color(c))
    
    return color_dict_full

def dict_color(category):
    color_dict = {}
    
    if category == 'Electricity':
        color_dict = {"NUCLEAR":"deeppink", "NUCLEAR_SMR": "deeppink", "CCGT":"darkorange", "CCGT_AMMONIA":"slateblue", "COAL_US" : "black", "COAL_IGCC" : "dimgray", "PV" : "yellow", "WIND_ONSHORE" : "lawngreen", "WIND_OFFSHORE" : "green", "HYDRO_RIVER" : "blue", "GEOTHERMAL" : "firebrick", "ELECTRICITY" : "dodgerblue"}
    elif category == 'Heat_low_T':
        color_dict = {"DHN_HP_ELEC" : "blue", "DHN_COGEN_GAS" : "orange", "DHN_COGEN_WOOD" : "sandybrown", "DHN_COGEN_WASTE" : "olive", "DHN_COGEN_WET_BIOMASS" : "seagreen", "DHN_COGEN_BIO_HYDROLYSIS" : "springgreen", "DHN_BOILER_GAS" : "darkorange", "DHN_BOILER_WOOD" : "sienna", "DHN_BOILER_OIL" : "blueviolet", "DHN_DEEP_GEO" : "firebrick", "DHN_SOLAR" : "gold", "DEC_HP_ELEC" : "cornflowerblue", "DEC_THHP_GAS" : "lightsalmon", "DEC_COGEN_GAS" : "goldenrod", "DEC_COGEN_OIL" : "mediumpurple", "DEC_ADVCOGEN_GAS" : "burlywood", "DEC_ADVCOGEN_H2" : "violet", "DEC_BOILER_GAS" : "moccasin", "DEC_BOILER_WOOD" : "peru", "DEC_BOILER_OIL" : "darkorchid", "DEC_SOLAR" : "yellow", "DEC_DIRECT_ELEC" : "deepskyblue"}
    elif category == 'Heat_high_T':
        color_dict = {"IND_COGEN_GAS":"orange", "IND_COGEN_WOOD":"peru", "IND_COGEN_WASTE" : "olive", "IND_BOILER_GAS" : "moccasin", "IND_BOILER_WOOD" : "goldenrod", "IND_BOILER_OIL" : "blueviolet", "IND_BOILER_COAL" : "black", "IND_BOILER_WASTE" : "olivedrab", "IND_DIRECT_ELEC" : "royalblue"}
    elif category == 'Mobility':
        color_dict = {"TRAMWAY_TROLLEY" : "dodgerblue", "BUS_COACH_DIESEL" : "dimgrey", "BUS_COACH_HYDIESEL" : "gray", "BUS_COACH_CNG_STOICH" : "orange", "BUS_COACH_FC_HYBRIDH2" : "violet", "TRAIN_PUB" : "blue", "CAR_GASOLINE" : "black", "CAR_DIESEL" : "lightgray", "CAR_NG" : "moccasin", "CAR_METHANOL":"orchid", "CAR_HEV" : "salmon", "CAR_PHEV" : "lightsalmon", "CAR_BEV" : "deepskyblue", "CAR_FUEL_CELL" : "magenta"}
    elif category == 'Freight':
        color_dict = {"TRAIN_FREIGHT" : "royalblue", "BOAT_FREIGHT_DIESEL" : "dimgrey", "BOAT_FREIGHT_NG" : "darkorange", "BOAT_FREIGHT_METHANOL" : "fuchsia", "TRUCK_DIESEL" : "darkgrey", "TRUCK_FUEL_CELL" : "violet", "TRUCK_ELEC" : "dodgerblue", "TRUCK_NG" : "moccasin", "TRUCK_METHANOL" : "orchid"}
    elif category == 'Ammonia':
        color_dict = {"HABER_BOSCH":"tomato", "AMMONIA" : "slateblue", "AMMONIA_RE" : "blue"}
    elif category == 'Methanol':
        color_dict = {"SYN_METHANOLATION":"violet","METHANE_TO_METHANOL":"orange","BIOMASS_TO_METHANOL":"peru", "METHANOL" : "orchid", "METHANOL_RE" : "mediumvioletred"}
    elif category == "HVC":
        color_dict = {"OIL_TO_HVC":"blueviolet", "GAS_TO_HVC":"orange", "BIOMASS_TO_HVC":"peru", "METHANOL_TO_HVC":"orchid"}
    elif category == 'Conversion':
        color_dict = {"H2_ELECTROLYSIS" : "violet", "H2_NG" : "magenta", "H2_BIOMASS" : "orchid", "GASIFICATION_SNG" : "orange", "PYROLYSIS" : "blueviolet", "ATM_CCS" : "black", "INDUSTRY_CCS" : "grey", "SYN_METHANOLATION" : "mediumpurple", "SYN_METHANATION" : "moccasin", "BIOMETHANATION" : "darkorange", "BIO_HYDROLYSIS" : "gold", "METHANE_TO_METHANOL" : "darkmagenta",'SMR':'orange', 'AMMONIA_TO_H2':'fuchsia'}
    elif category == 'Storage':
        color_dict = {"TS_DHN_SEASONAL" : "indianred", "BATT_LI" : "royalblue", "BEV_BATT" : "deepskyblue", "PHEV_BATT" : "lightskyblue", "PHS" : "dodgerblue", "TS_DEC_HP_ELEC" : "blue", "TS_DHN_DAILY" : "lightcoral", "TS_HIGH_TEMP" : "red", "SEASONAL_NG" : "orange", "SEASONAL_H2" : "violet", "SLF_STO" : "blueviolet", "TS_DEC_DIRECT_ELEC":"darkgoldenrod", "TS_DEC_THHP_GAS": "orange", "TS_DEC_COGEN_GAS":"coral", "TS_DEC_COGEN_OIL":"darkviolet", "TS_DEC_ADVCOGEN_GAS":"sandybrown", "TS_DEC_ADVCOGEN_H2": "plum", "TS_DEC_BOILER_GAS": "tan", "TS_DEC_BOILER_WOOD":"peru", "TS_DEC_BOILER_OIL": "darkviolet", "GAS_STORAGE": "orange", "H2_STORAGE": "violet", "CO2_STORAGE": "lightgray", "GASOLINE_STORAGE": "gray", "DIESEL_STORAGE": "silver", "AMMONIA_STORAGE": "slateblue", "LFO_STORAGE": "darkviolet"}
    elif category == 'Storage_daily':
        color_dict = {"BATT_LI" : "royalblue", "BEV_BATT" : "deepskyblue", "PHEV_BATT" : "lightskyblue", "TS_DEC_HP_ELEC" : "blue", "TS_DHN_DAILY" : "lightcoral", "TS_HIGH_TEMP" : "red", "TS_DEC_DIRECT_ELEC":"darkgoldenrod", "TS_DEC_THHP_GAS": "orange", "TS_DEC_COGEN_GAS":"coral", "TS_DEC_COGEN_OIL":"darkviolet", "TS_DEC_ADVCOGEN_GAS":"sandybrown", "TS_DEC_ADVCOGEN_H2": "plum", "TS_DEC_BOILER_GAS": "tan", "TS_DEC_BOILER_WOOD":"peru", "TS_DEC_BOILER_OIL": "darkviolet"}
    elif category == 'Resources':
        color_dict = {"ELECTRICITY" : "deepskyblue", "GASOLINE" : "gray", "DIESEL" : "silver", "BIOETHANOL" : "mediumorchid", "BIODIESEL" : "mediumpurple", "LFO" : "darkviolet", "GAS" : "orange", "GAS_RE" : "gold", "WOOD" : "saddlebrown", "WET_BIOMASS" : "seagreen", "COAL" : "black", "URANIUM" : "deeppink", "WASTE" : "olive", "H2" : "violet", "H2_RE" : "plum", "AMMONIA" : "slateblue", "AMMONIA_RE" : "blue", "METHANOL" : "orchid", "METHANOL_RE" : "mediumvioletred", "CO2_EMISSIONS" : "gainsboro", "RES_WIND" : "limegreen", "RES_SOLAR" : "yellow", "RES_HYDRO" : "blue", "RES_GEO" : "firebrick", "ELEC_EXPORT" : "chartreuse","CO2_ATM": "dimgray", "CO2_INDUSTRY": "darkgrey", "CO2_CAPTURED": "lightslategrey", "RE_FUELS": 'green','NRE_FUELS':'black', 'LOCAL_RE': 'limegreen', 'IMPORTED_ELECTRICITY': 'deepskyblue'}
    elif category == 'Sectors':
        color_dict = {"ELECTRICITY" : "deepskyblue", "HEAT_HIGH_T":"red","HEAT_LOW_T_DECEN":"lightpink", "HEAT_LOW_T_DHN":"indianred", "MOB_PUBLIC":"gold", "MOB_PRIVATE":"goldenrod","MOBILITY_FREIGHT":"darkgoldenrod", "NON_ENERGY": "darkviolet", "INFRASTRUCTURE":"grey","HVC":"cyan",'STORAGE':'chartreuse', 'OTHERS':'gainsboro', 'INDUSTRY': 'orange', 'HOUSEHOLDS': 'green', 'SERVICES':'grey', "HEAT_LOW_T":"lightpink", "MOBILITY_PASSENGER":"goldenrod"}
    elif category == 'Infrastructure':
        color_dict = {'EFFICIENCY': 'lime','DHN': 'orange','GRID': 'gold'}
    elif category == 'Years_1':
        color_dict = {'YEAR_2020': 'blue','YEAR_2025': 'orange','YEAR_2030': 'green', 'YEAR_2035': 'red', 'YEAR_2040': 'purple', 'YEAR_2045': 'brown', 'YEAR_2050':'pink'}
    elif category == 'Years_2':
        color_dict = {'2020': 'blue','2025': 'orange','2030': 'green', '2035': 'red', '2040': 'purple', '2045': 'brown', '2050':'pink'}
    elif category == 'Phases':
            color_dict = {'2015_2020': 'blue','2020_2025': 'orange','2025_2030': 'green', '2030_2035': 'red', '2035_2040': 'purple', '2040_2045': 'brown', '2045_2050':'pink'}
        
    return color_dict


def custom_fig(fig,title,yvals,xvals=['2020','2025','2030','2035','2040',
                    '2045','2050'], ftsize=18,annot_text=None,
               type_graph = None, neg_value = False, flip = False):

    def round_repdigit(n, ndigits=0):     
        if n != 0:
            i = int(np.ceil(np.log10(abs(n))))
            x = np.round(n, ndigits-i)
            if i-ndigits >= 0:
                x = int(x)
            return x     
        else:
            return 0
        
    gray = 'rgb(90,90,90)' 
    color = gray
    
    fig.update_layout(
        xaxis_color=color, yaxis_color=color,
        xaxis_mirror=False, yaxis_mirror=False,
        yaxis_showgrid=False, xaxis_showgrid=False,
        yaxis_linecolor='white', xaxis_linecolor='white',
        xaxis_tickfont_size=ftsize, yaxis_tickfont_size=ftsize,
        showlegend=False,
    )
    
    if title != None:
        fig.update_layout(
            title_text=title,titlefont=dict(family="Raleway",size=ftsize+10)
            )
    
    if type_graph == None:
        fig.update_xaxes(dict(ticks = "inside", ticklen=10))
        fig.update_xaxes(tickangle= 0,tickmode = 'array',tickwidth=2,tickcolor=gray,
                            tickfont=dict(
                                  family="Rawline",
                                  size=ftsize
                              ))
    fig.update_yaxes(dict(ticks = "inside", ticklen=10))
    if type_graph in ['strip','bar']:
        fig.update_xaxes(dict(ticks = "inside", ticklen=10))
        
    
    if not(flip):
        fig.update_yaxes(tickangle= 0,tickmode = 'array',tickwidth=2,tickcolor=gray,
                            tickfont=dict(
                                  family="Rawline",
                                  size=ftsize
                              ))
    
    fig.update_layout(
        yaxis = dict(
            tickmode = 'array',
            tickvals = fig.layout.yaxis.tickvals,
            ticktext = list(map(str,yvals))
            ))
    
            
    factor=0.05
    nrepdigit = 0
    
    fig.update_yaxes(tickvals=yvals)
    
    xstring = isinstance(fig.data[0].x[0],str)
    
    if xstring: ## ONLY VALID IF THE FIRST TRACE HAS ALL VALUES
        xvals = xvals
        xmin = 0
        xmax = len(xvals) - 1
    else:
        if not(flip):
            xvals = pd.Series(sum([list(i.x) for i in fig.data],[]))
            xmin = xvals.min()
            xmax = xvals.max()
        else:
            xmin = min(xvals)
            xmax = max(xvals)
        xampl = xmax-xmin
    
    
    if xstring:
        if fig.layout.xaxis.range is None:
            if type_graph in ['bar','strip']:
                fig.layout.xaxis.range = [xmin-factor*15, xmax+factor*15]
            elif type_graph == 'scatter':
                fig.layout.xaxis.range = [xmin-factor*6, xmax+factor*6]
            else:
                fig.layout.xaxis.range = [xmin-factor*3, xmax+factor*3]
        if fig.layout.xaxis.tickvals is None:
            fig.layout.xaxis.tickvals = xvals
    else:
        if fig.layout.xaxis.range is None:
            fig.layout.xaxis.range = [xmin-xampl*factor, xmax+xampl*factor]
        if fig.layout.xaxis.tickvals is None:
            fig.layout.xaxis.tickvals = [round_repdigit(x, nrepdigit) for x in [xmin, xmax]]
    
    if flip:
        fig.update_xaxes(tickvals=xvals)
        
    
    fig.layout.xaxis.tickvals = sorted(fig.layout.xaxis.tickvals)
    fig.layout.xaxis.range = sorted(fig.layout.xaxis.range)
    
    
    yvals = yvals
    
    ystring = isinstance(fig.data[0].y[0],str)
    
    if ystring: ## ONLY VALID IF THE FIRST TRACE HAS ALL VALUES
        ymin = 0
        ymax = len(yvals) - 1
    else:
        ymin = min(yvals)
        ymax = max(yvals)
    yampl = ymax-ymin
    
    if fig.layout.yaxis.range is None:
        fig.layout.yaxis.range = [ymin-yampl*factor, ymax+yampl*factor]
    if fig.layout.yaxis.tickvals is None:
        fig.layout.yaxis.tickvals = [round_repdigit(y, nrepdigit) for y in [ymin, ymax]]
    
    if not(ystring):
        fig.layout.yaxis.tickvals = sorted(fig.layout.yaxis.tickvals)
    fig.layout.yaxis.range = sorted(fig.layout.yaxis.range)
    
    fig.update_layout(xaxis_title=None, yaxis_title=None)
    
    if neg_value:
        if not(flip):
            fig.add_shape(x0=xmin,x1=xmax,
                      y0=0,y1=0,
                      type='line',layer="below",
                      line=dict(color=color,width=1),opacity=0.5)
        else:
            fig.add_shape(x0=0,x1=0,
                      y0=ymin,y1=ymax,
                      type='line',layer="below",
                      line=dict(color=color,width=1),opacity=0.5)
            
    
    fig.add_shape(x0=fig.layout.xaxis.range[0],x1=fig.layout.xaxis.range[0],
              y0=fig.layout.yaxis.tickvals[0],y1=fig.layout.yaxis.tickvals[-1],
              type='line',layer="above",
              line=dict(color=color,width=2),opacity=1)
    
    # if type_graph in [None,'bar']:
    fig.add_shape(x0=xmin,x1=xmax,
              y0=fig.layout.yaxis.range[0],y1=fig.layout.yaxis.range[0],
              type='line',layer="above",
              line=dict(color=color, width=2),opacity=1)
    
    if type_graph in ['scatter']:
        fig.update_layout({ax:{"visible":False, "matches":None} for ax in fig.to_dict()["layout"] if "xaxis" in ax})
    
    if type_graph in ['strip']:
        if not(flip):
            fig.add_shape(x0=0.5,x1=0.5,
                      y0=ymin,y1=ymax,
                      type='line',layer="above",
                      line=dict(color=color,width=2,dash="dot"),opacity=1)
            fig.add_shape(x0=xmax-0.5,x1=xmax-0.5,
                      y0=ymin,y1=ymax,
                      type='line',layer="above",
                      line=dict(color=color,width=2,dash="dot"),opacity=1)
        else:
            fig.add_shape(x0=xmin,x1=xmax,
                      y0=0.5,y1=0.5,
                      type='line',layer="above",
                      line=dict(color=color,width=2,dash="dot"),opacity=1)
            fig.add_shape(x0=xmin,x1=xmax,
                      y0=ymax-0.5,y1=ymax-0.5,
                      type='line',layer="above",
                      line=dict(color=color,width=2,dash="dot"),opacity=1)
    
    fig.update_layout(margin_b = 10, margin_r = 30, margin_l = 30)#,margin_pad = 20)

df = pd.DataFrame(columns=['Year','Sector','Value'])

#%% MISCELLANEOUS

## ELECTRICITY
list_row = ['2020','ELECTRICITY',64]
df.loc[len(df)] = list_row

list_row = ['2025','ELECTRICITY',71]
df.loc[len(df)] = list_row

list_row = ['2030','ELECTRICITY',77]
df.loc[len(df)] = list_row

list_row = ['2035','ELECTRICITY',84]
df.loc[len(df)] = list_row

list_row = ['2040','ELECTRICITY',91]
df.loc[len(df)] = list_row

list_row = ['2045','ELECTRICITY',98]
df.loc[len(df)] = list_row

list_row = ['2050','ELECTRICITY',105]
df.loc[len(df)] = list_row

## WOOD
list_row = ['2020','WOOD',30]
df.loc[len(df)] = list_row

list_row = ['2025','WOOD',31]
df.loc[len(df)] = list_row

list_row = ['2030','WOOD',32]
df.loc[len(df)] = list_row

list_row = ['2035','WOOD',33]
df.loc[len(df)] = list_row

list_row = ['2040','WOOD',34]
df.loc[len(df)] = list_row

list_row = ['2045','WOOD',35]
df.loc[len(df)] = list_row

list_row = ['2050','WOOD',36]
df.loc[len(df)] = list_row

## WET_BIOMASS
list_row = ['2020','WET_BIOMASS',5]
df.loc[len(df)] = list_row

list_row = ['2025','WET_BIOMASS',5]
df.loc[len(df)] = list_row

list_row = ['2030','WET_BIOMASS',6]
df.loc[len(df)] = list_row

list_row = ['2035','WET_BIOMASS',6]
df.loc[len(df)] = list_row

list_row = ['2040','WET_BIOMASS',6]
df.loc[len(df)] = list_row

list_row = ['2045','WET_BIOMASS',6]
df.loc[len(df)] = list_row

list_row = ['2050','WET_BIOMASS',6]
df.loc[len(df)] = list_row

## COAL
list_row = ['2020','COAL',16]
df.loc[len(df)] = list_row

list_row = ['2025','COAL',17]
df.loc[len(df)] = list_row

list_row = ['2030','COAL',18]
df.loc[len(df)] = list_row

list_row = ['2035','COAL',18]
df.loc[len(df)] = list_row

list_row = ['2040','COAL',18]
df.loc[len(df)] = list_row

list_row = ['2045','COAL',18]
df.loc[len(df)] = list_row

list_row = ['2050','COAL',18]
df.loc[len(df)] = list_row

## URANIUM
list_row = ['2020','URANIUM',4]
df.loc[len(df)] = list_row

list_row = ['2025','URANIUM',4]
df.loc[len(df)] = list_row

list_row = ['2030','URANIUM',4]
df.loc[len(df)] = list_row

list_row = ['2035','URANIUM',4]
df.loc[len(df)] = list_row

list_row = ['2040','URANIUM',4]
df.loc[len(df)] = list_row

list_row = ['2045','URANIUM',4]
df.loc[len(df)] = list_row

list_row = ['2050','URANIUM',4]
df.loc[len(df)] = list_row

## WASTE
list_row = ['2020','WASTE',21]
df.loc[len(df)] = list_row

list_row = ['2025','WASTE',22]
df.loc[len(df)] = list_row

list_row = ['2030','WASTE',22]
df.loc[len(df)] = list_row

list_row = ['2035','WASTE',23]
df.loc[len(df)] = list_row

list_row = ['2040','WASTE',24]
df.loc[len(df)] = list_row

list_row = ['2045','WASTE',24]
df.loc[len(df)] = list_row

list_row = ['2050','WASTE',25]
df.loc[len(df)] = list_row

color_map = dict_color_full()

fig = px.line(df,x='Year',y='Value',color='Sector',
               color_discrete_map=color_map,markers=True)

fig.update_traces(marker=dict(size=10))
fig.update_traces(line=dict(width=4))

title = "<b>Limited miscellaneous</b><br>[€<sub>2015</sub>/GWh]"
yvals = [min(df['Value']),max(df['Value'])]
xvals = [2020, 2025, 2030, 2035, 2040, 2045, 2050]

custom_fig(fig,title,yvals,
                xvals=xvals)
fig.write_html(dir_to_save+"Raw/Res_misc_raw.html")
fig.write_image(dir_to_save+"Raw/Res_misc.pdf", width=600, height=600)


#%% UNLIMITED_FOSS

df = pd.DataFrame(columns=['Year','Sector','Value'])

## GASOLINE
list_row = ['2020','GASOLINE',66]
df.loc[len(df)] = list_row

list_row = ['2025','GASOLINE',72]
df.loc[len(df)] = list_row

list_row = ['2030','GASOLINE',79]
df.loc[len(df)] = list_row

list_row = ['2035','GASOLINE',82]
df.loc[len(df)] = list_row

list_row = ['2040','GASOLINE',86]
df.loc[len(df)] = list_row

list_row = ['2045','GASOLINE',90]
df.loc[len(df)] = list_row

list_row = ['2050','GASOLINE',94]
df.loc[len(df)] = list_row

## DIESEL
list_row = ['2020','DIESEL',63]
df.loc[len(df)] = list_row

list_row = ['2025','DIESEL',70]
df.loc[len(df)] = list_row

list_row = ['2030','DIESEL',76]
df.loc[len(df)] = list_row

list_row = ['2035','DIESEL',80]
df.loc[len(df)] = list_row

list_row = ['2040','DIESEL',83]
df.loc[len(df)] = list_row

list_row = ['2045','DIESEL',87]
df.loc[len(df)] = list_row

list_row = ['2050','DIESEL',91]
df.loc[len(df)] = list_row

## LFO
list_row = ['2020','LFO',48]
df.loc[len(df)] = list_row

list_row = ['2025','LFO',53]
df.loc[len(df)] = list_row

list_row = ['2030','LFO',57]
df.loc[len(df)] = list_row

list_row = ['2035','LFO',60]
df.loc[len(df)] = list_row

list_row = ['2040','LFO',63]
df.loc[len(df)] = list_row

list_row = ['2045','LFO',66]
df.loc[len(df)] = list_row

list_row = ['2050','LFO',69]
df.loc[len(df)] = list_row

## GAS
list_row = ['2020','GAS',34]
df.loc[len(df)] = list_row

list_row = ['2025','GAS',38]
df.loc[len(df)] = list_row

list_row = ['2030','GAS',41]
df.loc[len(df)] = list_row

list_row = ['2035','GAS',44]
df.loc[len(df)] = list_row

list_row = ['2040','GAS',47]
df.loc[len(df)] = list_row

list_row = ['2045','GAS',50]
df.loc[len(df)] = list_row

list_row = ['2050','GAS',53]
df.loc[len(df)] = list_row

## H2
list_row = ['2020','H2',78]
df.loc[len(df)] = list_row

list_row = ['2025','H2',82]
df.loc[len(df)] = list_row

list_row = ['2030','H2',85]
df.loc[len(df)] = list_row

list_row = ['2035','H2',88]
df.loc[len(df)] = list_row

list_row = ['2040','H2',90]
df.loc[len(df)] = list_row

list_row = ['2045','H2',93]
df.loc[len(df)] = list_row

list_row = ['2050','H2',96]
df.loc[len(df)] = list_row

## AMMONIA
list_row = ['2020','AMMONIA',72]
df.loc[len(df)] = list_row

list_row = ['2025','AMMONIA',80]
df.loc[len(df)] = list_row

list_row = ['2030','AMMONIA',89]
df.loc[len(df)] = list_row

list_row = ['2035','AMMONIA',95]
df.loc[len(df)] = list_row

list_row = ['2040','AMMONIA',101]
df.loc[len(df)] = list_row

list_row = ['2045','AMMONIA',107]
df.loc[len(df)] = list_row

list_row = ['2050','AMMONIA',114]
df.loc[len(df)] = list_row

## METHANOL
list_row = ['2020','METHANOL',81]
df.loc[len(df)] = list_row

list_row = ['2025','METHANOL',89]
df.loc[len(df)] = list_row

list_row = ['2030','METHANOL',97]
df.loc[len(df)] = list_row

list_row = ['2035','METHANOL',102]
df.loc[len(df)] = list_row

list_row = ['2040','METHANOL',107]
df.loc[len(df)] = list_row

list_row = ['2045','METHANOL',112]
df.loc[len(df)] = list_row

list_row = ['2050','METHANOL',116]
df.loc[len(df)] = list_row

color_map = dict_color_full()

fig = px.line(df,x='Year',y='Value',color='Sector',
               color_discrete_map=color_map,markers=True)

fig.update_traces(marker=dict(size=10))
fig.update_traces(line=dict(width=4))

title = "<b>Unlimited fossil-based fuels</b><br>[€<sub>2015</sub>/GWh]"
yvals = [min(df['Value']),max(df['Value'])]
xvals = [2020, 2025, 2030, 2035, 2040, 2045, 2050]

custom_fig(fig,title,yvals,
                xvals=xvals)
fig.write_html(dir_to_save+"Raw/Res_foss_raw.html")
fig.write_image(dir_to_save+"Raw/Res_foss.pdf", width=600, height=600)


#%% UNLIMITED_RENEWABLES

df = pd.DataFrame(columns=['Year','Sector','Value'])

## BIOETHANOL
list_row = ['2020','BIOETHANOL',123]
df.loc[len(df)] = list_row

list_row = ['2025','BIOETHANOL',119]
df.loc[len(df)] = list_row

list_row = ['2030','BIOETHANOL',115]
df.loc[len(df)] = list_row

list_row = ['2035','BIOETHANOL',111]
df.loc[len(df)] = list_row

list_row = ['2040','BIOETHANOL',108]
df.loc[len(df)] = list_row

list_row = ['2045','BIOETHANOL',104]
df.loc[len(df)] = list_row

list_row = ['2050','BIOETHANOL',100]
df.loc[len(df)] = list_row

## BIODIESEL
list_row = ['2020','BIODIESEL',131]
df.loc[len(df)] = list_row

list_row = ['2025','BIODIESEL',128]
df.loc[len(df)] = list_row

list_row = ['2030','BIODIESEL',124]
df.loc[len(df)] = list_row

list_row = ['2035','BIODIESEL',120]
df.loc[len(df)] = list_row

list_row = ['2040','BIODIESEL',116]
df.loc[len(df)] = list_row

list_row = ['2045','BIODIESEL',113]
df.loc[len(df)] = list_row

list_row = ['2050','BIODIESEL',109]
df.loc[len(df)] = list_row

## GAS_RE
list_row = ['2020','GAS_RE',132]
df.loc[len(df)] = list_row

list_row = ['2025','GAS_RE',128]
df.loc[len(df)] = list_row

list_row = ['2030','GAS_RE',123]
df.loc[len(df)] = list_row

list_row = ['2035','GAS_RE',118]
df.loc[len(df)] = list_row

list_row = ['2040','GAS_RE',114]
df.loc[len(df)] = list_row

list_row = ['2045','GAS_RE',109]
df.loc[len(df)] = list_row

list_row = ['2050','GAS_RE',104]
df.loc[len(df)] = list_row

## H2_RE
list_row = ['2020','H2_RE',138]
df.loc[len(df)] = list_row

list_row = ['2025','H2_RE',132]
df.loc[len(df)] = list_row

list_row = ['2030','H2_RE',125]
df.loc[len(df)] = list_row

list_row = ['2035','H2_RE',119]
df.loc[len(df)] = list_row

list_row = ['2040','H2_RE',113]
df.loc[len(df)] = list_row

list_row = ['2045','H2_RE',107]
df.loc[len(df)] = list_row

list_row = ['2050','H2_RE',101]
df.loc[len(df)] = list_row

## AMMONIA_RE
list_row = ['2020','AMMONIA_RE',93]
df.loc[len(df)] = list_row

list_row = ['2025','AMMONIA_RE',89]
df.loc[len(df)] = list_row

list_row = ['2030','AMMONIA_RE',85]
df.loc[len(df)] = list_row

list_row = ['2035','AMMONIA_RE',82]
df.loc[len(df)] = list_row

list_row = ['2040','AMMONIA_RE',78]
df.loc[len(df)] = list_row

list_row = ['2045','AMMONIA_RE',75]
df.loc[len(df)] = list_row

list_row = ['2050','AMMONIA_RE',71]
df.loc[len(df)] = list_row

## METHANOL_RE
list_row = ['2020','METHANOL_RE',123]
df.loc[len(df)] = list_row

list_row = ['2025','METHANOL_RE',119]
df.loc[len(df)] = list_row

list_row = ['2030','METHANOL_RE',115]
df.loc[len(df)] = list_row

list_row = ['2035','METHANOL_RE',111]
df.loc[len(df)] = list_row

list_row = ['2040','METHANOL_RE',108]
df.loc[len(df)] = list_row

list_row = ['2045','METHANOL_RE',104]
df.loc[len(df)] = list_row

list_row = ['2050','METHANOL_RE',100]
df.loc[len(df)] = list_row

color_map = dict_color_full()

fig = px.line(df,x='Year',y='Value',color='Sector',
               color_discrete_map=color_map,markers=True)

fig.update_traces(marker=dict(size=10))
fig.update_traces(line=dict(width=4))

A = 4

title = "<b>Unlimited renewable fuels</b><br>[€<sub>2015</sub>/GWh]"
yvals = [min(df['Value']),max(df['Value'])]
xvals = [2020, 2025, 2030, 2035, 2040, 2045, 2050]

custom_fig(fig,title,yvals,
                xvals=xvals)
fig.write_html(dir_to_save+"Raw/Res_ren_raw.html")
fig.write_image(dir_to_save+"Raw/Res_ren.pdf", width=600, height=600)




