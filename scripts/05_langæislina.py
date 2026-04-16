import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
print("Byrjar...")
os.makedirs('figures', exist_ok=True)


df = pd.read_csv(r'C:\Users\jonst\OneDrive - Menntaský\Vatnafræði\Lokaverkefni\lamah_ice\D_gauges\2_timeseries\daily\ID_91.csv', sep=';')

# Búa til dagsetningu
df["date"] = pd.to_datetime({
    "year": df["YYYY"],
    "month": df["MM"],
    "day": df["DD"]
})

# Sía rétt tímabil
df = df[(df["date"] >= "1993-10-01") & (df["date"] <= "2023-09-30")]

# Breyta qobs í tölur
df["qobs"] = pd.to_numeric(df["qobs"], errors="coerce")

# Henda tómum gildum
q = df["qobs"].dropna().values

# Raða frá hæsta til lægsta
q_sorted = np.sort(q)[::-1]

# Reikna exceedance probability
n = len(q_sorted)
p_exceed = np.arange(1, n + 1) / (n + 1)

# Finna Q5, Q50 og Q95
Q5 = np.interp(0.05, p_exceed, q_sorted)
Q50 = np.interp(0.50, p_exceed, q_sorted)
Q95 = np.interp(0.95, p_exceed, q_sorted)

print(f"Q5 = {Q5:.2f} m³/s")
print(f"Q50 = {Q50:.2f} m³/s")
print(f"Q95 = {Q95:.2f} m³/s")

# Tafla með niðurstöðum
fdc_table = pd.DataFrame({
    "Stærð": ["Q5", "Q50", "Q95"],
    "Rennsli (m³/s)": [Q5, Q50, Q95]
})
print("\nTafla fyrir langæislínu:")
print(fdc_table.to_string(index=False))

# Teikna flow duration curve
plt.figure(figsize=(8, 5))
plt.plot(p_exceed * 100, q_sorted)
plt.yscale("log")
plt.xlim(0, 100)
plt.xlabel("Exceedance probability (%)")
plt.ylabel("Discharge (m³/s)")
plt.title("Flow duration curve - Vatnsdalsá (ID 91)")
plt.grid(True)
plt.tight_layout()
plt.savefig('figures/05_langaislina.png', dpi=300, bbox_inches='tight')
plt.show()

