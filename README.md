# Django_ANPR

Steps to install:

1) git clone https://github.com/Sharan-Sundar/Django_Anpr.git

2) Change db configuration in arima > settings.py   
DATABASES = {  
&nbsp;&nbsp;&nbsp;&nbsp;"default": {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"ENGINE": "django.db.backends.mysql",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"NAME": \<your db name>,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"HOST": "localhost",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"USER": \<your mysql username>,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"PASSWORD": \<your mysql password>,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"PORT": "3306",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"OPTIONS": {"init_command": "SET default_storage_engine=INNODB",},  
&nbsp;&nbsp;}  
  }  
Note: The above configuration is for mysql. Config will change wrt DB engine used.

3) Request for the static file zip and replace existing anpr > static folder

## Parameters

1. Latest5 - Refreshes every 2 seconds