# Import dependencies
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt

#################################################
# Database Setup
#################################################

# Create Flask app
app = Flask(__name__)

# Connect to SQLite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the database tables
Base = automap_base()
Base.prepare(engine, autoload_with=engine)

# Save references to tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Routes
#################################################

# Homepage Route - Lists all available API routes
@app.route("/")
def home():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation - Last 12 months of precipitation<br/>"
        f"/api/v1.0/stations - List of weather stations<br/>"
        f"/api/v1.0/tobs - Temperature observations from the most active station<br/>"
        f"/api/v1.0/start_date (YYYY-MM-DD) - Min, Avg, Max temp from start date<br/>"
        f"/api/v1.0/start_date/end_date (YYYY-MM-DD) - Min, Avg, Max temp for date range"
    )

# Precipitation Route - Returns last 12 months of precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    # Get the most recent date in the dataset
    latest_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(latest_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query precipitation data for the last 12 months
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    
    session.close()

    # Convert results into a dictionary {date: precipitation}
    precip_data = {date: prcp for date, prcp in results}
    return jsonify(precip_data)

# Stations Route - Returns a list of all weather stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    # Query all station names
    results = session.query(Station.station).all()
    
    session.close()

    # Convert results into a list
    stations = [station[0] for station in results]
    return jsonify(stations)

# TOBS Route - Returns temperature observations for the most active station in the last 12 months
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Find the most active station
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0]

    # Get the most recent date in the dataset
    latest_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(latest_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query temperature observations for the last 12 months
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago).all()
    
    session.close()

    # Convert results into a dictionary {date: temperature}
    tobs_data = {date: tobs for date, tobs in results}
    return jsonify(tobs_data)

# Start Date Route - Returns min, avg, and max temperature from the given start date onwards
@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)

    # Query min, avg, and max temperature from start date onwards
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).all()
    
    session.close()

    # Convert results to JSON format
    temp_data = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }
    return jsonify(temp_data)

# Start & End Date Route - Returns min, avg, and max temperature between given dates
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    session = Session(engine)

    # Query min, avg, and max temperature between given dates
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()

    # Convert results to JSON format
    temp_data = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }
    return jsonify(temp_data)

#################################################
# Run the Flask App
#################################################

if __name__ == "__main__":
    app.run(debug=True)
