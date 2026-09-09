import os
import csv
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from geoalchemy2.elements import WKTElement
from models import Substation 

# Load variables from a local .env file (this file is never uploaded to GitHub)
load_dotenv()

# Connect to the database (the real password lives in your local .env file)
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

print("Preparing to read CSV and bulk insert substations...")

objects_to_save = []

# 1. Open and read the CSV file you just created
try:
    with open('substation_data.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        
        # 2. Loop through every single row in the CSV
        for row in csv_reader:
            # Extract coordinates and format them for PostGIS
            point_string = f"POINT({row['longitude']} {row['latitude']})"
            
            # Create a new Substation object for this row
            new_station = Substation(
                station_id=row['station_id'],
                ring_cluster=row['ring'],
                capacity_kva=float(row['capacity']),
                coordinates=WKTElement(point_string, srid=4326)
            )
            
            # Add it to our master list
            objects_to_save.append(new_station)

    # 3. Send the entire list to PostgreSQL at once
    session.add_all(objects_to_save)
    session.commit()

    print(f"Success! {len(objects_to_save)} substations added to the spatial database.")

except FileNotFoundError:
    print("Error: Could not find 'substation_data.csv'. Make sure it is in the same folder as this script!")
except Exception as e:
    print(f"An error occurred: {e}")