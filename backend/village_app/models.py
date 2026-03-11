


# from django.contrib.gis.db import models
from django.db import models

class Village(models.Model):
    name = models.CharField(max_length=100)
    previous_census_population = models.IntegerField()
    current_census_population = models.IntegerField()
    village_area = models.FloatField()
    population = models.IntegerField(default=0)
    literacy_rate = models.FloatField()
    healthcare_access = models.CharField(max_length=20)
    infrastructure = models.JSONField(default=dict)
    # location = models.PointField(srid=4326)
    latitude = models.FloatField()
    longitude = models.FloatField()
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