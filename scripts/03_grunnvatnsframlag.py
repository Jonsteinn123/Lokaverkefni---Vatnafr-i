import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lfilter


Q_PATH = r'C:\Users\jonst\OneDrive - Menntaský\Vatnafræði\Lokaverkefni\lamah_ice\D_gauges\2_timeseries\daily\ID_91.csv'

q = pd.read_csv(Q_PATH, sep=';')
q['date'] = pd.to_datetime(q[['YYYY','MM','DD']].rename(columns={'YYYY':'year','MM':'month','DD':'day'}))
q = q.set_index('date').loc['1993-10-01':'2023-09-30']
q.loc[q['qobs'] < 0, 'qobs'] = np.nan
Q = q['qobs'].copy()


# 1. BASEFLOW SEPARATION 
# ══════════════════════════════════════════════════════════════════════════════
def ladson_baseflow(Q, alpha=0.925, passes=3):
    """
    Ladson et al. (2013) digital filter – 3 pass (fram, aftur, fram).
    alpha = 0.925 er staðlað gildi fyrir daglegt rennsli.
    """
    q = Q.values.copy()
    nan_mask = np.isnan(q)
    
    q_filled = pd.Series(q).interpolate().values

    def single_pass(streamflow, forward=True):
        if not forward:
            streamflow = streamflow[::-1]
        bf = np.zeros(len(streamflow))
        bf[0] = streamflow[0]
        for t in range(1, len(streamflow)):
            bf[t] = (alpha * bf[t-1] +
                     (1 - alpha) / 2 * (streamflow[t] + streamflow[t-1]))
            bf[t] = min(bf[t], streamflow[t])
            bf[t] = max(bf[t], 0)
        if not forward:
            bf = bf[::-1]
        return bf

    bf = q_filled
    for i, forward in enumerate([True, False, True]):
        bf = single_pass(bf, forward=forward)
        bf = np.minimum(bf, q_filled)

    bf[nan_mask] = np.nan
    return bf

baseflow = ladson_baseflow(Q)
bf_series = pd.Series(baseflow, index=Q.index, name='baseflow')


# 2. BASEFLOW INDEX (BFI)
# ══════════════════════════════════════════════════════════════════════════════
BFI = np.nansum(baseflow) / np.nansum(Q.values)
print(f"Baseflow Index (BFI): {BFI:.3f}  ({BFI*100:.1f}%)")

# BFI per ár
df_bf = pd.DataFrame({'Q': Q, 'BF': bf_series})
annual_bfi = df_bf.resample('YS-OCT').apply(lambda x: np.nansum(x['BF']) / np.nansum(x['Q']))
print("\nBFI á ári (vatnsfræðilegt ár, okt–sep):")
print(annual_bfi.round(3))


from scipy import stats

# ══════════════════════════════════════════════════════════════════════════════
# 3. RECESSION ANALYSIS – log-línuleg aðhvarfsgreining
# ══════════════════════════════════════════════════════════════════════════════
def find_recession_segments(Q, min_length=10):
    q = Q.values
    segments = []
    i = 1
    while i < len(q) - 1:
        if not np.isnan(q[i]) and q[i] < q[i-1] and q[i] > 0.01:
            j = i
            while j < len(q) - 1 and not np.isnan(q[j]) and q[j] < q[j-1]:
                j += 1
            if j - i >= min_length:
                segments.append((Q.index[i-1:j], q[i-1:j]))
            i = j
        else:
            i += 1
    return segments

segments = find_recession_segments(Q, min_length=10)

# Sía út vetrarmánuði (des, jan, feb) 
segments = [s for s in segments if s[0][0].month not in [12, 1, 2]]

# Aðhvarfsgreining á hverja runu, finna bestu
best = max(segments, key=lambda s: stats.linregress(np.arange(len(s[1])), np.log(s[1]))[2]**2)
t = np.arange(len(best[1]))
slope, intercept, r, _, _ = stats.linregress(t, np.log(best[1]))
k = -1 / slope
Q0 = np.exp(intercept)

