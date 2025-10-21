'''from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from village_app.models import Village
from village_app.utils.gis import generate_map_image as gis_generate_map_image
from village_app.utils.ai_recommendations import get_ai_recommendations
from village_app.utils.analytics import get_analytics
from village_app.utils.visualizations import generate_3d_model_image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
import os
from io import BytesIO

class Command(BaseCommand):
    help = 'Run the village development CLI tool'

    def handle(self, *args, **options):
        self.stdout.write("NextGen Rural Development Model")
        
        try:
            # Collect village data
            name = input("Enter village name: ")
            latitude = float(input("Enter latitude: "))
            longitude = float(input("Enter longitude: "))
            previous_census_population = int(input("Enter previous census population: "))
            current_census_population = int(input("Enter current census population: "))
            literacy_rate = float(input("Enter literacy rate (as a percentage, e.g., 75 for 75%): ")) / 100
            healthcare_access = input("Enter healthcare access (Good/Average/Poor): ")
            roads = input("Enter road type (e.g., paved/unpaved): ")
            parks = int(input("Enter number of parks: "))
            playgrounds = int(input("Enter number of playgrounds: "))
            lakes = int(input("Enter number of lakes: "))
            temples = int(input("Enter number of temples: "))
            number_of_schools = int(input("Enter number of schools: "))
            electricity_supply_hours = int(input("Enter electricity supply hours per day: "))
            renewable_energy_source = input("Does the village use renewable energy source? (y/n): ").lower() == 'y'
            water_supply_to_every_home = input("Is water supplied to every home? (y/n): ").lower() == 'y'
            sanitation_everyday = input("Is sanitation provided everyday? (y/n): ").lower() == 'y'
            waste_management_everyday = input("Is waste management provided everyday? (y/n): ").lower() == 'y'
            network_connectivity = input("Is there network connectivity? (y/n): ").lower() == 'y'
            market_availability = input("Is market available? (y/n): ").lower() == 'y'
            banks_atm_facility = input("Are banks/ATM facilities available? (y/n): ").lower() == 'y'
            green_cover = float(input("Enter green cover percentage (0-100): "))
            street_lighting = input("Is street lighting available? (y/n): ").lower() == 'y'
            public_transport = input("Is public transport available? (y/n): ").lower() == 'y'
            number_of_children = int(input("Enter number of children: "))
            village_area = float(input("Enter village area (in sq km): "))

            # Save village data
            village = Village(
                name=name,
                previous_census_population=previous_census_population,
                current_census_population=current_census_population,
                literacy_rate=literacy_rate,
                healthcare_access=healthcare_access,
                infrastructure={"roads": roads, "lakes": lakes, "temples": temples},
                location=Point(longitude, latitude),
                number_of_schools=number_of_schools,
                electricity_supply_hours=electricity_supply_hours,
                renewable_energy_source=renewable_energy_source,
                water_supply_to_every_home=water_supply_to_every_home,
                parks=parks,
                playgrounds=playgrounds,
                sanitation_everyday=sanitation_everyday,
                waste_management_everyday=waste_management_everyday,
                network_connectivity=network_connectivity,
                market_availability=market_availability,
                banks_atm_facility=banks_atm_facility,
                green_cover=green_cover,
                street_lighting=street_lighting,
                public_transport=public_transport,
                number_of_children=number_of_children,
                village_area=village_area
            )
            village.save()

            self.stdout.write(f"Village '{village.name}' saved with ID: {village.id}")

            # Generate outputs
            os.makedirs("outputs/maps", exist_ok=True)
            #os.makedirs("outputs/charts", exist_ok=True)
            #os.makedirs("outputs/models", exist_ok=True)
            os.makedirs("outputs/reports", exist_ok=True)

            # Generate map (using GeoPandas)
            map_path = f"outputs/maps/{village.id}_map.png"
            gis_generate_map_image(village, map_path)
            self.stdout.write(f"Map generated at: {map_path}")

            # Generate analytics
            village_data = {
                "name": village.name,
                "previous_census_population": village.previous_census_population,
                "current_census_population": village.current_census_population,
                "literacy_rate": village.literacy_rate,
                "healthcare_access": village.healthcare_access,
                "infrastructure": village.infrastructure,
                "number_of_schools": village.number_of_schools,
                "electricity_supply_hours": village.electricity_supply_hours,
                "renewable_energy_source": village.renewable_energy_source,
                "water_supply_to_every_home": village.water_supply_to_every_home,
                "parks": village.parks,
                "playgrounds": village.playgrounds,
                "sanitation_everyday": village.sanitation_everyday,
                "waste_management_everyday": village.waste_management_everyday,
                "network_connectivity": village.network_connectivity,
                "market_availability": village.market_availability,
                "banks_atm_facility": village.banks_atm_facility,
                "green_cover": village.green_cover,
                "street_lighting": village.street_lighting,
                "public_transport": village.public_transport,
                "number_of_children": village.number_of_children,
                "village_area": village.village_area
            }
            chart_path = f"outputs/charts/{village.id}_analytics.png"
            analytics = get_analytics(village_data, chart_path)
            self.stdout.write("Analytics Results:")
            for key, value in analytics.items():
                self.stdout.write(f"  {key}: {value}")
            self.stdout.write(f"Analytics chart generated at: {chart_path}")

            # Generate AI recommendations
            recommendations = get_ai_recommendations(village_data)
            self.stdout.write("AI Recommendations:")
            for key, value in recommendations.items():
                self.stdout.write(f"  {key}: {value}")

            # Generate 3D model image
            model_path = f"outputs/models/{village.id}_3d_model.png"
            generate_3d_model_image(village.id, model_path)
            self.stdout.write(f"3D model image generated at: {model_path}")

            # Generate PDF report
            report_path = f"outputs/reports/{village.id}_report.pdf"
            p = canvas.Canvas(report_path, pagesize=landscape(letter))
            page_width, page_height = landscape(letter)
            y = page_height - 50
            x = 100

            def new_page(p):
                p.showPage()
                return page_height - 50

            def draw_wrapped_text(p, x, y, text, max_width=500):
                words = text.split()
                lines = []
                current_line = ""
                for word in words:
                    test_line = f"{current_line} {word}".strip()
                    if p.stringWidth(test_line, "Helvetica", 12) <= max_width:
                        current_line = test_line
                    else:
                        lines.append(current_line)
                        current_line = word
                lines.append(current_line)
                for line in lines:
                    p.drawString(x, y, line)
                    y -= 20
                return y

            # Title and Basic Info
            p.drawString(x, y, f"Development Plan for: {village.name}")
            y -= 20
            p.drawString(x, y, f"Previous Census Pop: {village.previous_census_population}")
            y -= 20
            p.drawString(x, y, f"Current Census Pop: {village.current_census_population}")
            y -= 20
            p.drawString(x, y, f"Number of Children: {village.number_of_children}")
            y -= 20
            p.drawString(x, y, f"Village Area: {village.village_area} sq km")
            y -= 20
            p.drawString(x, y, f"Literacy Rate: {village.literacy_rate * 100}%")
            y -= 20
            p.drawString(x, y, f"Healthcare Access: {village.healthcare_access}")
            y -= 20

            # Infrastructure
            p.drawString(x, y, "Infrastructure:")
            y -= 20
            for key, value in village.infrastructure.items():
                p.drawString(x + 20, y, f"{key}: {value}")
                y -= 20
                if y < 50:
                    y = new_page(p)

            p.drawString(x + 20, y, f"Number of Schools: {village.number_of_schools}")
            y -= 20
            p.drawString(x + 20, y, f"Electricity Supply (hours/day): {village.electricity_supply_hours}")
            y -= 20
            p.drawString(x + 20, y, f"Renewable Energy Source: {village.renewable_energy_source}")
            y -= 20
            p.drawString(x + 20, y, f"Water Supply to Every Home: {village.water_supply_to_every_home}")
            y -= 20
            p.drawString(x + 20, y, f"Number of Parks: {village.parks}")
            y -= 20
            p.drawString(x + 20, y, f"Number of Playgrounds: {village.playgrounds}")
            y -= 20
            p.drawString(x + 20, y, f"Sanitation Everyday: {village.sanitation_everyday}")
            y -= 20
            p.drawString(x + 20, y, f"Waste Management Everyday: {village.waste_management_everyday}")
            y -= 20
            p.drawString(x + 20, y, f"Network Connectivity: {village.network_connectivity}")
            y -= 20
            p.drawString(x + 20, y, f"Market Availability: {village.market_availability}")
            y -= 20
            p.drawString(x + 20, y, f"Banks/ATM Facility: {village.banks_atm_facility}")
            y -= 20
            p.drawString(x + 20, y, f"Green Cover (%): {village.green_cover}")
            y -= 20
            p.drawString(x + 20, y, f"Street Lighting: {village.street_lighting}")
            y -= 20
            p.drawString(x + 20, y, f"Public Transport: {village.public_transport}")
            y -= 20
            if y < 50:
                y = new_page(p)

            # Analytics
            p.drawString(x, y, "Analytics:")
            y -= 20
            for key, value in analytics.items():
                y = draw_wrapped_text(p, x + 20, y, f"{key}: {value}")
                if y < 50:
                    y = new_page(p)

            # Recommendations
            p.drawString(x, y, "Recommendations:")
            y -= 20
            for key, value in recommendations.items():
                y = draw_wrapped_text(p, x + 20, y, f"{key}: {value}")
                if y < 50:
                    y = new_page(p)

            p.showPage()
            p.save()
            self.stdout.write(f"PDF report generated at: {report_path}")

        except Exception as e:
            self.stdout.write(f"Error: {str(e)}")'''




