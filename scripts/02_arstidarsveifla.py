import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

Q_PATH   = r'C:\Users\jonst\OneDrive - Menntaský\Vatnafræði\Lokaverkefni\lamah_ice\D_gauges\2_timeseries\daily\ID_91.csv'
MET_PATH = r'C:\Users\jonst\OneDrive - Menntaský\Vatnafræði\Lokaverkefni\lamah_ice\A_basins_total_upstrm\2_timeseries\daily\meteorological_data\ID_91.csv'

q = pd.read_csv(Q_PATH, sep=';')
q['date'] = pd.to_datetime(q[['YYYY','MM','DD']].rename(columns={'YYYY':'year','MM':'month','DD':'day'}))
q = q.set_index('date').loc['1993-10-01':'2023-09-30']
q.loc[q['qobs'] < 0, 'qobs'] = np.nan

met = pd.read_csv(MET_PATH, sep=';')
met['date'] = pd.to_datetime(met[['YYYY','MM','DD']].rename(columns={'YYYY':'year','MM':'month','DD':'day'}))
met = met.set_index('date').loc['1993-10-01':'2023-09-30']

df = q[['qobs']].join(met[['prec','2m_temp_mean']])
df.columns = ['Q', 'P', 'T']
clim = df.groupby(df.index.month).mean()

months = ['Jan','Feb','Mar','Apr','Maí','Jún','Júl','Ágú','Sep','Okt','Nóv','Des']

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
fig.suptitle('Árstíðasveifla – Vatnsdalsá, Forsæludalur (ID 91)\n1993–2023', fontsize=14, fontweight='bold')

ax1.plot(range(1,13), clim['T'].values, color='firebrick', linewidth=2, marker='o')
ax1.axhline(0, color='gray', linestyle='--', linewidth=0.8)
ax1.fill_between(range(1,13), clim['T'].values, 0, where=clim['T'].values>=0, alpha=0.15, color='firebrick', label='Yfir 0°C')
ax1.fill_between(range(1,13), clim['T'].values, 0, where=clim['T'].values<0, alpha=0.15, color='steelblue', label='Undir 0°C')
ax1.set_ylabel('Hitastig (°C)', fontsize=11)
ax1.set_title('Meðalhitastig')
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)

ax2.bar(range(1,13), clim['P'].values, color='steelblue', alpha=0.8, width=0.6)
ax2.set_ylabel('Úrkoma (mm/dag)', fontsize=11)
ax2.set_title('Meðalúrkoma')
ax2.grid(True, alpha=0.3, axis='y')

ax3.fill_between(range(1,13), clim['Q'].values, alpha=0.4, color='teal')
ax3.plot(range(1,13), clim['Q'].values, color='teal', linewidth=2, marker='o')
ax3.set_ylabel('Rennsli (m³/s)', fontsize=11)
ax3.set_title('Meðalrennsli')
ax3.grid(True, alpha=0.3)
ax3.set_xticks(range(1,13))
ax3.set_xticklabels(months, fontsize=10)
ax3.set_xlim(0.5, 12.5)

plt.tight_layout()
plt.savefig('figures/02_arstidarsveifla.png', dpi=150, bbox_inches='tight')
import os
print("Vistað í:", os.path.abspath('figures/02_arstidarsveifla.png'))
print("Skrá til:", os.path.exists('figures/02_arstidarsveifla.png'))
plt.show()
print("Myndin er komin!")
