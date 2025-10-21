'''# village_app/utils/ai_recommendations.py
def get_ai_recommendations(village_data):
    # Placeholder AI logic (replace with actual AI model, e.g., scikit-learn)
    recommendations = {
        "infrastructure": "Build more roads and a hospital." if village_data["infrastructure"].get("roads") == "unpaved" else "Maintain existing infrastructure.",
        "education": "Increase literacy programs." if village_data["literacy_rate"] < 0.7 else "Continue current education programs.",
        "healthcare": "Improve access to clinics." if village_data["healthcare_access"] == "Poor" else "Maintain healthcare services.",
        "economic_growth": "Promote small businesses."
    }
    return recommendations


def get_ai_recommendations(village_data):
    recommendations = {
        "infrastructure": "Build more roads and a hospital." if village_data['infrastructure']['roads'] == 'unpaved' else "Maintain current infrastructure.",
        "education": "Increase literacy programs." if village_data['literacy_rate'] < 0.7 else "Maintain education levels.",
        "healthcare": "Maintain healthcare services." if village_data['healthcare_access'] == 'Good' else "Improve healthcare access.",
        "economic_growth": "Promote small businesses."
    }
    if village_data['number_of_schools'] < 2:
        recommendations["education"] += " Add more schools."
    if village_data['electricity_supply_hours'] < 12:
        recommendations["infrastructure"] += " Improve electricity supply."
    if not village_data['renewable_energy_source']:
        recommendations["sustainability"] = "Consider adopting renewable energy sources."
    return recommendations


def get_ai_recommendations(village_data):
    recommendations = {}

    # Infrastructure Recommendations
    if village_data['infrastructure']['roads'] == 'unpaved':
        recommendations["infrastructure"] = "Pave roads to improve accessibility."
    else:
        recommendations["infrastructure"] = "Maintain current road conditions."
    if village_data['electricity_supply_hours'] < 12:
        recommendations["infrastructure"] += " Increase electricity supply to at least 12 hours/day."
    if village_data['water_supply_to_every_home'] is False:
        recommendations["infrastructure"] += " Ensure water supply to every home."
    if village_data['street_lighting'] is False:
        recommendations["infrastructure"] += " Install street lighting for safety."

    # Education Recommendations
    if village_data['number_of_schools'] < 2 or village_data['literacy_rate'] < 0.7:
        recommendations["education"] = "Increase the number of schools and literacy programs."
    else:
        recommendations["education"] = "Maintain current education infrastructure."

    # Healthcare Recommendations
    if village_data['healthcare_access'] not in ['Good']:
        recommendations["healthcare"] = "Improve healthcare access with additional facilities."
    else:
        recommendations["healthcare"] = "Maintain current healthcare services."

    # Sustainability Recommendations
    if not village_data['renewable_energy_source']:
        recommendations["sustainability"] = "Adopt renewable energy sources to reduce costs."
    if village_data['green_cover'] < 20:
        recommendations["sustainability"] += " Increase green cover to at least 20% for environmental benefits."
    if village_data['waste_management_everyday'] is False:
        recommendations["sustainability"] += " Implement daily waste management."

    # Community and Economic Recommendations
    if village_data['parks'] == 0 or village_data['playgrounds'] == 0:
        recommendations["community"] = "Develop parks and playgrounds for community recreation."
    if village_data['market_availability'] is False:
        recommendations["economic_growth"] = "Establish a local market to boost economy."
    if village_data['banks_atm_facility'] is False:
        recommendations["economic_growth"] += " Provide banks/ATM facilities for financial access."
    if village_data['public_transport'] is False:
        recommendations["transportation"] = "Introduce public transport for better connectivity."
    if village_data['network_connectivity'] is False:
        recommendations["connectivity"] = "Improve network connectivity for communication."

    # Sanitation Recommendations
    if village_data['sanitation_everyday'] is False:
        recommendations["sanitation"] = "Ensure daily sanitation services."

    return recommendations


def get_ai_recommendations(village_data):
    recommendations = {}

    # Infrastructure Recommendations
    if village_data['infrastructure']['roads'] == 'unpaved':
        recommendations["infrastructure"] = "Pave roads."
    else:
        recommendations["infrastructure"] = "Maintain roads."
    if village_data['electricity_supply_hours'] < 12:
        recommendations["infrastructure"] += " Increase electricity to 12+ hours."
    if not village_data['water_supply_to_every_home']:
        recommendations["infrastructure"] += " Ensure water to all homes."
    if not village_data['street_lighting']:
        recommendations["infrastructure"] += " Add street lighting."

    # Education Recommendations
    if village_data['number_of_schools'] < 2 or village_data['literacy_rate'] < 0.7:
        recommendations["education"] = "Add schools and literacy programs."
    else:
        recommendations["education"] = "Maintain education."

    # Healthcare Recommendations
    if village_data['healthcare_access'] not in ['Good']:
        recommendations["healthcare"] = "Improve healthcare facilities."
    else:
        recommendations["healthcare"] = "Maintain healthcare."

    # Sustainability Recommendations
    if not village_data['renewable_energy_source']:
        recommendations["sustainability"] = "Adopt renewable energy."
    if village_data['green_cover'] < 20:
        recommendations["sustainability"] += " Increase green cover to 20%."
    if not village_data['waste_management_everyday']:
        recommendations["sustainability"] += " Implement daily waste management."

    # Community and Economic Recommendations
    if village_data['parks'] == 0 or village_data['playgrounds'] == 0:
        recommendations["community"] = "Develop parks/playgrounds."
    if not village_data['market_availability']:
        recommendations["economic_growth"] = "Establish a local market."
    if not village_data['banks_atm_facility']:
        recommendations["economic_growth"] += " Add banks/ATMs."
    if not village_data['public_transport']:
        recommendations["transportation"] = "Introduce public transport."
    if not village_data['network_connectivity']:
        recommendations["connectivity"] = "Improve network connectivity."

    # Sanitation Recommendations
    if not village_data['sanitation_everyday']:
        recommendations["sanitation"] = "Ensure daily sanitation."

    return recommendations
'''