'''from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from village_app.models import Village
from village_app.utils.gis import generate_map_image as gis_generate_map_image
from village_app.utils.ai_recommendations import get_ai_recommendations
from village_app.utils.analytics import get_analytics
#from village_app.utils.visualizations import generate_map_image, generate_3d_model_image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import blue, green, black

import os
from io import BytesIO

class Command(BaseCommand):
    help = 'Run the village development CLI tool'

    def handle(self, *args, **options):
        self.stdout.write("Welcome to the Village Development CLI Tool!")
        
        try:
            # Collect village data
            name = input("Enter village name: ")
            previous_census_population = int(input("Enter previous census population: "))
            current_census_population = int(input("Enter current census population: "))
            village_area = float(input("Enter village area (sq km): "))
            literacy_rate = float(input("Enter literacy rate (as a percentage, e.g., 75 for 75%): ")) / 100
            healthcare_access = input("Enter healthcare access (Good/Average/Poor): ")
            roads = input("Enter road type (e.g., paved/unpaved): ")
            lakes = int(input("Enter number of lakes: "))
            temples = int(input("Enter number of temples: "))
            latitude = float(input("Enter latitude: "))
            longitude = float(input("Enter longitude: "))
            number_of_schools = int(input("Enter number of schools: "))
            electricity_supply_hours = int(input("Enter electricity supply hours per day: "))
            renewable_energy_source = input("Does the village use renewable energy source? (y/n): ").lower() == 'y'
            water_supply_to_every_home = input("Is water supplied to every home? (y/n): ").lower() == 'y'
            parks = int(input("Enter number of parks: "))
            playgrounds = int(input("Enter number of playgrounds: "))
            sanitation_everyday = input("Is sanitation provided everyday? (y/n): ").lower() == 'y'
            waste_management_everyday = input("Is waste management provided everyday? (y/n): ").lower() == 'y'
            network_connectivity = input("Is there network connectivity? (y/n): ").lower() == 'y'
            market_availability = input("Is market available? (y/n): ").lower() == 'y'
            banks_atm_facility = input("Are banks/ATM facilities available? (y/n): ").lower() == 'y'
            green_cover = float(input("Enter green cover percentage (0-100): "))
            street_lighting = input("Is street lighting available? (y/n): ").lower() == 'y'
            public_transport = input("Is public transport available? (y/n): ").lower() == 'y'
            number_of_children = int(input("Enter number of children: "))
            district = input("Enter district: ")
            pincode = input("Enter pincode: ")
            state = input("Enter state: ")
            sarpanch = input("Enter sarpanch name: ")
            MRO = input("Enter MRO name: ")

            # Save village data
            village = Village(
                name=name,
                previous_census_population=previous_census_population,
                current_census_population=current_census_population,
                village_area=village_area,
                population=current_census_population,  # Use current as population
                literacy_rate=literacy_rate,
                healthcare_access=healthcare_access,
                infrastructure={"roads": roads, "lakes": lakes, "temples": temples},
                location=Point(longitude, latitude),
                number_of_schools=number_of_schools,
                electricity_supply_hours=electricity_supply_hours,
                renewable_energy_source=renewable_energy_source,
                water_supply_to_every_home=water_supply_to_every_home,
                parks=parks,
                playgrounds=playgrounds,
                sanitation_everyday=sanitation_everyday,
                waste_management_everyday=waste_management_everyday,
                network_connectivity=network_connectivity,
                market_availability=market_availability,
                banks_atm_facility=banks_atm_facility,
                green_cover=green_cover,
                street_lighting=street_lighting,
                public_transport=public_transport,
                number_of_children=number_of_children,
                district=district,
                pincode=pincode,
                state=state,
                sarpanch=sarpanch,
                MRO=MRO
            )
            village.save()

            self.stdout.write(f"Village '{village.name}' saved with ID: {village.id}")

            # Generate outputs
            os.makedirs("outputs/maps", exist_ok=True)
            os.makedirs("outputs/charts", exist_ok=True)
            os.makedirs("outputs/models", exist_ok=True)
            os.makedirs("outputs/reports", exist_ok=True)

            # Generate map (using GeoPandas/PostGIS)
            map_path = f"outputs/maps/{village.id}_map.png"
            gis_generate_map_image(village, map_path)
            self.stdout.write(f"Map generated at: {map_path}")

            # Generate Leaflet map (replaced with Python)
            leaflet_map_path = f"outputs/maps/{village.id}_leaflet_map.png"
            generate_map_image(village.id, leaflet_map_path)
            self.stdout.write(f"Leaflet map generated at: {leaflet_map_path}")

            # Generate analytics
            village_data = {
                "name": village.name,
                "previous_census_population": village.previous_census_population,
                "current_census_population": village.current_census_population,
                "village_area": village.village_area,
                "population": village.population,
                "literacy_rate": village.literacy_rate,
                "healthcare_access": village.healthcare_access,
                "infrastructure": village.infrastructure,
                "number_of_schools": village.number_of_schools,
                "electricity_supply_hours": village.electricity_supply_hours,
                "renewable_energy_source": village.renewable_energy_source,
                "water_supply_to_every_home": village.water_supply_to_every_home,
                "parks": village.parks,
                "playgrounds": village.playgrounds,
                "sanitation_everyday": village.sanitation_everyday,
                "waste_management_everyday": village.waste_management_everyday,
                "network_connectivity": village.network_connectivity,
                "market_availability": village.market_availability,
                "banks_atm_facility": village.banks_atm_facility,
                "green_cover": village.green_cover,
                "street_lighting": village.street_lighting,
                "public_transport": village.public_transport,
                "number_of_children": village.number_of_children,
                "district": village.district,
                "pincode": village.pincode,
                "state": village.state,
                "sarpanch": village.sarpanch,
                "MRO": village.MRO
            }
            chart_path = f"outputs/charts/{village.id}_analytics.png"
            analytics = get_analytics(village_data, chart_path)
            self.stdout.write("Analytics Results:")
            for key, value in analytics.items():
                self.stdout.write(f"  {key}: {value}")
            self.stdout.write(f"Analytics chart generated at: {chart_path}")

            # Generate AI recommendations
            recommendations = get_ai_recommendations(village_data)
            self.stdout.write("AI Recommendations:")
            for key, value in recommendations.items():
                self.stdout.write(f"  {key}: {value}")

            # Generate 3D model image (replaced with Python)
            model_path = f"outputs/models/{village.id}_3d_model.png"
            generate_3d_model_image(village.id, model_path)
            self.stdout.write(f"3D model image generated at: {model_path}")

            # Generate PDF report
            report_path = f"outputs/reports/{village.id}_report.pdf"
            p = canvas.Canvas(report_path, pagesize=landscape(letter))
            page_width, page_height = landscape(letter)
            y = page_height - 50
            x = 100
            margin = 50
            styles = getSampleStyleSheet()
            heading_style = ParagraphStyle(name='Heading', parent=styles['Heading1'], textColor=blue, fontSize=14, spaceAfter=10)
            data_style = ParagraphStyle(name='Data', parent=styles['Normal'], textColor=green, fontSize=12)

            def new_page(p):
                p.showPage()
                p.setFont("Helvetica", 12)
                p.line(margin, page_height - margin, page_width - margin, page_height - margin)  # Top border
                p.line(margin, margin, page_width - margin, margin)  # Bottom border
                p.line(margin, page_height - margin, margin, margin)  # Left border
                p.line(page_width - margin, page_height - margin, page_width - margin, margin)  # Right border
                return page_height - 70

            # Draw borders for the first page
            p.setFont("Helvetica", 12)
            p.line(margin, page_height - margin, page_width - margin, page_height - margin)  # Top border
            p.line(margin, margin, page_width - margin, margin)  # Bottom border
            p.line(margin, page_height - margin, margin, margin)  # Left border
            p.line(page_width - margin, page_height - margin, page_width - margin, margin)  # Right border

            # Title
            p.drawString(x, y, f"Development Plan for {village.name}")
            y -= 30

            # Overview
            story = []
            story.append(Paragraph(f"<b>Overview</b>", heading_style))
            story.append(Paragraph(f"Previous Census Population: {village.previous_census_population}", data_style))
            story.append(Paragraph(f"Current Census Population: {village.current_census_population}", data_style))
            story.append(Paragraph(f"Number of Children: {village.number_of_children}", data_style))
            story.append(Paragraph(f"Village Area: {village.village_area} sq km", data_style))
            story.append(Paragraph(f"Literacy Rate: {village.literacy_rate * 100}%", data_style))
            story.append(Paragraph(f"Healthcare Access: {village.healthcare_access}", data_style))
            story.append(Paragraph(f"Population Growth Rate: {analytics['population_growth_rate']}%", data_style))
            from reportlab.platypus import SimpleDocTemplate
            doc = SimpleDocTemplate(report_path, pagesize=landscape(letter), leftMargin=margin, rightMargin=margin, topMargin=margin, bottomMargin=margin)
            doc.build(story)
            y -= len(story) * 20

            # Current Infrastructure Assessment
            p.setFont("Helvetica-Bold", 12)
            p.setFillColor(blue)
            p.drawString(x, y, "Current Infrastructure Assessment")
            p.setFillColor(black)
            y -= 20
            p.setFont("Helvetica", 12)
            p.setFillColor(green)
            p.drawString(x + 20, y, f"Roads: {village.infrastructure['roads']}")
            y -= 20
            p.drawString(x + 20, y, f"Lakes: {village.infrastructure['lakes']}")
            y -= 20
            p.drawString(x + 20, y, f"Temples: {village.infrastructure['temples']}")
            y -= 20
            p.drawString(x + 20, y, f"Number of Schools: {village.number_of_schools}")
            y -= 20
            p.drawString(x + 20, y, f"Electricity Supply (hours/day): {village.electricity_supply_hours}")
            y -= 20
            p.drawString(x + 20, y, f"Renewable Energy Source: {village.renewable_energy_source}")
            y -= 20
            p.drawString(x + 20, y, f"Water Supply to Every Home: {village.water_supply_to_every_home}")
            y -= 20
            p.drawString(x + 20, y, f"Number of Parks: {village.parks}")
            y -= 20
            p.drawString(x + 20, y, f"Number of Playgrounds: {village.playgrounds}")
            y -= 20
            p.drawString(x + 20, y, f"Sanitation Everyday: {village.sanitation_everyday}")
            y -= 20
            p.drawString(x + 20, y, f"Waste Management Everyday: {village.waste_management_everyday}")
            y -= 20
            p.drawString(x + 20, y, f"Network Connectivity: {village.network_connectivity}")
            y -= 20
            p.drawString(x + 20, y, f"Market Availability: {village.market_availability}")
            y -= 20
            p.drawString(x + 20, y, f"Banks/ATM Facility: {village.banks_atm_facility}")
            y -= 20
            p.drawString(x + 20, y, f"Green Cover (%): {village.green_cover}")
            y -= 20
            p.drawString(x + 20, y, f"Street Lighting: {village.street_lighting}")
            y -= 20
            p.drawString(x + 20, y, f"Public Transport: {village.public_transport}")
            y -= 20
            if y < 50:
                y = new_page(p)

            # Additional Details
            p.setFillColor(blue)
            p.drawString(x, y, "Additional Details")
            p.setFillColor(black)
            y -= 20
            p.setFillColor(green)
            p.drawString(x + 20, y, f"District: {village.district}")
            y -= 20
            p.drawString(x + 20, y, f"Pincode: {village.pincode}")
            y -= 20
            p.drawString(x + 20, y, f"State: {village.state}")
            y -= 20
            p.drawString(x + 20, y, f"Sarpanch: {village.sarpanch}")
            y -= 20
            p.drawString(x + 20, y, f"MRO: {village.MRO}")
            y -= 20
            if y < 50:
                y = new_page(p)

            # Analysis
            p.setFillColor(blue)
            p.drawString(x, y, "Analysis")
            p.setFillColor(black)
            y -= 20
            p.setFillColor(green)
            for key, value in analytics.items():
                p.drawString(x + 20, y, f"{key.replace('_', ' ').title()}: {value}")
                y -= 20
                if y < 50:
                    y = new_page(p)

            # Recommendations
            p.setFillColor(blue)
            p.drawString(x, y, "Recommendations")
            p.setFillColor(black)
            y -= 20
            p.setFillColor(green)
            for key, value in recommendations.items():
                p.drawString(x + 20, y, f"{key.replace('_', ' ').title()}: {value}")
                y -= 20
                if y < 50:
                    y = new_page(p)

            p.showPage()
            p.save()
            self.stdout.write(f"PDF report generated at: {report_path}")

        except Exception as e:
            self.stdout.write(f"Error: {str(e)}")'''



'''from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from village_app.models import Village
from village_app.utils.gis import generate_map_image as gis_generate_map_image
from village_app.utils.ai_recommendations import get_ai_recommendations
from village_app.utils.analytics import get_analytics
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import blue, green, black, HexColor
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.lib.units import inch
import os
from io import BytesIO

class Command(BaseCommand):
    help = 'Run the village development CLI tool'

    def handle(self, *args, **options):
        self.stdout.write("Welcome to the Village Development CLI Tool!")
        
        try:
            # Collect village data
            name = input("Enter village name: ")
            previous_census_population = int(input("Enter previous census population: "))
            current_census_population = int(input("Enter current census population: "))
            village_area = float(input("Enter village area (sq km): "))
            literacy_rate = float(input("Enter literacy rate (as a percentage, e.g., 75 for 75%): ")) / 100
            healthcare_access = input("Enter healthcare access (Good/Average/Poor): ")
            roads = input("Enter road type (e.g., paved/unpaved): ")
            lakes = int(input("Enter number of lakes: "))
            temples = int(input("Enter number of temples: "))
            latitude = float(input("Enter latitude: "))
            longitude = float(input("Enter longitude: "))
            number_of_schools = int(input("Enter number of schools: "))
            electricity_supply_hours = int(input("Enter electricity supply hours per day: "))
            renewable_energy_source = input("Does the village use renewable energy source? (y/n): ").lower() == 'y'
            water_supply_to_every_home = input("Is water supplied to every home? (y/n): ").lower() == 'y'
            parks = int(input("Enter number of parks: "))
            playgrounds = int(input("Enter number of playgrounds: "))
            sanitation_everyday = input("Is sanitation provided everyday? (y/n): ").lower() == 'y'
            waste_management_everyday = input("Is waste management provided everyday? (y/n): ").lower() == 'y'
            network_connectivity = input("Is there network connectivity? (y/n): ").lower() == 'y'
            market_availability = input("Is market available? (y/n): ").lower() == 'y'
            banks_atm_facility = input("Are banks/ATM facilities available? (y/n): ").lower() == 'y'
            green_cover = float(input("Enter green cover percentage (0-100): "))
            street_lighting = input("Is street lighting available? (y/n): ").lower() == 'y'
            public_transport = input("Is public transport available? (y/n): ").lower() == 'y'
            number_of_children = int(input("Enter number of children: "))
            district = input("Enter district: ")
            pincode = input("Enter pincode: ")
            state = input("Enter state: ")
            sarpanch = input("Enter sarpanch name: ")
            MRO = input("Enter MRO name: ")

            # Save village data
            village = Village(
                name=name,
                previous_census_population=previous_census_population,
                current_census_population=current_census_population,
                village_area=village_area,
                population=current_census_population,
                literacy_rate=literacy_rate,
                healthcare_access=healthcare_access,
                infrastructure={"roads": roads, "lakes": lakes, "temples": temples},
                location=Point(longitude, latitude),
                number_of_schools=number_of_schools,
                electricity_supply_hours=electricity_supply_hours,
                renewable_energy_source=renewable_energy_source,
                water_supply_to_every_home=water_supply_to_every_home,
                parks=parks,
                playgrounds=playgrounds,
                sanitation_everyday=sanitation_everyday,
                waste_management_everyday=waste_management_everyday,
                network_connectivity=network_connectivity,
                market_availability=market_availability,
                banks_atm_facility=banks_atm_facility,
                green_cover=green_cover,
                street_lighting=street_lighting,
                public_transport=public_transport,
                number_of_children=number_of_children,
                district=district,
                pincode=pincode,
                state=state,
                sarpanch=sarpanch,
                MRO=MRO
            )
            village.save()

            self.stdout.write(f"Village '{village.name}' saved with ID: {village.id}")

            # Generate outputs
            os.makedirs("outputs/maps", exist_ok=True)
            os.makedirs("outputs/charts", exist_ok=True)
            os.makedirs("outputs/models", exist_ok=True)
            os.makedirs("outputs/reports", exist_ok=True)

            # Generate map (using GeoPandas/PostGIS)
            map_path = f"outputs/maps/{village.id}_map.png"
            gis_generate_map_image(village, map_path)
            self.stdout.write(f"Map generated at: {map_path}")

            # Generate analytics
            village_data = {
                "name": village.name,
                "previous_census_population": village.previous_census_population,
                "current_census_population": village.current_census_population,
                "village_area": village.village_area,
                "population": village.population,
                "literacy_rate": village.literacy_rate,
                "healthcare_access": village.healthcare_access,
                "infrastructure": village.infrastructure,
                "number_of_schools": village.number_of_schools,
                "electricity_supply_hours": village.electricity_supply_hours,
                "renewable_energy_source": village.renewable_energy_source,
                "water_supply_to_every_home": village.water_supply_to_every_home,
                "parks": village.parks,
                "playgrounds": village.playgrounds,
                "sanitation_everyday": village.sanitation_everyday,
                "waste_management_everyday": village.waste_management_everyday,
                "network_connectivity": village.network_connectivity,
                "market_availability": village.market_availability,
                "banks_atm_facility": village.banks_atm_facility,
                "green_cover": village.green_cover,
                "street_lighting": village.street_lighting,
                "public_transport": village.public_transport,
                "number_of_children": village.number_of_children,
                "district": village.district,
                "pincode": village.pincode,
                "state": village.state,
                "sarpanch": village.sarpanch,
                "MRO": village.MRO
            }
            chart_path = f"outputs/charts/{village.id}_analytics.png"
            analytics = get_analytics(village_data, chart_path)
            self.stdout.write("Analytics Results:")
            for key, value in analytics.items():
                self.stdout.write(f"  {key}: {value}")
            self.stdout.write(f"Analytics chart generated at: {chart_path}")

            # Generate AI recommendations
            recommendations = get_ai_recommendations(village_data)
            self.stdout.write("AI Recommendations:")
            for key, value in recommendations.items():
                self.stdout.write(f"  {key}: {value}")

            # Generate PDF report
            report_path = f"outputs/reports/{village.id}_report.pdf"
            buffer = BytesIO()
            doc = SimpleDocTemplate(report_path, pagesize=landscape(letter), leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
            styles = getSampleStyleSheet()
            heading_style = ParagraphStyle(name='Heading', fontName='Helvetica-Bold', fontSize=14, textColor=blue, spaceAfter=10)
            subheading_style = ParagraphStyle(name='SubHeading', fontName='Helvetica', fontSize=12, textColor=blue, spaceAfter=8)
            data_style = ParagraphStyle(name='Data', fontName='Times-Roman', fontSize=11, textColor=green, spaceAfter=6)
            title_style = ParagraphStyle(name='Title', fontName='Helvetica-Bold', fontSize=16, textColor=black, alignment=1, spaceAfter=12)

            story = []

            # Header Section with Village Details
            header_box = Drawing(0, 0)
            header_box.add(Rect(-0.5*inch, -0.2*inch, 11*inch, 0.7*inch, fillColor=HexColor('#E6F0FA'), strokeColor=blue))
            story.append(header_box)
            story.append(Paragraph(f"Development Plan for {village.name}", title_style))
            story.append(Paragraph(f"District: {village.district}, State: {village.state}, Pincode: {village.pincode}", subheading_style))
            story.append(Paragraph(f"Sarpanch: {village.sarpanch}, MRO: {village.MRO}", subheading_style))
            story.append(Spacer(1, 0.2*inch))

            # Overview Section
            story.append(Paragraph("Overview", heading_style))
            story.append(Paragraph(f"Previous Census Population: {village.previous_census_population}", data_style))
            story.append(Paragraph(f"Current Census Population: {village.current_census_population}", data_style))
            story.append(Paragraph(f"Number of Children: {village.number_of_children}", data_style))
            story.append(Paragraph(f"Village Area: {village.village_area} sq km", data_style))
            story.append(Paragraph(f"Literacy Rate: {village.literacy_rate * 100}%", data_style))
            story.append(Paragraph(f"Healthcare Access: {village.healthcare_access}", data_style))
            story.append(Paragraph(f"Population Growth Rate: {analytics['population_growth_rate']}%", data_style))
            story.append(Spacer(1, 0.2*inch))

            # Current Infrastructure Assessment
            infra_box = Drawing(0, 0)
            infra_box.add(Rect(-0.5*inch, -0.2*inch, 11*inch, 2.5*inch, fillColor=HexColor('#F9F9F9'), strokeColor=blue))
            story.append(infra_box)
            story.append(Paragraph("Current Infrastructure Assessment", heading_style))
            story.append(Paragraph(f"Roads: {village.infrastructure['roads']}", data_style))
            story.append(Paragraph(f"Lakes: {village.infrastructure['lakes']}", data_style))
            story.append(Paragraph(f"Temples: {village.infrastructure['temples']}", data_style))
            story.append(Paragraph(f"Number of Schools: {village.number_of_schools}", data_style))
            story.append(Paragraph(f"Electricity Supply (hours/day): {village.electricity_supply_hours}", data_style))
            story.append(Paragraph(f"Renewable Energy Source: {village.renewable_energy_source}", data_style))
            story.append(Paragraph(f"Water Supply to Every Home: {village.water_supply_to_every_home}", data_style))
            story.append(Paragraph(f"Number of Parks: {village.parks}", data_style))
            story.append(Paragraph(f"Number of Playgrounds: {village.playgrounds}", data_style))
            story.append(Paragraph(f"Sanitation Everyday: {village.sanitation_everyday}", data_style))
            story.append(Paragraph(f"Waste Management Everyday: {village.waste_management_everyday}", data_style))
            story.append(Paragraph(f"Network Connectivity: {village.network_connectivity}", data_style))
            story.append(Paragraph(f"Market Availability: {village.market_availability}", data_style))
            story.append(Paragraph(f"Banks/ATM Facility: {village.banks_atm_facility}", data_style))
            story.append(Paragraph(f"Green Cover (%): {village.green_cover}", data_style))
            story.append(Paragraph(f"Street Lighting: {village.street_lighting}", data_style))
            story.append(Paragraph(f"Public Transport: {village.public_transport}", data_style))
            story.append(Spacer(1, 0.2*inch))

            # Additional Details
            details_box = Drawing(0, 0)
            details_box.add(Rect(-0.5*inch, -0.2*inch, 11*inch, 0.9*inch, fillColor=HexColor('#F9F9F9'), strokeColor=blue))
            story.append(details_box)
            story.append(Paragraph("Additional Details", heading_style))
            story.append(Paragraph(f"District: {village.district}", data_style))
            story.append(Paragraph(f"Pincode: {village.pincode}", data_style))
            story.append(Paragraph(f"State: {village.state}", data_style))
            story.append(Paragraph(f"Sarpanch: {village.sarpanch}", data_style))
            story.append(Paragraph(f"MRO: {village.MRO}", data_style))
            story.append(Spacer(1, 0.2*inch))

            # Analysis
            analysis_box = Drawing(0, 0)
            analysis_box.add(Rect(-0.5*inch, -0.2*inch, 11*inch, 1.5*inch, fillColor=HexColor('#F9F9F9'), strokeColor=blue))
            story.append(analysis_box)
            story.append(Paragraph("Analysis", heading_style))
            for key, value in analytics.items():
                story.append(Paragraph(f"{key.replace('_', ' ').title()}: {value}", data_style))
            story.append(Spacer(1, 0.2*inch))

            # Recommendations
            rec_box = Drawing(0, 0)
            rec_box.add(Rect(-0.5*inch, -0.2*inch, 11*inch, 2*inch, fillColor=HexColor('#F9F9F9'), strokeColor=blue))
            story.append(rec_box)
            story.append(Paragraph("Recommendations", heading_style))
            for key, value in recommendations.items():
                story.append(Paragraph(f"{key.replace('_', ' ').title()}: {value}", data_style))
            story.append(Spacer(1, 0.2*inch))

            # Build the PDF
            doc.build(story)
            self.stdout.write(f"PDF report generated at: {report_path}")

        except Exception as e:
            self.stdout.write(f"Error: {str(e)}")'''




