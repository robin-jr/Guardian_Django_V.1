# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class LicensePlates(models.Model):
    slno = models.AutoField(primary_key=True)
    camera_number = models.CharField(max_length=100)
    number_plate_number = models.CharField(max_length=50)
    image = models.CharField(max_length=100)
    date = models.DateTimeField()
    fullimage = models.CharField(max_length=100)

    class Meta:
        #managed = False
        db_table = "license_plates"

    def __str__(self):
        return self.number_plate_number


class Camera(models.Model):
    id = models.AutoField(primary_key=True)
    camera_number = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    url = models.CharField(max_length=100)
    

    class Meta:
        db_table = "camera_config"

    def __str__(self):
        return self.camera_number
