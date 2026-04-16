This folder contains the following files:
- 1_attributes
  - Gauge_attributes.csv (To ensure Icelandic characters are displayed correctly when opening the Gauge_attributes.csv file, please use UTF-8 encoding).
  - hydro_indices_1981_2018.csv (calculated using filtered streamflow data for the period from the first 1 October in the individual time series after 1981 to 30 September 2018 using meteorological data from RAV-II)
  - hydro_indices_1981_2018_unfiltered_obs.csv (calculated using raw streamflow data for the period from the first 1 October in the individual time series after 1981 to 30 September 2018 using meteorological data from RAV-II)
- 2_timeseries
  - daily
    - runoff time series for all gauges
  - daily_filtered
    - filtered runoff time series for all gauges (see Article section 4.1)
- 3_shapefiles (EPSG 3057)
  - gauges.shp

Additional information regarding the time series.
1. Unit of runoff data is m3/s. Conversion to runoff heights can be performed using the catchment area provided (attribute “area_calc” in the file "A_basins_total_upstrm/Catchment_attributes.csv", described in Appendix A of the accompanying paper). 
2. The timezone for all time series is GMT.
3. Quality codes are as follows: 

Quality codes assigned to water level observations.

Quality code | Class                     | Description/Criteria
-------------|---------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
40           | Good (of highest quality) | Data is good. Water level is recorded without any interruptions.
80           | Fair (second class)       | Water level data has minor interruptions, e.g., due to ice.
100          | Estimated                 | Data is estimated due to instrumentation failure, ice interruptions, or missing data. Estimations use nearby weather observations and/or nearby streamflow gauges.
120          | Suspect                   | Suspected data. Low quality. Two example reasons: A) The water level recording shows spikes but the main line is correct. B) The sensor experiences fluctuations, and there are no manual measurements available to confirm the accuracy of the data.
200          | Unchecked                 | Unchecked data.
250          | Missing                   | Missing data.