print(f"Besta runa: {best[0][0].date()} – {best[0][-1].date()}")
print(f"Recession constant k = {k:.1f} dagar")
print(f"R² = {r**2:.3f}")
# ══════════════════════════════════════════════════════════════════════════════
# 4. MYNDIR
# ══════════════════════════════════════════════════════════════════════════════

# — Mynd A: Baseflow separation, 2 ár sem dæmi —
fig, axes = plt.subplots(2, 1, figsize=(12, 8))
fig.suptitle('Baseflow Separation – Vatnsdalsá, Forsæludalur', fontsize=13, fontweight='bold')

# Heilt tímabil – BFI
ax = axes[0]
ax.fill_between(Q.index, Q.values, alpha=0.3, color='steelblue', label='Heildarrennsli Q')
ax.fill_between(bf_series.index, bf_series.values, alpha=0.6, color='teal', label=f'Grunnvatn (BFI = {BFI:.2f})')
ax.set_ylabel('Rennsli (m³/s)')
ax.set_title('1993–2023')
ax.legend()
ax.grid(True, alpha=0.3)

# Eitt ár nánar
zoom_start, zoom_end = '2010-10-01', '2012-09-30'
ax2 = axes[1]
ax2.fill_between(Q.loc[zoom_start:zoom_end].index, Q.loc[zoom_start:zoom_end].values,
                 alpha=0.3, color='steelblue', label='Heildarrennsli Q')
ax2.fill_between(bf_series.loc[zoom_start:zoom_end].index,
                 bf_series.loc[zoom_start:zoom_end].values,
                 alpha=0.6, color='teal', label='Grunnvatn')
ax2.set_ylabel('Rennsli (m³/s)')
ax2.set_title('Nærmynd: 2010–2012')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/03a_baseflow_separation.png', dpi=150, bbox_inches='tight')
plt.show()

# — Mynd B: Recession analysis scatter —
# — Mynd B: Recession analysis – log-línuleg aðhvarfsgreining —
fig2, axes2 = plt.subplots(1, 2, figsize=(12, 5))
fig2.suptitle('Recession Analysis – Vatnsdalsá, Forsæludalur', fontsize=13, fontweight='bold')

# Vinstri: Q(t)
ax3 = axes2[0]
t_fit = np.linspace(0, len(best[1])-1, 100)
Q_fit = Q0 * np.exp(-t_fit / k)
ax3.plot(best[0], best[1], 'bo-', markersize=5, label='Mælt rennsli')
ax3.plot(best[0][0] + pd.to_timedelta(t_fit, unit='D'),
         Q_fit, 'r--', linewidth=2,
         label=f'Q = {Q0:.0f}·e$^{{-t/{k:.1f}}}$')
ax3.set_xlabel('Dagsetning')
ax3.set_ylabel('Rennsli Q (m³/s)')
ax3.set_title('Q(t) með fitted línu')
ax3.legend()
ax3.grid(True, alpha=0.3)
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=30, ha='right')

# Hægri: ln(Q) á móti t
ax4 = axes2[1]
t_best = np.arange(len(best[1]))
ln_fit = intercept + slope * t_fit
ax4.plot(t_best, np.log(best[1]), 'bo', markersize=5, label='ln(Q) mælt')
ax4.plot(t_fit, ln_fit, 'r-', linewidth=2,
         label=f'y = {intercept:.2f} + ({slope:.4f})·t\nR² = {r**2:.3f}')
ax4.set_xlabel('Tími t (dagar frá upphafi)')
ax4.set_ylabel('ln(Q)')
ax4.set_title('ln(Q) sem fall af t')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/03b_recession_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

print("\nMyndirnar eru komnar!")
print(f"  → figures/03a_baseflow_separation.png")
print(f"  → figures/03b_recession_analysis.png")