'''def get_ai_recommendations(village_data):
    recommendations = {}

    # Infrastructure Recommendations
    if village_data['infrastructure']['roads'] == 'unpaved':
        recommendations["infrastructure"] = "Pave roads."
    else:
        recommendations["infrastructure"] = "Maintain roads."
    if village_data['electricity_supply_hours'] < 12:
        recommendations["infrastructure"] += " Supply electricity to 12+ hours."
    if not village_data['water_supply_to_every_home']:
        recommendations["infrastructure"] += " Ensure water pipeline connectivity to all homes."
    if not village_data['street_lighting']:
        recommendations["infrastructure"] += " Need to be street lighting."
    if village_data['infrastructure']['lakes'] < 1:
        recommendations["infrastructure"] += " Consider developing a lake for water resources."
    if village_data['infrastructure']['temples'] < 1:
        recommendations["infrastructure"] += " Build a temple for cultural significance."

    # Education Recommendations
    if village_data['number_of_schools'] < 2 or village_data['literacy_rate'] < 0.7:
        recommendations["education"] = "Build schools and literacy programs."
    else:
        recommendations["education"] = "Maintain education."

    # Healthcare Recommendations
    if village_data['healthcare_access'] not in ['Good']:
        recommendations["healthcare"] = "Improve healthcare facilities like medicine stores."
    else:
        recommendations["healthcare"] = "Maintain healthcare."

    # Sustainability Recommendations
    if not village_data['renewable_energy_source']:
        recommendations["sustainability"] = "Adopt renewable energy strategies."
    if village_data['green_cover'] < 20:
        recommendations["sustainability"] += " Increase green cover to 20%."
    if not village_data['waste_management_everyday']:
        recommendations["sustainability"] += " Implement daily waste management."

    # Community and Economic Recommendations
    if village_data['parks'] == 0 or village_data['playgrounds'] == 0:
        recommendations["community"] = "Build parks/playgrounds."
    if not village_data['market_availability']:
        recommendations["economic_growth"] = "Establish a local market."
    if not village_data['banks_atm_facility']:
        recommendations["economic_growth"] += " Establish banks/ATMs."
    if not village_data['public_transport']:
        recommendations["transportation"] = "Establish public transport like bus bay and buses."
    if not village_data['network_connectivity']:
        recommendations["connectivity"] = "Improve mobile network connectivity by installing cell towers."

    # Sanitation Recommendations
    if not village_data['sanitation_everyday']:
        recommendations["sanitation"] = "Ensure daily sanitation  using sanitation vehicles."

    return recommendations'''





