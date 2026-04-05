from django.urls import path
from prediction.views import index, predict

urlpatterns = [
    path("", index, name="index"),
    path("predict/", predict, name="predict"),
]
