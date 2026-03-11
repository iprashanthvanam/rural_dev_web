import geopandas as gpd

gdf = gpd.read_file("data/india_states/Admin2.shp")

# filter Telangana
telangana = gdf[gdf["ST_NM"] == "Telangana"]

telangana.to_file("data/telangana.geojson", driver="GeoJSON")

print("Telangana GeoJSON created")