'''from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from village_app.models import Village
from village_app.utils.gis import generate_map_image as gis_generate_map_image
from village_app.utils.ai_recommendations import get_ai_recommendations
from village_app.utils.analytics import get_analytics
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import blue, green, black, HexColor
from reportlab.lib.units import inch
import os

class Command(BaseCommand):
    help = 'Run the village development CLI tool'

    def handle(self, *args, **options):
        self.stdout.write("Welcome to the Village Development CLI Tool!")
        
        try:
            # Collect village data
            name = input("Enter village name: ")
            previous_census_population = int(input("Enter previous census population: "))
            current_census_population = int(input("Enter current census population: "))
            village_area = float(input("Enter village area (sq km): "))
            literacy_rate = float(input("Enter literacy rate (as a percentage, e.g., 75 for 75%): ")) / 100
            healthcare_access = input("Enter healthcare access (Good/Average/Poor): ")
            roads = input("Enter road type (e.g., paved/unpaved): ")
            lakes = int(input("Enter number of lakes: "))
            temples = int(input("Enter number of temples: "))
            latitude = float(input("Enter latitude: "))
            longitude = float(input("Enter longitude: "))
            number_of_schools = int(input("Enter number of schools: "))
            electricity_supply_hours = int(input("Enter electricity supply hours per day: "))
            renewable_energy_source = input("Does the village use renewable energy source? (y/n): ").lower() == 'y'
            water_supply_to_every_home = input("Is water supplied to every home? (y/n): ").lower() == 'y'
            parks = int(input("Enter number of parks: "))
            playgrounds = int(input("Enter number of playgrounds: "))
            sanitation_everyday = input("Is sanitation provided everyday? (y/n): ").lower() == 'y'
            waste_management_everyday = input("Is waste management provided everyday? (y/n): ").lower() == 'y'
            network_connectivity = input("Is there network connectivity? (y/n): ").lower() == 'y'
            market_availability = input("Is market available? (y/n): ").lower() == 'y'
            banks_atm_facility = input("Are banks/ATM facilities available? (y/n): ").lower() == 'y'
            green_cover = float(input("Enter green cover percentage (0-100): "))
            street_lighting = input("Is street lighting available? (y/n): ").lower() == 'y'
            public_transport = input("Is public transport available? (y/n): ").lower() == 'y'
            number_of_children = int(input("Enter number of children: "))
            district = input("Enter district: ")
            pincode = input("Enter pincode: ")
            state = input("Enter state: ")
            sarpanch = input("Enter sarpanch name: ")
            MRO = input("Enter MRO name: ")

            # Save village data
            village = Village(
                name=name,
                previous_census_population=previous_census_population,
                current_census_population=current_census_population,
                village_area=village_area,
                population=current_census_population,
                literacy_rate=literacy_rate,
                healthcare_access=healthcare_access,
                infrastructure={"roads": roads, "lakes": lakes, "temples": temples},
                location=Point(longitude, latitude),
                number_of_schools=number_of_schools,
                electricity_supply_hours=electricity_supply_hours,
                renewable_energy_source=renewable_energy_source,
                water_supply_to_every_home=water_supply_to_every_home,
                parks=parks,
                playgrounds=playgrounds,
                sanitation_everyday=sanitation_everyday,
                waste_management_everyday=waste_management_everyday,
                network_connectivity=network_connectivity,
                market_availability=market_availability,
                banks_atm_facility=banks_atm_facility,
                green_cover=green_cover,
                street_lighting=street_lighting,
                public_transport=public_transport,
                number_of_children=number_of_children,
                district=district,
                pincode=pincode,
                state=state,
                sarpanch=sarpanch,
                MRO=MRO
            )
            village.save()

            self.stdout.write(f"Village '{village.name}' saved with ID: {village.id}")

            # Generate outputs
            os.makedirs("outputs/maps", exist_ok=True)
            os.makedirs("outputs/charts", exist_ok=True)
            os.makedirs("outputs/models", exist_ok=True)
            os.makedirs("outputs/reports", exist_ok=True)

            # Generate map (using GeoPandas/PostGIS)
            map_path = f"outputs/maps/{village.id}_map.png"
            gis_generate_map_image(village, map_path)
            self.stdout.write(f"Map generated at: {map_path}")

            # Generate analytics
            village_data = {
                "name": village.name,
                "previous_census_population": village.previous_census_population,
                "current_census_population": village.current_census_population,
                "village_area": village.village_area,
                "population": village.population,
                "literacy_rate": village.literacy_rate,
                "healthcare_access": village.healthcare_access,
                "infrastructure": village.infrastructure,
                "number_of_schools": village.number_of_schools,
                "electricity_supply_hours": village.electricity_supply_hours,
                "renewable_energy_source": village.renewable_energy_source,
                "water_supply_to_every_home": village.water_supply_to_every_home,
                "parks": village.parks,
                "playgrounds": village.playgrounds,
                "sanitation_everyday": village.sanitation_everyday,
                "waste_management_everyday": village.waste_management_everyday,
                "network_connectivity": village.network_connectivity,
                "market_availability": village.market_availability,
                "banks_atm_facility": village.banks_atm_facility,
                "green_cover": village.green_cover,
                "street_lighting": village.street_lighting,
                "public_transport": village.public_transport,
                "number_of_children": village.number_of_children,
                "district": village.district,
                "pincode": village.pincode,
                "state": village.state,
                "sarpanch": village.sarpanch,
                "MRO": village.MRO
            }
            chart_path = f"outputs/charts/{village.id}_analytics.png"
            analytics = get_analytics(village_data, chart_path)
            self.stdout.write("Analytics Results:")
            for key, value in analytics.items():
                self.stdout.write(f"  {key}: {value}")
            self.stdout.write(f"Analytics chart generated at: {chart_path}")

            # Generate AI recommendations
            recommendations = get_ai_recommendations(village_data)
            self.stdout.write("AI Recommendations:")
            for key, value in recommendations.items():
                self.stdout.write(f"  {key}: {value}")

            # Generate PDF report
            report_path = f"outputs/reports/{village.id}_report.pdf"
            doc = SimpleDocTemplate(report_path, pagesize=landscape(letter), leftMargin=0.75*inch, rightMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch)
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(name='Title', fontName='Helvetica-Bold', fontSize=18, textColor=black, alignment=1, spaceAfter=12)
            heading_style = ParagraphStyle(name='Heading', fontName='Helvetica-Bold', fontSize=14, textColor=blue, spaceAfter=10)
            data_style = ParagraphStyle(name='Data', fontName='Helvetica', fontSize=11, textColor=green, leading=14)
            subheading_style = ParagraphStyle(name='SubHeading', fontName='Helvetica', fontSize=10, textColor=black, spaceAfter=6)

            story = []

            # Header with Village Details
            header_data = [
                [Paragraph(f"Development Plan for {village.name}", title_style)],
                [Paragraph(f"District: {village.district} | State: {village.state} | Pincode: {village.pincode}", subheading_style)],
                [Paragraph(f"Sarpanch: {village.sarpanch} | MRO: {village.MRO}", subheading_style)]
            ]
            header_table = Table(header_data, colWidths=[7.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor('#E0F7FA')),
                ('TEXTCOLOR', (0, 0), (-1, -1), black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, blue)
            ]))
            story.append(header_table)
            story.append(Spacer(1, 0.2*inch))

            # Current Infrastructure Assessment
            infra_data = [
                [Paragraph("Current Infrastructure Assessment", heading_style)],
                [Paragraph(f"Roads: {village.infrastructure['roads']}", data_style)],
                [Paragraph(f"Lakes: {village.infrastructure['lakes']}", data_style)],
                [Paragraph(f"Temples: {village.infrastructure['temples']}", data_style)],
                [Paragraph(f"Number of Schools: {village.number_of_schools}", data_style)],
                [Paragraph(f"Electricity Supply (hours/day): {village.electricity_supply_hours}", data_style)],
                [Paragraph(f"Renewable Energy Source: {village.renewable_energy_source}", data_style)],
                [Paragraph(f"Water Supply to Every Home: {village.water_supply_to_every_home}", data_style)],
                [Paragraph(f"Number of Parks: {village.parks}", data_style)],
                [Paragraph(f"Number of Playgrounds: {village.playgrounds}", data_style)],
                [Paragraph(f"Sanitation Everyday: {village.sanitation_everyday}", data_style)],
                [Paragraph(f"Waste Management Everyday: {village.waste_management_everyday}", data_style)],
                [Paragraph(f"Network Connectivity: {village.network_connectivity}", data_style)],
                [Paragraph(f"Market Availability: {village.market_availability}", data_style)],
                [Paragraph(f"Banks/ATM Facility: {village.banks_atm_facility}", data_style)],
                [Paragraph(f"Green Cover (%): {village.green_cover}", data_style)],
                [Paragraph(f"Street Lighting: {village.street_lighting}", data_style)],
                [Paragraph(f"Public Transport: {village.public_transport}", data_style)]
            ]
            infra_table = Table(infra_data, colWidths=[7.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F5F5F5')),
                ('TEXTCOLOR', (0, 0), (-1, -1), green),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('LEADING', (0, 0), (-1, -1), 14),
                ('GRID', (0, 0), (-1, -1), 0.5, blue),
                ('BOX', (0, 0), (-1, -1), 1, blue)
            ]))
            story.append(infra_table)
            story.append(Spacer(1, 0.2*inch))

            # Additional Details
            details_data = [
                [Paragraph("Additional Details", heading_style)],
                [Paragraph(f"District: {village.district}", data_style)],
                [Paragraph(f"Pincode: {village.pincode}", data_style)],
                [Paragraph(f"State: {village.state}", data_style)],
                [Paragraph(f"Sarpanch: {village.sarpanch}", data_style)],
                [Paragraph(f"MRO: {village.MRO}", data_style)]
            ]
            details_table = Table(details_data, colWidths=[7.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F5F5F5')),
                ('TEXTCOLOR', (0, 0), (-1, -1), green),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('LEADING', (0, 0), (-1, -1), 14),
                ('GRID', (0, 0), (-1, -1), 0.5, blue),
                ('BOX', (0, 0), (-1, -1), 1, blue)
            ]))
            story.append(details_table)
            story.append(Spacer(1, 0.2*inch))

            # Analysis
            analysis_data = [
                [Paragraph("Analysis", heading_style)]
            ]
            for key, value in analytics.items():
                analysis_data.append([Paragraph(f"{key.replace('_', ' ').title()}: {value}", data_style)])
            analysis_table = Table(analysis_data, colWidths=[7.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F5F5F5')),
                ('TEXTCOLOR', (0, 0), (-1, -1), green),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('LEADING', (0, 0), (-1, -1), 14),
                ('GRID', (0, 0), (-1, -1), 0.5, blue),
                ('BOX', (0, 0), (-1, -1), 1, blue)
            ]))
            story.append(analysis_table)
            story.append(Spacer(1, 0.2*inch))

            # Recommendations
            rec_data = [
                [Paragraph("Recommendations", heading_style)]
            ]
            for key, value in recommendations.items():
                rec_data.append([Paragraph(f"{key.replace('_', ' ').title()}: {value}", data_style)])
            rec_table = Table(rec_data, colWidths=[7.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F5F5F5')),
                ('TEXTCOLOR', (0, 0), (-1, -1), green),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('LEADING', (0, 0), (-1, -1), 14),
                ('GRID', (0, 0), (-1, -1), 0.5, blue),
                ('BOX', (0, 0), (-1, -1), 1, blue)
            ]))
            story.append(rec_table)

            # Build the PDF
            doc.build(story)
            self.stdout.write(f"PDF report generated at: {report_path}")

        except Exception as e:
            self.stdout.write(f"Error: {str(e)}")'''




