import pandas as pd
import numpy as np

Q_PATH = r'C:\Users\jonst\OneDrive - Menntaský\Vatnafræði\Lokaverkefni\lamah_ice\D_gauges\2_timeseries\daily\ID_91.csv'
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

with open('debug.txt', 'w') as f:
    f.write(str(clim['Q']))
    f.write('\n')
    f.write(str(df['Q'].describe()))