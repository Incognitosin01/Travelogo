from django.db import models


class Customer(models.Model):
    c_id = models.FloatField(primary_key=True)
    email = models.CharField(unique=True, max_length=200)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_no = models.FloatField()
    password = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'customer'

    def  __str__(self):
        return f'{self.first_name} {self.last_name}'


class DealLocation(models.Model):
    rating = models.FloatField(blank=True, null=True)
    location_id = models.FloatField(primary_key=True)
    loc_name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=500)

    class Meta:
        managed = True
        db_table = 'deal_location'

    def __str__(self):
        return f'{self.loc_name}'
    
class TravelAgency(models.Model):
    rating = models.FloatField(blank=True, null=True)
    agency_id = models.FloatField(primary_key=True)
    agen_name = models.CharField(max_length=200)
    location = models.ForeignKey(DealLocation, models.DO_NOTHING, blank=True, null=True)
    ph_no = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'travel_agency'


    def  __str__(self):
        return f'{self.agen_name}'
