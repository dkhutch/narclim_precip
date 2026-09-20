import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import geopandas as gpd
import cmaps

plt.rcParams['font.family'] = 'Helvetica'
plt.rcParams['font.size'] = 14

aus_states = gpd.read_file('../states/STE_2021_AUST_GDA2020.shp')
nsw = aus_states[aus_states['STE_NAME21'] == 'New South Wales']

histfile = 'ens_historical_rx1day_1991_2010.nc'
ssp126file = 'ens_ssp126_rx1day_2081_2100.nc'
ssp245file = 'ens_ssp245_rx1day_2081_2100.nc'
ssp370file = 'ens_ssp370_rx1day_2081_2100.nc'


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

pr_126 = (pr_126 - pr_hist) / pr_hist * 100
pr_245 = (pr_245 - pr_hist) / pr_hist * 100
pr_370 = (pr_370 - pr_hist) / pr_hist * 100

djf = [0,1,11]
jja = [5,6,7]

pr_126_djf = np.mean(pr_126[djf,:,:], axis=0)
pr_245_djf = np.mean(pr_245[djf,:,:], axis=0)
pr_370_djf = np.mean(pr_370[djf,:,:], axis=0)

# nsw.boundary.plot(linewidth=0.5, color='black')

xlims = [140, 154]
ylims = [-38, -28]

fig = plt.figure(figsize=(12,6))
gs = fig.add_gridspec(1,3)
(ax1, ax2, ax3) = gs.subplots()


levs = np.arange(-40, 41, 5)

nsw.boundary.plot(ax=ax1, linewidth=0.5, color='black')
h=ax1.contourf(lon, lat, pr_126_djf, levs, cmap=cmaps.MPL_BrBG, extend='both')
ax1.set_title('Low emissions')
# ax1.set_colorbar()
ax1.set_xlim(xlims)
ax1.set_ylim(ylims)
ax1.set_ylabel('Latitude (' + u'\xb0' + 'N)')

ax1.set_xlabel('Longitude (' + u'\xb0' + 'E)')

nsw.boundary.plot(ax=ax2, linewidth=0.5, color='black')
ax2.contourf(lon, lat, pr_245_djf, levs, cmap=cmaps.MPL_BrBG, extend='both')
ax2.set_title('Medium emissions')
# ax2.set_colorbar()
ax2.set_xlim(xlims)
ax2.set_ylim(ylims)

ax2.set_xlabel('Longitude (' + u'\xb0' + 'E)')

nsw.boundary.plot(ax=ax3, linewidth=0.5, color='black')
ax3.contourf(lon, lat, pr_370_djf, levs, cmap=cmaps.MPL_BrBG, extend='both')
ax3.set_title('High emissions')
# ax3.set_colorbar()
ax3.set_xlim(xlims)
ax3.set_ylim(ylims)

ax3.set_xlabel('Longitude (' + u'\xb0' + 'E)')

plt.subplots_adjust(bottom=0.2, top=0.95, left=0.08, right=0.95)

# tuple (left, bottom, width, height)
cbar_ax = fig.add_axes([0.2, 0.2, 0.62, 0.04])
fig.colorbar(h, cax=cbar_ax, orientation='horizontal', label='% change in summer extreme rain')

plt.savefig('370.pdf', dpi=500)
plt.close('all')