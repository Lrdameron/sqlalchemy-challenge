# SQLAlchemy Climate Analysis

## Overview
This repository contains a two-part Python project using SQLAlchemy and Flask to analyze climate data in Honolulu, Hawaii. The dataset includes precipitation, temperature observations, and weather stations.

## Features
### Part 1: Climate Data Analysis
- Uses SQLAlchemy to connect to a SQLite database and reflect tables.
- Performs precipitation analysis for the last 12 months.
- Identifies the most active weather station and retrieves temperature observations.
- Uses Pandas and Matplotlib to visualize temperature and precipitation trends.

### Part 2: Flask API
- Creates a Flask API to serve climate data.
- Available routes:
  - `/api/v1.0/precipitation` - Last 12 months of precipitation data.
  - `/api/v1.0/stations` - List of weather stations.
  - `/api/v1.0/tobs` - Temperature observations for the most active station.
  - `/api/v1.0/<start>` - Min, Avg, and Max temp from the start date onward.
  - `/api/v1.0/<start>/<end>` - Min, Avg, and Max temp for a date range.

## Dependencies
This project requires the following Python libraries:
- Flask
- SQLAlchemy
- Pandas
- Matplotlib

## Results & Insights
- Precipitation trends indicate seasonal fluctuations in Honolulu.
- The most active station, `USC00519281`, provides the most reliable temperature data.
- The Flask API enables easy access to historical climate data.

## Author
### Logan Dameron

## For Educational Purposes Only
