from django.urls import path

from . import views

app_name = "anpr"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:camera>/latest/", views.latest5, name="latest"),
    path("platesearch/", views.plate_search, name="plate_search"),
    path("platesearch/pdf", views.generate_EXCEL, name="generate_excel"),
    path("<str:camera>/convert/", views.convertRtspToHttp, name="convert"),
]
