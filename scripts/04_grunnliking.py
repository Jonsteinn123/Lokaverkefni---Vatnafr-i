# ══════════════════════════════════════════════════════════════════════════════
# Dæmi 4 – Tenging við grunnlíkingu vatnafræðinnar
# P = Q + ET + ΔS  →  ET = P - Q  (ΔS ≈ 0 yfir 30 ár)
# ══════════════════════════════════════════════════════════════════════════════

# Breyta úrkomu úr mm/dag í m³/s
# Flatarmál vatnasviðs þarf – sækjum úr gögnum
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

# Flatarmál vatnasviðsins í km² – þetta þarf að skoða í Catchment_attributes.csv
# Settu rétt gildi hér:
AREA_KM2 = 449.701
  # km²

# mm/dag → m³/s:  X mm/dag * area_m² / 1000 / 86400
area_m2 = AREA_KM2 * 1e6

# Nota df frá dæmi 2 (Q, P, T)
# P er í mm/dag, Q er í m³/s

# Meðalgildi yfir allt tímabilið
P_mean_mms = df['P'].mean()           # mm/dag
Q_mean_m3s = df['Q'].mean()           # m³/s

# Breyta Q í mm/dag til samanburðar
Q_mean_mms = Q_mean_m3s * 86400 / area_m2 * 1000

ET_mean_mms = P_mean_mms - Q_mean_mms

print(f"Meðalúrkoma  P  = {P_mean_mms:.2f} mm/dag")
print(f"Meðalrennsli Q  = {Q_mean_mms:.2f} mm/dag")
print(f"Meðaluppgufun ET = {ET_mean_mms:.2f} mm/dag")
print(f"\nÁrleg P  = {P_mean_mms*365:.1f} mm/ár")
print(f"Árleg Q  = {Q_mean_mms*365:.1f} mm/ár")
print(f"Árleg ET = {ET_mean_mms*365:.1f} mm/ár")