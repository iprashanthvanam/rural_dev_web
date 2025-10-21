'''# backend/village_app/views.py

from django.shortcuts import render, redirect
from django.contrib.gis.geos import Point
from .models import Village
from .utils.gis import generate_map_image as gis_generate_map_image
from .utils.ai_recommendations import get_ai_recommendations
from .utils.analytics import get_analytics
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import navy, green, black, white
from reportlab.lib.units import inch
import os

def input_form(request):
    if request.method == 'POST':
        print("Form submitted with POST method")  # Debug: Check if POST request is received
        try:
            # Extract form data
            name = request.POST.get('name')
            previous_census_population = int(request.POST.get('previous_census_population'))
            current_census_population = int(request.POST.get('current_census_population'))
            village_area = float(request.POST.get('village_area'))
            literacy_rate = float(request.POST.get('literacy_rate')) / 100
            healthcare_access = request.POST.get('healthcare_access')
            roads = request.POST.get('roads')
            lakes = int(request.POST.get('lakes'))
            temples = int(request.POST.get('temples'))
            latitude = float(request.POST.get('latitude'))
            longitude = float(request.POST.get('longitude'))
            number_of_schools = int(request.POST.get('number_of_schools'))
            number_of_hospitals = int(request.POST.get('number_of_hospitals'))
            post_office_availability = request.POST.get('post_office_availability') == 'on'
            petrol_bunks = int(request.POST.get('petrol_bunks'))
            electricity_supply_hours = int(request.POST.get('electricity_supply_hours'))
            renewable_energy_source = request.POST.get('renewable_energy_source') == 'on'
            water_supply_to_every_home = request.POST.get('water_supply_to_every_home') == 'on'
            parks = int(request.POST.get('parks'))
            playgrounds = int(request.POST.get('playgrounds'))
            sanitation_everyday = request.POST.get('sanitation_everyday') == 'on'
            waste_management_everyday = request.POST.get('waste_management_everyday') == 'on'
            network_connectivity = request.POST.get('network_connectivity') == 'on'
            market_availability = request.POST.get('market_availability') == 'on'
            banks_atm_facility = request.POST.get('banks_atm_facility') == 'on'
            green_cover = float(request.POST.get('green_cover'))
            street_lighting = request.POST.get('street_lighting') == 'on'
            public_transport = request.POST.get('public_transport') == 'on'
            number_of_children = int(request.POST.get('number_of_children'))
            district = request.POST.get('district')
            pincode = request.POST.get('pincode')
            state = request.POST.get('state')
            sarpanch = request.POST.get('sarpanch')
            MRO = request.POST.get('MRO')

            print("Form data extracted successfully")  # Debug: Confirm data extraction

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

            print(f"Village saved with ID: {village.id}")  # Debug: Confirm village is saved

            # Generate outputs
            os.makedirs("outputs/maps", exist_ok=True)
            os.makedirs("outputs/charts", exist_ok=True)
            os.makedirs("outputs/models", exist_ok=True)
            os.makedirs("outputs/reports", exist_ok=True)

            # Generate map
            map_path = f"outputs/maps/{village.id}_map.png"
            print(f"Generating map at: {map_path}")  # Debug
            gis_generate_map_image(village, map_path)

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
            print(f"Generating analytics chart at: {chart_path}")  # Debug
            analytics = get_analytics(village_data, chart_path)

            # Generate AI recommendations
            print("Generating AI recommendations")  # Debug
            recommendations = get_ai_recommendations(village_data)

            # Generate PDF report
            report_path = f"outputs/reports/{village.id}_report.pdf"
            print(f"Generating PDF report at: {report_path}")  # Debug
            doc = SimpleDocTemplate(report_path, pagesize=landscape(letter), leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(name='Title', fontName='Helvetica-Bold', fontSize=16, textColor=navy, alignment=1, spaceAfter=10)
            heading_style = ParagraphStyle(name='Heading', fontName='Helvetica-Bold', fontSize=12, textColor=navy, spaceAfter=6)
            data_style = ParagraphStyle(name='Data', fontName='Helvetica', fontSize=10, textColor=green, leading=12)

            story = []

            # Page 1: Header and Main Sections
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
                ["Post Office Availability", "Yes" if village.post_office_availability else "No"],
                ["Number of Petrol Bunks", str(village.petrol_bunks)],
                ["Roads", village.infrastructure["roads"]],
                ["Lakes", str(village.infrastructure["lakes"])],
                ["Temples", str(village.infrastructure["temples"])],
                ["Number of Schools", str(village.number_of_schools)],
                ["Electricity Supply (hours/day)", str(village.electricity_supply_hours)],
                ["Renewable Energy Source", "Yes" if village.renewable_energy_source else "No"],
                ["Water Supply to Every Home", "Yes" if village.water_supply_to_every_home else "No"],
                ["Number of Parks", str(village.parks)],
                ["Number of Playgrounds", str(village.playgrounds)],
                ["Sanitation Everyday", "Yes" if village.sanitation_everyday else "No"],
                ["Waste Management Everyday", "Yes" if village.waste_management_everyday else "No"],
                ["Network Connectivity", "Yes" if village.network_connectivity else "No"],
                ["Market Availability", "Yes" if village.market_availability else "No"],
                ["Banks/ATM Facility", "Yes" if village.banks_atm_facility else "No"],
                ["Green Cover (%)", str(village.green_cover)],
                ["Street Lighting", "Yes" if village.street_lighting else "No"],
                ["Public Transport", "Yes" if village.public_transport else "No"]
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
                ["Sustainability Index", "Yes" if analytics['sustainability_index'] else "No"],
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

            print("PDF generated successfully")  # Debug

            # Redirect to a success page with the village ID
            return redirect('success', village_id=village.id)

        except Exception as e:
            print(f"Error in form submission: {str(e)}")  # Debug: Log any errors
            return render(request, 'input_form.html', {'error': f"Error: {str(e)}"})

    return render(request, 'input_form.html')

def success(request, village_id):
    return render(request, 'success.html', {'village_id': village_id})'''



