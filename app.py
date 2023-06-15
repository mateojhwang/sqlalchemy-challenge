# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
import numpy as np
import pandas as pd
import datetime as dt


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(autoload_with=engine)

# Save references to each table
measurement_tb = base.classes.measurement
station_tb = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# prcp data
recent_date = session.query(measurement_tb.date).order_by(measurement_tb.date.desc()).first()
last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
prcp_data = session.query(measurement_tb.date, measurement_tb.prcp).filter(measurement_tb.date >= last_year).all()

# stations data
stations_list = []
for row in session.query(measurement_tb.station, func.count(measurement_tb.station)).\
    group_by(measurement_tb.station).order_by(func.count(measurement_tb.station)).all():
    stations_list.append(row)

# tobs data
tobs_data = session.query(measurement_tb.date, measurement_tb.tobs).filter(measurement_tb.date >= last_year).all()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/tobs")
def tobs():
    return (tobs_data)

@app.route("/api/v1.0/stations")
def station():
    return jsonify(stations_list)


@app.route("/api/v1.0/precipitation")
def prcp():
    return jsonify(prcp_data)

@app.route("/")
def home():

    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

if __name__ == "__main__":
    app.run(debug=True)