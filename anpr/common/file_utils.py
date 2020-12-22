import xlsxwriter
import PIL.Image as Image
#gsettings set org.gnome.desktop.media-handling automount-open false
import pyudev
import psutil
import os
import logging 

django_dir = os.environ['DJANGOPATH']
logs_dir = os.environ['LOGSPATH']#"/home/"+str(os.environ.get('USER'))+"/logs/"# Directory to store log files and the log file format
if not os.path.exists(logs_dir):# Create Directory if it doesn't exist
    os.makedirs(logs_dir)
logging.basicConfig(filename=logs_dir+"django.log", level=logging.INFO,
    format=("%(asctime)s - %(levelname)s:%(process)d:%(processName)s:%(filename)s - Function Name:%(funcName)s - Line No:%(lineno)d - %(message)s  "))

context = pyudev.Context()

def create_excel(filename, contents, headers):
    removable = [device for device in context.list_devices(subsystem='block', DEVTYPE='disk') if device.attributes.asstring('removable') == "1"]
    if(removable):
        for device in removable:
            partitions = [device.device_node for device in context.list_devices(subsystem='block', DEVTYPE='partition', parent=device)]
            print("All removable partitions: {}".format(", ".join(partitions)))
            print("Mounted removable partitions:")
            for p in psutil.disk_partitions():
                if p.device in partitions:
                    print("  {}: {}".format(p.device, p.mountpoint))
                    #os.copy()
                    print("Excel file saved to",str(p.mountpoint).split('/')[3])

                    # create a new excel and add a worksheet
                    workbook = xlsxwriter.Workbook(str(p.mountpoint)+"/"+filename, {'remove_timezone': True})
                    worksheet = workbook.add_worksheet()

                    # initializing
                    row_index = 0
                    col_index = 0
                    prefix_path = django_dir + "anpr/static/"

                    # writing the headings
                    cell_format = workbook.add_format({"bold": True, "align": "center", "font_size": 15})
                    worksheet.set_row(row_index, None, cell_format)
                    worksheet.write_row(row_index, col_index, headers)
                    row_index += 1

                    # resize cells
                    worksheet.set_default_row(100)
                    worksheet.set_column(0, len(contents[0].keys()) - 2, 30)

                    # writing remianing rows
                    for row_data in contents:
                        data = []
                        for key in row_data.keys():
                            if key != "capture_time" and key!= "image_path" and key!= "full_image":
                                #print(row_data[key])
                                data.append(row_data[key])
                        # writing a row till
                        worksheet.write_row(row_index, col_index, data)

                        # writing the date 
                        date_format = workbook.add_format({"num_format": "dd/mm/yyyy hh:mm:ss"})
                        worksheet.write_datetime(row_index, col_index + len(data), row_data["capture_time"], date_format)

                        # writing the image
                        path = prefix_path+row_data["image_path"]
                        with Image.open(path) as img:
                            img_width, img_height = img.size
                            #print("path",path,"img_width", img_width, "img_height", img_height)
                        x_scale = 30/img_width
                        y_scale = 100/img_height
                        print(worksheet.insert_image(row_index,
                                            col_index + len(data)+1,
                                            path,
                                            {"x_scale": x_scale*7.2,
                                             "y_scale": y_scale*1.5,
                                             "positioning": 1}))
                        row_index += 1
                    workbook.close()
    else:
        print("Insert USB or Try again") 
        logging.warning("INSERT USB OR TRY AGAIN")
