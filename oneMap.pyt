import arcpy
import os

class Toolbox(object):
    """ArcGIS Python Toolbox for OneMap Data Integration"""
    
    def __init__(self):
        self.label = "OneMap Data Integration"
        self.alias = "OneMapTool"
        self.tools = [DataIntegration]

class DataIntegration(object):
    """Tool to integrate GIS data into BP's OneMap system"""
    
    def __init__(self):
        self.label = "OneMap Data Integration"
        self.description = "Standardizes GIS datasets and exports them for different teams."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define tool parameters"""
        
        param0 = arcpy.Parameter(
            displayName="Input Folder (GIS Data Source)",
            name="input_folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        param1 = arcpy.Parameter(
            displayName="OneMap Geodatabase (Target GDB)",
            name="output_gdb",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Output")

        param2 = arcpy.Parameter(
            displayName="Export Format",
            name="export_format",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
            multiValue=False)

        param2.filter.type = "ValueList"
        param2.filter.list = ["GDB", "Shapefile", "GeoJSON", "Feature Service"]

        return [param0, param1, param2]

    def execute(self, parameters, messages):
        """Execute OneMap Data Integration"""

        input_folder = parameters[0].valueAsText
        output_gdb = parameters[1].valueAsText
        export_format = parameters[2].valueAsText

        arcpy.env.overwriteOutput = True

        # **Step 1: Ensure OneMap GDB Exists**
        if not arcpy.Exists(output_gdb):
            arcpy.AddMessage(f"📂 Creating OneMap database: {output_gdb}")
            arcpy.management.CreateFileGDB(os.path.dirname(output_gdb), os.path.basename(output_gdb))

        # **Step 2: Ensure Shapefile Output Folder Exists**
        shp_folder = os.path.join(os.path.dirname(output_gdb), "Shapefiles")
        if not os.path.exists(shp_folder):
            os.makedirs(shp_folder)

        # **Step 3: Integrate GIS Data**
        arcpy.AddMessage("🔄 Integrating datasets from input folder...")

        arcpy.env.workspace = input_folder  # Set workspace to input folder
        feature_classes = arcpy.ListFeatureClasses() or []  # Ensure list is not None

        if not feature_classes:
            arcpy.AddError("❌ No feature classes found in the input folder!")
            return

        for fc in feature_classes:
            in_fc = os.path.join(input_folder, fc)
            out_fc = os.path.join(output_gdb, fc)

            if arcpy.Exists(out_fc):
                arcpy.AddWarning(f"⚠️ {fc} already exists in target GDB. Skipping...")
            else:
                try:
                    if fc.lower().endswith(".shp"):  # Ensure Shapefiles are not stored in GDB
                        out_shp = os.path.join(shp_folder, fc)
                        arcpy.management.CopyFeatures(in_fc, out_shp)
                        arcpy.AddMessage(f"✅ Integrated {fc} into Shapefiles folder.")
                    else:
                        arcpy.management.CopyFeatures(in_fc, out_fc)
                        arcpy.AddMessage(f"✅ Integrated {fc} into GDB.")

                except arcpy.ExecuteError:
                    arcpy.AddError(f"❌ Error copying {fc}: {arcpy.GetMessages(2)}")

        # **Step 4: Schema Validation**
        arcpy.AddMessage("🔍 Performing schema validation...")
        arcpy.env.workspace = output_gdb

        fc_list = arcpy.ListFeatureClasses() or []  # Prevent NoneType error
        if fc_list:
            for fc in fc_list:
                fields = [f.name for f in arcpy.ListFields(fc)]
                if "Asset_ID" not in fields or "Last_Update" not in fields:
                    arcpy.AddWarning(f"⚠️ {fc} missing required fields!")
        else:
            arcpy.AddWarning("⚠️ No valid feature classes found in GDB for validation.")

        # **Step 5: Export Data Based on Role**
        export_folder = os.path.join(os.path.dirname(output_gdb), "Exports")
        if not os.path.exists(export_folder):
            os.makedirs(export_folder)

        arcpy.AddMessage(f"📦 Exporting data in {export_format} format...")

        if fc_list:
            for fc in fc_list:
                fc_path = os.path.join(output_gdb, fc)
                export_path = os.path.join(export_folder, fc)

                try:
                    if export_format == "Shapefile":
                        arcpy.conversion.FeatureClassToShapefile(fc_path, shp_folder)
                        arcpy.AddMessage(f"✅ Exported {fc} as Shapefile.")

                    elif export_format == "GeoJSON":
                        arcpy.FeaturesToJSON_conversion(fc_path, export_path + ".json")
                        arcpy.AddMessage(f"✅ Exported {fc} as GeoJSON.")

                    elif export_format == "Feature Service":
                        arcpy.AddMessage(f"🌍 {fc} would be published as a Feature Service.")

                except arcpy.ExecuteError:
                    arcpy.AddError(f"❌ Error exporting {fc}: {arcpy.GetMessages(2)}")
        else:
            arcpy.AddWarning("⚠️ No data available to export.")

        arcpy.AddMessage("✅ OneMap Data Integration Complete!")
