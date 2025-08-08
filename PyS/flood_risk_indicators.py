import arcpy

# Set environment
arcpy.env.workspace = r"C:\GIS_Projects\Floodwarningsystem\Floodwarningsystem.gdb"
arcpy.env.overwriteOutput = True

# Inputs
landuse_fc = "Land_use"
soil_fc = "Soil_type"

landuse_field = "Historic_L"
soil_field = "MSG84_1"

landuse_score_field = "LU_Score"
soil_score_field = "Soil_Score"

landuse_raster = "Landuse_reclass"
soil_raster = "Soiltype_reclass"

# Flood-prone scores (manually ranked)
landuse_scores = {
    "Built-up Area": 9,
    "Defence": 5,
    "Designed Landscape": 4,
    "Energy, Extraction and Waste": 6,
    "Leisure and Recreation": 3,
    "Moorland and Rough Grazing": 2,
    "Rural Settlement": 8,
    "Spiritual and Ritual": 3,
    "Transport": 7,
    "Woodland and Forestry": 1
}

soil_scores = {
    "Alluvial soils": 9,
    "Brown earths": 3,
    "Calcareous soils": 2,
    "Ground-water gleys": 8,
    "Lithosols": 1,
    "Peats": 7,
    "Podzols": 4,
    "Rankers": 2,
    "Regosols": 3,
    "Rendzinas": 2,
    "Scree": 1,
    "Surface-water gleys": 9
}

def add_score_field_and_populate(fc, field_name, score_dict, category_field):
    """Adds integer field and assigns score values based on a lookup dict"""
    if field_name not in [f.name for f in arcpy.ListFields(fc)]:
        arcpy.AddField_management(fc, field_name, "SHORT")
    with arcpy.da.UpdateCursor(fc, [category_field, field_name]) as cursor:
        for row in cursor:
            row[1] = score_dict.get(row[0], 0)  # 0 if unmatched
            cursor.updateRow(row)

try:
    print("🔄 Assigning scores to Land Use...")
    add_score_field_and_populate(landuse_fc, landuse_score_field, landuse_scores, landuse_field)
    arcpy.conversion.PolygonToRaster(landuse_fc, landuse_score_field, landuse_raster, cell_assignment="MAXIMUM_COMBINED_AREA")
    print(f"✅ Created raster: {landuse_raster}")

    print("🔄 Assigning scores to Soil Type...")
    add_score_field_and_populate(soil_fc, soil_score_field, soil_scores, soil_field)
    arcpy.conversion.PolygonToRaster(soil_fc, soil_score_field, soil_raster, cell_assignment="MAXIMUM_COMBINED_AREA")
    print(f"✅ Created raster: {soil_raster}")

except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
except Exception as e:
    print(f"⚠️ Error: {e}")
