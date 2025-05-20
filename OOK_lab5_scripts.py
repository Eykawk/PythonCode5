# Lab 5 scripts

import OOK_lab5_functions as l5
import geopandas as gpd
import matplotlib.pyplot as plt

#  Part 1:
#  Assign a variable to the Landsat file 
# Pass this to your new smart raster class
# Calculate NDVI and save to and output file
# Set the path to the Landsat image 
imagery_landsat = "Landsat_image_corv.tif"


# 2 Create a SmartRaster object using the Landsat imagery
r = l5.SmartRaster(imagery_landsat)

# 3 Call the method to calculate NDVI and save the result 
# This uses Band 4 and Band 3 by default
okay, result = r.calculate_ndvi(output_file= "ndvi_ouput.tif")



# Part 2:
# Assign a variable to the parcels data shapefile path
#  Pass this to your new smart vector class
#  Calculate zonal statistics and add to the attribute table of the parcels shapefile
# 1. Assign path to the shapefile 
parcels_vector = "Benton_County_TaxLots.shp"

# 2. Create a SmartVector object from your shapefile
smart_vector = l5.SmartVector(parcels_vector)

# 3. Call the method to compute zonal statistics from the NDVI raster
ndvi_raster = "ndvi_ouput.tif"

# This adds a new column with the average NDVI for each polygon
smart_vector.zonal_stats_to_field(ndvi_raster, output_field="NDVI_mean")

# 4. (Optional) Save updated shapefile to a new one
smart_vector.save_as("Corvallis_parcels_plusNDVI.shp")



#  Part 3: Optional
#  Use matplotlib to make a map of your census tracts with the average NDVI values


# Step 1: Load the updated shapefile with NDVI values
gdf = gpd.read_file("Corvallis_parcels_plusNDVI.shp")

# Step 2: Create the map
fig, ax = plt.subplots(figsize=(10, 8))

# Plot NDVI values using a green colormap
gdf.plot(
    column="NDVI_mean",      # Field to base colors on
    cmap="YlGn",             # Yellow-Green color scheme
    linewidth=0.1,           # Thin outlines
    edgecolor='black',
    legend=True,
    ax=ax
)

# Step 3: Style and show the map
ax.set_title("Mean NDVI by Parcel", fontsize=16)
ax.axis("off")  # Hide axes

# Show the map
plt.show()






