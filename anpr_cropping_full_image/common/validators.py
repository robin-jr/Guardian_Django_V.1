from datetime import datetime

LICENSE_PLATE_CHAR_LIMIT = 11

def is_valid(form_data, date_time_availability):
    if len(form_data["vehicle_no"]) > LICENSE_PLATE_CHAR_LIMIT:
        raise Exception("VEHICLE_NO_INVALID")
    
    if date_time_availability["status"] == "start_and_end":
        if date_time_availability["naive_start_date_time"] > date_time_availability["naive_end_date_time"]:
            raise Exception("DATE_TIME_RANGE_INVALID")
    return True

def get_status_date_time(start_date_time_str, end_date_time_str):
    date_time_availability = {}
    if len(start_date_time_str) > 0 and len(end_date_time_str) > 0:
        date_time_availability["status"] = "start_and_end"
        # convert date_time string to python date_time format
        date_time_availability["naive_start_date_time"] = datetime.strptime(start_date_time_str, '%Y-%m-%dT%H:%M')
        date_time_availability["naive_end_date_time"] = datetime.strptime(end_date_time_str, '%Y-%m-%dT%H:%M')
    elif len(start_date_time_str) > 0:
        date_time_availability["status"] = "start"
        date_time_availability["naive_start_date_time"] = datetime.strptime(start_date_time_str, '%Y-%m-%dT%H:%M')
    elif len(end_date_time_str) > 0:
        date_time_availability["status"] = "end"
        date_time_availability["naive_end_date_time"] = datetime.strptime(end_date_time_str, '%Y-%m-%dT%H:%M')
    else:
        date_time_availability["status"] = "none"
    print("date_time_availability", date_time_availability)
    return date_time_availability