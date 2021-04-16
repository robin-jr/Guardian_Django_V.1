#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging

logs_dir = os.environ['LOGSPATH']#"/home/"+str(os.environ.get('USER'))+"/logs/"# Directory to store log files and the log file format
if not os.path.exists(logs_dir):# Create Directory if it doesn't exist
    os.makedirs(logs_dir)
logging.basicConfig(filename=logs_dir+"django.log", level=logging.INFO,
    format=("%(asctime)s - %(levelname)s:%(process)d:%(processName)s:%(filename)s - Function Name:%(funcName)s - Line No:%(lineno)d - %(message)s  "))


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arima.settings')
    try:
        from django.core.management import execute_from_command_line
        logging.info("STARTED DJANGO SERVER")
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    logging.error("Django Server Shutdown either manually or due to improper installation of Django - could not import Django.")


if __name__ == '__main__':
    main()
