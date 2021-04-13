# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone

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
    camera_number = models.CharField(max_length=100, help_text="Name of the Camera. AVOID SPACES IN THE NAME.")
    latitude = models.DecimalField(max_digits=10, decimal_places=7, help_text="Latitude of the Camera Location.")
    longitude = models.DecimalField(max_digits=10, decimal_places=7, help_text="Longitude of the Camera Location.")
    url = models.CharField(max_length=400, help_text="Functioning RTSP link(rtsp://localhost:8554/ds-test) or Path to Local Video(/home/user/vid.mp4)")
    plate_model = models.CharField(max_length=100, default = "T20-FP16",help_text="Name of the Plate Model. Refer to Accuracy Benchmarking Sheet if needed.")
    char_model = models.CharField(max_length=100, default = "chars-ssd",help_text="Name of the Chars Model. Refer to Accuracy Benchmarking Sheet if needed.")
    vid_width = models.IntegerField(default = 1920, help_text="Width of the Video Resolution.")
    vid_height = models.IntegerField(default = 1080, help_text="Heigth of the Video Resolution.")


    plate_threshold = models.DecimalField(max_digits=10, decimal_places=1, default=0.5, help_text="Threshold for Plate Detection.")
    character_threshold = models.DecimalField(max_digits=10, decimal_places=1, default=0.5, help_text="Threshold for Character Detection and Recognition.")
    plate_interval = models.IntegerField(default = 4, help_text="Inference Interval for Plate Detection.")
    roi_y_min = models.IntegerField(default = 0, help_text="ROI_Y Minimum value from Top. Inference will happen only in [(xmin,ymin),(xmax,ymin),(xmin,ymax),(xmax,ymax)]-(Origin at the top left corner).")
    roi_x_min = models.IntegerField(default = 0, help_text="ROI_X Minimum value from Left. Inference will happen only in [(xmin,ymin),(xmax,ymin),(xmin,ymax),(xmax,ymax)]-(Origin at the top left corner).")
    roi_y_max = models.IntegerField(default = 1080, help_text="ROI_Y Maximum value from Top. Inference will happen only in [(xmin,ymin),(xmax,ymin),(xmin,ymax),(xmax,ymax)]-(Origin at the top left corner).")
    roi_x_max = models.IntegerField(default = 1980, help_text="ROI_X Maximum value from Left. Inference will happen only in [(xmin,ymin),(xmax,ymin),(xmin,ymax),(xmax,ymax)]-(Origin at the top left corner).")
    nireq = models.IntegerField(default = 1, help_text="Number of Inference Requests for plate detection. It is usually the number of streams.")
    video_display = models.BooleanField(default=False, help_text="Tick to turn it on. Enables video display with bounding boxes and FPS for debugging purposes. Remember to disable before Deployment.")
    class Meta:
        #managed = True
        db_table = "camera_config"

    def __str__(self):
        return self.camera_number