'''from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from village_app.models import Village
from village_app.utils.gis import generate_map_image as gis_generate_map_image
from village_app.utils.ai_recommendations import get_ai_recommendations
from village_app.utils.analytics import get_analytics
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import blue, green, black, HexColor
from reportlab.lib.units import inch
import os

class Command(BaseCommand):
    help = 'Run the village development CLI tool'

    def format_boolean(self, value):
        """Convert boolean values to 'Yes' or 'No' for display."""
        return "Yes" if value else "No"

    def handle(self, *args, **options):
        self.stdout.write("Welcome to the Village Development CLI Tool!")
        
        try:
            # Collect village data
            name = input("Enter village name: ")
            previous_census_population = int(input("Enter previous census population: "))
            current_census_population = int(input("Enter current census population: "))
            village_area = float(input("Enter village area (sq km): "))
            literacy_rate = float(input("Enter literacy rate (as a percentage, e.g., 75 for 75%): ")) / 100
            healthcare_access = input("Enter healthcare access (Good/Average/Poor): ")
            roads = input("Enter road type (e.g., paved/unpaved): ")
            lakes = int(input("Enter number of lakes: "))
            temples = int(input("Enter number of temples: "))
            latitude = float(input("Enter latitude: "))
            longitude = float(input("Enter longitude: "))
            number_of_schools = int(input("Enter number of schools: "))
            number_of_hospitals = int(input("Enter number of hospitals: "))  # New input
            post_office_availability = input("Is post office available? (y/n): ").lower() == 'y'  # New input
            petrol_bunks = int(input("Enter number of petrol bunks: "))  # New input
            electricity_supply_hours = int(input("Enter electricity supply hours per day: "))
            renewable_energy_source = input("Does the village use renewable energy source? (y/n): ").lower() == 'y'
            water_supply_to_every_home = input("Is water supplied to every home? (y/n): ").lower() == 'y'
            parks = int(input("Enter number of parks: "))
            playgrounds = int(input("Enter number of playgrounds: "))
            sanitation_everyday = input("Is sanitation provided everyday? (y/n): ").lower() == 'y'
            waste_management_everyday = input("Is waste management provided everyday? (y/n): ").lower() == 'y'
            network_connectivity = input("Is there network connectivity? (y/n): ").lower() == 'y'
            market_availability = input("Is market available? (y/n): ").lower() == 'y'
            banks_atm_facility = input("Are banks/ATM facilities available? (y/n): ").lower() == 'y'
            green_cover = float(input("Enter green cover percentage (0-100): "))
            street_lighting = input("Is street lighting available? (y/n): ").lower() == 'y'
            public_transport = input("Is public transport available? (y/n): ").lower() == 'y'
            number_of_children = int(input("Enter number of children: "))
            district = input("Enter district: ")
            pincode = input("Enter pincode: ")
            state = input("Enter state: ")
            sarpanch = input("Enter sarpanch name: ")
            MRO = input("Enter MRO name: ")

            # Save village data
            village = Village(
                name=name,
                previous_census_population=previous_census_population,
                current_census_population=current_census_population,
                village_area=village_area,
                population=current_census_population,
                literacy_rate=literacy_rate,
                healthcare_access=healthcare_access,
                infrastructure={"roads": roads, "lakes": lakes, "temples": temples},
                location=Point(longitude, latitude),
                number_of_schools=number_of_schools,
                number_of_hospitals=number_of_hospitals,  # New field
                post_office_availability=post_office_availability,  # New field
                petrol_bunks=petrol_bunks,  # New field
                electricity_supply_hours=electricity_supply_hours,
                renewable_energy_source=renewable_energy_source,
                water_supply_to_every_home=water_supply_to_every_home,
                parks=parks,
                playgrounds=playgrounds,
                sanitation_everyday=sanitation_everyday,
                waste_management_everyday=waste_management_everyday,
                network_connectivity=network_connectivity,
                market_availability=market_availability,
                banks_atm_facility=banks_atm_facility,
                green_cover=green_cover,
                street_lighting=street_lighting,
                public_transport=public_transport,
                number_of_children=number_of_children,
                district=district,
                pincode=pincode,
                state=state,
                sarpanch=sarpanch,
                MRO=MRO
            )
            village.save()

            self.stdout.write(f"Village '{village.name}' saved with ID: {village.id}")

            # Generate outputs
            os.makedirs("outputs/maps", exist_ok=True)
            os.makedirs("outputs/charts", exist_ok=True)
            os.makedirs("outputs/models", exist_ok=True)
            os.makedirs("outputs/reports", exist_ok=True)

            # Generate map (using GeoPandas/PostGIS)
            map_path = f"outputs/maps/{village.id}_map.png"
            gis_generate_map_image(village, map_path)
            self.stdout.write(f"Map generated at: {map_path}")

            # Generate analytics
            village_data = {
                "name": village.name,
                "previous_census_population": village.previous_census_population,
                "current_census_population": village.current_census_population,
                "village_area": village.village_area,
                "population": village.population,
                "literacy_rate": village.literacy_rate,
                "healthcare_access": village.healthcare_access,
                "infrastructure": village.infrastructure,
                "number_of_schools": village.number_of_schools,
                "number_of_hospitals": village.number_of_hospitals,  # New field
                "post_office_availability": village.post_office_availability,  # New field
                "petrol_bunks": village.petrol_bunks,  # New field
                "electricity_supply_hours": village.electricity_supply_hours,
                "renewable_energy_source": village.renewable_energy_source,
                "water_supply_to_every_home": village.water_supply_to_every_home,
                "parks": village.parks,
                "playgrounds": village.playgrounds,
                "sanitation_everyday": village.sanitation_everyday,
                "waste_management_everyday": village.waste_management_everyday,
                "network_connectivity": village.network_connectivity,
                "market_availability": village.market_availability,
                "banks_atm_facility": village.banks_atm_facility,
                "green_cover": village.green_cover,
                "street_lighting": village.street_lighting,
                "public_transport": village.public_transport,
                "number_of_children": village.number_of_children,
                "district": village.district,
                "pincode": village.pincode,
                "state": village.state,
                "sarpanch": village.sarpanch,
                "MRO": village.MRO
            }
            chart_path = f"outputs/charts/{village.id}_analytics.png"
            analytics = get_analytics(village_data, chart_path)
            self.stdout.write("Analytics Results:")
            for key, value in analytics.items():
                self.stdout.write(f"  {key}: {value}")
            self.stdout.write(f"Analytics chart generated at: {chart_path}")

            # Generate AI recommendations
            recommendations = get_ai_recommendations(village_data)
            self.stdout.write("AI Recommendations:")
            for key, value in recommendations.items():
                self.stdout.write(f"  {key}: {value}")

            # Generate PDF report
            report_path = f"outputs/reports/{village.id}_report.pdf"
            doc = SimpleDocTemplate(report_path, pagesize=landscape(letter), leftMargin=0.75*inch, rightMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch)
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(name='Title', fontName='Helvetica-Bold', fontSize=18, textColor=black, alignment=1, spaceAfter=12)
            heading_style = ParagraphStyle(name='Heading', fontName='Helvetica-Bold', fontSize=14, textColor=blue, spaceAfter=10)
            data_style = ParagraphStyle(name='Data', fontName='Helvetica', fontSize=11, textColor=green, leading=14)
            subheading_style = ParagraphStyle(name='SubHeading', fontName='Helvetica', fontSize=10, textColor=black, spaceAfter=6)

            story = []

            # Page 1: Header, Overview, Infrastructure, Additional Details
            # Header with Village Details
            header_data = [
                [Paragraph(f"Development Plan for {village.name}", title_style)],
                [Paragraph(f"District: {village.district} | State: {village.state} | Pincode: {village.pincode}", subheading_style)],
                [Paragraph(f"Sarpanch: {village.sarpanch} | MRO: {village.MRO}", subheading_style)]
            ]
            header_table = Table(header_data, colWidths=[7.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor('#E0F7FA')),
                ('TEXTCOLOR', (0, 0), (-1, -1), black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, blue)
            ]))
            story.append(header_table)
            story.append(Spacer(1, 0.2*inch))

            # Overview Section
            overview_data = [
                [Paragraph("Overview", heading_style)],
                [Paragraph(f"Previous Census Population: {village.previous_census_population}", data_style)],
                [Paragraph(f"Current Census Population: {village.current_census_population}", data_style)],
                #[Paragraph(f"Number of Children: {village.number_of_children}", data_style)],
                [Paragraph(f"Village Area: {village.village_area} sq km", data_style)],
                [Paragraph(f"Literacy Rate: {village.literacy_rate * 100}%", data_style)],
                [Paragraph(f"Population Growth Rate: {analytics['population_growth_rate']}%", data_style)]
            ]
            overview_table = Table(overview_data, colWidths=[7.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F5F5F5')),
                ('TEXTCOLOR', (0, 0), (-1, -1), green),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('LEADING', (0, 0), (-1, -1), 14),
                ('GRID', (0, 0), (-1, -1), 0.5, blue),
                ('BOX', (0, 0), (-1, -1), 1, blue)
            ]))
            story.append(overview_table)
            story.append(Spacer(1, 0.2*inch))

            # Current Infrastructure Assessment
            infra_data = [
                [Paragraph("Current Infrastructure Assessment", heading_style)],
                [Paragraph(f"Healthcare Access: {village.healthcare_access}", data_style)],  # Added
                [Paragraph(f"Number of Hospitals: {village.number_of_hospitals}", data_style)],  # Added
                [Paragraph(f"Post Office Availability: {self.format_boolean(village.post_office_availability)}", data_style)],  # Added
                [Paragraph(f"Number of Petrol Bunks: {village.petrol_bunks}", data_style)],  # Added
                [Paragraph(f"Roads: {village.infrastructure['roads']}", data_style)],
                [Paragraph(f"Lakes: {village.infrastructure['lakes']}", data_style)],
                [Paragraph(f"Temples: {village.infrastructure['temples']}", data_style)],
                [Paragraph(f"Number of Schools: {village.number_of_schools}", data_style)],
                [Paragraph(f"Electricity Supply (hours/day): {village.electricity_supply_hours}", data_style)],
                [Paragraph(f"Renewable Energy Source: {self.format_boolean(village.renewable_energy_source)}", data_style)],
                [Paragraph(f"Water Supply to Every Home: {self.format_boolean(village.water_supply_to_every_home)}", data_style)],
                [Paragraph(f"Number of Parks: {village.parks}", data_style)],
                [Paragraph(f"Number of Playgrounds: {village.playgrounds}", data_style)],
                [Paragraph(f"Sanitation Everyday: {self.format_boolean(village.sanitation_everyday)}", data_style)],
                [Paragraph(f"Waste Management Everyday: {self.format_boolean(village.waste_management_everyday)}", data_style)],
                [Paragraph(f"Network Connectivity: {self.format_boolean(village.network_connectivity)}", data_style)],
                [Paragraph(f"Market Availability: {self.format_boolean(village.market_availability)}", data_style)],
                [Paragraph(f"Banks/ATM Facility: {self.format_boolean(village.banks_atm_facility)}", data_style)],
                [Paragraph(f"Green Cover (%): {village.green_cover}", data_style)],
                [Paragraph(f"Street Lighting: {self.format_boolean(village.street_lighting)}", data_style)],
                [Paragraph(f"Public Transport: {self.format_boolean(village.public_transport)}", data_style)]
            ]
            infra_table = Table(infra_data, colWidths=[7.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F5F5F5')),
                ('TEXTCOLOR', (0, 0), (-1, -1), green),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('LEADING', (0, 0), (-1, -1), 14),
                ('GRID', (0, 0), (-1, -1), 0.5, blue),
                ('BOX', (0, 0), (-1, -1), 1, blue)
            ]))
            story.append(infra_table)
            story.append(Spacer(1, 0.2*inch))

            # Additional Details
            details_data = [
                [Paragraph("Additional Details", heading_style)],
                [Paragraph(f"District: {village.district}", data_style)],
                [Paragraph(f"Pincode: {village.pincode}", data_style)],
                [Paragraph(f"State: {village.state}", data_style)],
                [Paragraph(f"Sarpanch: {village.sarpanch}", data_style)],
                [Paragraph(f"MRO: {village.MRO}", data_style)]
            ]
            details_table = Table(details_data, colWidths=[7.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F5F5F5')),
                ('TEXTCOLOR', (0, 0), (-1, -1), green),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('LEADING', (0, 0), (-1, -1), 14),
                ('GRID', (0, 0), (-1, -1), 0.5, blue),
                ('BOX', (0, 0), (-1, -1), 1, blue)
            ]))
            story.append(details_table)

            # Page 2: Analysis and Recommendations
            story.append(PageBreak())

            # Repeat Header on Page 2
            story.append(header_table)
            story.append(Spacer(1, 0.2*inch))

            # Analysis
            analysis_data = [
                [Paragraph("Analysis", heading_style)],
                [Paragraph(f"Population Growth Rate: {analytics['population_growth_rate']}%", data_style)],
                [Paragraph(f"Population Density: {analytics['population_density']}", data_style)],
                [Paragraph(f"Area Suitability: {analytics['area_suitability']}", data_style)],
                [Paragraph(f"Literacy Score: {analytics['literacy_score']}", data_style)],
                [Paragraph(f"Schools Needed: {analytics['schools_needed']}", data_style)],
                [Paragraph(f"Hospitals Needed: {village.number_of_hospitals} hospital(s) (current: {village.number_of_hospitals})", data_style)],  # New field
                [Paragraph(f"Infrastructure Score: {analytics['infrastructure_score']}", data_style)],
                [Paragraph(f"Sustainability Index: {self.format_boolean(analytics['sustainability_index'])}", data_style)],
                [Paragraph(f"Community Score: {analytics['community_score']}", data_style)],
                [Paragraph(f"Healthcare Score: {analytics['healthcare_score']}", data_style)],
                [Paragraph(f"Healthcare Access Rating: {village.healthcare_access}", data_style)],  # New field
                [Paragraph(f"Post Office Availability: {self.format_boolean(village.post_office_availability)}", data_style)],  # New field
                [Paragraph(f"Petrol Bunks Accessibility: {village.petrol_bunks} bunk(s)", data_style)]  # New field
            ]
            analysis_table = Table(analysis_data, colWidths=[7.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F5F5F5')),
                ('TEXTCOLOR', (0, 0), (-1, -1), green),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('LEADING', (0, 0), (-1, -1), 14),
                ('GRID', (0, 0), (-1, -1), 0.5, blue),
                ('BOX', (0, 0), (-1, -1), 1, blue)
            ]))
            story.append(analysis_table)
            story.append(Spacer(1, 0.2*inch))

            # Recommendations
            rec_data = [
                [Paragraph("Recommendations", heading_style)],
                [Paragraph(f"Infrastructure: {recommendations['infrastructure']}", data_style)],
                [Paragraph(f"Education: {recommendations['education']}", data_style)],
                [Paragraph(f"Healthcare: {recommendations['healthcare']}", data_style)],
                [Paragraph(f"Sustainability: {recommendations['sustainability']}", data_style)],
                [Paragraph(f"Community: {recommendations['community']}", data_style)],
                [Paragraph(f"Economic Growth: {recommendations['economic_growth']}", data_style)],
                [Paragraph(f"Transportation: {recommendations['transportation']}", data_style)],
                [Paragraph(f"Connectivity: {recommendations['connectivity']}", data_style)],
                [Paragraph(f"Sanitation: {recommendations['sanitation']}", data_style)],
                [Paragraph(f"Healthcare Facilities: Improve healthcare facilities by building hospitals if none exist.", data_style)],  # New recommendation
                [Paragraph(f"Post Office Services: Establish a post office for better communication and services.", data_style)],  # New recommendation
                [Paragraph(f"Petrol Bunk Access: Ensure petrol bunks are available for better transportation support.", data_style)]  # New recommendation
            ]
            rec_table = Table(rec_data, colWidths=[7.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F5F5F5')),
                ('TEXTCOLOR', (0, 0), (-1, -1), green),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('LEADING', (0, 0), (-1, -1), 14),
                ('GRID', (0, 0), (-1, -1), 0.5, blue),
                ('BOX', (0, 0), (-1, -1), 1, blue)
            ]))
            story.append(rec_table)

            # Build the PDF
            doc.build(story)
            self.stdout.write(f"PDF report generated at: {report_path}")

        except Exception as e:
            self.stdout.write(f"Error: {str(e)}")'''





