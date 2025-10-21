# village_app/utils/gis.py
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for thread safety
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, box
import matplotlib.patches as mpatches
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configure matplotlib to use a font that supports emojis (e.g., Segoe UI Emoji on Windows)
plt.rcParams['font.family'] = 'Segoe UI Emoji'

def generate_map_image(village, output_path):
    """
    Generate a map image based on village location and infrastructure data.
    Uses GeoPandas to plot features from a GeoJSON file.
    """
    try:
        logger.info(f"Starting map generation for village {village.name} at {output_path}")

        # Load the GeoJSON file with a raw string path
        gdf = gpd.read_file(r"C:\Users\prash\Downloads\filtered_output.geojson")
        gdf = gdf.to_crs(epsg=4326)  # Ensure WGS84 coordinate system

        # Define a bounding box around the village (0.03 degrees buffer ~3-4 km for zoom)
        minx, miny = village.location.x - 0.03, village.location.y - 0.03
        maxx, maxy = village.location.x + 0.03, village.location.y + 0.03
        bbox = box(minx, miny, maxx, maxy)

        # Filter the GeoDataFrame to the bounding box and specific features
        gdf = gdf[gdf.intersects(bbox)]
        # Filter for roads, buildings, parks, water bodies, and landmarks
        gdf_roads = gdf[gdf['highway'].notna()]
        gdf_buildings = gdf[gdf['building'].notna()]
        gdf_parks = gdf[gdf['landuse'] == 'park']
        gdf_gardens = gdf[gdf['amenity'] == 'garden']
        gdf_water = gdf[gdf['natural'] == 'water']
        gdf_landmarks = gdf[gdf['amenity'].isin(['school', 'hospital', 'place_of_worship'])]

        # Create a GeoDataFrame with the village location
        village_point = Point(village.location.x, village.location.y)
        village_gdf = gpd.GeoDataFrame([{"name": village.name, "geometry": village_point}], crs="EPSG:4326")

        # Simulate existing landmarks based on input data
        landmarks = []
        if village.infrastructure['lakes'] > 0:
            landmarks.append(('Lake', '🏞️', Point(village.location.x - 0.01, village.location.y + 0.01)))
        if village.infrastructure['temples'] > 0:
            landmarks.append(('Temple', '🛕', Point(village.location.x, village.location.y)))
        if village.number_of_schools > 0:
            landmarks.append(('School', '🏫', Point(village.location.x + 0.01, village.location.y - 0.01)))
        landmarks_gdf = gpd.GeoDataFrame(landmarks, columns=['Feature', 'Symbol', 'geometry'], geometry='geometry', crs="EPSG:4326")

        # Recommended features to plot (only if they don't exist)
        recommended_features = []
        if village.number_of_hospitals == 0:
            recommended_features.append(('Hospital', '🏥', Point(village.location.x - 0.015, village.location.y - 0.015)))
        if not village.post_office_availability:
            recommended_features.append(('Post Office', '📮', Point(village.location.x + 0.015, village.location.y + 0.015)))
        if village.petrol_bunks == 0:
            recommended_features.append(('Petrol Bunk', '⛽', Point(village.location.x - 0.01, village.location.y)))
        if village.parks == 0:
            recommended_features.append(('Park', '🌳', Point(village.location.x + 0.02, village.location.y + 0.02)))
        if village.playgrounds == 0:
            recommended_features.append(('Playground', '🏞️', Point(village.location.x + 0.02, village.location.y - 0.02)))
        if not village.street_lighting:
            recommended_features.append(('Street Lighting', '💡', Point(village.location.x, village.location.y + 0.01)))
        if not village.renewable_energy_source:
            recommended_features.append(('Solar Panels', '☀️', Point(village.location.x - 0.02, village.location.y)))
        if not village.waste_management_everyday:
            recommended_features.append(('Dumping Yard', '🗑️', Point(village.location.x + 0.01, village.location.y)))
        if not village.network_connectivity:
            recommended_features.append(('Signal Tower', '📡', Point(village.location.x - 0.015, village.location.y + 0.015)))
        if not village.market_availability:
            recommended_features.append(('Market Yard', '🏪', Point(village.location.x + 0.015, village.location.y - 0.015)))
        if not village.banks_atm_facility:
            recommended_features.append(('Bank/ATM', '🏧', Point(village.location.x - 0.02, village.location.y - 0.02)))
        if not village.public_transport:
            recommended_features.append(('Bus Bay', '🚌', Point(village.location.x + 0.01, village.location.y + 0.02)))

        recommended_gdf = gpd.GeoDataFrame(recommended_features, columns=['Feature', 'Symbol', 'geometry'], geometry='geometry', crs="EPSG:4326")

        # Plot the map
        fig, ax = plt.subplots(figsize=(12, 12))
        # Plot water bodies (blue)
        if not gdf_water.empty:
            gdf_water.plot(ax=ax, color='lightblue', alpha=0.7)
        # Plot parks (green)
        if not gdf_parks.empty:
            gdf_parks.plot(ax=ax, color='forestgreen', alpha=0.6)
        # Plot gardens (lime green)
        if not gdf_gardens.empty:
            gdf_gardens.plot(ax=ax, color='limegreen', alpha=0.6)
        # Plot buildings (light gray)
        if not gdf_buildings.empty:
            gdf_buildings.plot(ax=ax, color='lightgray', alpha=0.5)
        # Plot roads (black)
        if not gdf_roads.empty:
            gdf_roads.plot(ax=ax, color='black', linewidth=1.2)
        # Plot landmarks from GeoJSON
        if not gdf_landmarks.empty:
            gdf_landmarks.plot(ax=ax, color='purple', marker='*', markersize=100)

        # Plot village location with emoji
        village_gdf.plot(ax=ax, color='red', marker='o', markersize=120)
        ax.text(village.location.x, village.location.y + 0.003, '🏘️', fontsize=20, ha='center', va='center')
        ax.text(village.location.x, village.location.y - 0.003, village.name, fontsize=8, ha='center', va='top')

        # Plot existing landmarks with emojis
        if not landmarks_gdf.empty:
            for idx, row in landmarks_gdf.iterrows():
                ax.text(row['geometry'].x, row['geometry'].y, row['Symbol'], fontsize=20, ha='center', va='center')
                ax.text(row['geometry'].x, row['geometry'].y - 0.003, row['Feature'], fontsize=8, ha='center', va='top')

        # Plot recommended features with emojis
        if not recommended_gdf.empty:
            for idx, row in recommended_gdf.iterrows():
                ax.text(row['geometry'].x, row['geometry'].y, row['Symbol'], fontsize=20, ha='center', va='center')
                ax.text(row['geometry'].x, row['geometry'].y - 0.003, row['Feature'], fontsize=8, ha='center', va='top')

        # Create a custom legend
        legend_elements = [
            mpatches.Patch(color='lightblue', alpha=0.7, label='Water Bodies'),
            mpatches.Patch(color='forestgreen', alpha=0.6, label='Parks'),
            mpatches.Patch(color='limegreen', alpha=0.6, label='Gardens'),
            mpatches.Patch(color='lightgray', alpha=0.5, label='Buildings'),
            mpatches.Patch(color='black', label='Roads'),
            mpatches.Patch(color='purple', label='Landmarks')
        ]
        ax.legend(handles=legend_elements, loc='upper left', fontsize=10)

        # Customize the map
        ax.set_title(f"Development Map for {village.name}", fontsize=14, pad=15)
        ax.set_xlabel("Longitude", fontsize=12)
        ax.set_ylabel("Latitude", fontsize=12)
        ax.set_xlim(minx, maxx)
        ax.set_ylim(miny, maxy)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.set_facecolor('aliceblue')

        # Save and close the plot
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"Map successfully generated at {output_path}")

    except Exception as e:
        logger.error(f"Error generating map for village {village.name}: {str(e)}")
        raise