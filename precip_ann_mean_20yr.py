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

origdir = os.getcwd()

for mm in models:
    os.chdir(mm)
    for ss in scenarios:
        flist = []
        if ss == 'historical':
            t0, t1 = hist_0, hist_1
        elif ss[:3] == 'ssp':
            t0, t1 = scen_0, scen_1
        text_f = f'{ss}_pr_rx1day'
        for tt in range(t0, t1+1):
            flist.append(f'{mm}_{text_f}_{tt}_ann.nc')
        fstring = ' '.join(flist)
        outfile = f'{mm}_rx1day_{ss}_{t0}_{t1}_ann.nc'
        cmd = f'ncra -O {fstring} {outfile}'
        print(cmd)
        os.system(cmd)
    os.chdir(origdir)
