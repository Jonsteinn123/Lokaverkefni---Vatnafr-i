# Vatnafræðileg greining á Vatnsdalsá

Lokaverkefni í Vatnafræði (UMV201G), Háskóla Íslands, vor 2026.

**Höfundar:** Heiðar Snær Ragnarsson & Jónsteinn Helgi Þórsson  
**Vatnasvið:** Vatnsdalsá, Forsæludalur (ID 91)  
**Tímabil:** 1. október 1993 – 30. september 2023

## Gögn

Gögnin sem notuð eru í verkefninu eru úr **LamaH-Ice** gagnasettinu (Helgason og Nijssen, 2024):  
https://www.hydroshare.org/resource/705d69c0f77c48538d83cf383f8c63d6/

Gögnin eru ekki geymd í repoinu. Hlaðið niður `lamah_ice.zip` af ofangreindri slóð og staðsetjið þau svona:

data/
D_gauges/2_timeseries/daily/ID_91.csv
A_basins_total_upstrm/2_timeseries/daily/meteorological_data/ID_91.csv

## Hvernig keyra má kóðann

Opna terminal og keyra eftirfarandi:

```bash
py scripts/02_arstidarsveifla.py
py scripts/03_grunnvatnsframlag.py
py scripts/04_grunnliking.py
py scripts/05_langæislina.py
py scripts/06_flodagreining.py
py scripts/07_leitnigreining.py
py scripts/08_rennslisatburdur.py
```

## Hvaða kóðar búa til hvaða myndir

| Kóðaskrá | Mynd |
|--------|------|
| `02_arstidarsveifla.py` | `figures/02_arstidarsveifla.png` |
| `03_grunnvatnsframlag.py` | `figures/03a_baseflow_separation.png`, `figures/03b_recession_analysis.png` |
| `05_langaislina.py` | `figures/05_langaislina.png` |
| `06_flodagreining.py` | `figures/06_flodagreining.png` |
| `08_rennslisatburdur.py` | `figures/08_rennslisatburdur.png` |