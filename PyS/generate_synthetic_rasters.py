import arcpy
from arcpy.sa import *

# Set environment
arcpy.env.workspace = r"C:\GIS_Projects\Floodwarningsystem\Floodwarningsystem.gdb"
arcpy.env.overwriteOutput = True

# Reference raster for cell size and spatial reference
reference_raster = "Slope_Highlands"  # Ensure this exists in your gdb

try:
    # Check out the Spatial Analyst extension
    arcpy.CheckOutExtension("Spatial")

    # Use reference raster properties
    ref = arcpy.Describe(reference_raster)
    cell_size = ref.meanCellWidth
    extent = ref.extent

    # Set the extent and snap raster to align the new rasters
    arcpy.env.extent = extent
    arcpy.env.snapRaster = reference_raster
    arcpy.env.cellSize = cell_size

    # Create constant rasters
    rainfall_risk = CreateConstantRaster(3, "INTEGER", cell_size)
    rainfall_risk.save("Rainfall_Risk")
    print("✅ Saved synthetic rainfall risk raster as: Rainfall_Risk")

    river_risk = CreateConstantRaster(3, "INTEGER", cell_size)
    river_risk.save("RiverLevel_Risk")
    print("✅ Saved synthetic river level risk raster as: RiverLevel_Risk")

except Exception as e:
    print(f"⚠️ Error: {e}")

finally:
    arcpy.CheckInExtension("Spatial")
