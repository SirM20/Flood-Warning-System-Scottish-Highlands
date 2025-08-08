import arcpy
from arcpy.sa import *

arcpy.env.workspace = r"C:\GIS_Projects\Floodwarningsystem\Floodwarningsystem.gdb"
arcpy.env.overwriteOutput = True

try:
    arcpy.CheckOutExtension("Spatial")
    
    flood_risk_raster = Raster("FloodRisk_Overlay")
    
    # Reclassify: 0-3 Low, 4-6 Medium, 7-10 High
    remap = RemapRange([[0, 3, 1], [4, 6, 2], [7, 10, 3]])
    risk_zones = Reclassify(flood_risk_raster, "Value", remap)
    risk_zones.save("Flood_Risk_Zones")
    
    print("✅ Reclassified flood zones saved as: Flood_Risk_Zones")

except Exception as e:
    print(f"❌ Error: {e}")
finally:
    arcpy.CheckInExtension("Spatial")
