import requests
import logging
import time
import json
from datetime import datetime

# === CONFIG ===
API_KEY = "ADD YOUR KEY HERE"
TOKEN_URL = "https://timeseries.sepa.org.uk/KiWebPortal/rest/auth/oidcServer/token"
STATION_LIST_FILE = r"C:\GIS_Projects\Floodwarningsystem\PyS\highland_stations.json"  # <-- update if needed

# === LOGGING ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_sepa_token(api_key):
    logging.info("Authenticating with SEPA...")
    headers = {"Authorization": "Basic " + api_key}
    data = {"grant_type": "client_credentials"}
    try:
        resp = requests.post(TOKEN_URL, headers=headers, data=data)
        resp.raise_for_status()
        return resp.json()["access_token"]
    except Exception as e:
        logging.error(f"Failed to authenticate with SEPA: {e}")
        return None

def fetch_latest_value(ts_id, access_token):
    url = f"https://timeseries.sepa.org.uk/KiWIS/KiWIS?data-source=0&request=getTimeseriesValues&ts_id={ts_id}&period=P1D&format=json"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        values = data[0]["data"]
        if values:
            latest = values[-1]
            return float(latest[1])  # value column
    except Exception as e:
        logging.warning(f"Failed to fetch data for ts_id {ts_id}: {e}")
    return None  # fallback to mock later

def main():
    access_token = get_sepa_token(API_KEY)
    if not access_token:
        logging.warning("Skipping live data fetch due to authentication failure.")
        return

    with open(STATION_LIST_FILE, "r") as f:
        stations = json.load(f)

    rainfall_vals = []
    river_vals = []

    for s in stations:
        name = s["name"]
        ts_id_rain = s.get("rainfall_ts_id")
        ts_id_river = s.get("river_ts_id")

        logging.info(f"📍 Fetching data for: {name}")

        rainfall = fetch_latest_value(ts_id_rain, access_token) if ts_id_rain else None
        river = fetch_latest_value(ts_id_river, access_token) if ts_id_river else None

        # Use mock if fetch fails
        if rainfall is None:
            logging.warning(f"❌ Rainfall data not found for {name}, using mock value 3.5mm")
            rainfall = 3.5
        if river is None:
            logging.warning(f"❌ River level data not found for {name}, using mock value 1.2m")
            river = 1.2

        logging.info(f"✅ {name} | Rainfall: {rainfall} mm | River level: {river} m")
        rainfall_vals.append(rainfall)
        river_vals.append(river)

    # Aggregate
    avg_rain = round(sum(rainfall_vals) / len(rainfall_vals), 2)
    avg_river = round(sum(river_vals) / len(river_vals), 2)

    logging.info(f"🌧️ Average Rainfall across Highland: {avg_rain} mm")
    logging.info(f"🌊 Average River Level across Highland: {avg_river} m")

    # You can return or save this data for Step 4 integration
    return avg_rain, avg_river

if __name__ == "__main__":
    main()
