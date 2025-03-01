OneMap Data Integration Tool

Author: Aliasghar Bazrafkan

Date: February 28, 2025

Version: 1.0

Tool Type: ArcGIS Python Toolbox (.pyt)

Compatible With: ArcGIS Pro 3.x

📌 Overview

The OneMap Data Integration Tool is designed to streamline GIS data management and sharing across multiple teams in big companies’ OneMap platform. The tool allows users to import, validate, and export GIS datasets from various sources while ensuring schema consistency and data standardization.

🎯 Key Features

✔ Automatic Integration of GIS Datasets – Import feature classes from a folder into an ArcGIS geodatabase.

✔ Schema Validation – Checks for required fields like Asset_ID and Last_Update.

✔ Multiple Export Formats – Convert data into Shapefiles, GeoJSON, or ArcGIS Feature Services.

✔ Ensures a Single Source of Truth – Standardizes geospatial data storage for companies’ OneMap.

✔ Detailed Logs & Error Handling – Provides clear success/error messages during execution.


🛠️ Installation & Requirements

1. System Requirements
ArcGIS Pro 3.x (or later)
Python 3.x (included in ArcGIS Pro)
ArcPy library (included in ArcGIS Pro)
Spatial Analyst Extension (Required if using raster analysis)

3. Setup Instructions
Download the OneMap Tool (OneMapIntegration.pyt)
Place the script in a project folder (e.g., C:\Users\YourName\Documents\ArcGIS\Projects\OneMap\).
Open ArcGIS Pro, go to the Catalog Pane, and navigate to your .pyt file.
Right-click the toolbox → Click Add to Project.
Run the tool from the Geoprocessing pane in ArcGIS Pro.


🚀 How to Use the Tool

1️⃣ Open the OneMap Integration Tool

In ArcGIS Pro, go to the Geoprocessing Toolbox and locate OneMap Data Integration.

2️⃣ Select Input & Output

Input Folder: Choose a folder containing your GIS datasets (.shp, .gdb, etc.).
Output Geodatabase: Specify where the integrated datasets should be stored.
Export Format (Optional): Choose between:
Geodatabase (default)
Shapefile
GeoJSON
Feature Service

3️⃣ Click Run
The tool will integrate datasets, validate schemas, and export data in the selected format.

📂 Output Files

The tool organizes outputs as follows:

📁 Inside the Selected Output Folder
File Type	Description
OneMap.gdb/	Geodatabase containing integrated datasets.
Shapefiles/	Folder with exported Shapefiles (if selected).
Exports/	Folder containing GeoJSON or Feature Service outputs.

🔍 Troubleshooting

Issue	Solution
No datasets appear in the geodatabase	Ensure the input folder contains feature classes.
Schema validation fails	Some datasets may be missing required fields (Asset_ID, Last_Update).
Export format error	Check if GeoJSON or Feature Service is supported in your ArcGIS Pro version.

📌 Future Improvements

Enhanced schema validation for BP-specific attributes.

Automated metadata tagging for better searchability.

Cloud & Mobile GIS support for companies’ distributed teams.









![image](https://github.com/user-attachments/assets/7f0ac997-4fd7-4002-b215-611b9daffd6b)






![image](https://github.com/user-attachments/assets/7b545fca-7c14-4c90-87b2-e8f7564e2bf3)
