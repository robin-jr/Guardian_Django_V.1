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
        #managed = True
        db_table = "license_plates"

    def __str__(self):
        return self.number_plate_number


class Camera(models.Model):
    id = models.AutoField(primary_key=True)
    camera_number = models.CharField(max_length=100, help_text="Name of the Camera.")
    latitude = models.DecimalField(max_digits=10, decimal_places=7, help_text="Latitude of the Camera Location.")
    longitude = models.DecimalField(max_digits=10, decimal_places=7, help_text="Longitude of the Camera Location.")
    url = models.CharField(max_length=400, help_text="Functioning RTSP link(rtsp://localhost:8554/ds-test) or Path to Local Video(/home/user/vid.mp4.")
    plate_threshold = models.DecimalField(max_digits=10, decimal_places=1, default=0.5, help_text="Threshold for Plate Detection.")
    character_threshold = models.DecimalField(max_digits=10, decimal_places=1, default=0.5, help_text="Threshold for Character Detection and Recognition.")
    plate_interval = models.IntegerField(default = 4, help_text="Inference Interval for Plate Detection")
    roi_y = models.IntegerField(default = 540, help_text="ROI_Y value from Top. Ex: 680 for (1920,1080)-> Inference will happen only in (0,1080-680) to (1920,1080-680) = (0,400) to (1920,400)")
    roi_x = models.IntegerField(default = 640, help_text="ROI_X value from Left. Ex: 920 for (1920,1080)-> Inference will happen only in (920,0) to (1920,0)")
    nireq = models.IntegerField(default = 1, help_text="Number of Inference Requests for plate detection. It is usually the number of streams.")
    video_display = models.BooleanField(default=False, help_text="Tick to turn it on. Enables video display with bounding boxes and FPS for debugging purposes. Remember to disable before Deployment.")
    class Meta:
        db_table = "camera_config"

    def __str__(self):
        return self.camera_number
