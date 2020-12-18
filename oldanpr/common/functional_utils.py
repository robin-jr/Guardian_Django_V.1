from ..models import Camera, LicensePlates
from django.utils.timezone import make_aware
import pytz

def get_filtered_data(form_data, date_time_availability, criteria_order):
    license_plates = []
    plate_number = form_data['vehicle_no']
    camera_id = form_data['selected_camera']

    # get camera name for camera id
    cameras = Camera.objects.all()
    print(cameras.count(),camera_id)
    if(int(camera_id) == 0):
        camera_name = "All"
    else:
        camera = Camera.objects.get(pk=camera_id)
        camera_name = camera.camera_number
    print("camera_name", camera_name)

    # convert naive datetime object(without timezone info) to datetime object(with timezone info)
    if "naive_start_date_time" in date_time_availability.keys():
        start_date_time = make_aware(date_time_availability["naive_start_date_time"]) 
        print("aware_start_date_time", start_date_time)
    if "naive_end_date_time" in date_time_availability.keys():
        end_date_time = make_aware(date_time_availability["naive_end_date_time"])
        print("aware_end_date_time", end_date_time)

    # filtering data based on criteria
    if (camera_name == "All"):
        license_plate_queryset_by_camera_name = LicensePlates.objects.all()
    else:
        license_plate_queryset_by_camera_name = LicensePlates.objects.filter(camera_number=camera_name)
    print("license_plate_queryset_by_camera_name",len(license_plate_queryset_by_camera_name), license_plate_queryset_by_camera_name)
    if criteria_order == "continuous":
        queryset_further_by_plate_number = license_plate_queryset_by_camera_name.filter(number_plate_number__icontains=plate_number)
        print("queryset_further_by_plate_number",len(queryset_further_by_plate_number), queryset_further_by_plate_number)
    else:
        queryset_further_by_plate_number = license_plate_queryset_by_camera_name.exclude(number_plate_number__icontains=plate_number)
        print("queryset_further_by_plate_number",len(queryset_further_by_plate_number), queryset_further_by_plate_number)
    if date_time_availability["status"] == "start_and_end":
        final_license_plate_query_set = queryset_further_by_plate_number.filter(date__gte=start_date_time, date__lte=end_date_time)
        print("final_license_plate_query_set", len(final_license_plate_query_set), final_license_plate_query_set)
    elif  date_time_availability["status"] == "start": 
        final_license_plate_query_set = queryset_further_by_plate_number.filter(date__gte=start_date_time)
        print("final_license_plate_query_set", len(final_license_plate_query_set), final_license_plate_query_set)
    elif date_time_availability["status"] == "end":
        final_license_plate_query_set = queryset_further_by_plate_number.filter(date__lte=end_date_time)
        print("final_license_plate_query_set", len(final_license_plate_query_set), final_license_plate_query_set)
    elif date_time_availability["status"] == "none":
        final_license_plate_query_set = queryset_further_by_plate_number

    oredered_final_license_plate_query_set = final_license_plate_query_set.order_by("-date")

    for lp in oredered_final_license_plate_query_set:
        temp_lp = {}
        temp_lp["slno"] = lp.slno
        temp_lp["camera_name"] = lp.camera_number
        temp_lp["capture_time"] = lp.date.astimezone(pytz.timezone("Asia/Kolkata"))
        print("lp.date", lp.slno, lp.number_plate_number, temp_lp["capture_time"])
        temp_lp["plate_number"] = lp.number_plate_number
        temp_lp["image_path"] = "anpr/" + lp.image
        temp_lp["fullimage"] = lp.fullimage
        if criteria_order == "continuous":
            license_plates.append(temp_lp)
        else:
            for index, char in enumerate(plate_number):
                if char.upper() in temp_lp["plate_number"]:
                    if index == len(plate_number)-1:
                        license_plates.append(temp_lp)
                else:
                    break

    print(len(license_plates))
    return license_plates
