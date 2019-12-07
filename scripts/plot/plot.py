#!/usr/bin/env python
#############################################
# Original Matlab Author: Joseph Schoonover #
# Adaptation to Python:   Adam Kubaryk      #
#############################################

import matplotlib
matplotlib.use('agg') # cannot plt.show() with this, but pyplot fails on the compute nodes without an X Server
import matplotlib.pyplot as plt
from matplotlib import ticker
from mpl_toolkits.basemap import Basemap
from os import listdir, path, makedirs
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from netCDF4 import Dataset
import glob
import yaml
import io
import numpy as np
import errno

def mkdir_p(file_path):
  try:
    makedirs(file_path)
  except OSError as e:
    if e.errno == errno.EEXIST and path.isdir(file_path):
      pass
    else:
      raise

# ----------------------------------------------------------------------------- #
## parsing options
parser = ArgumentParser(description='Make plots from height-gridded NetCDF IPE output', formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--input_directory',  help='directory where IPE height-gridded NetCDF files are stored', type=str, required=True)
parser.add_argument('-o', '--output_directory', help='directory where plots are stored', type=str, required=True)
args = parser.parse_args()

# create output path if it doesn't yet exist
mkdir_p(args.output_directory)

# Parse the plot_settings.yaml file
with open('plot_settings.yaml', 'r' ) as stream:
  plot_settings = yaml.load(stream)


for plt_obj in plot_settings["plots"]:

  # If the netcdf_prefix is given, create a list of files
  if plt_obj['plot']['netcdf_prefix']:
    nc_files = glob.glob(args.input_directory+'/'+plt_obj['plot']['netcdf_prefix']+'*.nc')


  mymin   = plt_obj['plot']['minimum']
  mymax   = plt_obj['plot']['maximum']
  ncolors = plt_obj['plot']['n_colors']
  myticks = plt_obj['plot']['n_ticks']
  units   = plt_obj['plot']['units']
  ncontours = plt_obj['plot']['n_contours']
  mycolormap = plt_obj['plot']['color_map']
  

  for nc_file in nc_files:

    # Gather data
    dataset = Dataset(path.join(args.input_directory,nc_file))
    timestamp = nc_file.split(".")[3]
    year    = timestamp[0:4]
    month   = timestamp[4:6]
    day     = timestamp[6:8]
    hour    = timestamp[8:10]
    minute  = timestamp[10:12]
    datestamp = day+'/'+month+'/'+year+' UT '+hour+':'+minute
    print( ' Reading file     : '+path.join(args.input_directory,nc_file) )
    print( ' Model date       : '+datestamp)
    print( ' Reading variable : '+plt_obj['plot']['netcdf_name'])
  

    for plot_type in plt_obj['plot']['type']:

      print( ' > > Creating  '+plot_type+' plot.')

      lon = dataset.variables['longitude'][:]
      if plot_type == 'polar':
        lon = np.append(lon,lon[0])

      lat = dataset.variables['latitude'][:]
      if plt_obj['plot']['altitude'] > 0 :
        # Spatial 3-D data set
        # Ultimately, we will do vertical interpolation here.
        data = dataset.variables[plt_obj['plot']['netcdf_name']][0,47,:,:]
      else:
        # Spatial 2-D data set
        data = dataset.variables[plt_obj['plot']['netcdf_name']][0,:,:]


      plt.figure()
  
      if plot_type == 'polar':
        m = Basemap(lon_0=0,lat_0=90,projection='ortho')
      else:
        m = Basemap(llcrnrlon=lon[0],llcrnrlat=lat[0],urcrnrlon=lon[-1],urcrnrlat=lat[-1],projection='cyl')
  
      lon,lat = np.meshgrid(lon,lat)
      x,y = m(lon,lat)
  
      if plot_type == 'polar':
        b = np.reshape(data[:,0],(-1,1))
        data = np.hstack((data,b))
  
      m.drawcoastlines()
      m.drawstates()
      m.drawcountries()
  
      if mymin == mymax :
        cmap = m.contourf(x,y, data)
      else:
        cmap = m.contourf(x,y, data, np.linspace(mymin, mymax, ncolors), cmap=mycolormap)
  
      if ncontours > 0:
        m.contour(x,y, data, np.linspace(mymin, mymax, ncontours), colors=plot_settings['plot_settings']['contour_line_color'], 
                                                                   linewidths=plot_settings['plot_settings']['contour_line_width'])	
  
      if mymin == mymax :
         cbar = m.colorbar(cmap)
      else:
        cbar = m.colorbar(cmap, ticks=np.linspace(mymin,mymax,myticks))
  
      cbar.ax.yaxis.label.set_font_properties(matplotlib.font_manager.FontProperties(family=plot_settings['plot_settings']['font_family'],
                                                                                     size=plot_settings['plot_settings']['font_size']))
      cbar.ax.set_title('['+units+']',y=1.04)
  
      if plot_type == 'mercator':
         plt.xticks([0, 90, 180, 270, 360],['$0^o E$', '$90^o E$', '$180^o E$', '$270^o E$', '$360^o E$'])
         plt.yticks([-90, -45, 0, 45, 90],['$90^o S$', '$45^o S$', '$0^o$', '$45^o N$', '$90^o N$'])
         plt.grid()
      
      plt.title(plt_obj['plot']['title']+'\n'+datestamp, fontsize=plot_settings['plot_settings']['title_font_size'], 
                                                     fontname=plot_settings['plot_settings']['font_family'])
      # output
      plt.savefig(path.join(args.output_directory,plt_obj['plot']['save_name']+'.'+plot_type+'.'+timestamp+'.eps'))
      plt.close()
