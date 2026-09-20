import numpy as np
import netCDF4 as nc
import os

basedir = 'https://thredds.nci.org.au/thredds/dodsC/zz63/NARCliM2-0/output-CMIP6/DD/NARCliM2-0-SEAus-04/NSW-Government'
model_dict = {'ACCESS-ESM1-5': 'r6i1p1f1',
             'EC-Earth3-Veg':  'r1i1p1f1',
             'MPI-ESM1-2-HR':  'r1i1p1f1',
             'NorESM2-MM':     'r1i1p1f1',
             'UKESM1-0-LL':    'r1i1p1f2'}
scenarios = ['historical','ssp126','ssp245','ssp370']
wrf = 'NARCliM2-0-WRF412R5'
n2_tag = 'NARCliM2-0-SEAus-04'
nsw = 'NSW-Government'
version = 'v1-r1'
freq = 'day'

hist_0, hist_1 = 1951, 2014
scen_0, scen_1 = 2081, 2100

jan = '0101'
dec_normal = '1231'
dec_ukesm = '1230'

file_dump = 'file_dump.txt'
fdump = open(file_dump,'w')

# for ss in ['historical','ssp370']:
# for ss in ['ssp126','ssp245']:
for ss in scenarios:
    for mm in model_dict:
        cmd = f'mkdir -p {mm}'
        os.system(cmd)
        if mm=='UKESM1-0-LL':
            dec=dec_ukesm
        else:
            dec=dec_normal
        ridx = model_dict[mm]
        run_dir = f'{basedir}/{mm}/{ss}/{ridx}/{wrf}/{version}/{freq}/pr/latest'
        if ss == 'historical':
            t0, t1 = hist_0, hist_1
        elif ss[:3] == 'ssp':
            t0, t1 = scen_0, scen_1
        for tt in range(t0, t1+1):
            fname = f'pr_{n2_tag}_{mm}_{ss}_{ridx}_{nsw}_{wrf}_{version}_day_{tt}{jan}-{tt}{dec}.nc'
            fullfile = f'{run_dir}/{fname}'
            outfile = f'{mm}/{mm}_{ss}_pr_rx1day_{tt}.nc'

            fdump.write(f'{fullfile},{outfile}\n')

fdump.close()






