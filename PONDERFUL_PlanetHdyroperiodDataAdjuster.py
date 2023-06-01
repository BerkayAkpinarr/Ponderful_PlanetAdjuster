import os
import geopandas as gpd
import numpy as np

# Specify the folder path containing the shapefiles
folder_path = 'C:/Users/BerkayAkpinar/Desktop/PonderfulHydroperiod/pond_data/Water/SpainData/SpainSep/SpainSeptember'

# Specify the path to the target layer
target_layer_path = 'C:/Users/BerkayAkpinar/Desktop/PonderfulHydroperiod/Fixed_area_all.shp'

# Locate a folder to store the output shapefiles
output_folder = 'C:/Users/BerkayAkpinar/Desktop/PonderfulHydroperiod/pond_data/Water/SpainData/SpainSep/SpainSeptember/Dissolved/'

# Get a list of shapefiles in the folder
shapefiles = [f for f in os.listdir(folder_path) if f.endswith('.shp')]

# Iterate through the shapefiles
for shapefile in shapefiles:
    # Construct the full path to the shapefile
    file_path = os.path.join(folder_path, shapefile)

    try:
        # Load the input and target layers
        input_layer = gpd.read_file(file_path)
        target_layer = gpd.read_file(target_layer_path)

        ##Clip
        clipped_layer = dissolved_layer.geometry.clip(target_layer)

        # Perform the attribute join by location
        joined_layer = gpd.sjoin(input_layer, target_layer, how='inner', op='intersects')

        # Dissolve Layer
        dissolved_layer = joined_layer.dissolve(by=['id','Name','area'])

        ##Clip
        clipped_layer = dissolved_layer.geometry.clip(target_layer)

        # Calculate the area in hectares
        # Set the GeoDataFrame's CRS if not already defined
        clipped_layer = clipped_layer.geometry.to_crs(32632)

        planet_areas = clipped_layer.geometry.area/10000
        clipped_layer = gpd.GeoDataFrame(clipped_layer)


        #clipped_layer['planet'] = areas_hectar
        clipped_layer = clipped_layer.assign(planet_area=lambda x: planet_areas)

        # Construct the output shapefile path
        output_file = os.path.join(output_folder, f'joined_dissolved_{shapefile}')
        clipped_layer.to_file(output_file)



        print(f'Attribute join successful for {shapefile}. Output shapefile: {output_file}')
    except Exception as e:
        print(f'Attribute join failed for {shapefile}!')
        print(str(e))

# Set the folder path containing the shapefiles
shapefile_folder = output_folder

# Get a list of all shapefiles in the folder
shapefile_list = [filename for filename in os.listdir(shapefile_folder) if filename.endswith('.shp')]

# Iterate over the shapefiles
for shapefile_name in shapefile_list:
    # Read the shapefile into a GeoDataFrame
    shapefile_path = os.path.join(shapefile_folder, shapefile_name)
    gdf = gpd.read_file(shapefile_path)
    gdf = gdf.drop(columns=['geometry'])

    # Extract the filename from the shapefile path
    filename = os.path.basename(shapefile_path)

    # Define the number of characters to extract
    n = 12
    # Create a new column with the last n characters of the filename
    gdf['last_n_chars'] = filename[-n:]

    # Set the output CSV file path
    csv_path = os.path.join(shapefile_folder, f'{os.path.splitext(shapefile_name)[0]}.csv')

    # Save the GeoDataFrame as a CSV file
    gdf.to_csv(csv_path, index=False)