# backend\village_app\views.py

'''import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.gis.geos import Point
from .models import Village
from .utils.gis import generate_map_image as gis_generate_map_image
from .utils.ai_recommendations import get_ai_recommendations
from .utils.analytics import get_analytics
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import navy, green, black, white
from reportlab.lib.units import inch

def input_form(request):
    print(f"Request method: {request.method}")  # Debug: Check request method
    if request.method == 'POST':
        print("Form submitted with POST method")  # Debug
        try:
            # Extract form data (add validation)
            name = request.POST.get('name')
            if not name:
                raise ValueError("Village name is required.")
            previous_census_population = int(request.POST.get('previous_census_population') or 0)
            current_census_population = int(request.POST.get('current_census_population') or 0)
            village_area = float(request.POST.get('village_area') or 0)
            literacy_rate = float(request.POST.get('literacy_rate') or 0) / 100
            healthcare_access = request.POST.get('healthcare_access', 'Poor')
            roads = request.POST.get('roads', 'unpaved')
            lakes = int(request.POST.get('lakes') or 0)
            temples = int(request.POST.get('temples') or 0)
            latitude = float(request.POST.get('latitude') or 0)
            longitude = float(request.POST.get('longitude') or 0)
            number_of_schools = int(request.POST.get('number_of_schools') or 0)
            number_of_hospitals = int(request.POST.get('number_of_hospitals') or 0)
            post_office_availability = request.POST.get('post_office_availability') == 'on'
            petrol_bunks = int(request.POST.get('petrol_bunks') or 0)
            electricity_supply_hours = int(request.POST.get('electricity_supply_hours') or 0)
            renewable_energy_source = request.POST.get('renewable_energy_source') == 'on'
            water_supply_to_every_home = request.POST.get('water_supply_to_every_home') == 'on'
            parks = int(request.POST.get('parks') or 0)
            playgrounds = int(request.POST.get('playgrounds') or 0)
            sanitation_everyday = request.POST.get('sanitation_everyday') == 'on'
            waste_management_everyday = request.POST.get('waste_management_everyday') == 'on'
            network_connectivity = request.POST.get('network_connectivity') == 'on'
            market_availability = request.POST.get('market_availability') == 'on'
            banks_atm_facility = request.POST.get('banks_atm_facility') == 'on'
            green_cover = float(request.POST.get('green_cover') or 0)
            street_lighting = request.POST.get('street_lighting') == 'on'
            public_transport = request.POST.get('public_transport') == 'on'
            number_of_children = int(request.POST.get('number_of_children') or 0)
            district = request.POST.get('district', '')
            pincode = request.POST.get('pincode', '')
            state = request.POST.get('state', '')
            sarpanch = request.POST.get('sarpanch', '')
            MRO = request.POST.get('MRO', '')

            print("Form data extracted successfully")  # Debug
            print(f"Data: {name}, {previous_census_population}, {current_census_population}, ...")  # Debug partial data

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

            print(f"Village saved with ID: {village.id}")  # Debug

            # Generate outputs (simplified for testing)
            os.makedirs("outputs/maps", exist_ok=True)
            os.makedirs("outputs/charts", exist_ok=True)
            os.makedirs("outputs/reports", exist_ok=True)

            map_path = f"outputs/maps/{village.id}_map.png"
            print(f"Generating map at: {map_path}")
            with open(map_path, 'w') as f:  # Placeholder map
                f.write("Placeholder map for " + village.name)

            chart_path = f"outputs/charts/{village.id}_analytics.png"
            print(f"Generating chart at: {chart_path}")
            with open(chart_path, 'w') as f:  # Placeholder chart
                f.write("Placeholder chart")

            report_path = f"outputs/reports/{village.id}_report.pdf"
            print(f"Generating PDF at: {report_path}")
            c = canvas.Canvas(report_path, pagesize=letter)
            c.drawString(100, 750, f"Report for {village.name}")
            c.save()

            print("Outputs generated successfully")

            return redirect('success', village_id=village.id)

        except Exception as e:
            print(f"Error in form submission: {str(e)}")  # Debug
            return render(request, 'input_form.html', {'error': f"Error: {str(e)}"})

    return render(request, 'input_form.html')

def success(request, village_id):
    return render(request, 'success.html', {'village_id': village_id})'''





