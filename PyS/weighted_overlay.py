import arcpy
from arcpy.sa import *

# Set the workspace
arcpy.env.workspace = r"C:\GIS_Projects\Floodwarningsystem\Floodwarningsystem.gdb"
arcpy.env.overwriteOutput = True

try:
    arcpy.CheckOutExtension("Spatial")

    # Input rasters
    landuse = Raster("Landuse_reclass")
    soil = Raster("Soiltype_reclass")
    slope = Raster("Slope_Highlands")
    rainfall = Raster("Rainfall_Risk")
    river = Raster("RiverLevel_Risk")

    # Normalize weights to sum to 1
    flood_risk = (
        landuse * 0.25 +
        soil * 0.20 +
        slope * 0.15 +
        rainfall * 0.20 +
        river * 0.20
    )

    # Save output raster
    flood_risk.save("Flood_Risk_Map")
    print("✅ Composite Flood Risk Map saved as: Flood_Risk_Map")

except Exception as e:
    print(f"⚠️ Error during weighted overlay: {e}")

finally:
    arcpy.CheckInExtension("Spatial")
