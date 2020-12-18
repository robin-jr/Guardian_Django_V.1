from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
import json

from .models import LicensePlates, Camera
from .common.validators import is_valid, get_status_date_time
from .common.functional_utils import get_filtered_data
from .common.file_utils import create_excel

# Create your views here.


def index(request):
    cameraQuerySet = Camera.objects.all()
    cameras = []
    for cam in cameraQuerySet:
        temp = {}
        temp["id"] = cam.id
        temp["camera_number"] = cam.camera_number
        temp["latitude"] = str(cam.latitude)
        temp["longitude"] = str(cam.longitude)
        temp["url"] = cam.url
        cameras.append(temp)

    count = LicensePlates.objects.count()

    licensePlates = LicensePlates.objects.filter(
        camera_number=cameras[0]["camera_number"]
    ).order_by("-slno")[:5]
    for lp in licensePlates:
        lp.image = "anpr/" + lp.image

    return render(
        request,
        "anpr/index.html",
        {
            "count": count,
            "licensePlates": licensePlates,
            "cameraJSON": json.dumps(cameras),
            "cameras": cameras,
            "selectedCamera": cameras[0],
        },
    )


def latest5(request, camera):
    print(camera)
    count = LicensePlates.objects.count()
    licensePlates = LicensePlates.objects.filter(camera_number=camera).order_by(
        "-slno"
    )[:5]
    for lp in licensePlates:
        lp.image = "anpr/" + lp.image

    return render(
        request, "anpr/latest5.html", {"licensePlates": licensePlates, "count": count}
    )


def plate_search(request):
    # get camera name list for dropdown
    cameraQuerySet = Camera.objects.all()
    cameras = []
    t = {}
    t["id"] = "0"
    t["name"] = "All"
    cameras.append(t)
    for camera in cameraQuerySet:
        temp = {}
        temp["id"] = camera.id
        temp["name"] = camera.camera_number
        temp["latitude"] = str(camera.latitude)
        temp["longitude"] = str(camera.longitude)
        cameras.append(temp)

    if request.method == "GET":
        form_data = request.GET
        print("form_data", form_data)
        if len(form_data.keys()) == 0:
            return render(request, "anpr/plate_search.html", {"cameras": cameras,})
        try:
            date_time_availability = get_status_date_time(
                form_data["start_date_time"], form_data["end_date_time"]
            )
            if is_valid(form_data, date_time_availability):
                print("Searching Records... ")
                print("Continuous Plate Records")
                license_plates_continous_order_plate_number = get_filtered_data(
                    form_data, date_time_availability, "continuous"
                )
                print("Random Plate Records")
                license_plate_random_order_plate_number = get_filtered_data(
                    form_data, date_time_availability, "random"
                )
                license_plates = (
                    license_plates_continous_order_plate_number
                    + license_plate_random_order_plate_number
                )
                return render(
                    request,
                    "anpr/plate_search.html",
                    {
                        "license_plates": license_plates,
                        "cameras": cameras,
                        "cameraJSON": json.dumps(cameras),
                        "filter_conditions": form_data,
                    },
                )
        except Exception as e:
            if e.args[0] == "VEHICLE_NO_INVALID":
                print("Invalid Data")
                error = "Vehicle No exists the char limit."
            elif e.args[0] == "DATE_TIME_RANGE_INVALID":
                print("Invalid Data")
                error = "Start Date/Time is greater than End Date/Time."
            else:
                print("error", e.args[0])
                error = "Oops! Something went wrong."

            return render(
                request, "anpr/plate_search.html", {"error": error, "cameras": cameras,}
            )
    else:
        return HttpResponseBadRequest("Bad Request!")


def generate_EXCEL(request):
    form_data = request.GET
    print("form_data", form_data)
    print("Generating excel...")
    try:
        date_time_availability = get_status_date_time(
            form_data["start_date_time"], form_data["end_date_time"]
        )
        if is_valid(form_data, date_time_availability):
            license_plates_continous_order_plate_number = get_filtered_data(
                form_data, date_time_availability, "continuous"
            )
            license_plate_random_order_plate_number = get_filtered_data(
                form_data, date_time_availability, "random"
            )
            contents = (
                license_plates_continous_order_plate_number
                + license_plate_random_order_plate_number
            )
        print("len(contents)", len(contents))
        headers = ["Sl. No", "Camera Name", "Plate Number", "Capture Time", "Image"]
        filename = "vehicle_lists.xlsx"
        create_excel(filename, contents, headers)
    except xlsxwriter.exceptions.FileCreateError as e:
        # For Python 3 use input() instead of raw_input().
        print("Excel Creation Error")
        decision = raw_input(
            "Exception caught in workbook.close(): %s\n"
            "Please close the file if it is open in Excel.\n"
            "Try to write file again? [Y/n]: " % e
        )
        return HttpResponseBadRequest(decision)
    except Exception as e:
        print("Invalid Filter Data")
        return HttpResponseBadRequest("Invalid Filter Data")
    print("Excel generated successfully.")
    return HttpResponse("Success")