'''# backend\village_app\views.py

import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.gis.geos import Point
from .models import Village

def input_form(request):
    print(f"Request method: {request.method}")  # Debug
    if request.method == 'POST':
        print("Form submitted with POST method")  # Debug
        try:
            # Extract form data with defaults
            name = request.POST.get('name', '')
            previous_census_population = int(request.POST.get('previous_census_population') or 0)
            current_census_population = int(request.POST.get('current_census_population') or 0)
            village_area = float(request.POST.get('village_area') or 0)
            literacy_rate = float(request.POST.get('literacy_rate') or 0) / 100
            healthcare_access = request.POST.get('healthcare_access', 'Poor')
            roads = request.POST.get('roads', 'unpaved')
            lakes = int(request.POST.get('lakes') or 0)
            temples = int(request.POST.get('temples') or 0)
            latitude = float(request.POST.get('latitude') or 0)
            longitude = float(request.POST.get('longitude') or 0)
            number_of_schools = int(request.POST.get('number_of_schools') or 0)
            number_of_hospitals = int(request.POST.get('number_of_hospitals') or 0)
            post_office_availability = request.POST.get('post_office_availability') == 'on'
            petrol_bunks = int(request.POST.get('petrol_bunks') or 0)
            electricity_supply_hours = int(request.POST.get('electricity_supply_hours') or 0)
            renewable_energy_source = request.POST.get('renewable_energy_source') == 'on'
            water_supply_to_every_home = request.POST.get('water_supply_to_every_home') == 'on'
            parks = int(request.POST.get('parks') or 0)
            playgrounds = int(request.POST.get('playgrounds') or 0)
            sanitation_everyday = request.POST.get('sanitation_everyday') == 'on'
            waste_management_everyday = request.POST.get('waste_management_everyday') == 'on'
            network_connectivity = request.POST.get('network_connectivity') == 'on'
            market_availability = request.POST.get('market_availability') == 'on'
            banks_atm_facility = request.POST.get('banks_atm_facility') == 'on'
            green_cover = float(request.POST.get('green_cover') or 0)
            street_lighting = request.POST.get('street_lighting') == 'on'
            public_transport = request.POST.get('public_transport') == 'on'
            number_of_children = int(request.POST.get('number_of_children') or 0)
            district = request.POST.get('district', '')
            pincode = request.POST.get('pincode', '')
            state = request.POST.get('state', '')
            sarpanch = request.POST.get('sarpanch', '')
            MRO = request.POST.get('MRO', '')

            print("Form data extracted:", name, previous_census_population, current_census_population)  # Debug

            # Save to database
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
            print(f"Village saved with ID: {village.id}")  # Debug

            # Generate placeholder outputs
            os.makedirs("outputs/maps", exist_ok=True)
            os.makedirs("outputs/charts", exist_ok=True)
            os.makedirs("outputs/reports", exist_ok=True)

            map_path = f"outputs/maps/{village.id}_map.png"
            with open(map_path, 'w') as f:
                f.write("Placeholder map")
            print(f"Map generated at: {map_path}")

            chart_path = f"outputs/charts/{village.id}_analytics.png"
            with open(chart_path, 'w') as f:
                f.write("Placeholder chart")
            print(f"Chart generated at: {chart_path}")

            report_path = f"outputs/reports/{village.id}_report.pdf"
            with open(report_path, 'w') as f:
                f.write("Placeholder PDF")
            print(f"PDF generated at: {report_path}")

            return redirect('success', village_id=village.id)

        except Exception as e:
            print(f"Error in form submission: {str(e)}")  # Debug
            return render(request, 'input_form.html', {'error': f"Error: {str(e)}"})

    return render(request, 'input_form.html')

def success(request, village_id):
    return render(request, 'success.html', {'village_id': village_id})'''








