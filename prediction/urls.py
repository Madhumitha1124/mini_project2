from django.urls import path
from .views import index, predict, soil_analysis, soil_recommendation_api, advanced_soil_analysis, get_weather_api, get_market_data_api

urlpatterns = [
    path('', index, name='index'),
    path('predict/', predict, name='predict'),
    path('soil-analysis/', soil_analysis, name='soil_analysis'),
    path('api/soil-recommendations/', soil_recommendation_api, name='soil_recommendation_api'),
    path('api/weather/', get_weather_api, name='get_weather_api'),
    path('api/market-data/', get_market_data_api, name='get_market_data_api'),
    path('advanced-soil-analysis/', advanced_soil_analysis, name='advanced_soil_analysis'),
]
