from django.urls import path
from .views import (
    CategoryDetailAPI, CategoryListAPI,
    ControllerUpdateAPI, ControllerDetailAPI, ControllerListAPI,
    DeviceChangeControllerAPI, DeviceDetailAPI, DeviceListAPI, DeviceUpdateStateAPI,
    ErrorCreateAPI, ErrorDetailAPI, ErrorListAPI, ErrorUpdateAPI,
    InputDetailAPI, InputListAPI,
    UsedCommandsListAPI,    # for Command History
    RoomDetailAPI, RoomListAPI

)
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "IoT_Server"

urlpatterns = [
    path('category=<pk>/detail', CategoryDetailAPI.as_view(), name="Category Details"),
    path('categories', CategoryListAPI.as_view(), name='Available Categories'),

    path('controller=<pk>/update', ControllerUpdateAPI.as_view(), name='Controller Update'),
    path('controller=<pk>/detail', ControllerDetailAPI.as_view(), name='Controller Details'),
    path('controllers/', ControllerListAPI.as_view(), name='Available Controllers'),

    path('device=<pk>/control_change', DeviceChangeControllerAPI.as_view(), name='Change Control on Device'),
    path('device=<pk>/detail', DeviceDetailAPI.as_view(), name='Device Details'),
    path('device=<pk>/update', DeviceUpdateStateAPI.as_view(), name='Update State of Device'),
    path('devices/', DeviceListAPI.as_view(), name='List of Devices'),

    path('error/create', ErrorCreateAPI.as_view(), name='Create New Error'),
    path('error=<pk>/detail', ErrorDetailAPI.as_view(), name='Error Details'),
    path('error=<pk>/update', ErrorUpdateAPI.as_view(), name='Update Error Description'),
    path('errors/', ErrorListAPI.as_view(), name='List of Errors'),

    path('input=<pk>/detail/', InputDetailAPI.as_view(), name='Input Data Details'),
    path('inputs/', InputListAPI.as_view(), name='Input Data History'),

    path('outputs/', UsedCommandsListAPI.as_view(), name='Output Commands History'),

    path('room=<pk>/detail/', RoomDetailAPI.as_view(), name='Room Details'),
    path('rooms/', RoomListAPI.as_view(), name='Available Rooms'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