'''# backend\village_app\views.py
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.gis.geos import Point
from .models import Village

def input_form(request):
    print(f"View called - Request method: {request.method}")  # Debug
    if request.method == 'POST':
        print("POST request received")  # Debug
        try:
            print("POST data:", request.POST)  # Debug all form data
            name = request.POST.get('name', '')
            if not name:
                raise ValueError("Village name is required.")
            print(f"Extracted name: {name}")  # Debug

            # Minimal save to test database
            village = Village(name=name, population=0, location=Point(0, 0))
            village.save()
            print(f"Village saved with ID: {village.id}")  # Debug

            # Generate placeholder outputs
            os.makedirs("outputs/maps", exist_ok=True)
            os.makedirs("outputs/charts", exist_ok=True)
            os.makedirs("outputs/reports", exist_ok=True)

            map_path = f"outputs/maps/{village.id}_map.png"
            with open(map_path, 'w') as f:
                f.write("Placeholder map")
            print(f"Map generated at: {map_path}")

            chart_path = f"outputs/charts/{village.id}_analytics.png"
            with open(chart_path, 'w') as f:
                f.write("Placeholder chart")
            print(f"Chart generated at: {chart_path}")

            report_path = f"outputs/reports/{village.id}_report.pdf"
            with open(report_path, 'w') as f:
                f.write("Placeholder PDF")
            print(f"PDF generated at: {report_path}")

            return redirect('success', village_id=village.id)

        except Exception as e:
            print(f"Error in form submission: {str(e)}")  # Debug with full traceback
            return render(request, 'input_form.html', {'error': f"Error: {str(e)}"})

    print("Rendering form (GET request)")  # Debug
    return render(request, 'input_form.html')

def success(request, village_id):
    print("Success view called with village_id: {village_id}")  # Debug
    return render(request, 'success.html', {'village_id': village_id})'''




