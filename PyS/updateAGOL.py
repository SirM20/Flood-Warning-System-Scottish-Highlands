import requests
import json
import logging
from arcgis.gis import GIS

# === CONFIGURATION ===
json_path = r"C:\GIS_Projects\Floodwarningsystem\PyS\highland_stations.json"
access_key = "YOUR SEPA KEY"
agol_username = "Your argis online username"
agol_password = "your arcgis online pass"
agol_item_id = "00"  # Your AGOL feature layer item ID

# === LOGGING SETUP ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# === SEPA API AUTHENTICATION ===
logging.info("🔐 Authenticating with SEPA API...")
token_url = "https://timeseries.sepa.org.uk/KiWebPortal/rest/auth/oidcServer/token"
headers = {"Authorization": "Basic " + access_key}
token_response = requests.post(token_url, headers=headers, data="grant_type=client_credentials")
access_token = token_response.json().get("access_token")
auth_header = {"Authorization": "Bearer " + access_token}

# === LOAD STATIONS FROM JSON ===
with open(json_path, "r") as f:
    stations_data = json.load(f)
stations = {s["name"]: (s["lat"], s["lon"]) for s in stations_data}

# === CONNECT TO AGOL LAYER ===
logging.info("🌐 Connecting to AGOL Feature Layer via item ID...")
gis = GIS("https://www.arcgis.com", agol_username, agol_password)
item = gis.content.get(agol_item_id)
if not item:
    raise Exception("❌ Could not find AGOL item by item ID.")
layer = item.layers[0]  # Get first sublayer

# === FETCH EXISTING FEATURES ===
logging.info("📥 Fetching existing features...")
existing_features = layer.query(where="1=1", out_fields="station_name", return_geometry=True).features

# === UPDATE FEATURES ===
logging.info("🔄 Updating features with live SEPA values...")
updates = []

for feature in existing_features:
    name = feature.attributes["station_name"]
    if name not in stations:
        logging.warning(f"⚠️ Station not in JSON: {name}")
        continue

    # TODO: Replace these mock values with actual SEPA API data per station
    rainfall = 3.5
    river_level = 1.2

    feature.attributes["rainfall_mm"] = rainfall
    feature.attributes["river_level_m"] = river_level
    updates.append(feature)

    logging.info(f"✅ {name} | Rainfall: {rainfall} mm | River: {river_level} m")

# === PUSH UPDATES TO AGOL ===
if updates:
    logging.info("📤 Sending updates to ArcGIS Online...")
    result = layer.edit_features(updates=updates)
    if result.get("updateResults"):
        logging.info("🎉 Successfully updated AGOL layer.")
    else:
        logging.warning("❌ Update failed.")
else:
    logging.info("ℹ️ No updates were made.")
