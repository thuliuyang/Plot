# -*- coding: utf-8 -*-
"""
Created on Mon May 14 22:30:39 2018

@author: liuyang
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn.apionly as sns

#import geopandas as gp


def topct(a):
    return '%.1f' % a

year = 2011
syr = str(year)
scenarios = ['base.' + syr,'fixmet_no_anth.' + syr ]

idir_stat = './'
odir_plot = './'

cmap = sns.color_palette('Paired', 11)

emis_spe = ['NH3_agr']

sectors = ['AGR','ENE','IND','TRA','RCO','SLV','WST','AIR']

itbls_spe = {}

# Read data
if_stat = idir_stat + 'deaths.xls'
for sid,spe in enumerate(emis_spe):
    itbls_spe[spe] = pd.read_excel(if_stat,spe)


for spe in emis_spe:
    #input table process
    itbl_spe = itbls_spe[spe] #pd.read_excel(if_stat,spe)
    #'cons' consumption-based
    itbl_cons_spe = itbl_spe.copy()
    itbl_cons_spe_tot = itbl_cons_spe.sum(axis=1)/1000

    fig = plt.figure(figsize=(16,16))
    #--------------------------------------------------------------------------
    #Worldwide deposition due to each region’s consumption of products
    ax1 = fig.add_subplot(221) #axes([0,0,1,1], axisbg='w', frame_on=False)
    
    
    mtbl_cons_spe = itbl_cons_spe_tot.to_frame(name='Emission')
    mtbl_cons_spe['region'] = mtbl_cons_spe.index
    
    dep_str = np.round(mtbl_cons_spe['Emission'],2)
    dep_str = dep_str.apply(topct)
    mtbl_cons_spe.index = dep_str
    mtbl_cons_spe.sort_values('Emission',inplace=True)
    
    f_spe = mtbl_cons_spe['Emission'].plot(ax = ax1,kind='barh', colors =  cmap,width = 0.8, legend=False)

    plt.title('Premature deaths',fontsize=16)
    
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    
    plt.xlim(0,120)
    plt.xlabel('thousand person/year',fontsize=16)
    plt.ylabel('')
    
    regions_name = mtbl_cons_spe['region']
    ticklabels =mtbl_cons_spe['region']
    
    for rid in range(0,np.shape(mtbl_cons_spe.index)[0]):
        plt.text(mtbl_cons_spe['Emission'].iloc[rid]+0.5,rid,mtbl_cons_spe.iloc[rid,1],alpha=1,rotation=0,
                 horizontalalignment='left',#fontweight = 'bold',
                 verticalalignment='center',fontsize=16,
                 multialignment='center')#,fontweight='bold') #,transform=ax.transAxes