'''def get_ai_recommendations(village_data):
    recommendations = {}

    # Infrastructure
    infra_recommendations = []
    if village_data["infrastructure"]["roads"] == "unpaved":
        infra_recommendations.append("Pave roads")
    if village_data["electricity_supply_hours"] < 12:
        infra_recommendations.append("Supply electricity for 12+ hours")
    if not village_data["water_supply_to_every_home"]:
        infra_recommendations.append("Ensure water pipeline connectivity to all homes")
    if not village_data["street_lighting"]:
        infra_recommendations.append("Add street lighting")
    if village_data["infrastructure"]["lakes"] == 0:
        infra_recommendations.append("Consider developing a lake")
    if village_data["infrastructure"]["temples"] == 0:
        infra_recommendations.append("Build a temple for cultural significance")
    recommendations["infrastructure"] = ", ".join(infra_recommendations) or "No major infrastructure improvements needed."

    # Education
    education_recommendations = []
    if village_data["number_of_schools"] == 0:
        education_recommendations.append("Build schools")
    if village_data["literacy_rate"] < 0.75:
        education_recommendations.append("Improve literacy programs")
    recommendations["education"] = ", ".join(education_recommendations) or "Education facilities are adequate."

    # Healthcare
    healthcare_recommendations = []
    if village_data["healthcare_access"] != "Good":
        healthcare_recommendations.append("Improve healthcare facilities like medicine stores")
    if village_data["number_of_hospitals"] == 0:
        healthcare_recommendations.append("Build a hospital")
    recommendations["healthcare"] = ", ".join(healthcare_recommendations) or "Healthcare facilities are sufficient."

    # Sustainability
    sustainability_recommendations = []
    if not village_data["renewable_energy_source"]:
        sustainability_recommendations.append("Adopt renewable energy strategies")
    if village_data["green_cover"] < 20:
        sustainability_recommendations.append("Increase green cover to 20%")
    if not village_data["waste_management_everyday"]:
        sustainability_recommendations.append("Implement daily waste management")
    recommendations["sustainability"] = ", ".join(sustainability_recommendations) or "Sustainability measures are in place."

    # Community
    community_recommendations = []
    if village_data["parks"] == 0:
        community_recommendations.append("Build parks")
    if village_data["playgrounds"] == 0:
        community_recommendations.append("Build playgrounds")
    recommendations["community"] = ", ".join(community_recommendations) or "Community facilities are adequate."

    # Economic Growth
    economic_recommendations = []
    if not village_data["market_availability"]:
        economic_recommendations.append("Establish a local market")
    if not village_data["banks_atm_facility"]:
        economic_recommendations.append("Establish banks/ATMs")
    if village_data["petrol_bunks"] == 0:
        economic_recommendations.append("Set up petrol bunks for economic activity")
    recommendations["economic_growth"] = ", ".join(economic_recommendations) or "Economic facilities are sufficient."

    # Transportation
    transportation_recommendations = []
    if not village_data["public_transport"]:
        transportation_recommendations.append("Establish public transport like bus bay and buses")
    recommendations["transportation"] = ", ".join(transportation_recommendations) or "Transportation facilities are adequate."

    # Connectivity
    connectivity_recommendations = []
    if not village_data["network_connectivity"]:
        connectivity_recommendations.append("Improve mobile network connectivity by installing cell towers")
    if not village_data["post_office_availability"]:
        connectivity_recommendations.append("Establish a post office")
    recommendations["connectivity"] = ", ".join(connectivity_recommendations) or "Connectivity is sufficient."

    # Sanitation
    sanitation_recommendations = []
    if not village_data["sanitation_everyday"]:
        sanitation_recommendations.append("Ensure daily sanitation using sanitation vehicles")
    recommendations["sanitation"] = ", ".join(sanitation_recommendations) or "Sanitation practices are in place."

    return recommendations'''



