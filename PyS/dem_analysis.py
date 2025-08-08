import arcpy
from arcpy.sa import *
import time
import datetime

# ===== 🎬 START TIMER =====
start_time = time.time()

# ===== 🎯 WORKSPACE SETUP =====
arcpy.env.workspace = r"C:\GIS_Projects\Floodwarningsystem\Floodwarningsystem.gdb"
arcpy.env.overwriteOutput = True
dem = "DEM"  # 🔍 Input DEM raster

# ===== 🧩 CHECK EXTENSION =====
arcpy.CheckOutExtension("Spatial")

# ===== 🎨 TERMINAL COLORS =====
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"
RESET = "\033[0m"

def log(msg, level="info"):
    emoji = {
        "info": "🔷",
        "success": "✅",
        "start": "🚀",
        "error": "❌",
        "done": "🎉",
    }.get(level, "ℹ️")
    color = {
        "info": CYAN,
        "success": GREEN,
        "start": YELLOW,
        "error": RED,
        "done": GREEN,
    }.get(level, RESET)
    print(f"{color}{emoji} {msg}{RESET}")

try:
    log("Starting terrain analysis using ArcPy...", "start")
    log(f"Using DEM raster: {dem}", "info")

    # ===== 🧭 SLOPE =====
    log("Generating Slope raster...", "info")
    slope_raster = Slope(dem, "DEGREE")
    slope_output = "Slope_Highlands5"
    slope_raster.save(slope_output)
    log(f"Slope raster saved as: {slope_output}", "success")

    # ===== 🧭 FLOW DIRECTION =====
    log("Generating Flow Direction raster...", "info")
    flow_dir_raster = FlowDirection(dem)
    flow_dir_output = "FlowDir_Highlands5"
    flow_dir_raster.save(flow_dir_output)
    log(f"Flow Direction raster saved as: {flow_dir_output}", "success")

    # ===== 🧭 FLOW ACCUMULATION =====
    log("Generating Flow Accumulation raster...", "info")
    flow_acc_raster = FlowAccumulation(flow_dir_raster)
    flow_acc_output = "FlowAcc_Highlands5"
    flow_acc_raster.save(flow_acc_output)
    log(f"Flow Accumulation raster saved as: {flow_acc_output}", "success")

    # ===== 🕒 END TIMER AND SUMMARY =====
    end_time = time.time()
    duration = round(end_time - start_time, 2)
    log(f"All raster analyses completed in {duration} seconds.", "done")
    log("ArcPy automated terrain processing finished successfully.", "done")

except arcpy.ExecuteError:
    log("ArcPy execution error:", "error")
    print(arcpy.GetMessages(2))

except Exception as e:
    log(f"Unexpected error: {e}", "error")

finally:
    arcpy.CheckInExtension("Spatial")
