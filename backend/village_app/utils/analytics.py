'''# village_app/utils/analytics.py
import matplotlib.pyplot as plt

def get_analytics(village_data, output_path):
    analytics = {
        "population_growth": "Stable",
        "literacy_trend": "Improving" if village_data["literacy_rate"] > 0.5 else "Declining",
        "healthcare_score": 7.5 if village_data["healthcare_access"] == "Good" else 4.0
    }

    # Generate a chart
    fig, ax = plt.subplots()
    ax.bar(['Population', 'Literacy Rate'], [village_data['population'], village_data['literacy_rate'] * 100])
    ax.set_title("Village Analytics")
    plt.savefig(output_path, format='png')
    plt.close()

    return analytics


import matplotlib.pyplot as plt

def get_analytics(village_data, chart_path):
    # Example analytics based on new data
    fig, ax = plt.subplots()
    categories = ['Schools', 'Electricity (hrs)', 'Green Cover (%)']
    values = [village_data['number_of_schools'], village_data['electricity_supply_hours'], village_data['green_cover']]
    ax.bar(categories, values)
    ax.set_title('Village Infrastructure Analytics')
    plt.savefig(chart_path)
    plt.close()
    return {
        "population_growth": "Stable",
        "infrastructure_score": sum(values) / len(values) if values else 0,
        "sustainability_index": village_data['renewable_energy_source'] and village_data['green_cover'] > 20
    }
    



import matplotlib.pyplot as plt

def get_analytics(village_data, chart_path):
    # Detailed analytics
    analytics = {}

    # Population and Education
    analytics["population_growth"] = "Stable"
    analytics["literacy_score"] = village_data["literacy_rate"] * 100
    children_per_school = village_data["number_of_children"] / max(village_data["number_of_schools"], 1) if village_data["number_of_schools"] > 0 else village_data["number_of_children"]
    recommended_schools = max(1, int(village_data["number_of_children"] / 300))  # Assume 300 children per school
    analytics["schools_needed"] = f"{recommended_schools} schools (current: {village_data['number_of_schools']})"

    # Infrastructure
    infrastructure_score = (
        (village_data["electricity_supply_hours"] / 24 * 20) +
        (village_data["water_supply_to_every_home"] * 20) +
        (village_data["street_lighting"] * 20) +
        (village_data["public_transport"] * 20)
    ) / 80 * 100
    analytics["infrastructure_score"] = round(infrastructure_score, 2)

    # Sustainability
    sustainability_index = (
        (village_data["renewable_energy_source"] * 25) +
        (village_data["green_cover"] / 100 * 25) +
        (village_data["waste_management_everyday"] * 25) +
        (village_data["sanitation_everyday"] * 25)
    )
    analytics["sustainability_index"] = sustainability_index > 50

    # Community and Economic
    community_score = (
        (village_data["parks"] * 25) +
        (village_data["playgrounds"] * 25) +
        (village_data["market_availability"] * 25) +
        (village_data["banks_atm_facility"] * 25)
    ) / 100 * 100
    analytics["community_score"] = round(community_score, 2)

    # Connectivity
    connectivity_score = village_data["network_connectivity"] * 100
    analytics["connectivity_score"] = connectivity_score

    # Healthcare
    healthcare_score = {"Good": 100, "Average": 50, "Poor": 0}.get(village_data["healthcare_access"], 0)
    analytics["healthcare_score"] = healthcare_score

    # Generate chart
    fig, ax = plt.subplots(figsize=(10, 6))
    categories = ["Infra Score", "Sustainability", "Community", "Connectivity", "Healthcare"]
    values = [infrastructure_score, sustainability_index, community_score, connectivity_score, healthcare_score]
    ax.bar(categories, values)
    ax.set_title(f"Analytics for {village_data['name']}")
    for i, v in enumerate(values):
        ax.text(i, v + 1, str(round(v, 2)), ha='center')
    plt.savefig(chart_path)
    plt.close()

    return analytics
'''



