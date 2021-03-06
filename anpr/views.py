from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.db.models.functions import Length
from django.db.models import Count
import json
import os
import xlsxwriter
import PIL.Image as Image
from .models import LicensePlates, Camera
from .common.validators import is_valid, get_status_date_time
from .common.functional_utils import get_filtered_data
from .common.file_utils import create_excel
from subprocess import Popen
global camname
from datetime import datetime
import logging


django_dir = os.environ['DJANGOPATH']#"/home/user/Django_Anpr-master/" # Directory containing Django manage.py
logs_dir = os.environ['LOGSPATH']#"/home/"+str(os.environ.get('USER'))+"/logs/"# Directory to store log files and the log file format
if not os.path.exists(logs_dir):# Create Directory if it doesn't exist
    os.makedirs(logs_dir)
logging.basicConfig(filename=logs_dir+"django.log", level=logging.INFO,
    format=("%(asctime)s - %(levelname)s:%(process)d:%(processName)s:%(filename)s - Function Name:%(funcName)s - Line No:%(lineno)d - %(message)s  "))
#logging.info("STARTED DJANGO SERVER")


# Create your views here.
#def power_off(request):
#    if request.POST:
#      print("Shutting Down")
#    return render(request,'index.html',{})

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
    #for lp in licensePlates:
    #    lp.image = "anpr/" + lp.image

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
    #print(camera)
    count = LicensePlates.objects.count()
    licensePlates = LicensePlates.objects.filter(camera_number=camera).order_by("-slno")\
    .annotate(text_len=Length('number_plate_number')).filter(text_len__gt=5).filter(text_len__lt=12)[:5]

    #https://books.agiliq.com/projects/django-orm-cookbook/en/latest/distinct.html
    #distinct = LicensePlates.objects.filter(camera_number=camera).values('number_plate_number').distinct()#.order_by("-slno")\
    #.annotate(text_len=Length('number_plate_number')).filter(text_len__gt=5).values('number_plate_number').\
    #annotate(name_count=Count('number_plate_number')).filter(name_count=1)
    #records = User.objects.filter(first_name__in=[item['first_name'] for item in distinct])
    #licensePlates = LicensePlates.objects.filter(camera_number=camera).order_by("-slno")\
    #.annotate(text_len=Length('number_plate_number')).filter(text_len__gt=5).\
    #filter(number_plate_number__in=[item['number_plate_number'] for item in distinct])[:5]#.distinct()[:5]
    #staff = LicensePlates.objects.all().values('number_plate_number').distinct()
    #print(staff.query)
    #for item in staff:
    #	print("ITEM",item)
    #print(staff[:5])
    #ids = licensePlates.values_list('number_plate_number', flat=True).distinct()[:5]																																											
    #print(ids)
    #print("Plates",plates)
    #licensePlates = LicensePlates.objects.filter(camera_number=camera).order_by(
    #    "-slno"
    #)[:5]
    #print(licensePlates)
    #for lp in licensePlates:
    #    lp.image = "anpr/" + lp.image

    return render(
        request, "anpr/latest5.html", {"licensePlates": licensePlates, "count": count}
    )


