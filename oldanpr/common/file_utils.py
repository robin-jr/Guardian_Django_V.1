from PIL import Image
import xlsxwriter
import io

def get_resized_image_data(file_path, bound_width_height):
    # get the image and resize it
    im = Image.open(file_path)
    im.thumbnail(bound_width_height, Image.ANTIALIAS)  # ANTIALIAS is important if shrinking

    # stuff the image data into a bytestream that excel can read
    im_bytes = io.BytesIO()
    im.save(im_bytes, format='PNG')
    return im_bytes

def create_excel(filename, contents, headers):
    # create a new excel and add a worksheet
    workbook = xlsxwriter.Workbook(filename, {'remove_timezone': True})
    worksheet = workbook.add_worksheet()

    # initializing
    row_index = 0
    col_index = 0
    prefix_path = "/home/god2/dproject/django_env/latest_arima/arima/anpr/static/"

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
            if key != "capture_time" and key!= "image_path" and key!= "fullimage":
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
            print("path",path,"img_width", img_width, "img_height", img_height)
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
