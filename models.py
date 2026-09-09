import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base
from geoalchemy2 import Geometry

# Load variables from a local .env file (this file is never uploaded to GitHub)
load_dotenv()

# This Base class allows SQLAlchemy to map our Python class to a PostgreSQL table
Base = declarative_base()

class Substation(Base):
    __tablename__ = 'substations'

    # 1. Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # 2. Your Specific Substation Data
    station_id = Column(String(50), nullable=False)  # e.g., "SUB-01" or "Science-RMU"
    ring_cluster = Column(String(100))               # e.g., "Ring 1 - Academic"
    capacity_kva = Column(Float)                     # e.g., 500.0
    
    # 3. Fault Status (Keeping this for your monitoring engine later)
    current_status = Column(String(20), default="OK")

    # 4. GIS Mapping Coordinates (SRID 4326 for standard GPS)
    coordinates = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)

    def __repr__(self):
        return f"<Substation(id='{self.station_id}', ring='{self.ring_cluster}')>"


# --- Connect to the Database and Create the Tables ---

## --- Connect to the Database and Create the Tables ---

# The real password now lives ONLY in your local .env file, never in this code.
DATABASE_URL = os.getenv("DATABASE_URL")

print("Connecting to the NEPA Unilag database...")
engine = create_engine(DATABASE_URL, echo=True)

# 1. DROP the old table first (Deletes the old structure)
#print("Dropping old tables...")
#Base.metadata.drop_all(engine)

# 2. CREATE the new table (Builds the new structure with your updated columns)
print("Creating updated spatial tables...")
Base.metadata.create_all(engine)

print("Success! The fresh 'substations' table is ready for your CSV data.")