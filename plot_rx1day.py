import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import geopandas as gpd
import cmaps

plt.rcParams['font.family'] = 'Helvetica'
plt.rcParams['font.size'] = 14

# Shapefile for states and territories:
# https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs/edition-3-july-2021-june-2026/access-and-downloads/digital-boundary-files/STE_2021_AUST_SHP_GDA2020.zip
aus_states = gpd.read_file('../states/STE_2021_AUST_GDA2020.shp')
nsw = aus_states[aus_states['STE_NAME21'] == 'New South Wales']

histfile = 'ens_historical_rx1day_1991_2010_ann.nc'
ssp126file = 'ens_ssp126_rx1day_2081_2100_ann.nc'
ssp245file = 'ens_ssp245_rx1day_2081_2100_ann.nc'
ssp370file = 'ens_ssp370_rx1day_2081_2100_ann.nc'


f = nc.Dataset(histfile,'r')
lon = f.variables['lon'][:]
lat = f.variables['lat'][:]
pr_hist = f.variables['pr_rx1day'][:] * 86400.
f.close()

f = nc.Dataset(ssp126file,'r')
pr_126 = f.variables['pr_rx1day'][:] * 86400.
f.close()

f = nc.Dataset(ssp245file,'r')
pr_245 = f.variables['pr_rx1day'][:] * 86400.
f.close()

f = nc.Dataset(ssp370file,'r')
pr_370 = f.variables['pr_rx1day'][:] * 86400.
f.close()

pr_hist = np.squeeze(pr_hist)

xlims = [140, 154]
ylims = [-38, -28]

fig = plt.figure(figsize=(8,6))
gs = fig.add_gridspec(1,1)
ax1 = gs.subplots()

levs = np.arange(20, 121, 10)

nsw.boundary.plot(ax=ax1, linewidth=1, color='black')
h=ax1.contourf(lon, lat, pr_hist, levs, cmap=cmaps.BlGrYeOrReVi200_r, extend='max')
ax1.set_title('Historical baseline Rx1day 1991-2010')
# ax1.set_colorbar()
ax1.set_xlim(xlims)
ax1.set_ylim(ylims)
ax1.set_ylabel('Latitude (' + u'\xb0' + 'N)')
ax1.set_xlabel('Longitude (' + u'\xb0' + 'E)')


plt.subplots_adjust(bottom=0.3, top=0.95, left=0.08, right=0.95)

# tuple (left, bottom, width, height)
cbar_ax = fig.add_axes([0.25, 0.15, 0.55, 0.04])
fig.colorbar(h, cax=cbar_ax, orientation='horizontal', label='Annual extreme rain Rx1day (mm/day)')

plt.savefig('hist.pdf', dpi=500)
plt.close('all')