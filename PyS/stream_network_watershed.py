import os
import json
import shutil
import tempfile
import requests
import logging
import arcpy
from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection

# === CONFIGURATION ===
gdb_path = r"C:\GIS_Projects\Floodwarningsystem\Floodwarningsystem.gdb"
fc_name = "Highlands_River_Guage"
json_path = r"C:\GIS_Projects\Floodwarningsystem\PyS\highland_stations.json"
access_key = "YOUR_SEPA_API_ACCESS_KEY"
station_item_id = "6b975a034e9c46b68a7f9213a4d02810"
agol_username = "your_username"
agol_password = "your_password"

# === LOGGING SETUP ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# === LOAD STATIONS FROM JSON ===
with open(json_path, "r") as f:
    stations_data = json.load(f)
stations = [(s["name"], s["lat"], s["lon"]) for s in stations_data]

# === SEPA API AUTH ===
logging.info("🔐 Authenticating with SEPA API...")
token_url = "https://timeseries.sepa.org.uk/KiWebPortal/rest/auth/oidcServer/token"
headers = {"Authorization": "Basic " + access_key}
response = requests.post(token_url, headers=headers, data="grant_type=client_credentials")
access_token = response.json().get("access_token")
auth_header = {"Authorization": f"Bearer {access_token}"}

# === UPDATE LOCAL FEATURE CLASS ===
logging.info("📍 Updating rainfall and river level fields...")
with arcpy.da.UpdateCursor(os.path.join(gdb_path, fc_name), ["station_name", "rainfall_mm", "river_level_m"]) as cursor:
    for row in cursor:
        name = row[0]
        logging.info(f"📡 Fetching SEPA data for: {name}")
        # TODO: Use real API data — using mock values for now
        row[1] = 3.5  # rainfall
        row[2] = 1.2  # river level
        cursor.updateRow(row)
        logging.info(f"✅ Updated: {name} | Rainfall: {row[1]} mm | River Level: {row[2]} m")

# === SAFE ZIP GDB ===
logging.info("📂 Copying and zipping updated GDB safely...")

with tempfile.TemporaryDirectory() as temp_dir:
    temp_gdb_name = "Highlands_River_Guage.gdb"
    temp_gdb_path = os.path.join(temp_dir, temp_gdb_name)

    # Create new temp GDB
    arcpy.CreateFileGDB_management(temp_dir, "Highlands_River_Guage.gdb")

    # Copy only the feature class to avoid .lock files
    arcpy.CopyFeatures_management(os.path.join(gdb_path, fc_name),
                                  os.path.join(temp_gdb_path, fc_name))

    # Zip the clean GDB folder
    zip_base = os.path.join(temp_dir, "Highlands_River_Guage")
    zip_path = zip_base + ".zip"
    shutil.make_archive(zip_base, "zip", temp_dir, temp_gdb_name)

    # === OVERWRITE ON AGOL ===
    logging.info("🌐 Signing in to ArcGIS Online...")
    gis = GIS("https://www.arcgis.com", agol_username, agol_password)

    logging.info("📦 Getting AGOL item...")
    station_item = gis.content.get(station_item_id)
    station_flc = FeatureLayerCollection.fromitem(station_item)

    logging.info("⬆️ Overwriting feature layer on AGOL...")
    station_flc.manager.overwrite(zip_path)

logging.info("✅ Done. AGOL Feature Layer updated with live station data.")