def plate_search(request):
    # get camera name list for dropdown
    logging.info("Plate Search - Start")
    cameraQuerySet = Camera.objects.all()
    cameras = []
    cam_temp = {}
    cam_temp["id"] = "0"
    cam_temp["name"] = "All"
    cameras.append(cam_temp)
    for camera in cameraQuerySet:
        temp = {}
        temp["id"] = camera.id
        temp["name"] = camera.camera_number
        temp["latitude"] = str(camera.latitude)
        temp["longitude"] = str(camera.longitude)
        cameras.append(temp)

    if request.method == "GET":
        form_data = request.GET
        #print("form_data", form_data)
        if len(form_data.keys()) == 0:
            return render(request, "anpr/plate_search.html", {"cameras": cameras})
            logging.info("Plate Search - End")

        try:
            date_time_availability = get_status_date_time(
                form_data["start_date_time"], form_data["end_date_time"]
            )
            if is_valid(form_data, date_time_availability):
                #print("Searching Records... ")
                #print("Continuous Plate Records")
                license_plates_continous_order_plate_number = get_filtered_data(
                    form_data, date_time_availability, "continuous"
                )
                if form_data["vehicle_no"]:
                    #print("Random Plate Records", form_data["vehicle_no"], len(form_data["vehicle_no"]))
                    license_plate_random_order_plate_number = get_filtered_data(form_data, date_time_availability, "random")
                    license_plates = license_plates_continous_order_plate_number+license_plate_random_order_plate_number
                else:
                    license_plates = license_plates_continous_order_plate_number
                logging.info("Plate Search - End")
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
            logging.error("PLATE SEARCH ERROR:"+str(error))
            logging.info("Plate Search - End")
            return render(
                request, "anpr/plate_search.html", {"error": error, "cameras": cameras,}
            )
    else:
        logging.info("Plate Search - End")
        return HttpResponseBadRequest("Bad Request!")
    logging.info("Plate Search - End")

def generate_EXCEL(request):
    form_data = request.GET
    #print("Generating excel...")
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
        headers = ["Sl. No", "Camera Name", "Plate Number", "Capture Time", "Image"]
        #filename = "vehicles_list.xlsx"
        #print(form_data)
        # get camera name for camera id
        cameras = Camera.objects.all()
        camera_id = form_data['selected_camera']
        if(int(camera_id) == 0):
            camera_name = "All"
        else:
            camera = Camera.objects.get(pk=camera_id)
            camera_name = camera.camera_number
        filename = "Camera-"+camera_name+"-"#+"---PLATENUMBER---"+form_data['vehicle_no']
        if(form_data["start_date_time"]):
            filename = filename + datetime.strptime(form_data["start_date_time"], '%Y-%m-%dT%H:%M').strftime("%d%b%y-%H.%M")
        if(form_data["end_date_time"]):
            filename = filename + "-to-" + datetime.strptime(form_data["end_date_time"], '%Y-%m-%dT%H:%M').strftime("%d%b%y-%H.%M")+ ".xlsx"
        else:
            filename = filename + ".xlsx"    
        #print(form_data['vehicle_no']+"_"+camera_name+"_"+form_data["start_date_time"].replace("T","_")+"_"+form_data["end_date_time"].replace("T","_"))
        create_excel(filename, contents, headers)
    except xlsxwriter.exceptions.FileCreateError as e:
        # For Python 3 use input() instead of raw_input().
        #print("Excel Creation Error",str(e))
        logging.error("EXCEL WRITING ERROR :"+str(e))
        decision = input(
            "Exception caught in workbook.close(): %s\n"
            "Please close the file if it is open in Excel.\n"
            "Try to write file again? [Y/n]: " % e
        )
        return HttpResponseBadRequest(decision)
    except Exception as e:
        logging.error("EXCEL INVALID DATA ERROR :"+str(e))
        #print("Invalid Filter Data")
        return HttpResponseBadRequest("Invalid Filter Data")
    #print("Excel generated successfully.")
    return HttpResponse("Success")
    
    
#from .mjpg_serve import actualConvert
def convertRtspToHttp(request,camera):
    # #print("Passed Camera",camera)
    # try:
    #     pid.kill()
    #     #print("Killed process",pid)
    # except Exception as e:
    #     print("Exception while killing",str(e))
    print("Views Camname", camera)
    #pid = Popen(['python',django_dir+'anpr/mjpg_serve.py',camera])#watch', 'ls'])
    #print("Process id",pid)
    #os.system("python /home/user/mountedSDCard/Django_Anpr-master/anpr/mjpg_serve.py")
    #actualConvert(camera)
    #print("Actually Converted")
    #rtsp://admin:v1ps$123@192.168.1.229:554/Streaming/channels/1/
    return HttpResponse("Success")

            
