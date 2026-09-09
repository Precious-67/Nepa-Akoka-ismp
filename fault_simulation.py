import os
import time
import random
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Substation 

# Load variables from a local .env file (this file is never uploaded to GitHub)
load_dotenv()

# 1. Connect to the database (the real password lives in your local .env file)
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

print("⚡ Starting NEPA Akoka Fault Simulation Engine...")
print("Press Ctrl+C to stop the simulation.\n")

try:
    # 2. Start the continuous monitoring loop
    while True: 
        # Grab all the substations currently in your database
        stations = session.query(Substation).all()
        fault_count = 0
        
        print(f"[{time.strftime('%H:%M:%S')}] Pinging {len(stations)} substations...")

        for station in stations:
            # 3. The Logic: 90% chance the station is fine, 10% chance it trips
            health_check = random.random()
            
            if health_check > 0.10:
                station.current_status = "OK"
            else:
                station.current_status = "FAULT"
                fault_count += 1
                # Notice we are now using your new station_id and ring_cluster columns!
                print(f"   🚨 ALERT: Power failure detected at {station.station_id} (Located in: {station.ring_cluster})!")

        # 4. Save the new statuses to PostgreSQL
        session.commit()
        
        if fault_count == 0:
            print("   ✅ Grid is stable. All stations operating normally.")
            
        print("-" * 50)
        
        # 5. Pause for 5 seconds before checking again
        time.sleep(10) 
        
except KeyboardInterrupt:
    print("\n🛑 Simulation safely stopped by user.")