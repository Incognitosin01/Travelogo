from django.db import models

class Customer(models.Model):
    email_id = models.CharField(max_length=50)
    customer_id = models.FloatField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone_no = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
