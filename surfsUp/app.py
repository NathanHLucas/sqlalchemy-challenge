# Import the dependencies.

from flask import Flask, jsonify
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, text
from sqlalchemy.ext.declarative import declarative_base


#################################################
# Database Setup
#################################################

#create engine
engine = create_engine(r"sqlite:///C:\Users\nrhl1\OneDrive\Desktop\UTBootcamp\Challenges\sqlalchemy-challenge\surfsUp\Resources\hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to my Module 10 challenge assignment 'Home' page!<br/>"
        f"<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitations<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        )

#displays a dictionary of last 12 months of precipitation expressed as a json using (jsonify)
@app.route("/api/v1.0/precipitations")
def precipitations():
    print("Server received request for 'Precipitations' page...")
    query = text(f"SELECT date,prcp FROM measurement WHERE measurement.date BETWEEN '2016-08-23' AND '2017-08-23'")
    df = pd.read_sql_query(query, engine)
    dict = df.to_dict(orient='list')
    return jsonify(dict)

#return a JSON list of stations
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")
    query = text("SELECT DISTINCT station.station FROM station")
    df = pd.read_sql_query(query, engine)
    dict = df.to_dict(orient='list')
    return jsonify(dict)

#return a JSON list of temperature observations for the previous year at the most active station
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Temperatures' page...")
    query = text(f"SELECT tobs FROM measurement WHERE station = 'USC00519281' AND date BETWEEN '2016-08-23' AND '2017-08-23'")
    df = pd.read_sql_query(query, engine)
    dict = df.to_dict(orient="list")
    return jsonify(dict)

#return a JSON list of the minimum, average, and maximum temperature from a specified start date to the last date
@app.route("/api/v1.0/<start>")
def start(start):
    print("Server received request for 'Temperatures from Start Date' page...")
    query = text(f"SELECT tobs FROM measurement WHERE date BETWEEN '{start}' AND '2017-08-23'")
    df = pd.read_sql_query(query, engine)
    dict = {"Min": min(df["tobs"]), "Average": np.mean(df["tobs"]), "Max": max(df["tobs"])}
    return jsonify(dict)

#return a JSON list of the minimum, average, and maximum temperature from a specified start date to a specified end date
@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    print("Server received request for 'Temperatures from Start Date to End Date' page...")
    query = text(f"SELECT tobs FROM measurement WHERE date BETWEEN '{start}' AND '{end}'")
    df = pd.read_sql_query(query, engine)
    dict = {"Min": min(df["tobs"]), "Average": np.mean(df["tobs"]), "Max": max(df["tobs"])}
    return jsonify(dict)

if __name__ == "__main__":
    app.run(debug=True)


# Close Session
session.close()

