'''from django.contrib.gis.db import models

class Village(models.Model):
    name = models.CharField(max_length=100)
    population = models.IntegerField()
    literacy_rate = models.FloatField()
    healthcare_access = models.CharField(max_length=20)  # Altered field
    infrastructure = models.JSONField(default=dict)     # Altered field
    location = models.PointField(srid=4326)



from django.contrib.gis.db import models

class Village(models.Model):
    name = models.CharField(max_length=100)
    population = models.IntegerField()
    literacy_rate = models.FloatField()
    healthcare_access = models.CharField(max_length=20)
    infrastructure = models.JSONField(default=dict)
    location = models.PointField(srid=4326)
    # New fields
    number_of_schools = models.IntegerField(default=0)
    electricity_supply_hours = models.IntegerField(default=0)  # Hours per day
    renewable_energy_source = models.BooleanField(default=False)  # Y/N
    water_supply_to_every_home = models.BooleanField(default=False)
    parks = models.IntegerField(default=0)
    playgrounds = models.IntegerField(default=0)
    sanitation_everyday = models.BooleanField(default=False)
    waste_management_everyday = models.BooleanField(default=False)
    network_connectivity = models.BooleanField(default=False)
    market_availability = models.BooleanField(default=False)
    banks_atm_facility = models.BooleanField(default=False)
    green_cover = models.FloatField(default=0.0)  # Percentage or area
    street_lighting = models.BooleanField(default=False)
    public_transport = models.BooleanField(default=False)
    number_of_children = models.IntegerField(default=0)
    previous_census_population = models.IntegerField()  # Previous census population
    current_census_population = models.IntegerField()
    village_area = models.FloatField(default=0.0)

    def __str__(self):
        return self.name'''



'''
from django.contrib.gis.db import models

class Village(models.Model):
    name = models.CharField(max_length=100)
    previous_census_population = models.IntegerField()
    current_census_population = models.IntegerField()
    literacy_rate = models.FloatField()
    healthcare_access = models.CharField(max_length=20)
    infrastructure = models.JSONField(default=dict)
    location = models.PointField(srid=4326)
    number_of_schools = models.IntegerField(default=0)
    electricity_supply_hours = models.IntegerField(default=0)
    renewable_energy_source = models.BooleanField(default=False)
    water_supply_to_every_home = models.BooleanField(default=False)
    parks = models.IntegerField(default=0)
    playgrounds = models.IntegerField(default=0)
    sanitation_everyday = models.BooleanField(default=False)
    waste_management_everyday = models.BooleanField(default=False)
    network_connectivity = models.BooleanField(default=False)
    market_availability = models.BooleanField(default=False)
    banks_atm_facility = models.BooleanField(default=False)
    green_cover = models.FloatField(default=0.0)
    street_lighting = models.BooleanField(default=False)
    public_transport = models.BooleanField(default=False)
    number_of_children = models.IntegerField(default=0)
    village_area = models.FloatField(default=0.0)
    number_of_parks = models.IntegerField(default=0)  # Add this field
    number_of_playgrounds = models.IntegerField(default=0)

    def __str__(self):
        return self.name'''


'''from django.contrib.gis.db import models

class Village(models.Model):
    name = models.CharField(max_length=100)
    previous_census_population = models.IntegerField()  # New field
    current_census_population = models.IntegerField()  # New field
    village_area = models.FloatField()  # New field in sq km
    population = models.IntegerField()  # Use current_census_population as population
    number_of_hospitals = models.IntegerField(default=0)  # New field
    post_office_availability = models.BooleanField(default=False)  # New field
    petrol_bunks = models.IntegerField(default=0)  # New field
    literacy_rate = models.FloatField()
    healthcare_access = models.CharField(max_length=20)
    infrastructure = models.JSONField(default=dict)
    location = models.PointField(srid=4326)
    number_of_schools = models.IntegerField(default=0)
    electricity_supply_hours = models.IntegerField(default=0)
    renewable_energy_source = models.BooleanField(default=False)
    water_supply_to_every_home = models.BooleanField(default=False)
    parks = models.IntegerField(default=0)
    playgrounds = models.IntegerField(default=0)
    sanitation_everyday = models.BooleanField(default=False)
    waste_management_everyday = models.BooleanField(default=False)
    network_connectivity = models.BooleanField(default=False)
    market_availability = models.BooleanField(default=False)
    banks_atm_facility = models.BooleanField(default=False)
    green_cover = models.FloatField(default=0.0)
    street_lighting = models.BooleanField(default=False)
    public_transport = models.BooleanField(default=False)
    number_of_children = models.IntegerField(default=0)
    district = models.CharField(max_length=100, default="")  # New field
    pincode = models.CharField(max_length=10, default="")   # New field
    state = models.CharField(max_length=100, default="")    # New field
    sarpanch = models.CharField(max_length=100, default="") # New field
    MRO = models.CharField(max_length=100, default="")      # New field

    def __str__(self):
        return self.name'''














