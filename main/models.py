from django.db import models


# Create your models here.

class Hospitals(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    hospital_name = models.TextField(blank=True, null=True)
    n95_weekly_volume = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'Hospitals'
