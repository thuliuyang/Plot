# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 15:51:07 2016

@author: YIXUAN
"""


#bar plot of nitrogen deaths in each region induced by consumptions
#similar plot of Fig 4 in the Nature paper 

#yzheng,2018/04/28

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn.apionly as sns


def topct(a):
    return '%.1f' % a

year = 2011
syr = str(year)
scenarios = ['base.' + syr,'fixmet_no_anth.' + syr ]
reg_scenarios = []
for i in range(1,14):
    scenarios.append('fixmet.'+syr+'.con'+str(i))
    reg_scenarios.append('fixmet.'+syr+'.con'+str(i))

idir_stat = './'
odir_plot = './'

regions_name = ['China','Rest of East Asia','India','Rest of Asia','Russia','Western Europe','Eastern Europe','USA','Canada','Middle east and north Africa','Latin America','Sub-Saharan Africa','Rest of the world']

ticklabels = ['China','Rest of\nEast Asia','India','Rest of\nAsia','Russia','Western\nEurope','Eastern\nEurope','USA','Canada','Middle east and\nnorth Africa','Latin\nAmerica','Sub-Saharan\nAfrica','Rest of\nthe world']

cmap = sns.color_palette('Paired', 13)
cmap[12] = (0.66,0.66,0.66)

emis_spe = ['death']
emis_N_ratio = [14./(14.+16*2),14./(14.+1*3)]
sectors = ['AGR','ENE','IND','TRA','RCO','SLV','WST','AIR']

itbls_spe = {}

if_stat = idir_stat + 'data.xls'
for sid,spe in enumerate(emis_spe):
    itbls_spe[spe] = pd.read_excel(if_stat,spe)/1000.


for spe in emis_spe:
    #input table process
    itbl_spe = itbls_spe[spe] #pd.read_excel(if_stat,spe)
    #'cons' consumption-based
    itbl_cons_spe = itbl_spe.copy()
    itbl_cons_spe.columns = regions_name
    itbl_cons_spe_tot = itbl_cons_spe.sum(axis=0)
    itbl_base_spe_tot = itbl_cons_spe.sum(axis=1)

    fig = plt.figure(figsize=(16,16))
    
    
    #--------------------------------------------------------------------------
    #Worldwide deposition due to each region’s consumption of products
    ax1 = fig.add_subplot(221) #axes([0,0,1,1], axisbg='w', frame_on=False)
    
    
    mtbl_cons_spe = itbl_cons_spe_tot.to_frame(name='death')
    mtbl_cons_spe['colors'] = cmap
    mtbl_cons_spe['region'] = mtbl_cons_spe.index
    
    dep_str = np.round(mtbl_cons_spe['death'],2)
    dep_str = dep_str.apply(topct)
    mtbl_cons_spe.index = dep_str
    mtbl_cons_spe.sort_values('death',inplace=True)
    
    f_spe = mtbl_cons_spe['death'].plot(ax = ax1,kind='barh', colors = mtbl_cons_spe['colors'],width = 0.8, legend=False)
#    plt.tight_layout(pad=0.1,w_pad = 1.25,h_pad=1.8)
#    plt.xticks(rotation = 0,size=18)
#    plt.yticks(size=18)
    plt.title('(a) Worldwide death due to\neach region\'s consumption of products',fontsize=16)
    
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    
    plt.xlim(0,350)
    
    plt.ylabel('')
    
    
    for rid in range(0,np.shape(mtbl_cons_spe.index)[0]):
        plt.text(mtbl_cons_spe['death'].iloc[rid]+0.5,rid,mtbl_cons_spe.iloc[rid,2],alpha=1,rotation=0,
                 horizontalalignment='left',#fontweight = 'bold',
                 verticalalignment='center',fontsize=16,
                 multialignment='center')#,fontweight='bold') #,transform=ax.transAxes
    
    
    #--------------------------------------------------------------------------
    #'Local' deposition due to each region’s consumption of products
    ax2 = fig.add_subplot(222) #axes([0,0,1,1], axisbg='w', frame_on=False)
    mtbl_cons_spe_lc = pd.DataFrame(np.zeros(len(regions_name)),index=regions_name,columns=['death'])
    for rid,reg in enumerate(regions_name):
        mtbl_cons_spe_lc.loc[reg,'death'] = itbl_cons_spe.iloc[rid,rid]
        
    mtbl_cons_spe_lc['colors'] = cmap
    mtbl_cons_spe_lc['region'] = mtbl_cons_spe_lc.index
    
    dep_str = np.round(mtbl_cons_spe_lc['death'],2)
    dep_str = dep_str.apply(topct)
    mtbl_cons_spe_lc.index = dep_str
    mtbl_cons_spe_lc.sort_values('death',inplace=True)
    
    f_spe = mtbl_cons_spe_lc['death'].plot(ax = ax2,kind='barh', colors = mtbl_cons_spe_lc['colors'],width = 0.8, legend=False)
#    plt.tight_layout(pad=0.1,w_pad = 1.25,h_pad=1.8)
#    plt.xticks(rotation = 0,size=18)
#    plt.yticks(size=18)
    plt.title('(b) \'Local\' death due to\neach region\'s consumption of products',fontsize=16)
    
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    
    plt.xlim(0,350)
    plt.ylabel('')
    
    
    for rid in range(0,np.shape(mtbl_cons_spe.index)[0]):
        plt.text(mtbl_cons_spe_lc['death'].iloc[rid]+0.5,rid,mtbl_cons_spe_lc.iloc[rid,2],alpha=1,rotation=0,
                 horizontalalignment='left',#fontweight = 'bold',
                 verticalalignment='center',fontsize=16,
                 multialignment='center')#,fontweight='bold') #,transform=ax.transAxes


    
    #--------------------------------------------------------------------------
    #Deposition outside region due to each region’s consumption of products
    ax3 = fig.add_subplot(223) #axes([0,0,1,1], axisbg='w', frame_on=False)
    mtbl_cons_spe_out = itbl_cons_spe_tot.to_frame(name='death')
    mtbl_cons_spe_lc.set_index('region',inplace=True)
    
    mtbl_cons_spe_out['death'] = mtbl_cons_spe_out['death']  - mtbl_cons_spe_lc['death']
    
    mtbl_cons_spe_out['colors'] = cmap
    mtbl_cons_spe_out['region'] = mtbl_cons_spe_out.index
    
    dep_str = np.round(mtbl_cons_spe_out['death'],2)
    dep_str = dep_str.apply(topct)
    mtbl_cons_spe_out.index = dep_str
    mtbl_cons_spe_out.sort_values('death',inplace=True)
    
    f_spe = mtbl_cons_spe_out['death'].plot(ax = ax3,kind='barh', colors = mtbl_cons_spe_out['colors'],width = 0.8, legend=False)
#    plt.tight_layout(pad=0.1,w_pad = 1.25,h_pad=1.8)
#    plt.xticks(rotation = 0,size=18)
#    plt.yticks(size=18)
    plt.title('(c) Death outside region due to\neach region\'s consumption of products',fontsize=16)
    
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    
    plt.xlim(0,45)
    plt.ylabel('')
    
    
    for rid in range(0,np.shape(mtbl_cons_spe.index)[0]):
        plt.text(mtbl_cons_spe_out['death'].iloc[rid]+0.5,rid,mtbl_cons_spe_out.iloc[rid,2],alpha=1,rotation=0,
                 horizontalalignment='left',#fontweight = 'bold',
                 verticalalignment='center',fontsize=16,
                 multialignment='center')#,fontweight='bold') #,transform=ax.transAxes
        
    
    
    

    #--------------------------------------------------------------------------
    #Deposition in each region due to other regions’ consumption of products
    ax4 = fig.add_subplot(224) #axes([0,0,1,1], axisbg='w', frame_on=False)
    mtbl_cons_spe_oth = itbl_base_spe_tot.to_frame(name='death')
    
    mtbl_cons_spe_oth['death'] = mtbl_cons_spe_oth['death']  - mtbl_cons_spe_lc['death']
    
    mtbl_cons_spe_oth['colors'] = cmap
    mtbl_cons_spe_oth['region'] = mtbl_cons_spe_oth.index
    
    dep_str = np.round(mtbl_cons_spe_oth['death'],2)
    dep_str = dep_str.apply(topct)
    mtbl_cons_spe_oth.index = dep_str
    mtbl_cons_spe_oth.sort_values('death',inplace=True)
    
    f_spe = mtbl_cons_spe_oth['death'].plot(ax = ax4,kind='barh', colors = mtbl_cons_spe_oth['colors'],width = 0.8, legend=False)
#    plt.tight_layout(pad=0.1,w_pad = 1.25,h_pad=1.8)
#    plt.xticks(rotation = 0,size=18)
#    plt.yticks(size=18)
    plt.title('(d) Death in each region due to\nother regions\' consumption of products',fontsize=16)
    
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    
    plt.xlim(0,80)
    plt.ylabel('')
    
    
    for rid in range(0,np.shape(mtbl_cons_spe.index)[0]):
        plt.text(mtbl_cons_spe_oth['death'].iloc[rid]+0.5,rid,mtbl_cons_spe_oth.iloc[rid,2],alpha=1,rotation=0,
                 horizontalalignment='left',#fontweight = 'bold',
                 verticalalignment='center',fontsize=16,
                 multialignment='center')#,fontweight='bold') #,transform=ax.transAxes
        
    
    
    
    of_plot = odir_plot + 'Barplot_Consumption-based_EmisAmount_'+spe+'.png'
    plt.savefig(of_plot, dpi=300,bbox_inches='tight',pad=0.1)    


        
        




