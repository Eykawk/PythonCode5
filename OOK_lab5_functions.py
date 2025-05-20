#####################
# Block 1:  Import the packages you'll need
# 
# 

import os, sys
import rasterio
import geopandas as gpd
import numpy as np
import rasterio.mask
from shapely.geometry import mapping
import matplotlib.pyplot as plt




##################
# Block 2: 
# set the working directory to the directory where the data are

# Change this to the directory where your data are

data_dir = "R:\\2025\\Spring\\GEOG562\\Students\\oseikwao\\LAB5\\Lab5_code\\"
os.chdir(data_dir)
print(os.getcwd())


##################
# Block 3: 
#   Set up a new smart raster class using rasterio  
#    that will have a method called "calculate_ndvi"

class Smartraster:
    def __init__(self, raster_path):
        """
        Initialize the Smartrater class
        Opens the raster file using rasterio and stores the dtaset.
        """
        self.raster_path = raster_path
        self.dataset = rasterio.open(raster_path)

    def calculate_ndvi(self, nir_band=4, red_band=3, output_file ="ndvi_output.tif"):
        """
        Calculate NDVI and save it as a new raster.
        
        Parameters:
        - nir_band: Band number for Near Infrared (e.g., Band 4)
        - red_band: Band number for Red (e.g., Band 3)
        - output_file: Path to save the NDVI raster
        """
        try:
            # Read the bands 
            nir = self.dataset.read(nir_band).astype('float32')
            red = self.dataset.read(red_band).astype('float32')
            

            # Calculate rhe NDVI including a value to avoid zero division
            ndvi =(nir - red) / (nir + red + 1e-6)

            # Prepare otput metadata
            meta = self.dataset.meta.copy()
            meta.update(dtype='float32', count=1)

            # Write NDVI raster
            with rasterio.open(output_file, 'w', **meta) as dst:
                dst.write(ndvi, 1)

            print(f"NDVI rater saved as {output_file}")
            return True, output_file
    
        except Exception as e:
            print(f"Error during NDVI computation: {e}")
            return False, None
        








##################
# Block 4: 
#   Set up a new smart vector class using geopandas
#    that will have a method similar to what did in lab 4
#    to calculate the zonal statistics for a raster
#    and add them as a column to the attribute table of the vector
class SmartVector:
    def __init__(self, vector_path, id_field="OBJECTID"):
        """
        This section :
        1. Initializes the SmartVector object.
        2. Loads the vector data 
        3. Sets the unique ID field used to join zonal statistics
        """
        self.vector_path = vector_path
        self.gdf = gpd.read_file(vector_path)
        self.id_field = id_field

    def zonal_stats_to_field(self, raster_path, output_field="ZonalStats"):
        """
        This section :
        1. Calculates the mean value of the raster within each polygon feature
        2. Stores it in a new field in the GeoDAtaFrame
        """
        stats = {}

        try:
            with rasterio.open(raster_path) as src:
                for idx, row in self.gdf.iterrows():
                    geom = [mapping(row.geometry)]
                    try:
                        out_image, out_transform = rasterio.mask.mask(src, geom, crop=True)
                        out_image = out_image[0] # uses the first band
                        masked_data = out_image[out_image != src.nodata]# remove NoData values

                        if masked_data.size > 0:
                            mean_val = masked_data.mean()
                        else:
                            mean_val = np.nan
                    except Exception as e:
                        mean_val = np.nan

                    stats[row[self.id_field]] = mean_val

        except Exception as e:
            print(f"Error opening raster file: {e}")
            return False
        
        # adding a new column and assigning new values
        self.gdf[output_field] = self.gdf[self.id_field].map(stats)
        print(f"Zonal statistics added to field '{output_field}'.")
        return True
    def save_as(self, output_path):
        """
        Saves the updated GeoDataFrame to a new file.
        """
        self.gdf.to_file(output_path)
        print(f"Vector data updated and saved to '{output_path}'.")









##