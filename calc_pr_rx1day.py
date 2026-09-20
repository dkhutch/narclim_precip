#!/usr/bin/env python
import numpy as np
import netCDF4 as nc
import os
import argparse

parser = argparse.ArgumentParser(description='script to calculate pr_rx1day from NarCLIM data')
parser.add_argument("input", help='file containing comma seprated names of Narclim precip data and output data')
args = parser.parse_args()

with open(args.input) as file:
    lines = [line.rstrip() for line in file]

nline = len(lines)

# note we put a zero at the start of calendar to enable the cumsum idx later...
noleap_mon = [0,31,28,31,30,31,30,31,31,30,31,30,31]
leap_mon   = [0,31,29,31,30,31,30,31,31,30,31,30,31]
uk_mon     = [0,30,30,30,30,30,30,30,30,30,30,30,30]

noleap_idx = np.cumsum(noleap_mon)
leap_idx   = np.cumsum(leap_mon)
uk_idx     = np.cumsum(uk_mon)

for i in range(nline):
    fnames = lines[i].split(',')
    infile = fnames[0]
    outfile = fnames[1]

    if os.path.exists(outfile):
        print(outfile, 'exists, skipping...')
        continue
    else:
        print('processing', outfile)

    f = nc.Dataset(infile,'r')
    rlat = f.variables['rlat'][:]
    rlat_atts = f.variables['rlat'].__dict__
    rlon = f.variables['rlon'][:]
    rlon_atts = f.variables['rlon'].__dict__    
    lat = f.variables['lat'][:]
    lat_atts = f.variables['lat'].__dict__ 
    lon = f.variables['lon'][:]
    lon_atts = f.variables['lon'].__dict__   
    nlat, nlon = lon.shape
    time = f.variables['time'][:]
    time_atts = f.variables['time'].__dict__
    pr = f.variables['pr'][:]
    pr_atts = f.variables['pr'].__dict__    
    del pr_atts['_FillValue']

    f.close()

    if time.shape[0] == 365:
        tlims = noleap_idx
    elif time.shape[0] == 366:
        tlims = leap_idx
    elif time.shape[0] == 360:
        tlims = uk_idx 

    pr_rx1day = np.ma.masked_array(np.zeros((12, nlat, nlon), 'f4'), False)
    time_mon = np.zeros(12, 'f8')
    for zz in range(12):
        z0 = tlims[zz]
        z1 = tlims[zz+1]
        pr_rx1day[zz, :, :] = np.max(pr[z0:z1, :, :], axis=0)
        time_mon[zz] = np.mean(time[z0:z1])

    f = nc.Dataset(outfile,'w')
    f.history = f'get_precip.py on {infile}'

    f.createDimension('rlat', nlat)
    f.createDimension('rlon', nlon)
    f.createDimension('time', 0)

    time_o = f.createVariable('time', 'f8', ('time'))
    time_o.setncatts(time_atts)
    time_o[:] = time_mon[:]

    rlon_o = f.createVariable('rlon', 'f8', ('rlon'))
    rlon_o.setncatts(rlon_atts)
    rlon_o[:] = rlon[:]

    rlat_o = f.createVariable('rlat', 'f8', ('rlat'))
    rlat_o.setncatts(rlat_atts)
    rlat_o[:] = rlat[:]

    lon_o = f.createVariable('lon', 'f8', ('rlat','rlon'), zlib=True, complevel=5)
    lon_o.setncatts(lon_atts)
    lon_o[:] = lon[:]

    lat_o = f.createVariable('lat', 'f8', ('rlat','rlon'), zlib=True, complevel=5)
    lat_o.setncatts(lat_atts)
    lat_o[:] = lat[:]

    pr_rx1day_o = f.createVariable('pr_rx1day', 'f8', ('time','rlat','rlon'), 
        fill_value=-1.0e20, zlib=True, complevel=5)
    pr_rx1day_o.setncatts(pr_atts)
    pr_rx1day_o[:] = pr_rx1day[:]

    f.close()