'''# backend\village_app\views.py
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.gis.geos import Point
from .models import Village

def input_form(request):
    print(f"View called - Request method: {request.method}")  # Debug
    if request.method == 'POST':
        print("POST request received")  # Debug
        try:
            print("POST data:", request.POST)  # Debug all form data
            name = request.POST.get('name', '')
            if not name:
                raise ValueError("Village name is required.")
            print(f"Extracted name: {name}")  # Debug

            # Extract and debug literacy_rate
            literacy_rate_str = request.POST.get('literacy_rate', '')
            print(f"Raw literacy_rate from POST: {literacy_rate_str}")  # Debug
            literacy_rate = float(literacy_rate_str) / 100 if literacy_rate_str else 0.0
            print(f"Converted literacy_rate: {literacy_rate}")  # Debug

            # Extract other fields (simplified for debugging)
            previous_census_population = int(request.POST.get('previous_census_population') or 0)
            current_census_population = int(request.POST.get('current_census_population') or 0)
            village_area = float(request.POST.get('village_area') or 0)
            healthcare_access = request.POST.get('healthcare_access', 'Poor')
            roads = request.POST.get('roads', 'unpaved')
            lakes = int(request.POST.get('lakes') or 0)
            temples = int(request.POST.get('temples') or 0)
            latitude = float(request.POST.get('latitude') or 0)
            longitude = float(request.POST.get('longitude') or 0)
            number_of_schools = int(request.POST.get('number_of_schools') or 0)
            number_of_hospitals = int(request.POST.get('number_of_hospitals') or 0)
            post_office_availability = request.POST.get('post_office_availability') == 'on'
            petrol_bunks = int(request.POST.get('petrol_bunks') or 0)
            electricity_supply_hours = int(request.POST.get('electricity_supply_hours') or 0)
            renewable_energy_source = request.POST.get('renewable_energy_source') == 'on'
            water_supply_to_every_home = request.POST.get('water_supply_to_every_home') == 'on'
            parks = int(request.POST.get('parks') or 0)
            playgrounds = int(request.POST.get('playgrounds') or 0)
            sanitation_everyday = request.POST.get('sanitation_everyday') == 'on'
            waste_management_everyday = request.POST.get('waste_management_everyday') == 'on'
            network_connectivity = request.POST.get('network_connectivity') == 'on'
            market_availability = request.POST.get('market_availability') == 'on'
            banks_atm_facility = request.POST.get('banks_atm_facility') == 'on'
            green_cover = float(request.POST.get('green_cover') or 0)
            street_lighting = request.POST.get('street_lighting') == 'on'
            public_transport = request.POST.get('public_transport') == 'on'
            number_of_children = int(request.POST.get('number_of_children') or 0)
            district = request.POST.get('district', '')
            pincode = request.POST.get('pincode', '')
            state = request.POST.get('state', '')
            sarpanch = request.POST.get('sarpanch', '')
            MRO = request.POST.get('MRO', '')

            # Save to database
            village = Village(
                name=name,
                previous_census_population=previous_census_population,
                current_census_population=current_census_population,
                village_area=village_area,
                population=current_census_population,
                literacy_rate=literacy_rate,  # Ensure this is set
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
            print(f"Village saved with ID: {village.id}")  # Debug

            # Generate placeholder outputs
            os.makedirs("outputs/maps", exist_ok=True)
            os.makedirs("outputs/charts", exist_ok=True)
            os.makedirs("outputs/reports", exist_ok=True)

            map_path = f"outputs/maps/{village.id}_map.png"
            with open(map_path, 'w') as f:
                f.write("Placeholder map")
            print(f"Map generated at: {map_path}")

            chart_path = f"outputs/charts/{village.id}_analytics.png"
            with open(chart_path, 'w') as f:
                f.write("Placeholder chart")
            print(f"Chart generated at: {chart_path}")

            report_path = f"outputs/reports/{village.id}_report.pdf"
            with open(report_path, 'w') as f:
                f.write("Placeholder PDF")
            print(f"PDF generated at: {report_path}")

            return redirect('success', village_id=village.id)

        except Exception as e:
            print(f"Error in form submission: {str(e)}")  # Debug with full traceback
            return render(request, 'input_form.html', {'error': f"Error: {str(e)}"})

    print("Rendering form (GET request)")  # Debug
    return render(request, 'input_form.html')

def success(request, village_id):
    print("Success view called with village_id: {village_id}")  # Debug
    return render(request, 'success.html', {'village_id': village_id})'''









