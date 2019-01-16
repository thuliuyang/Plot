# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 15:51:07 2016

@author: YIXUAN
#绘制重点区域production和consumptipn-based的NH3导致的过早死亡（mass)
#yzheng,2018/06/20
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import os
from mpl_toolkits.basemap import Basemap
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import seaborn.apionly as sns
np.seterr(all = 'ignore')


def make_colormap(seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)

def cmap_discretize_2(cmap, N):
    """Return a discrete colormap from the continuous colormap cmap.

        cmap: colormap instance, eg. cm.jet. 
        N: number of colors.

    Example
        x = resize(arange(100), (5,100))
        djet = cmap_discretize(cm.jet, 5)
        imshow(x, cmap=djet)
    """

    if type(cmap) == str:
        cmap = plt.get_cmap(cmap)
    colors_i = np.concatenate((np.linspace(0, 1., N), (0.,0.,0.,0.)))
    colors_rgba = cmap(colors_i)
    indices = np.linspace(0, 1., N+1)
    cdict = {}
    for ki,key in enumerate(('red','green','blue')):
        cdict[key] = [ (indices[i], colors_rgba[i-1,ki], colors_rgba[i,ki])
                       for i in range(N+1) ]
    # Return colormap object.
    return mcolors.LinearSegmentedColormap(cmap.name + "_%d"%N, cdict, 1024)

Fig = 'Map_deaths'

year = 2011
syr = str(year)
regions_name_plot = ['global','Rest of East Asia','China','India','USA','Western Europe']
scenarios_con = [] #['base.' + syr,'fixmet_no_anth.' + syr ]
scenarios_pro = [] 
for i in range(1,13):
    scenarios_con.append('con'+str(i))
    scenarios_pro.append('pro'+str(i))
    
legend_ticks = [0,0.1,1,2,4,6,8,10,20,40,60,80,100,200,400,600,800,1000,2000,4000,6000,8000,10000]
num_colors_input = len(legend_ticks)-1

#------
cmap = sns.color_palette("Reds", num_colors_input)
cmap[0] = (1,1,1)
cmap = matplotlib.colors.ListedColormap(cmap)
bounds = legend_ticks

norm = matplotlib.colors.BoundaryNorm(boundaries=bounds, ncolors=num_colors_input) #num_colors_input)

idir_dep = './conemis/' 

odir_plot = './'

if not os.path.exists(odir_plot):
    os.makedirs(odir_plot)

nr_spe = ['total_nitrogen']
nr_spe_map = {'total_nitrogen':['total'],
              'NHx':['nh4wet','nhxdry'],
              'NOy':['no3wet','noydry']}
    
itbls_dep = {}

for sid,scen in enumerate(regions_name_plot):
    if_nrdep = idir_dep+'deaths_all_nh3_' + scen + '_con_agr.nc'  
    itbl_dep = Dataset(if_nrdep)['death'][:]          
    itbls_dep[scen] = itbl_dep.copy()


        
of_plot = odir_plot + Fig + '_6regions.png'

fig = plt.figure(figsize=(20, 13))
for rid,reg in enumerate(regions_name_plot):    
    arr_base_mass = itbls_dep[reg].copy()
    syr = '%4d' % year
        
    #for spid,spe in enumerate(nr_spe):
    for pcid,pro_con in enumerate(['con']):
    #arr_base_flux = Dataset(if_base)[spe+'_flux'][:]
        arr_mass = itbls_dep[reg]
        arr_mass = arr_mass
        ax = fig.add_subplot(3,2,rid+1) #axes([0,0,1,1], axisbg='w', frame_on=False)
        m = Basemap(ellps = 'WGS84',
            llcrnrlon=-181.250 ,llcrnrlat=-60, urcrnrlon=178.750 ,urcrnrlat=80.,
            suppress_ticks=True)#resolution='i',
        
        m.drawmapboundary()
        

        lat = np.arange(-90,90,1)
        lon = np.arange(-180,180,1)
        x,y = np.meshgrid(lon,lat)
        x,y = m(x,y)    

        cs = m.pcolor(x,y,np.squeeze(arr_mass),norm=norm,cmap=cmap,alpha=1)
        print(reg,pro_con,np.max(arr_mass))

        m.readshapefile('./World_Countries/World_Countries',
                'world',drawbounds=True,linewidth=0.4,color='k',
                zorder=2) 
        plt.tight_layout(pad=0.4,w_pad =2 ,h_pad=0.5)

num_colors = num_colors_input
mappable = cm.ScalarMappable(norm=norm,cmap=cmap)
mappable.set_array([])
mappable.set_clim(-0.5, 10000)
#cbar_ax = fig.add_axes([0.01, -0.04, 0.98,0.02])
cbar_ax = fig.add_axes([0.01, -0.025, 0.98,0.02])

colorbar = plt.colorbar(mappable,cax=cbar_ax, 
                                norm=norm,ticks=bounds,boundaries = bounds, spacing='uniform',orientation='horizontal')
 

slegend_ticks = [str(i) for i in legend_ticks]

colorbar.set_ticklabels(slegend_ticks)    
colorbar.ax.tick_params(labelsize=22)
label = 'Deaths per 100 km × 100 km'
colorbar.set_label(label.encode('base64','strict'),fontsize = 32) 
plt.savefig(of_plot, dpi=300,bbox_inches='tight')    

