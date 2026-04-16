Basin delineation C: Like delineation B but excludes catchments with moderate or strong human or natural influence on streamflow.

This folder contains the following files:
- 1_attributes
  - Catchment_attributes.csv
  - Gauge_hierarchy.csv
- 2_timeseries
  - annual
    - corine_land_cover_timeseries
        - CORINE land cover timeseries for all (intermediate) catchments with no or low degree of impact
  - daily
    - meteorological_data
        - meteorological time series for all (intermediate) catchments with no or low degree of impact
    - modis_fractional_snow_cover_and_glacier_albedo 
        - MODIS fractional snow cover for all (intermediate) catchments with no or low degree of impact
- 3_shapefiles (EPSG 3057)
  - Basins_C.shp

Additional information regarding the time series.
1. The units of the meteorological time series can be obtained from Appendix A of the accompanying paper.
2. The timezone for all time series is GMT.
3. One value of the hourly time series represents the mean or sum from the indexed hour to the next following hour, 
   i.e. the value at 00:00 indicates the mean or sum from 00:00 to 01:00.