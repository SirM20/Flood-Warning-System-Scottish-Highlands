import arcpy
from arcpy.sa import *

# Set environment
arcpy.env.workspace = r"C:\GIS_Projects\Floodwarningsystem\Floodwarningsystem.gdb"
arcpy.env.overwriteOutput = True

try:
    arcpy.CheckOutExtension("Spatial")

    # Input raster names
    rasters = {
        "Landuse_reclass": "resamp_landuse",
        "Soiltype_reclass": "resamp_soil",
        "Slope_Highlands": "resamp_slope",
        "Rainfall_Risk": "resamp_rainfall",
        "RiverLevel_Risk": "resamp_river"
    }

    # Resample all to 25m using bilinear (or "NEAREST" if categorical)
    for in_ras, out_ras in rasters.items():
        print(f"🔄 Resampling {in_ras} to 25m...")
        arcpy.management.Resample(in_ras, out_ras, "25 25", "NEAREST")

    # Load resampled rasters
    landuse = Raster("resamp_landuse")
    soil = Raster("resamp_soil")
    slope = Raster("resamp_slope")
    rainfall = Raster("resamp_rainfall")
    river = Raster("resamp_river")

    # Define weights (adjust as needed)
    w_landuse = 0.2
    w_soil = 0.2
    w_slope = 0.2
    w_rainfall = 0.2
    w_river = 0.2

    # Perform weighted overlay
    flood_risk = (landuse * w_landuse +
                  soil * w_soil +
                  slope * w_slope +
                  rainfall * w_rainfall +
                  river * w_river)

    # Save output
    output_name = "FloodRisk_Overlay"
    flood_risk.save(output_name)
    print(f"✅ Flood risk overlay saved as: {output_name}")

except arcpy.ExecuteError:
    print("❌ ArcPy Error:")
    print(arcpy.GetMessages(2))

except Exception as e:
    print(f"❌ General Error: {e}")

finally:
    arcpy.CheckInExtension("Spatial")