'''from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from village_app.models import Village
from village_app.utils.gis import generate_map_image as gis_generate_map_image
from village_app.utils.ai_recommendations import get_ai_recommendations
from village_app.utils.analytics import get_analytics
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import blue, green, black, HexColor, white
from reportlab.lib.units import inch
import os

class Command(BaseCommand):
    help = 'Run the village development CLI tool'

    def format_boolean(self, value):
        """Convert boolean values to 'Yes' or 'No' for display."""
        return "Yes" if value else "No"

    def handle(self, *args, **options):
        self.stdout.write("Welcome to the Village Development CLI Tool!")
        
        try:
            # Collect village data
            name = input("Enter village name: ")
            previous_census_population = int(input("Enter previous census population: "))
            current_census_population = int(input("Enter current census population: "))
            village_area = float(input("Enter village area (sq km): "))
            literacy_rate = float(input("Enter literacy rate (as a percentage, e.g., 75 for 75%): ")) / 100
            healthcare_access = input("Enter healthcare access (Good/Average/Poor): ")
            roads = input("Enter road type (e.g., paved/unpaved): ")
            lakes = int(input("Enter number of lakes: "))
            temples = int(input("Enter number of temples: "))
            latitude = float(input("Enter latitude: "))
            longitude = float(input("Enter longitude: "))
            number_of_schools = int(input("Enter number of schools: "))
            number_of_hospitals = int(input("Enter number of hospitals: "))
            post_office_availability = input("Is post office available? (y/n): ").lower() == 'y'
            petrol_bunks = int(input("Enter number of petrol bunks: "))
            electricity_supply_hours = int(input("Enter electricity supply hours per day: "))
            renewable_energy_source = input("Does the village use renewable energy source? (y/n): ").lower() == 'y'
            water_supply_to_every_home = input("Is water supplied to every home? (y/n): ").lower() == 'y'
            parks = int(input("Enter number of parks: "))
            playgrounds = int(input("Enter number of playgrounds: "))
            sanitation_everyday = input("Is sanitation provided everyday? (y/n): ").lower() == 'y'
            waste_management_everyday = input("Is waste management provided everyday? (y/n): ").lower() == 'y'
            network_connectivity = input("Is there network connectivity? (y/n): ").lower() == 'y'
            market_availability = input("Is market available? (y/n): ").lower() == 'y'
            banks_atm_facility = input("Are banks/ATM facilities available? (y/n): ").lower() == 'y'
            green_cover = float(input("Enter green cover percentage (0-100): "))
            street_lighting = input("Is street lighting available? (y/n): ").lower() == 'y'
            public_transport = input("Is public transport available? (y/n): ").lower() == 'y'
            number_of_children = int(input("Enter number of children: "))
            district = input("Enter district: ")
            pincode = input("Enter pincode: ")
            state = input("Enter state: ")
            sarpanch = input("Enter sarpanch name: ")
            MRO = input("Enter MRO name: ")

            # Save village data
            village = Village(
                name=name,
                previous_census_population=previous_census_population,
                current_census_population=current_census_population,
                village_area=village_area,
                population=current_census_population,
                literacy_rate=literacy_rate,
                healthcare_access=healthcare_access,
                infrastructure={"roads": roads, "lakes": lakes, "temples": temples},
                location=Point(longitude, latitude),
                number_of_schools=number_of_schools,
                number_of_hospitals=number_of_hospitals,
                post_office_availability=post_office_availability,
                petrol_bunks=petrol_bunks,
                electricity_supply_hours=electricity_supply_hours,
                renewable_energy_source=renewable_energy_source,
                water_supply_to_every_home=water_supply_to_every_home,
                parks=parks,
                playgrounds=playgrounds,
                sanitation_everyday=sanitation_everyday,
                waste_management_everyday=waste_management_everyday,
                network_connectivity=network_connectivity,
                market_availability=market_availability,
                banks_atm_facility=banks_atm_facility,
                green_cover=green_cover,
                street_lighting=street_lighting,
                public_transport=public_transport,
                number_of_children=number_of_children,
                district=district,
                pincode=pincode,
                state=state,
                sarpanch=sarpanch,
                MRO=MRO
            )
            village.save()

            self.stdout.write(f"Village '{village.name}' saved with ID: {village.id}")

            # Generate outputs
            os.makedirs("outputs/maps", exist_ok=True)
            os.makedirs("outputs/charts", exist_ok=True)
            os.makedirs("outputs/models", exist_ok=True)
            os.makedirs("outputs/reports", exist_ok=True)

            # Generate map (using GeoPandas/PostGIS)
            map_path = f"outputs/maps/{village.id}_map.png"
            gis_generate_map_image(village, map_path)
            self.stdout.write(f"Map generated at: {map_path}")

            # Generate analytics
            village_data = {
                "name": village.name,
                "previous_census_population": village.previous_census_population,
                "current_census_population": village.current_census_population,
                "village_area": village.village_area,
                "population": village.population,
                "literacy_rate": village.literacy_rate,
                "healthcare_access": village.healthcare_access,
                "infrastructure": village.infrastructure,
                "number_of_schools": village.number_of_schools,
                "number_of_hospitals": village.number_of_hospitals,
                "post_office_availability": village.post_office_availability,
                "petrol_bunks": village.petrol_bunks,
                "electricity_supply_hours": village.electricity_supply_hours,
                "renewable_energy_source": village.renewable_energy_source,
                "water_supply_to_every_home": village.water_supply_to_every_home,
                "parks": village.parks,
                "playgrounds": village.playgrounds,
                "sanitation_everyday": village.sanitation_everyday,
                "waste_management_everyday": village.waste_management_everyday,
                "network_connectivity": village.network_connectivity,
                "market_availability": village.market_availability,
                "banks_atm_facility": village.banks_atm_facility,
                "green_cover": village.green_cover,
                "street_lighting": village.street_lighting,
                "public_transport": village.public_transport,
                "number_of_children": village.number_of_children,
                "district": village.district,
                "pincode": village.pincode,
                "state": village.state,
                "sarpanch": village.sarpanch,
                "MRO": village.MRO
            }
            chart_path = f"outputs/charts/{village.id}_analytics.png"
            analytics = get_analytics(village_data, chart_path)
            self.stdout.write("Analytics Results:")
            for key, value in analytics.items():
                self.stdout.write(f"  {key}: {value}")
            self.stdout.write(f"Analytics chart generated at: {chart_path}")

            # Generate AI recommendations
            recommendations = get_ai_recommendations(village_data)
            self.stdout.write("AI Recommendations:")
            for key, value in recommendations.items():
                self.stdout.write(f"  {key}: {value}")

            # Generate PDF report
            report_path = f"outputs/reports/{village.id}_report.pdf"
            doc = SimpleDocTemplate(report_path, pagesize=letter, leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(name='Title', fontName='Helvetica-Bold', fontSize=16, textColor=black, alignment=1, spaceAfter=12)
            section_style = ParagraphStyle(name='Section', fontName='Helvetica-Bold', fontSize=12, textColor=white, alignment=1, spaceAfter=6)
            label_style = ParagraphStyle(name='Label', fontName='Helvetica', fontSize=10, textColor=black, alignment=0, leading=14)
            value_style = ParagraphStyle(name='Value', fontName='Helvetica', fontSize=10, textColor=black, alignment=0, leading=14)
            declaration_style = ParagraphStyle(name='Declaration', fontName='Helvetica', fontSize=10, textColor=black, alignment=0, spaceBefore=12)

            story = []

            # Page 1: Village Details, Overview, Infrastructure
            # Title
            story.append(Paragraph("VILLAGE DEVELOPMENT REPORT", title_style))
            story.append(Spacer(1, 0.2*inch))

            # Village Details Section
            village_details_data = [
                [Paragraph("VILLAGE DETAILS", section_style)]
            ]
            details = [
                ("Village Name", village.name),
                ("District", village.district),
                ("State", village.state),
                ("Pincode", village.pincode),
                ("Sarpanch", village.sarpanch),
                ("MRO", village.MRO)
            ]
            for label, value in details:
                village_details_data.append([
                    Paragraph(f"{label}:", label_style),
                    Paragraph(str(value), value_style)
                ])
            village_details_table = Table(village_details_data, colWidths=[2*inch, 3.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), blue),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, black),
                ('BOX', (0, 0), (-1, -1), 1, black)
            ]))
            story.append(village_details_table)
            story.append(Spacer(1, 0.2*inch))

            # Overview Section
            overview_data = [
                [Paragraph("OVERVIEW", section_style)]
            ]
            overview_items = [
                ("Previous Census Population", village.previous_census_population),
                ("Current Census Population", village.current_census_population),
                ("Village Area", f"{village.village_area} sq km"),
                ("Literacy Rate", f"{village.literacy_rate * 100}%"),
                ("Population Growth Rate", f"{analytics['population_growth_rate']}%")
            ]
            for label, value in overview_items:
                overview_data.append([
                    Paragraph(f"{label}:", label_style),
                    Paragraph(str(value), value_style)
                ])
            overview_table = Table(overview_data, colWidths=[2*inch, 3.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), blue),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, black),
                ('BOX', (0, 0), (-1, -1), 1, black)
            ]))
            story.append(overview_table)
            story.append(Spacer(1, 0.2*inch))

            # Current Infrastructure Assessment Section
            infra_data = [
                [Paragraph("CURRENT INFRASTRUCTURE ASSESSMENT", section_style)]
            ]
            infra_items = [
                ("Healthcare Access", village.healthcare_access),
                ("Number of Hospitals", village.number_of_hospitals),
                ("Post Office Availability", self.format_boolean(village.post_office_availability)),
                ("Number of Petrol Bunks", village.petrol_bunks),
                ("Roads", village.infrastructure['roads']),
                ("Lakes", village.infrastructure['lakes']),
                ("Temples", village.infrastructure['temples']),
                ("Number of Schools", village.number_of_schools),
                ("Electricity Supply (hours/day)", village.electricity_supply_hours),
                ("Renewable Energy Source", self.format_boolean(village.renewable_energy_source)),
                ("Water Supply to Every Home", self.format_boolean(village.water_supply_to_every_home)),
                ("Number of Parks", village.parks),
                ("Number of Playgrounds", village.playgrounds),
                ("Sanitation Everyday", self.format_boolean(village.sanitation_everyday)),
                ("Waste Management Everyday", self.format_boolean(village.waste_management_everyday)),
                ("Network Connectivity", self.format_boolean(village.network_connectivity)),
                ("Market Availability", self.format_boolean(village.market_availability)),
                ("Banks/ATM Facility", self.format_boolean(village.banks_atm_facility)),
                ("Green Cover (%)", village.green_cover),
                ("Street Lighting", self.format_boolean(village.street_lighting)),
                ("Public Transport", self.format_boolean(village.public_transport))
            ]
            for label, value in infra_items:
                infra_data.append([
                    Paragraph(f"{label}:", label_style),
                    Paragraph(str(value), value_style)
                ])
            infra_table = Table(infra_data, colWidths=[2*inch, 3.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), blue),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, black),
                ('BOX', (0, 0), (-1, -1), 1, black)
            ]))
            story.append(infra_table)

            # Declaration Section
            story.append(Paragraph("Declaration: This report is generated based on the data provided and is true to the best of our knowledge.", declaration_style))
            story.append(Paragraph("Date: ____________________", declaration_style))
            story.append(Paragraph("Signature: ____________________", declaration_style))

            # Page 2: Analysis and Recommendations
            story.append(PageBreak())

            # Title
            story.append(Paragraph("VILLAGE DEVELOPMENT REPORT", title_style))
            story.append(Spacer(1, 0.2*inch))

            # Analysis Section
            analysis_data = [
                [Paragraph("ANALYSIS", section_style)]
            ]
            analysis_items = [
                ("Population Growth Rate", f"{analytics['population_growth_rate']}%"),
                ("Population Density", analytics['population_density']),
                ("Area Suitability", analytics['area_suitability']),
                ("Literacy Score", analytics['literacy_score']),
                ("Schools Needed", analytics['schools_needed']),
                ("Hospitals Needed", f"{village.number_of_hospitals} hospital(s) (current: {village.number_of_hospitals})"),
                ("Infrastructure Score", analytics['infrastructure_score']),
                ("Sustainability Index", self.format_boolean(analytics['sustainability_index'])),
                ("Community Score", analytics['community_score']),
                ("Healthcare Score", analytics['healthcare_score']),
                ("Healthcare Access Rating", village.healthcare_access),
                ("Post Office Availability", self.format_boolean(village.post_office_availability)),
                ("Petrol Bunks Accessibility", f"{village.petrol_bunks} bunk(s)")
            ]
            for label, value in analysis_items:
                analysis_data.append([
                    Paragraph(f"{label}:", label_style),
                    Paragraph(str(value), value_style)
                ])
            analysis_table = Table(analysis_data, colWidths=[2*inch, 3.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), blue),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, black),
                ('BOX', (0, 0), (-1, -1), 1, black)
            ]))
            story.append(analysis_table)
            story.append(Spacer(1, 0.2*inch))

            # Recommendations Section
            rec_data = [
                [Paragraph("RECOMMENDATIONS", section_style)]
            ]
            rec_items = [
                ("Infrastructure", recommendations['infrastructure']),
                ("Education", recommendations['education']),
                ("Healthcare", recommendations['healthcare']),
                ("Sustainability", recommendations['sustainability']),
                ("Community", recommendations['community']),
                ("Economic Growth", recommendations['economic_growth']),
                ("Transportation", recommendations['transportation']),
                ("Connectivity", recommendations['connectivity']),
                ("Sanitation", recommendations['sanitation']),
                ("Healthcare Facilities", recommendations['healthcare_facilities']),
                ("Post Office Services", recommendations['post_office_services']),
                ("Petrol Bunk Access", recommendations['petrol_bunk_access'])
            ]
            for label, value in rec_items:
                rec_data.append([
                    Paragraph(f"{label}:", label_style),
                    Paragraph(str(value), value_style)
                ])
            rec_table = Table(rec_data, colWidths=[2*inch, 3.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), blue),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, black),
                ('BOX', (0, 0), (-1, -1), 1, black)
            ]))
            story.append(rec_table)

            # Declaration Section
            story.append(Paragraph("Declaration: This report is generated based on the data provided and is true to the best of our knowledge.", declaration_style))
            story.append(Paragraph("Date: ____________________", declaration_style))
            story.append(Paragraph("Signature: ____________________", declaration_style))

            # Build the PDF
            doc.build(story)
            self.stdout.write(f"PDF report generated at: {report_path}")

        except Exception as e:
            self.stdout.write(f"Error: {str(e)}")'''