'''
import matplotlib.pyplot as plt

def get_analytics(village_data, chart_path):
    analytics = {}

    # Population Growth
    population_growth_rate = ((village_data["current_census_population"] - village_data["previous_census_population"]) /
                            village_data["previous_census_population"] * 100) if village_data["previous_census_population"] > 0 else 0
    analytics["population_growth_rate"] = f"{round(population_growth_rate, 2)}%"
    analytics["population_growth_scale"] = "High" if population_growth_rate > 5 else "Moderate" if population_growth_rate > 0 else "Low"

    # Population vs. Area
    population_density = village_data["current_census_population"] / village_data["village_area"] if village_data["village_area"] > 0 else 0
    analytics["population_density"] = f"{round(population_density, 2)} people/km²"
    analytics["area_suitability"] = "Overcrowded" if population_density > 500 else "Balanced" if population_density > 100 else "Sparse"

    # Education
    children_per_school = village_data["number_of_children"] / max(village_data["number_of_schools"], 1) if village_data["number_of_schools"] > 0 else village_data["number_of_children"]
    recommended_schools = max(1, int(village_data["number_of_children"] / 300))
    analytics["schools_needed"] = f"{recommended_schools} schools (current: {village_data['number_of_schools']})"
    analytics["literacy_score"] = village_data["literacy_rate"] * 100

    # Infrastructure
    infrastructure_score = (
        (village_data["electricity_supply_hours"] / 24 * 20) +
        (village_data["water_supply_to_every_home"] * 20) +
        (village_data["street_lighting"] * 20) +
        (village_data["public_transport"] * 20)
    ) / 80 * 100
    analytics["infrastructure_score"] = round(infrastructure_score, 2)

    # Sustainability
    sustainability_index = (
        (village_data["renewable_energy_source"] * 25) +
        (village_data["green_cover"] / 100 * 25) +
        (village_data["waste_management_everyday"] * 25) +
        (village_data["sanitation_everyday"] * 25)
    )
    analytics["sustainability_index"] = sustainability_index > 50

    # Community and Economic
    community_score = (
        (village_data["parks"] * 25) +
        (village_data["playgrounds"] * 25) +
        (village_data["market_availability"] * 25) +
        (village_data["banks_atm_facility"] * 25)
    ) / 100 * 100
    analytics["community_score"] = round(community_score, 2)

    # Connectivity
    connectivity_score = village_data["network_connectivity"] * 100
    analytics["connectivity_score"] = connectivity_score

    # Healthcare
    healthcare_score = {"Good": 100, "Average": 50, "Poor": 0}.get(village_data["healthcare_access"], 0)
    analytics["healthcare_score"] = healthcare_score

    # Generate chart
    fig, ax = plt.subplots(figsize=(12, 6))
    categories = ["Pop Growth", "Density", "Infra Score", "Sustainability", "Community", "Connectivity", "Healthcare"]
    values = [abs(population_growth_rate), population_density, infrastructure_score, sustainability_index, community_score, connectivity_score, healthcare_score]
    ax.bar(categories, values)
    ax.set_title(f"Analytics for {village_data['name']}")
    for i, v in enumerate(values):
        ax.text(i, v + 1, str(round(v, 2)), ha='center', rotation=45)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    return analytics'''


