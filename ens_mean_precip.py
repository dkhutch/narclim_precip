import numpy as np
import netCDF4 as nc
import os

hist_0, hist_1 = 1991, 2010
scen_0, scen_1 = 2081, 2100

models = ['ACCESS-ESM1-5',
          'EC-Earth3-Veg',
          'MPI-ESM1-2-HR',
          'NorESM2-MM',
          'UKESM1-0-LL']

scenarios = ['historical','ssp126','ssp245','ssp370']

for ss in scenarios:
    if ss == 'historical':
        t0, t1 = hist_0, hist_1
    elif ss[:3] == 'ssp':
        t0, t1 = scen_0, scen_1
    flist = []
    for mm in models:
        memfile = f'{mm}/{mm}_rx1day_{ss}_{t0}_{t1}_mean.nc'
        flist.append(memfile)
    fstr = ' '.join(flist)
    outfile = f'ens_{ss}_rx1day_{t0}_{t1}.nc'
    cmd = f'ncea {fstr} {outfile}'
    print(cmd)
    os.system(cmd)

