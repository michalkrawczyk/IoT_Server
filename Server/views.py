from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

# TODO:Order alphabetically
from .models import (
    Category,
    CommandHistory,
    Controller,
    Device,
    Error,
    InputDataHistory,
    Room)

from .serializers import (
    CategorySerializer, CategoryDetailSerializer,
    ControllerAuthSerializer, ControllerUpdateSerializer, ControllerSerializer,
    DeviceSerializer, DeviceChangeControllerSerializer, DeviceDetailSerializer, DeviceUpdateStateSerializer,
    ErrorCreateSerializer, ErrorUpdateSerializer,  ErrorSelectSerializer,
    InputDataSerializer,
    OutputDataSerializer,   # as CommandHistory
    RoomSerializer)


#post update checking if controller has higher priority
##############################
#Category Views

class CategoryDetailAPI(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class CategoryListAPI(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "type"]


##############################
#Controller Views

class ControllerDetailAPI(RetrieveAPIView):
    queryset = Controller.objects.all()
    serializer_class = ControllerSerializer


class ControllerUpdateAPI(UpdateAPIView):
    queryset = Controller.objects.all()
    serializer_class = ControllerUpdateSerializer


class ControllerListAPI(ListAPIView):
    queryset = Controller.objects.all()
    serializer_class = ControllerSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["controller_id", "name", "ip", "priority"]


# TODO: Password Change on Controller with Authentication


##############################
#Device Views

class DeviceChangeControllerAPI(UpdateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceChangeControllerSerializer


class DeviceDetailAPI(RetrieveAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceDetailSerializer


class DeviceListAPI(ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["device_id", "active", "error_state__name", "category__name", "room__name", "controller__name"]


class DeviceUpdateStateAPI(UpdateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceUpdateStateSerializer


##############################
#Error Views

class ErrorCreateAPI(CreateAPIView):
    queryset = Error.objects.all()
    serializer_class = ErrorCreateSerializer


class ErrorDetailAPI(RetrieveAPIView):
    queryset = Error.objects.all()
    serializer_class = ErrorSelectSerializer


class ErrorListAPI(ListAPIView):
    queryset = Error.objects.all()
    serializer_class = ErrorSelectSerializer


class ErrorUpdateAPI(UpdateAPIView):
    queryset = Error.objects.all()
    serializer_class = ErrorUpdateSerializer


##############################
#Input Data Views

class InputDetailAPI(RetrieveAPIView):
    queryset = InputDataHistory.objects.all()
    serializer_class = InputDataSerializer


class InputListAPI(ListAPIView):
    queryset = InputDataHistory.objects.all()
    serializer_class = InputDataSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["device__device_id", "device__name", "datetime"]


##############################
#Output Data Views - Command History

class UsedCommandsListAPI(ListAPIView):
    queryset = CommandHistory.objects.all()
    serializer_class = OutputDataSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["device__device_id", "device__name", "datetime"]


##############################
#Room Views

class RoomDetailAPI(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    # lookup_field = "room_id"


class RoomListAPI(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]


# TODO: Consider Update API's with Authentication
# TODO: Consider SerializerMethodField (for displaying releted fields in proper format)
#  and UpdateRetrieveAPIView for List APIs
