# Import the dependencies.
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()


# reflect the tables
Base.prepare(engine, reflect=True)

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
    print("Server requested climate app home page...")
    return (
        f"Welcome to the Honolulu Hawaii Climate App!<br/>"
        f"----------------------------------<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"<br>"
        
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server requested climate app precipitation page...")


    session = Session(engine)
    
    most_recent_date_str = session.query(func.max(measurement.date)).scalar()
    most_recent_date = dt.date.fromisoformat(most_recent_date_str)
    previous_year = most_recent_date - dt.timedelta(days=365)

    precip_data = session.query(measurement.date, func.avg(measurement.prcp))\
    .filter(measurement.date >= previous_year).group_by(measurement.date)\
    .all()

    session.close()

    precip_dict = {} 
    for date, prcp in precip_data:
        precip_dict[date] = prcp

    return jsonify(precip_dict)


@app.route("/api/v1.0/stations")
def stations():
    print("Server requested climate app station data...")

    session = Session(engine)

    station_data = session.query(station.id, station.station, station.name).all()

    session.close()

    station_list = []
    for stations in station_data:
        stations_dict = {} 

        stations_dict['id'] = stations[0]
        stations_dict['station'] = stations[1]
        stations_dict[name] = stations[2]

        station_list.append(stations_dict)

    return jsonify(list_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    print("Server requested Climate App Temp Observation Data ...")

    session = Session(engine)

    active_station = session.query(measurement.station, func.count(measurement.station)).\
                    order_by(func.count(measurement.station).desc()).\
                    group_by(measurement.station).\
                    all()

               

    most_active = active_station[0][0]


    lowest_temp = session.query(measurement.tobs, func.min(measurement.tobs))\
    .filter(measurement.station == most_active).scalar()

    highest_temp = session.query(measurement.tobs, func.max(measurement.tobs))\
    .filter(measurement.station == most_active).scalar()

    avg_temp = session.query(measurement.tobs, func.avg(measurement.tobs))\
    .filter(measurement.station == most_active).scalar()

    session.close() 

    print([{lowest_temp} ,{highest_temp} , {avg_temp}])


    
    
if __name__ == "__main__":
    app.run(debug=True)