'''from django.db import models
from django.contrib.gis.db import models as gis_models

class Village(models.Model):
    name = models.CharField(max_length=255)
    previous_census_population = models.IntegerField()
    current_census_population = models.IntegerField()
    village_area = models.FloatField()  # Reverted from 'area'
    literacy_rate = models.FloatField()
    healthcare_access = models.CharField(max_length=50)
    location = gis_models.PointField(srid=4326)
    number_of_schools = models.IntegerField(default=0)
    number_of_hospitals = models.IntegerField(default=0)
    post_office_availability = models.BooleanField(default=False)
    petrol_bunks = models.IntegerField(default=0)
    electricity_supply_hours = models.IntegerField(default=0)
    renewable_energy_source = models.BooleanField(default=False)
    water_supply_to_every_home = models.BooleanField(default=False)  # Reverted from 'water_supply_to_homes'
    parks = models.IntegerField(default=0)
    playgrounds = models.IntegerField(default=0)
    sanitation_everyday = models.BooleanField(default=False)
    waste_management_everyday = models.BooleanField(default=False)
    network_connectivity = models.BooleanField(default=False)
    market_availability = models.BooleanField(default=False)
    banks_atm_facility = models.BooleanField(default=False)
    green_cover_percentage = models.FloatField(default=0)  # Keep this if it’s new and compatible
    street_lighting = models.BooleanField(default=False)
    public_transport = models.BooleanField(default=False)
    number_of_children = models.IntegerField(default=0)
    district = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    state = models.CharField(max_length=255)
    sarpanch_name = models.CharField(max_length=255, default="")  # Keep this if new
    mro_name = models.CharField(max_length=255, default="")  # Keep this if new

    def __str__(self):
        return self.name'''


'''from django.db import models
from django.contrib.gis.db import models as gis_models

class Infrastructure(models.Model):
    roads = models.CharField(max_length=255, blank=True)
    lakes = models.IntegerField(default=0)
    temples = models.IntegerField(default=0)

    def __str__(self):
        return f"Infrastructure for {self.id}"

class Village(models.Model):
    name = models.CharField(max_length=255)
    previous_census_population = models.IntegerField()
    current_census_population = models.IntegerField()
    village_area = models.FloatField()
    literacy_rate = models.FloatField()
    healthcare_access = models.CharField(max_length=50)
    location = gis_models.PointField(srid=4326)
    population = models.IntegerField(default=0)  # Restored field
    infrastructure = models.OneToOneField(Infrastructure, on_delete=models.CASCADE, null=True)  # Restored field
    green_cover = models.FloatField(default=0)  # Restored field
    sarpanch = models.CharField(max_length=255, blank=True)  # Restored field
    MRO = models.CharField(max_length=255, blank=True)  # Restored field
    number_of_schools = models.IntegerField(default=0)
    number_of_hospitals = models.IntegerField(default=0)
    post_office_availability = models.BooleanField(default=False)
    petrol_bunks = models.IntegerField(default=0)
    electricity_supply_hours = models.IntegerField(default=0)
    renewable_energy_source = models.BooleanField(default=False)
    water_supply_to_every_home = models.BooleanField(default=False)
    parks = models.IntegerField(default=0)
    playgrounds = models.IntegerField(default=0)
    sanitation_everyday = models.BooleanField(default=False)
    waste_management_everyday = models.BooleanField(default=False)
    network_connectivity = models.BooleanField(default=False)
    market_availability = models.BooleanField(default=False)
    banks_atm_facility = models.BooleanField(default=False)
    street_lighting = models.BooleanField(default=False)
    public_transport = models.BooleanField(default=False)
    number_of_children = models.IntegerField(default=0)
    district = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    state = models.CharField(max_length=255)

    def __str__(self):
        return self.name'''











from django.contrib.gis.db import models

class Village(models.Model):
    name = models.CharField(max_length=100)
    previous_census_population = models.IntegerField()
    current_census_population = models.IntegerField()
    village_area = models.FloatField()
    population = models.IntegerField(default=0)
    literacy_rate = models.FloatField()
    healthcare_access = models.CharField(max_length=20)
    infrastructure = models.JSONField(default=dict)
    location = models.PointField(srid=4326)
    number_of_schools = models.IntegerField(default=0)
    number_of_hospitals = models.IntegerField(default=0)  
    post_office_availability = models.BooleanField(default=False) 
    petrol_bunks = models.IntegerField(default=0) 
    electricity_supply_hours = models.IntegerField(default=0)
    renewable_energy_source = models.BooleanField(default=False)
    water_supply_to_every_home = models.BooleanField(default=False)
    parks = models.IntegerField(default=0)
    playgrounds = models.IntegerField(default=0)
    sanitation_everyday = models.BooleanField(default=False)
    waste_management_everyday = models.BooleanField(default=False)
    network_connectivity = models.BooleanField(default=False)
    market_availability = models.BooleanField(default=False)
    banks_atm_facility = models.BooleanField(default=False)
    green_cover = models.FloatField(default=0.0)
    street_lighting = models.BooleanField(default=False)
    public_transport = models.BooleanField(default=False)
    number_of_children = models.IntegerField(default=0)
    district = models.CharField(max_length=100, default="")
    pincode = models.CharField(max_length=10, default="")
    state = models.CharField(max_length=100, default="")
    sarpanch = models.CharField(max_length=100, default="")
    MRO = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name