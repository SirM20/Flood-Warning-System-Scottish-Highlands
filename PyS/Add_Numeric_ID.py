import arcpy

# Set your file geodatabase
gdb = r"C:\GIS_Projects\Floodwarningsystem\Floodwarningsystem.gdb"
arcpy.env.workspace = gdb
arcpy.env.overwriteOutput = True

# Layers to process
layers = ["FloodRiskMap", "Highlands_River_Guage"]

# Ensure UniqueID field exists and is populated with OBJECTID
for layer in layers:
    fields = [f.name for f in arcpy.ListFields(layer)]
    
    if "UniqueID" not in fields:
        arcpy.AddField_management(layer, "UniqueID", "LONG")
        print(f"✅ 'UniqueID' field added to {layer}")
    else:
        print(f"ℹ️ 'UniqueID' already exists in {layer}, recalculating...")

    arcpy.CalculateField_management(layer, "UniqueID", "!OBJECTID!", "PYTHON3")
    print(f"✅ 'UniqueID' values calculated for {layer}")
