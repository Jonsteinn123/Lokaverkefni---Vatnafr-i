Basin delineation A: The entire upstream area of each gauge.

This folder contains the following files:
- 1_attributes
  - Catchment_attributes.csv
  - Water_balance.csv (Calculated using filtered streamflow data)
  - Water_balance_unfiltered.csv (Calculated using all available streamflow data)
- 2_timeseries
  - annual
    - corine_land_cover_timeseries
        - CORINE land cover timeseries for all catchments
    - glacier_timeseries
        - Glacier extent (represended by areal extent in km2 ("g_area_dyn") and basin fraction ("g_frac_dyn"))
        - Glacier mass balance for catchments draining Vatnajökull and Langjökull glaciers, 32 catchments in total. Timeseries provided: Annual net mass balance ("annual_net_MB"), summer mass balance ("summer_MB") and winter mass balance ("winter_MB"). The measurement unit is [meters water equivalent / year].
  - daily
    - meteorological_data
        - meteorological time series for all catchments
    - modis_fractional_snow_cover_and_glacier_albedo
        - MODIS fractional snow cover (and glacier albedo) for all (glaciated) catchments
- 3_shapefiles (EPSG 3057)
  - Basins_A.shp
  - Basins_A.gpkg
  - glaciers_in_catchments.shp

Additional information regarding the time series.
1. The units of the meteorological time series can be obtained from Appendix A of the accompanying paper.
2. The timezone for all time series is GMT.
3. One value of the hourly time series represents the mean or sum from the indexed hour to the next following hour, 
   i.e. the value at 00:00 indicates the mean or sum from 00:00 to 01:00.