def get_ai_recommendations(village_data):
    recommendations = {}

    # Infrastructure
    infra_recommendations = []
    if village_data["infrastructure"]["roads"] == "unpaved":
        infra_recommendations.append("Pave roads")
    if village_data["electricity_supply_hours"] < 12:
        infra_recommendations.append("Supply electricity for 12+ hours")
    if not village_data["water_supply_to_every_home"]:
        infra_recommendations.append("Ensure water pipeline connectivity to all homes")
    if not village_data["street_lighting"]:
        infra_recommendations.append("Add street lighting")
    if village_data["infrastructure"]["lakes"] == 0:
        infra_recommendations.append("Consider developing a lake")
    if village_data["infrastructure"]["temples"] == 0:
        infra_recommendations.append("Build a temple for cultural significance")
    recommendations["infrastructure"] = ", ".join(infra_recommendations) or "No major infrastructure improvements needed."

    # Education
    education_recommendations = []
    if village_data["number_of_schools"] == 0:
        education_recommendations.append("Build schools")
    if village_data["literacy_rate"] < 0.75:
        education_recommendations.append("Improve literacy programs")
    recommendations["education"] = ", ".join(education_recommendations) or "Education facilities are adequate."

    # Healthcare
    healthcare_recommendations = []
    if village_data["healthcare_access"] != "Good":
        healthcare_recommendations.append("Improve healthcare facilities like medicine stores")
    if village_data["number_of_hospitals"] == 0:
        healthcare_recommendations.append("Build a hospital")
    recommendations["healthcare"] = ", ".join(healthcare_recommendations) or "Healthcare facilities are sufficient."

    # Sustainability
    sustainability_recommendations = []
    if not village_data["renewable_energy_source"]:
        sustainability_recommendations.append("Adopt renewable energy strategies")
    if village_data["green_cover"] < 20:
        sustainability_recommendations.append("Increase green cover to 20%")
    if not village_data["waste_management_everyday"]:
        sustainability_recommendations.append("Implement daily waste management")
    recommendations["sustainability"] = ", ".join(sustainability_recommendations) or "Sustainability measures are in place."

    # Community
    community_recommendations = []
    if village_data["parks"] == 0:
        community_recommendations.append("Build parks")
    if village_data["playgrounds"] == 0:
        community_recommendations.append("Build playgrounds")
    recommendations["community"] = ", ".join(community_recommendations) or "Community facilities are adequate."

    # Economic Growth
    economic_recommendations = []
    if not village_data["market_availability"]:
        economic_recommendations.append("Establish a local market")
    if not village_data["banks_atm_facility"]:
        economic_recommendations.append("Establish banks/ATMs")
    if village_data["petrol_bunks"] == 0:
        economic_recommendations.append("Set up petrol bunks for economic activity")
    recommendations["economic_growth"] = ", ".join(economic_recommendations) or "Economic facilities are sufficient."

    # Transportation
    transportation_recommendations = []
    if not village_data["public_transport"]:
        transportation_recommendations.append("Establish public transport like bus bay and buses")
    recommendations["transportation"] = ", ".join(transportation_recommendations) or "Transportation facilities are adequate."

    # Connectivity
    connectivity_recommendations = []
    if not village_data["network_connectivity"]:
        connectivity_recommendations.append("Improve mobile network connectivity by installing cell towers")
    if not village_data["post_office_availability"]:
        connectivity_recommendations.append("Establish a post office")
    recommendations["connectivity"] = ", ".join(connectivity_recommendations) or "Connectivity is sufficient."

    # Sanitation
    sanitation_recommendations = []
    if not village_data["sanitation_everyday"]:
        sanitation_recommendations.append("Ensure daily sanitation using sanitation vehicles")
    recommendations["sanitation"] = ", ".join(sanitation_recommendations) or "Sanitation practices are in place."

    # Additional Recommendations
    recommendations["healthcare_facilities"] = "Improve healthcare facilities by building hospitals if none exist." if village_data["number_of_hospitals"] == 0 else "Healthcare facilities are adequate."
    recommendations["post_office_services"] = "Establish a post office for better communication and services." if not village_data["post_office_availability"] else "Post office services are available."
    recommendations["petrol_bunk_access"] = "Ensure petrol bunks are available for better transportation support." if village_data["petrol_bunks"] == 0 else "Petrol bunks are sufficient."

    return recommendations