'''from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from village_app.models import Village
from village_app.utils.gis import generate_map_image as gis_generate_map_image
from village_app.utils.ai_recommendations import get_ai_recommendations
from village_app.utils.analytics import get_analytics
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import blue, green, black, HexColor
from reportlab.lib.units import inch
import os

class Command(BaseCommand):
    help = 'Run the village development CLI tool'

    def format_boolean(self, value):
        """Convert boolean values to 'Yes' or 'No' for display."""
        return "Yes" if value else "No"

    def handle(self, *args, **options):
        self.stdout.write("Welcome to the Village Development CLI Tool!")
        
        try:
            # Collect village data
            name = input("Enter village name: ")
            previous_census_population = int(input("Enter previous census population: "))
            current_census_population = int(input("Enter current census population: "))
            village_area = float(input("Enter village area (sq km): "))
            literacy_rate = float(input("Enter literacy rate (as a percentage, e.g., 75 for 75%): ")) / 100
            healthcare_access = input("Enter healthcare access (Good/Average/Poor): ")
            roads = input("Enter road type (e.g., paved/unpaved): ")
            lakes = int(input("Enter number of lakes: "))
            temples = int(input("Enter number of temples: "))
            latitude = float(input("Enter latitude: "))
            longitude = float(input("Enter longitude: "))
            number_of_schools = int(input("Enter number of schools: "))
            number_of_hospitals = int(input("Enter number of hospitals: "))  # New input
            post_office_availability = input("Is post office available? (y/n): ").lower() == 'y'  # New input
            petrol_bunks = int(input("Enter number of petrol bunks: "))  # New input
            electricity_supply_hours = int(input("Enter electricity supply hours per day: "))
            renewable_energy_source = input("Does the village use renewable energy source? (y/n): ").lower() == 'y'
            water_supply_to_every_home = input("Is water supplied to every home? (y/n): ").lower() == 'y'
            parks = int(input("Enter number of parks: "))
            playgrounds = int(input("Enter number of playgrounds: "))
            sanitation_everyday = input("Is sanitation provided everyday? (y/n): ").lower() == 'y'
            waste_management_everyday = input("Is waste management provided everyday? (y/n): ").lower() == 'y'
            network_connectivity = input("Is there network connectivity? (y/n): ").lower() == 'y'
            market_availability = input("Is market available? (y/n): ").lower() == 'y'
            banks_atm_facility = input("Are banks/ATM facilities available? (y/n): ").lower() == 'y'
            green_cover = float(input("Enter green cover percentage (0-100): "))
            street_lighting = input("Is street lighting available? (y/n): ").lower() == 'y'
            public_transport = input("Is public transport available? (y/n): ").lower() == 'y'
            number_of_children = int(input("Enter number of children: "))
            district = input("Enter district: ")
            pincode = input("Enter pincode: ")
            state = input("Enter state: ")
            sarpanch = input("Enter sarpanch name: ")
            MRO = input("Enter MRO name: ")

            # Save village data
            village = Village(
                name=name,
                previous_census_population=previous_census_population,
                current_census_population=current_census_population,
                village_area=village_area,
                population=current_census_population,
                literacy_rate=literacy_rate,
                healthcare_access=healthcare_access,
                infrastructure={"roads": roads, "lakes": lakes, "temples": temples},
                location=Point(longitude, latitude),
                number_of_schools=number_of_schools,
                number_of_hospitals=number_of_hospitals,  # New field
                post_office_availability=post_office_availability,  # New field
                petrol_bunks=petrol_bunks,  # New field
                electricity_supply_hours=electricity_supply_hours,
                renewable_energy_source=renewable_energy_source,
                water_supply_to_every_home=water_supply_to_every_home,
                parks=parks,
                playgrounds=playgrounds,
                sanitation_everyday=sanitation_everyday,
                waste_management_everyday=waste_management_everyday,
                network_connectivity=network_connectivity,
                market_availability=market_availability,
                banks_atm_facility=banks_atm_facility,
                green_cover=green_cover,
                street_lighting=street_lighting,
                public_transport=public_transport,
                number_of_children=number_of_children,
                district=district,
                pincode=pincode,
                state=state,
                sarpanch=sarpanch,
                MRO=MRO
            )
            village.save()

            self.stdout.write(f"Village '{village.name}' saved with ID: {village.id}")

            # Generate outputs
            os.makedirs("outputs/maps", exist_ok=True)
            os.makedirs("outputs/charts", exist_ok=True)
            os.makedirs("outputs/models", exist_ok=True)
            os.makedirs("outputs/reports", exist_ok=True)

            # Generate map (using GeoPandas/PostGIS)
            map_path = f"outputs/maps/{village.id}_map.png"
            gis_generate_map_image(village, map_path)
            self.stdout.write(f"Map generated at: {map_path}")

            # Generate analytics
            village_data = {
                "name": village.name,
                "previous_census_population": village.previous_census_population,
                "current_census_population": village.current_census_population,
                "village_area": village.village_area,
                "population": village.population,
                "literacy_rate": village.literacy_rate,
                "healthcare_access": village.healthcare_access,
                "infrastructure": village.infrastructure,
                "number_of_schools": village.number_of_schools,
                "number_of_hospitals": village.number_of_hospitals,  # New field
                "post_office_availability": village.post_office_availability,  # New field
                "petrol_bunks": village.petrol_bunks,  # New field
                "electricity_supply_hours": village.electricity_supply_hours,
                "renewable_energy_source": village.renewable_energy_source,
                "water_supply_to_every_home": village.water_supply_to_every_home,
                "parks": village.parks,
                "playgrounds": village.playgrounds,
                "sanitation_everyday": village.sanitation_everyday,
                "waste_management_everyday": village.waste_management_everyday,
                "network_connectivity": village.network_connectivity,
                "market_availability": village.market_availability,
                "banks_atm_facility": village.banks_atm_facility,
                "green_cover": village.green_cover,
                "street_lighting": village.street_lighting,
                "public_transport": village.public_transport,
                "number_of_children": village.number_of_children,
                "district": village.district,
                "pincode": village.pincode,
                "state": village.state,
                "sarpanch": village.sarpanch,
                "MRO": village.MRO
            }
            chart_path = f"outputs/charts/{village.id}_analytics.png"
            analytics = get_analytics(village_data, chart_path)
            self.stdout.write("Analytics Results:")
            for key, value in analytics.items():
                self.stdout.write(f"  {key}: {value}")
            self.stdout.write(f"Analytics chart generated at: {chart_path}")

            # Generate AI recommendations
            recommendations = get_ai_recommendations(village_data)
            self.stdout.write("AI Recommendations:")
            for key, value in recommendations.items():
                self.stdout.write(f"  {key}: {value}")

            # Generate PDF report
            report_path = f"outputs/reports/{village.id}_report.pdf"
            doc = SimpleDocTemplate(report_path, pagesize=landscape(letter), leftMargin=0.75*inch, rightMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch)
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(name='Title', fontName='Helvetica-Bold', fontSize=18, textColor=black, alignment=1, spaceAfter=12)
            heading_style = ParagraphStyle(name='Heading', fontName='Helvetica-Bold', fontSize=14, textColor=blue, spaceAfter=10)
            data_style = ParagraphStyle(name='Data', fontName='Helvetica', fontSize=11, textColor=green, leading=14)
            subheading_style = ParagraphStyle(name='SubHeading', fontName='Helvetica', fontSize=10, textColor=black, spaceAfter=6)

            story = []

            # Page 1: Header, Overview, Infrastructure, Additional Details
            # Header with Village Details
            header_data = [
                [Paragraph(f"Development Plan for {village.name}", title_style)],
                [Paragraph(f"District: {village.district} | State: {village.state} | Pincode: {village.pincode}", subheading_style)],
                [Paragraph(f"Sarpanch: {village.sarpanch} | MRO: {village.MRO}", subheading_style)]
            ]
            header_table = Table(header_data, colWidths=[7.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor('#E0F7FA')),
                ('TEXTCOLOR', (0, 0), (-1, -1), black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, blue)
            ]))
            story.append(header_table)
            story.append(Spacer(1, 0.2*inch))

            # Overview Section
            overview_data = [
                [Paragraph("Overview", heading_style)],
                [Paragraph(f"Previous Census Population: {village.previous_census_population}", data_style)],
                [Paragraph(f"Current Census Population: {village.current_census_population}", data_style)],
                [Paragraph(f"Number of Children: {village.number_of_children}", data_style)],
                [Paragraph(f"Village Area: {village.village_area} sq km", data_style)],
                [Paragraph(f"Literacy Rate: {village.literacy_rate * 100}%", data_style)],
                [Paragraph(f"Population Growth Rate: {analytics['population_growth_rate']}%", data_style)]
            ]
            overview_table = Table(overview_data, colWidths=[7.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F5F5F5')),
                ('TEXTCOLOR', (0, 0), (-1, -1), green),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('LEADING', (0, 0), (-1, -1), 14),
                ('GRID', (0, 0), (-1, -1), 0.5, blue),
                ('BOX', (0, 0), (-1, -1), 1, blue)
            ]))
            story.append(overview_table)
            story.append(Spacer(1, 0.2*inch))

            # Current Infrastructure Assessment
            infra_data = [
                [Paragraph("Current Infrastructure Assessment", heading_style)],
                [Paragraph(f"Healthcare Access: {village.healthcare_access}", data_style)],  # Added
                [Paragraph(f"Number of Hospitals: {village.number_of_hospitals}", data_style)],  # Added
                [Paragraph(f"Post Office Availability: {self.format_boolean(village.post_office_availability)}", data_style)],  # Added
                [Paragraph(f"Number of Petrol Bunks: {village.petrol_bunks}", data_style)],  # Added
                [Paragraph(f"Roads: {village.infrastructure['roads']}", data_style)],
                [Paragraph(f"Lakes: {village.infrastructure['lakes']}", data_style)],
                [Paragraph(f"Temples: {village.infrastructure['temples']}", data_style)],
                [Paragraph(f"Number of Schools: {village.number_of_schools}", data_style)],
                [Paragraph(f"Electricity Supply (hours/day): {village.electricity_supply_hours}", data_style)],
                [Paragraph(f"Renewable Energy Source: {self.format_boolean(village.renewable_energy_source)}", data_style)],
                [Paragraph(f"Water Supply to Every Home: {self.format_boolean(village.water_supply_to_every_home)}", data_style)],
                [Paragraph(f"Number of Parks: {village.parks}", data_style)],
                [Paragraph(f"Number of Playgrounds: {village.playgrounds}", data_style)],
                [Paragraph(f"Sanitation Everyday: {self.format_boolean(village.sanitation_everyday)}", data_style)],
                [Paragraph(f"Waste Management Everyday: {self.format_boolean(village.waste_management_everyday)}", data_style)],
                [Paragraph(f"Network Connectivity: {self.format_boolean(village.network_connectivity)}", data_style)],
                [Paragraph(f"Market Availability: {self.format_boolean(village.market_availability)}", data_style)],
                [Paragraph(f"Banks/ATM Facility: {self.format_boolean(village.banks_atm_facility)}", data_style)],
                [Paragraph(f"Green Cover (%): {village.green_cover}", data_style)],
                [Paragraph(f"Street Lighting: {self.format_boolean(village.street_lighting)}", data_style)],
                [Paragraph(f"Public Transport: {self.format_boolean(village.public_transport)}", data_style)]
            ]
            infra_table = Table(infra_data, colWidths=[7.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F5F5F5')),
                ('TEXTCOLOR', (0, 0), (-1, -1), green),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('LEADING', (0, 0), (-1, -1), 14),
                ('GRID', (0, 0), (-1, -1), 0.5, blue),
                ('BOX', (0, 0), (-1, -1), 1, blue)
            ]))
            story.append(infra_table)
            story.append(Spacer(1, 0.2*inch))

            # Additional Details
            details_data = [
                [Paragraph("Additional Details", heading_style)],
                [Paragraph(f"District: {village.district}", data_style)],
                [Paragraph(f"Pincode: {village.pincode}", data_style)],
                [Paragraph(f"State: {village.state}", data_style)],
                [Paragraph(f"Sarpanch: {village.sarpanch}", data_style)],
                [Paragraph(f"MRO: {village.MRO}", data_style)]
            ]
            details_table = Table(details_data, colWidths=[7.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F5F5F5')),
                ('TEXTCOLOR', (0, 0), (-1, -1), green),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('LEADING', (0, 0), (-1, -1), 14),
                ('GRID', (0, 0), (-1, -1), 0.5, blue),
                ('BOX', (0, 0), (-1, -1), 1, blue)
            ]))
            story.append(details_table)

            # Page 2: Analysis and Recommendations
            story.append(PageBreak())

            # Repeat Header on Page 2
            story.append(header_table)
            story.append(Spacer(1, 0.2*inch))

            # Analysis
            analysis_data = [
                [Paragraph("Analysis", heading_style)],
                [Paragraph(f"Population Growth Rate: {analytics['population_growth_rate']}%", data_style)],
                [Paragraph(f"Population Density: {analytics['population_density']}", data_style)],
                [Paragraph(f"Area Suitability: {analytics['area_suitability']}", data_style)],
                [Paragraph(f"Literacy Score: {analytics['literacy_score']}", data_style)],
                [Paragraph(f"Schools Needed: {analytics['schools_needed']}", data_style)],
                [Paragraph(f"Hospitals Needed: {village.number_of_hospitals} hospital(s) (current: {village.number_of_hospitals})", data_style)],  # New field
                [Paragraph(f"Infrastructure Score: {analytics['infrastructure_score']}", data_style)],
                [Paragraph(f"Sustainability Index: {self.format_boolean(analytics['sustainability_index'])}", data_style)],
                [Paragraph(f"Community Score: {analytics['community_score']}", data_style)],
                [Paragraph(f"Healthcare Score: {analytics['healthcare_score']}", data_style)],
                [Paragraph(f"Healthcare Access Rating: {village.healthcare_access}", data_style)],  # New field
                [Paragraph(f"Post Office Availability: {self.format_boolean(village.post_office_availability)}", data_style)],  # New field
                [Paragraph(f"Petrol Bunks Accessibility: {village.petrol_bunks} bunk(s)", data_style)]  # New field
            ]
            analysis_table = Table(analysis_data, colWidths=[7.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F5F5F5')),
                ('TEXTCOLOR', (0, 0), (-1, -1), green),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('LEADING', (0, 0), (-1, -1), 14),
                ('GRID', (0, 0), (-1, -1), 0.5, blue),
                ('BOX', (0, 0), (-1, -1), 1, blue)
            ]))
            story.append(analysis_table)
            story.append(Spacer(1, 0.2*inch))

            # Recommendations
            rec_data = [
                [Paragraph("Recommendations", heading_style)],
                [Paragraph(f"Infrastructure: {recommendations['infrastructure']}", data_style)],
                [Paragraph(f"Education: {recommendations['education']}", data_style)],
                [Paragraph(f"Healthcare: {recommendations['healthcare']}", data_style)],
                [Paragraph(f"Sustainability: {recommendations['sustainability']}", data_style)],
                [Paragraph(f"Community: {recommendations['community']}", data_style)],
                [Paragraph(f"Economic Growth: {recommendations['economic_growth']}", data_style)],
                [Paragraph(f"Transportation: {recommendations['transportation']}", data_style)],
                [Paragraph(f"Connectivity: {recommendations['connectivity']}", data_style)],
                [Paragraph(f"Sanitation: {recommendations['sanitation']}", data_style)],
                [Paragraph(f"Healthcare Facilities: Improve healthcare facilities by building hospitals if none exist.", data_style)],  # New recommendation
                [Paragraph(f"Post Office Services: Establish a post office for better communication and services.", data_style)],  # New recommendation
                [Paragraph(f"Petrol Bunk Access: Ensure petrol bunks are available for better transportation support.", data_style)]  # New recommendation
            ]
            rec_table = Table(rec_data, colWidths=[7.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F5F5F5')),
                ('TEXTCOLOR', (0, 0), (-1, -1), green),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('LEADING', (0, 0), (-1, -1), 14),
                ('GRID', (0, 0), (-1, -1), 0.5, blue),
                ('BOX', (0, 0), (-1, -1), 1, blue)
            ]))
            story.append(rec_table)

            # Build the PDF
            doc.build(story)
            self.stdout.write(f"PDF report generated at: {report_path}")

        except Exception as e:
            self.stdout.write(f"Error: {str(e)}")'''




