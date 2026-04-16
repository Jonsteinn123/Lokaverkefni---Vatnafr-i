import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gumbel_r, lognorm, pearson3
import os
os.makedirs('figures', exist_ok=True)

# Lesa gögn
df = pd.read_csv(r'C:\Users\jonst\OneDrive - Menntaský\Vatnafræði\Lokaverkefni\lamah_ice\D_gauges\2_timeseries\daily\ID_91.csv', sep=';')

# Dagsetning
df["date"] = pd.to_datetime({
    "year": df["YYYY"],
    "month": df["MM"],
    "day": df["DD"]
})

# Rétt tímabil
df = df[(df["date"] >= "1993-10-01") & (df["date"] <= "2023-09-30")].copy()

# Rennsli í tölum
df["qobs"] = pd.to_numeric(df["qobs"], errors="coerce")

# Vatnaár (okt-sep)
df["water_year"] = df["date"].dt.year
df.loc[df["date"].dt.month >= 10, "water_year"] += 1


def annual_peak_month(df: pd.DataFrame) -> pd.DataFrame:
    idx = df.groupby("water_year")["qobs"].idxmax()
    peaks = df.loc[idx, ["water_year", "date", "qobs"]].copy()
    peaks["month"] = peaks["date"].dt.month
    return peaks.sort_values("water_year")


peaks_91 = annual_peak_month(df)

# Fjöldi annual peaks í hverjum mánuði
month_counts = peaks_91["month"].value_counts().sort_index()

months = np.arange(1, 13)
vals = np.array([month_counts.get(m, 0) for m in months])

month_labels = ["Jan", "Feb", "Mar", "Apr", "Maí", "Jún",
                "Júl", "Ágú", "Sep", "Okt", "Nóv", "Des"]

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(months, vals, width=0.7)

ax.set_title("Árstíðasveifla flóða - ID 91")
ax.set_xlabel("Mánuður")
ax.set_ylabel("Fjöldi annual peaks")
ax.set_xticks(months)
ax.set_xticklabels(month_labels)

plt.tight_layout()
plt.savefig("arstidasveifla.png", dpi=300, bbox_inches="tight")


print(peaks_91[["water_year", "date", "qobs", "month"]])

# Liður 6 - Seinni hluti

annual_peak_values = peaks_91["qobs"].dropna().values
annual_peak_values = np.sort(annual_peak_values)

print("\nFjöldi annual peaks:", len(annual_peak_values))
print("Annual peak flows:")
print(annual_peak_values)

# Gringorten plotting positions
n = len(annual_peak_values)
rank = np.arange(1, n + 1)
F_gringorten = (rank - 0.44) / (n + 0.12)


# Gumbel
params_gumbel = gumbel_r.fit(annual_peak_values)
q_gumbel_fit = gumbel_r.ppf(F_gringorten, *params_gumbel)

# Log Normal 3
params_logn3 = lognorm.fit(annual_peak_values)
q_logn3_fit = lognorm.ppf(F_gringorten, *params_logn3)

# Log Pearson 3
log_peaks = np.log10(annual_peak_values)
params_lp3 = pearson3.fit(log_peaks)
q_lp3_fit = 10 ** pearson3.ppf(F_gringorten, *params_lp3)

# RMSE samanburður
rmse_gumbel = np.sqrt(np.mean((annual_peak_values - q_gumbel_fit)**2))
rmse_logn3 = np.sqrt(np.mean((annual_peak_values - q_logn3_fit)**2))
rmse_lp3 = np.sqrt(np.mean((annual_peak_values - q_lp3_fit)**2))

print("\nRMSE samanburður:")
print(f"Gumbel      RMSE = {rmse_gumbel:.2f}")
print(f"LogNormal3  RMSE = {rmse_logn3:.2f}")
print(f"LogPearson3 RMSE = {rmse_lp3:.2f}")

# Samanburðarmynd dreifinga
plt.figure(figsize=(8, 5))
plt.plot(F_gringorten, annual_peak_values, "o", label="Empirical (Gringorten)")
plt.plot(F_gringorten, q_gumbel_fit, label="Gumbel")
plt.plot(F_gringorten, q_logn3_fit, label="Log Normal 3")
plt.plot(F_gringorten, q_lp3_fit, label="Log Pearson 3")

plt.xlabel("Non-exceedance probability")
plt.ylabel("Annual peak discharge (m³/s)")
plt.title("Flood frequency fit - ID 91")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('figures/06_flodagreining.png', dpi=300, bbox_inches='tight')




# Q10, Q50, Q100
F10 = 0.90
F50 = 0.98
F100 = 0.99

# Gumbel
Q10_g = gumbel_r.ppf(F10, *params_gumbel)
Q50_g = gumbel_r.ppf(F50, *params_gumbel)
Q100_g = gumbel_r.ppf(F100, *params_gumbel)

# Log Normal 3
Q10_ln3 = lognorm.ppf(F10, *params_logn3)
Q50_ln3 = lognorm.ppf(F50, *params_logn3)
Q100_ln3 = lognorm.ppf(F100, *params_logn3)

# Log Pearson 3
Q10_lp3 = 10 ** pearson3.ppf(F10, *params_lp3)
Q50_lp3 = 10 ** pearson3.ppf(F50, *params_lp3)
Q100_lp3 = 10 ** pearson3.ppf(F100, *params_lp3)

print("\nQ10, Q50, Q100:")
print(f"Gumbel      : Q10={Q10_g:.2f}, Q50={Q50_g:.2f}, Q100={Q100_g:.2f}")
print(f"LogNormal3  : Q10={Q10_ln3:.2f}, Q50={Q50_ln3:.2f}, Q100={Q100_ln3:.2f}")
print(f"LogPearson3 : Q10={Q10_lp3:.2f}, Q50={Q50_lp3:.2f}, Q100={Q100_lp3:.2f}")

# Tafla með niðurstöðum
results_table = pd.DataFrame({
    "Dreifing": ["Gumbel", "Log Normal 3", "Log Pearson 3"],
    "RMSE": [rmse_gumbel, rmse_logn3, rmse_lp3],
    "Q10 (m3/s)": [Q10_g, Q10_ln3, Q10_lp3],
    "Q50 (m3/s)": [Q50_g, Q50_ln3, Q50_lp3],
    "Q100 (m3/s)": [Q100_g, Q100_ln3, Q100_lp3]
})

results_table = results_table.round(2)

print("\nNiðurstöðutafla:")
print(results_table.to_string(index=False))

plt.show()