# Integrated Substation Management Platform (ISMP) — NEPA Akoka, UNILAG

**Course:** CSC 316 — Systems Analysis and Design
**Institution:** University of Lagos (UNILAG)
**Team:** Group 23 — EchoWork
**Session:** 2025/2026

## Overview

The University of Lagos, Akoka campus runs its own 11kV power distribution network (nicknamed "NEPA Akoka"), made up of 4 rings, 8 feeders, and roughly 40–50 substations spread across campus — including several underground ones. Right now, faults (short circuits, overloads, insulation failures) are only discovered *after* the lights go out, because there's no digital monitoring in place — engineers have to physically patrol cables and inspect substations by hand.

This project designs (as a systems-analysis case study, not a physical deployment) an **Integrated Substation Management Platform** that would replace this manual, reactive process with a centralized, GIS-based, real-time monitoring system.

## What the System Is Designed to Do

- **GIS Mapping Module** — Plots the exact location of every substation (including underground ones) on an interactive map, so engineers can see the whole grid at a glance.
- **Real-Time Monitoring Module** — Tracks live status per substation (voltage, load, temperature) from a single dashboard instead of manual site visits.
- **Fault Detection & Alerting Module** — Flags anomalies automatically and pinpoints exactly which substation is affected and where it is.
- **Predictive Health Analytics Module** — Looks at historical data to flag equipment at risk of failure *before* it fails, enabling planned maintenance instead of emergency repairs.
- **Reporting Module** — Turns raw monitoring data into performance reports for planning and budget decisions.

## What's in This Repository

| File | What it does |
|---|---|
| `docs/CSC316_ISMP_Report_NEPA_Akoka.docx` | Full project report — background, problem statement, objectives, feasibility study, system design (DFDs, ERDs), and conclusion |
| `models.py` | Defines the `Substation` database table (id, station name, ring cluster, capacity, live status, GPS coordinates) using SQLAlchemy + PostGIS |
| `seed_script.py` | Reads `substation_data.csv` and loads all the substation records into the database |
| `fault_simulation.py` | Simulates the fault-detection engine — periodically "checks" every substation and randomly flags ~10% as faulty, to demonstrate how live monitoring would work |
| `map_generator.py` | Generates an interactive campus map (`unilag_grid_map.html`) with a green/red marker for every substation, showing its live status |
| `substation_data.csv` | Sample geospatial + capacity data for ~40 UNILAG substations, used to seed the database |
| `unilag_grid_map.html` | A pre-generated example of the interactive map output |

## Tech Stack

- **Python** (SQLAlchemy, GeoAlchemy2, Folium)
- **PostgreSQL + PostGIS** (spatial database for storing substation locations)
- **QGIS-style geospatial mapping concepts**

## Running This Locally

1. Install PostgreSQL with the PostGIS extension enabled, and create a database.
2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to a new file named `.env`, and fill in your real database password:
   ```
   cp .env.example .env
   ```
4. Run the scripts in this order:
   ```
   python models.py         # creates the database table
   python seed_script.py    # loads substation data from the CSV
   python fault_simulation.py   # starts the live fault-checking loop
   python map_generator.py  # generates the interactive map
   ```

> **Note:** This project was built as a systems-design case study for a university course. The fault detection here is *simulated* (random), since no physical IoT sensors were deployed on the real NEPA Akoka grid as part of this study.

## 👥 Team

Group 23 — EchoWork, CSC 316, University of Lagos

## 🔒 Security Note

Database credentials are loaded from a local `.env` file (excluded from this repo via `.gitignore`) rather than being hardcoded — see `.env.example` for the format.
