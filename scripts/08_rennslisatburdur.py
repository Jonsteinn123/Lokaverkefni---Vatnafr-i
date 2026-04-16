import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

Q_PATH   = r'C:\Users\jonst\OneDrive - Menntaský\Vatnafræði\Lokaverkefni\lamah_ice\D_gauges\2_timeseries\daily\ID_91.csv'
MET_PATH = r'C:\Users\jonst\OneDrive - Menntaský\Vatnafræði\Lokaverkefni\lamah_ice\A_basins_total_upstrm\2_timeseries\daily\meteorological_data\ID_91.csv'

# ── Lesa gögn ─────────────────────────────────────────────────────────────────
q = pd.read_csv(Q_PATH, sep=';')
q['date'] = pd.to_datetime(q[['YYYY','MM','DD']].rename(columns={'YYYY':'year','MM':'month','DD':'day'}))
q = q.set_index('date').loc['1993-10-01':'2023-09-30']
q.loc[q['qobs'] < 0, 'qobs'] = np.nan

met = pd.read_csv(MET_PATH, sep=';')
met['date'] = pd.to_datetime(met[['YYYY','MM','DD']].rename(columns={'YYYY':'year','MM':'month','DD':'day'}))
met = met.set_index('date').loc['1993-10-01':'2023-09-30']

df = q[['qobs']].join(met[['prec','2m_temp_mean']])
df.columns = ['Q', 'P', 'T']

# ── Finna 5 stærstu flóð og velja eitt ───────────────────────────────────────
top5 = df['Q'].nlargest(5)
print("5 stærstu flóðin:")
print(top5.round(1))

# Við veljum stærsta flóðið
peak_date = top5.index[0]
print(f"\nValið flóð: {peak_date.date()}, Q = {top5.iloc[0]:.1f} m³/s")

# 15 dagar fyrir og eftir topp
start = peak_date - pd.Timedelta(days=8)
end   = peak_date + pd.Timedelta(days=15)
ev = df.loc[start:end].copy()

# Tímamarkar – breyttu dagsetningarnar ef þú sérð eitthvað annað í myndinni
onset    = pd.Timestamp('1995-06-08')  # rennsli byrjar að hækka
rain_end = pd.Timestamp('1995-06-17')  # úrkoma lýkur
excess_end = pd.Timestamp('1995-06-26')  # breyttu ef þú sérð betri dagsetningu
# ── Mynd ─────────────────────────────────────────────────────────────────────
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
fig.suptitle(f'Rennslisatburður – Vatnsdalsá\n{start.date()} til {end.date()}',
             fontsize=13, fontweight='bold')

# Rennsli
ax1.plot(ev.index, ev['Q'], color='steelblue', linewidth=2)
ax1.fill_between(ev.index, ev['Q'], alpha=0.2, color='steelblue')
ax1.set_ylabel('Rennsli (m³/s)')
ax1.axvline(peak_date, color='red', linestyle='--', linewidth=1.5, label=f'Qmax = {top5.iloc[0]:.1f} m³/s')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Excess rain release time – frá lok úrkomu að grunnlínu
# Rennslið fer niður í ~25-30 m³/s (grunnlína) um 26. júní eða seinna


ax1.annotate('', xy=(excess_end, 15), xytext=(rain_end, 15),
             arrowprops=dict(arrowstyle='<->', color='darkorange', lw=1.5))
ax1.text(rain_end + (excess_end - rain_end)/2, 20, 'Excess rain\nrelease time',
         ha='center', color='darkorange', fontsize=8)

# Úrkoma
ax2.bar(ev.index, ev['P'], color='royalblue', alpha=0.7, width=0.8)
ax2.set_ylabel('Úrkoma (mm/dag)')
ax2.grid(True, alpha=0.3, axis='y')

# Hitastig
ax3.plot(ev.index, ev['T'], color='firebrick', linewidth=2)
ax3.axhline(0, color='gray', linestyle='--', linewidth=0.8)
ax3.fill_between(ev.index, ev['T'], 0, where=ev['T'] >= 0, alpha=0.15, color='firebrick')
ax3.fill_between(ev.index, ev['T'], 0, where=ev['T'] < 0, alpha=0.15, color='steelblue')
ax3.set_ylabel('Hitastig (°C)')
ax3.grid(True, alpha=0.3)


# Time-to-peak
ax1.annotate('', xy=(peak_date, 130), xytext=(onset, 130),
             arrowprops=dict(arrowstyle='<->', color='darkgreen', lw=1.5))
ax1.text((onset + (peak_date - onset)/2), 135, 'Time-to-peak', 
         ha='center', color='darkgreen', fontsize=9)

# Recession time
ax1.annotate('', xy=(end, 30), xytext=(peak_date, 30),
             arrowprops=dict(arrowstyle='<->', color='purple', lw=1.5))
ax1.text((peak_date + (end - peak_date)/2), 45, 'Recession time',
         ha='center', color='purple', fontsize=9)

# Excess rain release time
ax1.axvline(rain_end, color='royalblue', linestyle=':', linewidth=1.5, label='Lok úrkomu')
ax1.legend()
plt.tight_layout()
plt.savefig('figures/08_rennslisatburdur.png', dpi=150, bbox_inches='tight')
plt.show()
print("Myndin er komin!")