from django.shortcuts import render, redirect
from django.contrib.gis.geos import Point
from .models import Village
from .utils.gis import generate_map_image as gis_generate_map_image
from .utils.ai_recommendations import get_ai_recommendations
from .utils.analytics import get_analytics
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import navy, green, black, white
from reportlab.lib.units import inch
import os
from reportlab.platypus import PageBreak


def input_form(request):
    if request.method == 'POST':
        print("Form submitted with POST method")  # Debug
        try:
            # Extract form data
            name = request.POST.get('name')
            previous_census_population = int(request.POST.get('previous_census_population'))
            current_census_population = int(request.POST.get('current_census_population'))
            village_area = float(request.POST.get('village_area'))
            literacy_rate = float(request.POST.get('literacy_rate')) / 100
            healthcare_access = request.POST.get('healthcare_access')
            roads = request.POST.get('roads')
            lakes = int(request.POST.get('lakes'))
            temples = int(request.POST.get('temples'))
            latitude = float(request.POST.get('latitude'))
            longitude = float(request.POST.get('longitude'))
            number_of_schools = int(request.POST.get('number_of_schools'))
            number_of_hospitals = int(request.POST.get('number_of_hospitals'))
            post_office_availability = request.POST.get('post_office_availability') == 'on'
            petrol_bunks = int(request.POST.get('petrol_bunks'))
            electricity_supply_hours = int(request.POST.get('electricity_supply_hours'))
            renewable_energy_source = request.POST.get('renewable_energy_source') == 'on'
            water_supply_to_every_home = request.POST.get('water_supply_to_every_home') == 'on'
            parks = int(request.POST.get('parks'))
            playgrounds = int(request.POST.get('playgrounds'))
            sanitation_everyday = request.POST.get('sanitation_everyday') == 'on'
            waste_management_everyday = request.POST.get('waste_management_everyday') == 'on'
            network_connectivity = request.POST.get('network_connectivity') == 'on'
            market_availability = request.POST.get('market_availability') == 'on'
            banks_atm_facility = request.POST.get('banks_atm_facility') == 'on'
            green_cover = float(request.POST.get('green_cover'))
            street_lighting = request.POST.get('street_lighting') == 'on'
            public_transport = request.POST.get('public_transport') == 'on'
            number_of_children = int(request.POST.get('number_of_children'))
            district = request.POST.get('district')
            pincode = request.POST.get('pincode')
            state = request.POST.get('state')
            sarpanch = request.POST.get('sarpanch')
            MRO = request.POST.get('MRO')

            print("Form data extracted successfully")  # Debug

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

            print(f"Village saved with ID: {village.id}")  # Debug

            # Generate outputs
            os.makedirs("outputs/maps", exist_ok=True)
            os.makedirs("outputs/charts", exist_ok=True)
            os.makedirs("outputs/models", exist_ok=True)
            os.makedirs("outputs/reports", exist_ok=True)

            # Generate map
            map_path = f"outputs/maps/{village.id}_map.png"
            print(f"Generating map at: {map_path}")  # Debug
            gis_generate_map_image(village, map_path)

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
            print(f"Generating analytics chart at: {chart_path}")  # Debug
            analytics = get_analytics(village_data, chart_path)

            # Generate AI recommendations
            print("Generating AI recommendations")  # Debug
            recommendations = get_ai_recommendations(village_data)

            # Generate PDF report
            report_path = f"outputs/reports/{village.id}_report.pdf"
            print(f"Generating PDF report at: {report_path}")  # Debug
            doc = SimpleDocTemplate(report_path, pagesize=landscape(letter), leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(name='Title', fontName='Helvetica-Bold', fontSize=16, textColor=navy, alignment=1, spaceAfter=10)
            heading_style = ParagraphStyle(name='Heading', fontName='Helvetica-Bold', fontSize=12, textColor=navy, spaceAfter=6)
            data_style = ParagraphStyle(name='Data', fontName='Helvetica', fontSize=10, textColor=green, leading=12, wordWrap='CJK')

            story = []

            # Page 1: Header and Main Sections
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
                ('TEXTCOLOR', (0, 1), (-1, -1), green),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('WORDWRAP', (0, 1), (-1, -1), 'CJK')
            ]))
            overview_table._argW[1] = 5*inch  # Ensure second column can expand
            story.append(overview_table)
            story.append(Spacer(1, 0.1*inch))

            # Current Infrastructure Assessment
            infra_data = [
                ["CURRENT INFRASTRUCTURE ASSESSMENT"],
                ["Healthcare Access", village.healthcare_access],
                ["Number of Hospitals", str(village.number_of_hospitals)],
                ["Post Office Availability", "Yes" if village.post_office_availability else "No"],
                ["Number of Petrol Bunks", str(village.petrol_bunks)],
                ["Roads", village.infrastructure["roads"]],
                ["Lakes", str(village.infrastructure["lakes"])],
                ["Temples", str(village.infrastructure["temples"])],
                ["Number of Schools", str(village.number_of_schools)],
                ["Electricity Supply (hours/day)", str(village.electricity_supply_hours)],
                ["Renewable Energy Source", "Yes" if village.renewable_energy_source else "No"],
                ["Water Supply to Every Home", "Yes" if village.water_supply_to_every_home else "No"],
                ["Number of Parks", str(village.parks)],
                ["Number of Playgrounds", str(village.playgrounds)],
                ["Sanitation Everyday", "Yes" if village.sanitation_everyday else "No"],
                ["Waste Management Everyday", "Yes" if village.waste_management_everyday else "No"],
                ["Network Connectivity", "Yes" if village.network_connectivity else "No"],
                ["Market Availability", "Yes" if village.market_availability else "No"],
                ["Banks/ATM Facility", "Yes" if village.banks_atm_facility else "No"],
                ["Green Cover (%)", str(village.green_cover)],
                ["Street Lighting", "Yes" if village.street_lighting else "No"],
                ["Public Transport", "Yes" if village.public_transport else "No"]
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
                ('TEXTCOLOR', (0, 1), (-1, -1), green),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('WORDWRAP', (0, 1), (-1, -1), 'CJK')
            ]))
            infra_table._argW[1] = 5*inch  # Ensure second column can expand
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
                ('TEXTCOLOR', (0, 1), (-1, -1), green),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('WORDWRAP', (0, 1), (-1, -1), 'CJK')
            ]))
            story.append(details_table)

            # Page 2: Analysis and Recommendations
            story.append(PageBreak())

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
                ["Sustainability Index", "Yes" if analytics['sustainability_index'] else "No"],
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
                ('TEXTCOLOR', (0, 1), (-1, -1), green),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('WORDWRAP', (0, 1), (-1, -1), 'CJK')
            ]))
            analysis_table._argW[1] = 5*inch  # Ensure second column can expand
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
                ('TEXTCOLOR', (0, 1), (-1, -1), green),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('WORDWRAP', (0, 1), (-1, -1), 'CJK')
            ]))
            rec_table._argW[1] = 5*inch  # Ensure second column can expand
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
                ('TEXTCOLOR', (0, 1), (-1, -1), black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('WORDWRAP', (0, 1), (-1, -1), 'CJK')
            ]))
            story.append(declaration_table)

            # Build the PDF
            doc.build(story)

            print("PDF generated successfully")  # Debug

            # Redirect to a success page with the village ID
            return redirect('success', village_id=village.id)

        except Exception as e:
            print(f"Error in form submission: {str(e)}")  # Debug
            return render(request, 'input_form.html', {'error': f"Error: {str(e)}"})

    return render(request, 'input_form.html')

def success(request, village_id):
    return render(request, 'success.html', {'village_id': village_id})