'''
import matplotlib.pyplot as plt

def get_analytics(village_data, chart_path):
    analytics = {}

    # Population and Growth
    population_growth_rate = ((village_data["current_census_population"] - village_data["previous_census_population"]) / 
                            village_data["previous_census_population"] * 100) if village_data["previous_census_population"] > 0 else 0
    analytics["population_growth_rate"] = round(population_growth_rate, 2)
    analytics["population_growth_scale"] = "High" if population_growth_rate > 10 else "Moderate" if population_growth_rate > 0 else "Low"
    population_density = village_data["current_census_population"] / village_data["village_area"] if village_data["village_area"] > 0 else 0
    analytics["population_density"] = round(population_density, 2)
    analytics["area_suitability"] = "Overcrowded" if population_density > 2000 else "Dense" if population_density > 1000 else "Suitable"

    # Education
    analytics["literacy_score"] = village_data["literacy_rate"] * 100
    children_per_school = village_data["number_of_children"] / max(village_data["number_of_schools"], 1) if village_data["number_of_schools"] > 0 else village_data["number_of_children"]
    recommended_schools = max(1, int(village_data["number_of_children"] / 300))  # 300 children per school
    analytics["schools_needed"] = f"{recommended_schools} schools (current: {village_data['number_of_schools']})"

    # Infrastructure
    infrastructure_score = (
        (village_data["electricity_supply_hours"] / 24 * 20) +
        (village_data["water_supply_to_every_home"] * 20) +
        (village_data["street_lighting"] * 20) +
        (village_data["public_transport"] * 20)
    ) / 80 * 100
    analytics["infrastructure_score"] = round(infrastructure_score, 2)

    # Sustainability
    sustainability_index = (
        (village_data["renewable_energy_source"] * 25) +
        (village_data["green_cover"] / 100 * 25) +
        (village_data["waste_management_everyday"] * 25) +
        (village_data["sanitation_everyday"] * 25)
    )
    analytics["sustainability_index"] = sustainability_index > 50

    # Community and Economic
    community_score = (
        (village_data["parks"] * 25) +
        (village_data["playgrounds"] * 25) +
        (village_data["market_availability"] * 25) +
        (village_data["banks_atm_facility"] * 25)
    ) / 100 * 100
    analytics["community_score"] = round(community_score, 2)

    # Connectivity
    connectivity_score = village_data["network_connectivity"] * 100
    analytics["connectivity_score"] = connectivity_score

    # Healthcare
    healthcare_score = {"Good": 100, "Average": 50, "Poor": 0}.get(village_data["healthcare_access"], 0)
    analytics["healthcare_score"] = healthcare_score

    # Population vs Area Chart
    fig, ax = plt.subplots(figsize=(10, 6))
    categories = ["Population Density", "Infra Score", "Sustainability", "Community", "Connectivity", "Healthcare"]
    values = [population_density, infrastructure_score, sustainability_index, community_score, connectivity_score, healthcare_score]
    ax.bar(categories, values)
    ax.set_title(f"Analytics for {village_data['name']}")
    for i, v in enumerate(values):
        ax.text(i, v + 1, str(round(v, 2)), ha='center')
    plt.savefig(chart_path)
    plt.close()

    return analytics'''



