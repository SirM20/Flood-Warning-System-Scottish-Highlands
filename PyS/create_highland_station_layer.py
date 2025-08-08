import arcpy
import json
import os

# === Paths ===
gdb = r"C:\GIS_Projects\Floodwarningsystem\Floodwarningsystem.gdb"
station_fc = "Highland_Stations"
json_path = r"C:\GIS_Projects\Floodwarningsystem\PyS\highland_stations.json"

# === Load station data from JSON ===
with open(json_path, "r") as f:
    stations = json.load(f)

# === Create feature class ===
arcpy.env.workspace = gdb
arcpy.env.overwriteOutput = True

print("🛠️ Creating station feature class...")
arcpy.CreateFeatureclass_management(out_path=gdb, out_name=station_fc, geometry_type="POINT", spatial_reference=4326)

# Add fields
fields = ["station_name", "rainfall_mm", "river_level_m"]
arcpy.AddField_management(station_fc, "station_name", "TEXT", field_length=100)
arcpy.AddField_management(station_fc, "rainfall_mm", "DOUBLE")
arcpy.AddField_management(station_fc, "river_level_m", "DOUBLE")

# === Insert station points ===
with arcpy.da.InsertCursor(station_fc, ["SHAPE@XY", "station_name", "rainfall_mm", "river_level_m"]) as cursor:
    for station in stations:
        name = station.get("name")
        lat = station.get("lat")
        lon = station.get("lon")
        if name and lat and lon:
            cursor.insertRow([(lon, lat), name, 0.0, 0.0])

print(f"✅ Created station feature class with {len(stations)} points: {station_fc}")