'''from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from village_app.models import Village
from village_app.utils.gis import generate_map_image as gis_generate_map_image
from village_app.utils.ai_recommendations import get_ai_recommendations
from village_app.utils.analytics import get_analytics
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import navy, green, black, white
from reportlab.lib.units import inch
import os

class Command(BaseCommand):
    help = 'Run the village development CLI tool'

    def format_boolean(self, value):
        """Convert boolean values to 'Yes' or 'No' for display."""
        return "Yes" if value else "No"

    def handle(self, *args, **options):
        self.stdout.write("Welcome to the Village Development CLI Tool!")
        
        try:
            # Collect village data
            name = input("Enter village name: ")
            previous_census_population = int(input("Enter previous census population: "))
            current_census_population = int(input("Enter current census population: "))
            village_area = float(input("Enter village area (sq km): "))
            literacy_rate = float(input("Enter literacy rate (as a percentage, e.g., 75 for 75%): ")) / 100
            healthcare_access = input("Enter healthcare access (Good/Average/Poor): ")
            roads = input("Enter road type (e.g., paved/unpaved): ")
            lakes = int(input("Enter number of lakes: "))
            temples = int(input("Enter number of temples: "))
            latitude = float(input("Enter latitude: "))
            longitude = float(input("Enter longitude: "))
            number_of_schools = int(input("Enter number of schools: "))
            number_of_hospitals = int(input("Enter number of hospitals: "))
            post_office_availability = input("Is post office available? (y/n): ").lower() == 'y'
            petrol_bunks = int(input("Enter number of petrol bunks: "))
            electricity_supply_hours = int(input("Enter electricity supply hours per day: "))
            renewable_energy_source = input("Does the village use renewable energy source? (y/n): ").lower() == 'y'
            water_supply_to_every_home = input("Is water supplied to every home? (y/n): ").lower() == 'y'
            parks = int(input("Enter number of parks: "))
            playgrounds = int(input("Enter number of playgrounds: "))
            sanitation_everyday = input("Is sanitation provided everyday? (y/n): ").lower() == 'y'
            waste_management_everyday = input("Is waste management provided everyday? (y/n): ").lower() == 'y'
            network_connectivity = input("Is there network connectivity? (y/n): ").lower() == 'y'
            market_availability = input("Is market available? (y/n): ").lower() == 'y'
            banks_atm_facility = input("Are banks/ATM facilities available? (y/n): ").lower() == 'y'
            green_cover = float(input("Enter green cover percentage (0-100): "))
            street_lighting = input("Is street lighting available? (y/n): ").lower() == 'y'
            public_transport = input("Is public transport available? (y/n): ").lower() == 'y'
            number_of_children = int(input("Enter number of children: "))
            district = input("Enter district: ")
            pincode = input("Enter pincode: ")
            state = input("Enter state: ")
            sarpanch = input("Enter sarpanch name: ")
            MRO = input("Enter MRO name: ")

            # Save village data
            village = Village(
                name=name,
                previous_census_population=previous_census_population,
                current_census_population=current_census_population,
                village_area=village_area,
                population=current_census_population,
                literacy_rate=literacy_rate,
                healthcare_access=healthcare_access,
                infrastructure={"roads": roads, "lakes": lakes, "temples": temples},
                location=Point(longitude, latitude),
                number_of_schools=number_of_schools,
                number_of_hospitals=number_of_hospitals,
                post_office_availability=post_office_availability,
                petrol_bunks=petrol_bunks,
                electricity_supply_hours=electricity_supply_hours,
                renewable_energy_source=renewable_energy_source,
                water_supply_to_every_home=water_supply_to_every_home,
                parks=parks,
                playgrounds=playgrounds,
                sanitation_everyday=sanitation_everyday,
                waste_management_everyday=waste_management_everyday,
                network_connectivity=network_connectivity,
                market_availability=market_availability,
                banks_atm_facility=banks_atm_facility,
                green_cover=green_cover,
                street_lighting=street_lighting,
                public_transport=public_transport,
                number_of_children=number_of_children,
                district=district,
                pincode=pincode,
                state=state,
                sarpanch=sarpanch,
                MRO=MRO
            )
            village.save()

            self.stdout.write(f"Village '{village.name}' saved with ID: {village.id}")

            # Generate outputs
            os.makedirs("outputs/maps", exist_ok=True)
            os.makedirs("outputs/charts", exist_ok=True)
            os.makedirs("outputs/models", exist_ok=True)
            os.makedirs("outputs/reports", exist_ok=True)

            # Generate map
            map_path = f"outputs/maps/{village.id}_map.png"
            gis_generate_map_image(village, map_path)
            self.stdout.write(f"Map generated at: {map_path}")

            # Generate analytics
            village_data = {
                "name": village.name,
                "previous_census_population": village.previous_census_population,
                "current_census_population": village.current_census_population,
                "village_area": village.village_area,
                "population": village.population,
                "literacy_rate": village.literacy_rate,
                "healthcare_access": village.healthcare_access,
                "infrastructure": village.infrastructure,
                "number_of_schools": village.number_of_schools,
                "number_of_hospitals": village.number_of_hospitals,
                "post_office_availability": village.post_office_availability,
                "petrol_bunks": village.petrol_bunks,
                "electricity_supply_hours": village.electricity_supply_hours,
                "renewable_energy_source": village.renewable_energy_source,
                "water_supply_to_every_home": village.water_supply_to_every_home,
                "parks": village.parks,
                "playgrounds": village.playgrounds,
                "sanitation_everyday": village.sanitation_everyday,
                "waste_management_everyday": village.waste_management_everyday,
                "network_connectivity": village.network_connectivity,
                "market_availability": village.market_availability,
                "banks_atm_facility": village.banks_atm_facility,
                "green_cover": village.green_cover,
                "street_lighting": village.street_lighting,
                "public_transport": village.public_transport,
                "number_of_children": village.number_of_children,
                "district": village.district,
                "pincode": village.pincode,
                "state": village.state,
                "sarpanch": village.sarpanch,
                "MRO": village.MRO
            }
            chart_path = f"outputs/charts/{village.id}_analytics.png"
            analytics = get_analytics(village_data, chart_path)
            self.stdout.write("Analytics Results:")
            for key, value in analytics.items():
                self.stdout.write(f"  {key}: {value}")
            self.stdout.write(f"Analytics chart generated at: {chart_path}")

            # Generate AI recommendations
            recommendations = get_ai_recommendations(village_data)
            self.stdout.write("AI Recommendations:")
            for key, value in recommendations.items():
                self.stdout.write(f"  {key}: {value}")

            # Generate PDF report
            report_path = f"outputs/reports/{village.id}_report.pdf"
            doc = SimpleDocTemplate(report_path, pagesize=landscape(letter), leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(name='Title', fontName='Helvetica-Bold', fontSize=16, textColor=navy, alignment=1, spaceAfter=10)
            heading_style = ParagraphStyle(name='Heading', fontName='Helvetica-Bold', fontSize=12, textColor=navy, spaceAfter=6)
            data_style = ParagraphStyle(name='Data', fontName='Helvetica', fontSize=10, textColor=green, leading=12)

            story = []

            # Page 1: Header and Main Sections
            # Header
            header_data = [
                [Paragraph(f"DEVELOPMENT PLAN FOR {village.name.upper()}", title_style)],
                [Paragraph(f"District: {village.district} | State: {village.state} | Pincode: {village.pincode}", data_style)],
                [Paragraph(f"Sarpanch: {village.sarpanch} | MRO: {village.MRO}", data_style)]
            ]
            header_table = Table(header_data, colWidths=[7*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), navy),
                ('TEXTCOLOR', (0, 0), (-1, -1), white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('GRID', (0, 0), (-1, -1), 1, navy)
            ]))
            story.append(header_table)
            story.append(Spacer(1, 0.1*inch))

            # Overview
            overview_data = [
                ["OVERVIEW"],
                ["Previous Census Population", str(village.previous_census_population)],
                ["Current Census Population", str(village.current_census_population)],
                ["Number of Children", str(village.number_of_children)],
                ["Village Area (sq km)", str(village.village_area)],
                ["Literacy Rate (%)", f"{village.literacy_rate * 100:.1f}"],
                ["Population Growth Rate (%)", f"{analytics['population_growth_rate']:.1f}"]
            ]
            overview_table = Table(overview_data, colWidths=[2*inch, 5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), navy),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, navy),
                ('BACKGROUND', (0, 1), (-1, -1), white),
                ('TEXTCOLOR', (0, 1), (-1, -1), green)
            ]))
            story.append(overview_table)
            story.append(Spacer(1, 0.1*inch))

            # Current Infrastructure Assessment
            infra_data = [
                ["CURRENT INFRASTRUCTURE ASSESSMENT"],
                ["Healthcare Access", village.healthcare_access],
                ["Number of Hospitals", str(village.number_of_hospitals)],
                ["Post Office Availability", self.format_boolean(village.post_office_availability)],
                ["Number of Petrol Bunks", str(village.petrol_bunks)],
                ["Roads", village.infrastructure["roads"]],
                ["Lakes", str(village.infrastructure["lakes"])],
                ["Temples", str(village.infrastructure["temples"])],
                ["Number of Schools", str(village.number_of_schools)],
                ["Electricity Supply (hours/day)", str(village.electricity_supply_hours)],
                ["Renewable Energy Source", self.format_boolean(village.renewable_energy_source)],
                ["Water Supply to Every Home", self.format_boolean(village.water_supply_to_every_home)],
                ["Number of Parks", str(village.parks)],
                ["Number of Playgrounds", str(village.playgrounds)],
                ["Sanitation Everyday", self.format_boolean(village.sanitation_everyday)],
                ["Waste Management Everyday", self.format_boolean(village.waste_management_everyday)],
                ["Network Connectivity", self.format_boolean(village.network_connectivity)],
                ["Market Availability", self.format_boolean(village.market_availability)],
                ["Banks/ATM Facility", self.format_boolean(village.banks_atm_facility)],
                ["Green Cover (%)", str(village.green_cover)],
                ["Street Lighting", self.format_boolean(village.street_lighting)],
                ["Public Transport", self.format_boolean(village.public_transport)]
            ]
            infra_table = Table(infra_data, colWidths=[2*inch, 5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), navy),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, navy),
                ('BACKGROUND', (0, 1), (-1, -1), white),
                ('TEXTCOLOR', (0, 1), (-1, -1), green)
            ]))
            story.append(infra_table)
            story.append(Spacer(1, 0.1*inch))

            # Additional Details
            details_data = [
                ["ADDITIONAL DETAILS"],
                ["District", village.district],
                ["Pincode", village.pincode],
                ["State", village.state],
                ["Sarpanch", village.sarpanch],
                ["MRO", village.MRO]
            ]
            details_table = Table(details_data, colWidths=[2*inch, 5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), navy),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, navy),
                ('BACKGROUND', (0, 1), (-1, -1), white),
                ('TEXTCOLOR', (0, 1), (-1, -1), green)
            ]))
            story.append(details_table)

            # Page 2: Analysis and Recommendations
            story.append(PageBreak())

            # Header on Page 2
            story.append(header_table)
            story.append(Spacer(1, 0.1*inch))

            # Analysis
            analysis_data = [
                ["ANALYSIS"],
                ["Population Growth Rate (%)", f"{analytics['population_growth_rate']:.1f}"],
                ["Population Density", f"{analytics['population_density']:.1f}"],
                ["Area Suitability", analytics['area_suitability']],
                ["Literacy Score", f"{analytics['literacy_score']:.1f}"],
                ["Schools Needed", str(analytics['schools_needed'])],
                ["Hospitals Needed", str(analytics['hospitals_needed'])],
                ["Infrastructure Score", f"{analytics['infrastructure_score']:.1f}"],
                ["Sustainability Index", self.format_boolean(analytics['sustainability_index'])],
                ["Community Score", str(analytics['community_score'])],
                ["Healthcare Score", str(analytics['healthcare_score'])]
            ]
            analysis_table = Table(analysis_data, colWidths=[2*inch, 5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), navy),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, navy),
                ('BACKGROUND', (0, 1), (-1, -1), white),
                ('TEXTCOLOR', (0, 1), (-1, -1), green)
            ]))
            story.append(analysis_table)
            story.append(Spacer(1, 0.1*inch))

            # Recommendations
            rec_data = [
                ["RECOMMENDATIONS"],
                ["Infrastructure", recommendations['infrastructure']],
                ["Education", recommendations['education']],
                ["Healthcare", recommendations['healthcare']],
                ["Sustainability", recommendations['sustainability']],
                ["Community", recommendations['community']],
                ["Economic Growth", recommendations['economic_growth']],
                ["Transportation", recommendations['transportation']],
                ["Connectivity", recommendations['connectivity']],
                ["Sanitation", recommendations['sanitation']]
            ]
            rec_table = Table(rec_data, colWidths=[2*inch, 5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), navy),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, navy),
                ('BACKGROUND', (0, 1), (-1, -1), white),
                ('TEXTCOLOR', (0, 1), (-1, -1), green)
            ]))
            story.append(rec_table)
            story.append(Spacer(1, 0.1*inch))

            # Declaration
            declaration_data = [
                ["DECLARATION"],
                ["I hereby declare that the information provided above is true to the best of my knowledge and belief.", ""],
                ["Place:", ""],
                ["Date: 30/04/2025", ""],
                ["Signature:", ""]
            ]
            declaration_table = Table(declaration_data, colWidths=[2*inch, 5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), navy),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, navy),
                ('BACKGROUND', (0, 1), (-1, -1), white),
                ('TEXTCOLOR', (0, 1), (-1, -1), black)
            ]))
            story.append(declaration_table)

            # Build the PDF
            doc.build(story)
            self.stdout.write(f"PDF report generated at: {report_path}")

        except Exception as e:
            self.stdout.write(f"Error: {str(e)}")'''