# village_app/utils/analytics.py
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for thread safety
import matplotlib.pyplot as plt
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_analytics(village_data, output_path):
    logger.info(f"Generating analytics for village {village_data['name']} at {output_path}")

    # Extract data
    try:
        prev_pop = village_data["previous_census_population"]
        curr_pop = village_data["current_census_population"]
        area = village_data["village_area"]
        literacy_rate = village_data["literacy_rate"]
        healthcare_access = village_data["healthcare_access"]
        number_of_schools = village_data["number_of_schools"]
        number_of_hospitals = village_data["number_of_hospitals"]
        post_office_availability = village_data["post_office_availability"]
        petrol_bunks = village_data["petrol_bunks"]
        electricity_hours = village_data["electricity_supply_hours"]
        renewable_energy = village_data["renewable_energy_source"]
        water_supply = village_data["water_supply_to_every_home"]
        sanitation = village_data["sanitation_everyday"]
        waste_management = village_data["waste_management_everyday"]
        network_connectivity = village_data["network_connectivity"]
        market = village_data["market_availability"]
        banks_atm = village_data["banks_atm_facility"]
        green_cover = village_data["green_cover"]
        street_lighting = village_data["street_lighting"]
        public_transport = village_data["public_transport"]
    except KeyError as e:
        logger.error(f"Missing key in village_data: {str(e)}")
        raise ValueError(f"Missing required key in village_data: {str(e)}")

    # Validate data
    if not isinstance(prev_pop, (int, float)) or prev_pop < 0:
        logger.warning(f"Invalid previous_census_population: {prev_pop}. Setting to 0.")
        prev_pop = 0
    if not isinstance(curr_pop, (int, float)) or curr_pop < 0:
        logger.warning(f"Invalid current_census_population: {curr_pop}. Setting to 0.")
        curr_pop = 0
    if not isinstance(area, (int, float)) or area <= 0:
        logger.warning(f"Invalid village_area: {area}. Setting to 1 to avoid division by zero.")
        area = 1
    if not isinstance(literacy_rate, (int, float)) or literacy_rate < 0 or literacy_rate > 1:
        logger.warning(f"Invalid literacy_rate: {literacy_rate}. Setting to 0.")
        literacy_rate = 0

    # Population growth rate
    growth_rate = ((curr_pop - prev_pop) / prev_pop) * 100 if prev_pop > 0 else 0

    # Population density
    density = curr_pop / area if area > 0 else 0

    # Area suitability
    suitability = "Overcrowded" if density > 500 else "Sustainable"

    # Literacy score
    literacy_score = literacy_rate * 100

    # Schools needed (1 school per 1000 people as a rough estimate)
    schools_needed = max(0, (curr_pop // 1000) - number_of_schools)

    # Hospitals needed (1 hospital per 5000 people as a rough estimate)
    hospitals_needed = max(0, (curr_pop // 5000) - number_of_hospitals)

    # Infrastructure score (simple scoring based on availability)
    infra_score = sum([
        1 if electricity_hours > 12 else 0,
        1 if renewable_energy else 0,
        1 if water_supply else 0,
        1 if sanitation else 0,
        1 if waste_management else 0,
        1 if network_connectivity else 0,
        1 if market else 0,
        1 if banks_atm else 0,
        1 if street_lighting else 0,
        1 if public_transport else 0,
        1 if post_office_availability else 0,
        1 if petrol_bunks > 0 else 0
    ]) * 10 / 12

    # Sustainability index
    sustainability_index = renewable_energy and green_cover > 20 and waste_management

    # Community score (based on parks, playgrounds, etc.)
    community_score = (village_data["parks"] + village_data["playgrounds"]) * 10

    # Healthcare score
    healthcare_score = 100 if healthcare_access == "Good" else 50 if healthcare_access == "Average" else 0

    # Plot a simple analytics chart
    try:
        fig, ax = plt.subplots(figsize=(8, 6))
        metrics = ["Growth Rate", "Density", "Infra Score", "Literacy", "Healthcare"]
        values = [growth_rate, density, infra_score, literacy_score, healthcare_score]
        # Ensure values are valid for plotting
        values = [max(0, float(v)) for v in values]  # Prevent negative values
        ax.bar(metrics, values, color='skyblue')
        ax.set_title("Village Analytics")
        ax.set_ylabel("Value")
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        logger.info(f"Analytics chart generated at {output_path}")
    except Exception as e:
        logger.error(f"Error generating analytics chart: {str(e)}")
        # Do not raise; continue with analytics data

    # Always return the analytics data, even if chart generation fails
    analytics_data = {
        "population_growth_rate": round(growth_rate, 1),
        "population_density": round(density, 1),
        "area_suitability": suitability,
        "literacy_score": round(literacy_score, 1),
        "schools_needed": schools_needed,
        "hospitals_needed": hospitals_needed,
        "infrastructure_score": round(infra_score, 1),
        "sustainability_index": sustainability_index,
        "community_score": community_score,
        "healthcare_score": healthcare_score
    }
    logger.info("Analytics data generated successfully")
    return analytics_data