import arcpy

# Set your workspace
arcpy.env.workspace = r"C:\GIS_Projects\Floodwarningsystem\Floodwarningsystem.gdb"
arcpy.env.overwriteOutput = True

# Input raster
flood_risk_raster = "FloodMap"  # Adjust if your raster has a different name
output_polygon = "FloodRisk_Polygon"

# Convert raster to polygon
arcpy.RasterToPolygon_conversion(in_raster=flood_risk_raster,
                                  out_polygon_features=output_polygon,
                                  simplify="NO_SIMPLIFY",
                                  raster_field="Value")

print(f"✅ Flood risk raster converted to polygon: {output_polygon}")
