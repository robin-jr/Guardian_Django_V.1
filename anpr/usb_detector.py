import os
import pyudev
import subprocess
import psutil

context = pyudev.Context()

removable = []
for device in context.list_devices(subsystem='block', DEVTYPE='disk'):# if device.attributes.asstring('removable') == "1"]
    try:
        device_parent = device.parent.device_path
        if("usb" in device_parent):
            print(device.sys_name,device.device_type,device.time_since_initialized,device.parent.device_path)#.attributes.asstring('time_since_initialized'))#)
            removable.append(device)
    except Exception as e:
        print("Exception : ",str(e))
        continue    

#removable = [device for device in context.list_devices(subsystem='block', DEVTYPE='disk')if device.attributes.asstring('removable') == "1"]

if(removable):
    for device in removable:
        print("Removable Device:",device)
        partitions = [device.device_node for device in context.list_devices(subsystem='block', DEVTYPE='partition', parent=device)]
        print("All removable partitions: {}".format(", ".join(partitions)))
        print("Mounted removable partitions:")
        for p in psutil.disk_partitions():
            if p.device in partitions:
                print("  {}: {}".format(p.device, p.mountpoint))