from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from village_app.models import Village
from village_app.utils.gis import generate_map_image as gis_generate_map_image
from village_app.utils.ai_recommendations import get_ai_recommendations
from village_app.utils.analytics import get_analytics
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import blue, green, black, HexColor, white
from reportlab.lib.units import inch
import os

class Command(BaseCommand):
    help = 'Run the village development CLI tool'

    def format_boolean(self, value):
        """Convert boolean values to 'Yes' or 'No' for display."""
        return "Yes" if value else "No"

    def handle(self, *args, **options):
        self.stdout.write("Welcome to the Village Development CLI Tool!")
        
        try:
            # Collect village data
            name = input("Enter village name: ")
            previous_census_population = int(input("Enter previous census population: "))
            current_census_population = int(input("Enter current census population: "))
            village_area = float(input("Enter village area (sq km): "))
            literacy_rate = float(input("Enter literacy rate (as a percentage, e.g., 75 for 75%): ")) / 100
            healthcare_access = input("Enter healthcare access (Good/Average/Poor): ")
            roads = input("Enter road type (e.g., paved/unpaved): ")
            lakes = int(input("Enter number of lakes: "))
            temples = int(input("Enter number of temples: "))
            latitude = float(input("Enter latitude: "))
            longitude = float(input("Enter longitude: "))
            number_of_schools = int(input("Enter number of schools: "))
            number_of_hospitals = int(input("Enter number of hospitals: "))
            post_office_availability = input("Is post office available? (y/n): ").lower() == 'y'
            petrol_bunks = int(input("Enter number of petrol bunks: "))
            electricity_supply_hours = int(input("Enter electricity supply hours per day: "))
            renewable_energy_source = input("Does the village use renewable energy source? (y/n): ").lower() == 'y'
            water_supply_to_every_home = input("Is water supplied to every home? (y/n): ").lower() == 'y'
            parks = int(input("Enter number of parks: "))
            playgrounds = int(input("Enter number of playgrounds: "))
            sanitation_everyday = input("Is sanitation provided everyday? (y/n): ").lower() == 'y'
            waste_management_everyday = input("Is waste management provided everyday? (y/n): ").lower() == 'y'
            network_connectivity = input("Is there network connectivity? (y/n): ").lower() == 'y'
            market_availability = input("Is market available? (y/n): ").lower() == 'y'
            banks_atm_facility = input("Are banks/ATM facilities available? (y/n): ").lower() == 'y'
            green_cover = float(input("Enter green cover percentage (0-100): "))
            street_lighting = input("Is street lighting available? (y/n): ").lower() == 'y'
            public_transport = input("Is public transport available? (y/n): ").lower() == 'y'
            number_of_children = int(input("Enter number of children: "))
            district = input("Enter district: ")
            pincode = input("Enter pincode: ")
            state = input("Enter state: ")
            sarpanch = input("Enter sarpanch name: ")
            MRO = input("Enter MRO name: ")

            # Save village data
            village = Village(
                name=name,
                previous_census_population=previous_census_population,
                current_census_population=current_census_population,
                village_area=village_area,
                population=current_census_population,
                literacy_rate=literacy_rate,
                healthcare_access=healthcare_access,
                infrastructure={"roads": roads, "lakes": lakes, "temples": temples},
                location=Point(longitude, latitude),
                number_of_schools=number_of_schools,
                number_of_hospitals=number_of_hospitals,
                post_office_availability=post_office_availability,
                petrol_bunks=petrol_bunks,
                electricity_supply_hours=electricity_supply_hours,
                renewable_energy_source=renewable_energy_source,
                water_supply_to_every_home=water_supply_to_every_home,
                parks=parks,
                playgrounds=playgrounds,
                sanitation_everyday=sanitation_everyday,
                waste_management_everyday=waste_management_everyday,
                network_connectivity=network_connectivity,
                market_availability=market_availability,
                banks_atm_facility=banks_atm_facility,
                green_cover=green_cover,
                street_lighting=street_lighting,
                public_transport=public_transport,
                number_of_children=number_of_children,
                district=district,
                pincode=pincode,
                state=state,
                sarpanch=sarpanch,
                MRO=MRO
            )
            village.save()

            self.stdout.write(f"Village '{village.name}' saved with ID: {village.id}")

            # Generate outputs
            os.makedirs("outputs/maps", exist_ok=True)
            os.makedirs("outputs/charts", exist_ok=True)
            os.makedirs("outputs/models", exist_ok=True)
            os.makedirs("outputs/reports", exist_ok=True)

            # Generate map (using GeoPandas/PostGIS)
            map_path = f"outputs/maps/{village.id}_map.png"
            gis_generate_map_image(village, map_path)
            self.stdout.write(f"Map generated at: {map_path}")

            # Generate analytics
            village_data = {
                "name": village.name,
                "previous_census_population": village.previous_census_population,
                "current_census_population": village.current_census_population,
                "village_area": village.village_area,
                "population": village.population,
                "literacy_rate": village.literacy_rate,
                "healthcare_access": village.healthcare_access,
                "infrastructure": village.infrastructure,
                "number_of_schools": village.number_of_schools,
                "number_of_hospitals": village.number_of_hospitals,
                "post_office_availability": village.post_office_availability,
                "petrol_bunks": village.petrol_bunks,
                "electricity_supply_hours": village.electricity_supply_hours,
                "renewable_energy_source": village.renewable_energy_source,
                "water_supply_to_every_home": village.water_supply_to_every_home,
                "parks": village.parks,
                "playgrounds": village.playgrounds,
                "sanitation_everyday": village.sanitation_everyday,
                "waste_management_everyday": village.waste_management_everyday,
                "network_connectivity": village.network_connectivity,
                "market_availability": village.market_availability,
                "banks_atm_facility": village.banks_atm_facility,
                "green_cover": village.green_cover,
                "street_lighting": village.street_lighting,
                "public_transport": village.public_transport,
                "number_of_children": village.number_of_children,
                "district": village.district,
                "pincode": village.pincode,
                "state": village.state,
                "sarpanch": village.sarpanch,
                "MRO": village.MRO
            }
            chart_path = f"outputs/charts/{village.id}_analytics.png"
            analytics = get_analytics(village_data, chart_path)
            self.stdout.write("Analytics Results:")
            for key, value in analytics.items():
                self.stdout.write(f"  {key}: {value}")
            self.stdout.write(f"Analytics chart generated at: {chart_path}")

            # Generate AI recommendations
            recommendations = get_ai_recommendations(village_data)
            self.stdout.write("AI Recommendations:")
            for key, value in recommendations.items():
                self.stdout.write(f"  {key}: {value}")

            # Generate PDF report
            report_path = f"outputs/reports/{village.id}_report.pdf"
            doc = SimpleDocTemplate(report_path, pagesize=letter, leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(name='Title', fontName='Helvetica-Bold', fontSize=16, textColor=black, alignment=1, spaceAfter=12)
            section_style = ParagraphStyle(name='Section', fontName='Helvetica-Bold', fontSize=12, textColor=white, alignment=1, spaceAfter=6)
            label_style = ParagraphStyle(name='Label', fontName='Helvetica', fontSize=10, textColor=black, alignment=0, leading=14)
            value_style = ParagraphStyle(name='Value', fontName='Helvetica', fontSize=10, textColor=black, alignment=0, leading=14)
            declaration_style = ParagraphStyle(name='Declaration', fontName='Helvetica', fontSize=10, textColor=black, alignment=0, spaceBefore=12)

            story = []

            # Page 1: Village Details, Overview, Infrastructure
            # Title
            story.append(Paragraph("VILLAGE DEVELOPMENT REPORT", title_style))
            story.append(Spacer(1, 0.2*inch))

            # Village Details Section
            village_details_data = [
                [Paragraph("VILLAGE DETAILS", section_style)]
            ]
            details = [
                ("Village Name", village.name),
                ("District", village.district),
                ("State", village.state),
                ("Pincode", village.pincode),
                ("Sarpanch", village.sarpanch),
                ("MRO", village.MRO)
            ]
            for label, value in details:
                village_details_data.append([
                    Paragraph(f"{label}:", label_style),
                    Paragraph(str(value), value_style)
                ])
            village_details_table = Table(village_details_data, colWidths=[2*inch, 3.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), blue),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, black),
                ('BOX', (0, 0), (-1, -1), 1, black)
            ]))
            story.append(village_details_table)
            story.append(Spacer(1, 0.2*inch))

            # Overview Section
            overview_data = [
                [Paragraph("OVERVIEW", section_style)]
            ]
            overview_items = [
                ("Previous Census Population", village.previous_census_population),
                ("Current Census Population", village.current_census_population),
                ("Number of Children", village.number_of_children),
                ("Village Area", f"{village.village_area} sq km"),
                ("Literacy Rate", f"{village.literacy_rate * 100}%"),
                ("Population Growth Rate", f"{analytics['population_growth_rate']}%")
            ]
            for label, value in overview_items:
                overview_data.append([
                    Paragraph(f"{label}:", label_style),
                    Paragraph(str(value), value_style)
                ])
            overview_table = Table(overview_data, colWidths=[2*inch, 3.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), blue),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, black),
                ('BOX', (0, 0), (-1, -1), 1, black)
            ]))
            story.append(overview_table)
            story.append(Spacer(1, 0.2*inch))

            # Current Infrastructure Assessment Section
            infra_data = [
                [Paragraph("CURRENT INFRASTRUCTURE ASSESSMENT", section_style)]
            ]
            infra_items = [
                ("Healthcare Access", village.healthcare_access),
                ("Number of Hospitals", village.number_of_hospitals),
                ("Post Office Availability", self.format_boolean(village.post_office_availability)),
                ("Number of Petrol Bunks", village.petrol_bunks),
                ("Roads", village.infrastructure['roads']),
                ("Lakes", village.infrastructure['lakes']),
                ("Temples", village.infrastructure['temples']),
                ("Number of Schools", village.number_of_schools),
                ("Electricity Supply (hours/day)", village.electricity_supply_hours),
                ("Renewable Energy Source", self.format_boolean(village.renewable_energy_source)),
                ("Water Supply to Every Home", self.format_boolean(village.water_supply_to_every_home)),
                ("Number of Parks", village.parks),
                ("Number of Playgrounds", village.playgrounds),
                ("Sanitation Everyday", self.format_boolean(village.sanitation_everyday)),
                ("Waste Management Everyday", self.format_boolean(village.waste_management_everyday)),
                ("Network Connectivity", self.format_boolean(village.network_connectivity)),
                ("Market Availability", self.format_boolean(village.market_availability)),
                ("Banks/ATM Facility", self.format_boolean(village.banks_atm_facility)),
                ("Green Cover (%)", village.green_cover),
                ("Street Lighting", self.format_boolean(village.street_lighting)),
                ("Public Transport", self.format_boolean(village.public_transport))
            ]
            for label, value in infra_items:
                infra_data.append([
                    Paragraph(f"{label}:", label_style),
                    Paragraph(str(value), value_style)
                ])
            infra_table = Table(infra_data, colWidths=[2*inch, 3.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), blue),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, black),
                ('BOX', (0, 0), (-1, -1), 1, black)
            ]))
            story.append(infra_table)

            # Declaration Section
            story.append(Paragraph("Declaration: This report is generated based on the data provided and is true to the best of our knowledge.", declaration_style))
            story.append(Paragraph("Date: ____________________", declaration_style))
            story.append(Paragraph("Signature: ____________________", declaration_style))

            # Page 2: Analysis and Recommendations
            story.append(PageBreak())

            # Title
            story.append(Paragraph("VILLAGE DEVELOPMENT REPORT", title_style))
            story.append(Spacer(1, 0.2*inch))

            # Analysis Section
            analysis_data = [
                [Paragraph("ANALYSIS", section_style)]
            ]
            analysis_items = [
                ("Population Growth Rate", f"{analytics['population_growth_rate']}%"),
                ("Population Density", analytics['population_density']),
                ("Area Suitability", analytics['area_suitability']),
                ("Literacy Score", analytics['literacy_score']),
                ("Schools Needed", analytics['schools_needed']),
                ("Hospitals Needed", f"{village.number_of_hospitals} hospital(s) (current: {village.number_of_hospitals})"),
                ("Infrastructure Score", analytics['infrastructure_score']),
                ("Sustainability Index", self.format_boolean(analytics['sustainability_index'])),
                ("Community Score", analytics['community_score']),
                ("Healthcare Score", analytics['healthcare_score']),
                ("Healthcare Access Rating", village.healthcare_access),
                ("Post Office Availability", self.format_boolean(village.post_office_availability)),
                ("Petrol Bunks Accessibility", f"{village.petrol_bunks} bunk(s)")
            ]
            for label, value in analysis_items:
                analysis_data.append([
                    Paragraph(f"{label}:", label_style),
                    Paragraph(str(value), value_style)
                ])
            analysis_table = Table(analysis_data, colWidths=[2*inch, 3.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), blue),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, black),
                ('BOX', (0, 0), (-1, -1), 1, black)
            ]))
            story.append(analysis_table)
            story.append(Spacer(1, 0.2*inch))

            # Recommendations Section
            rec_data = [
                [Paragraph("RECOMMENDATIONS", section_style)]
            ]
            rec_items = [
                ("Infrastructure", recommendations['infrastructure']),
                ("Education", recommendations['education']),
                ("Healthcare", recommendations['healthcare']),
                ("Sustainability", recommendations['sustainability']),
                ("Community", recommendations['community']),
                ("Economic Growth", recommendations['economic_growth']),
                ("Transportation", recommendations['transportation']),
                ("Connectivity", recommendations['connectivity']),
                ("Sanitation", recommendations['sanitation']),
                ("Healthcare Facilities", recommendations['healthcare_facilities']),
                ("Post Office Services", recommendations['post_office_services']),
                ("Petrol Bunk Access", recommendations['petrol_bunk_access'])
            ]
            for label, value in rec_items:
                rec_data.append([
                    Paragraph(f"{label}:", label_style),
                    Paragraph(str(value), value_style)
                ])
            rec_table = Table(rec_data, colWidths=[2*inch, 3.5*inch], style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), blue),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, black),
                ('BOX', (0, 0), (-1, -1), 1, black)
            ]))
            story.append(rec_table)

            # Declaration Section
            story.append(Paragraph("Declaration: This report is generated based on the data provided and is true to the best of our knowledge.", declaration_style))
            story.append(Paragraph("Date: ____________________", declaration_style))
            story.append(Paragraph("Signature: ____________________", declaration_style))

            # Build the PDF
            doc.build(story)
            self.stdout.write(f"PDF report generated at: {report_path}")

        except Exception as e:
            self.stdout.write(f"Error: {str(e)}")