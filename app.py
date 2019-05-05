###############################################################################
# Student: Rafael Santos    - HOMEWORK  10 - SQL Alchemy (FLASK APP)
# Data Analytics and Visualization - cohort 3
###############################################################################

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
# Adding this - From Dom's example
from sqlalchemy.orm import scoped_session, sessionmaker


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Adding this - From Dom's example
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# /
# Home page.
# List all routes that are available.

@app.route("/")
def Home():
    """List of all available api routes."""
    
    return (
        f"Welcome to Homework 10 API! - by Rafael Santos<br/><br/>"
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start_date><br/>"
        f"/api/v1.0/<start_date>/<end_date><br/>"
    )


          
# /api/v1.0/precipitation
# Convert the query results to a Dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.          
          
@app.route("/api/v1.0/precipitation")
def YearPrec():
    
    temp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-22')\
                                                              .order_by(Measurement.date.asc()).all()

    date =[]
    precipitation=[]
    precipitation_dict ={}
    for date1, prcp1 in temp:
        date.append(date1)
        precipitation.append(prcp1)
    
    precipitation_dict = {date:precipitation for date,prcp in zip(date, precipitation)}


    return jsonify(precipitation_dict)


# /api/v1.0/stations
# Return a JSON list of stations from the dataset.
          
@app.route("/api/v1.0/stations")
def Stations():
    
    station_list_query = session.query(Station.station).all()
    station_list=[]
    
    for station1 in station_list_query:
          station_list.append(station1)
    
    return jsonify(station_list)
          

# /api/v1.0/tobs
# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.
          
@app.route("/api/v1.0/tobs")
def TempLastYear():
    
    LastYearTemp_query = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > '2017-08-22').all()
    LastYearTemp_list=[]
    
    for tobs1 in LastYearTemp_query:
          LastYearTemp_list.append(tobs1)
          
    
    return jsonify(LastYearTemp_list)



# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, 
## and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between 
## the start and end date inclusive.
          
@app.route("/api/v1.0/<start_date>")

def TempStats(start_date):
        
    
    TempStats_query = session.query(func.min(Measurement.tobs),\
    func.max(Measurement.tobs),func.avg(Measurement.tobs))\
    .filter(Measurement.date > start_date)\
    .all()

    Tmin = []
    Tavg=[]
    Tmax=[]
    TempStats_=[]
    
    for TempMin1,TempMax1,TempAvg1 in TempStats_query:
        Tmin.append(TempMin1)
        Tavg.append(TempAvg1)
        Tmax.append(TempMax1)
    
    TempStats_ = [Tmin,Tavg,Tmax]
           
    return jsonify(TempStats_)


@app.route("/api/v1.0/<start_date>/<end_date>")

def TempStats2(start_date,end_date):

    TempStats_query = session.query(func.min(Measurement.tobs),\
    func.max(Measurement.tobs),func.avg(Measurement.tobs))\
    .filter(Measurement.date > start_date)\
    .filter(Measurement.date < end_date)\
    .all()

    Tmin = []
    Tavg=[]
    Tmax=[]
    TempStats_=[]
    
    for TempMin1,TempMax1,TempAvg1 in TempStats_query:
        Tmin.append(TempMin1)
        Tavg.append(TempAvg1)
        Tmax.append(TempMax1)
    
    TempStats_ = [Tmin,Tavg,Tmax]
           
    return jsonify(TempStats_)


          
# Adding this - - From Dom's example
@app.teardown_appcontext
def cleanup(resp_or_exc):
    print('Teardown received')
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)