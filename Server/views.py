from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView, RetrieveUpdateAPIView
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

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.exceptions import ValidationError

from .model_utils.PrivateMethods import hash_and_salt


##############################
#Category Views

class CategoryDetailAPI(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class CategoryListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "type"]


##############################
#Controller Views

class ControllerAuthUpdate(UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Controller.objects.all()
    serializer_class = ControllerAuthSerializer

    def perform_update(self, serializer):
        used_salt = serializer.instance.salt
        new_pass = serializer.validated_data['password']
        serializer.save(password=hash_and_salt(used_salt, new_pass))
    #add option with changing if old password is validated?


class ControllerDetailAPI(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Controller.objects.all()
    serializer_class = ControllerSerializer


class ControllerUpdateAPI(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Controller.objects.all()
    serializer_class = ControllerUpdateSerializer


class ControllerListAPI(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Controller.objects.all()
    serializer_class = ControllerSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["controller_id", "name", "ip", "priority"]


##############################
#Device Views

class DeviceChangeControllerAPI(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Device.objects.all()
    serializer_class = DeviceChangeControllerSerializer

    def perform_update(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            old = serializer.instance.controller
            new = serializer.validated_data['controller']
            old_priority = old.priority
            new_priority = new.priority

            if old_priority <= new_priority or old_priority == 0 or old_priority is None:
                serializer.save()
            else:
                raise ValidationError("Higher Priority on Older Controller")


class DeviceDetailAPI(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Device.objects.all()
    serializer_class = DeviceDetailSerializer


class DeviceListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["device_id", "active", "error_state__name", "category__name", "room__name", "controller__name"]


class DeviceUpdateStateAPI(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Device.objects.all()
    serializer_class = DeviceUpdateStateSerializer


##############################
#Error Views

class ErrorCreateAPI(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Error.objects.all()
    serializer_class = ErrorCreateSerializer


class ErrorDetailAPI(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Error.objects.all()
    serializer_class = ErrorSelectSerializer


class ErrorListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Error.objects.all()
    serializer_class = ErrorSelectSerializer


class ErrorUpdateAPI(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Error.objects.all()
    serializer_class = ErrorUpdateSerializer


##############################
#Input Data Views

class InputDetailAPI(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = InputDataHistory.objects.all()
    serializer_class = InputDataSerializer


class InputListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = InputDataHistory.objects.all()
    serializer_class = InputDataSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["device__device_id", "device__name", "datetime"]


##############################
#Output Data Views - Command History

class UsedCommandsListAPI(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = CommandHistory.objects.all()
    serializer_class = OutputDataSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["device__device_id", "device__name", "datetime"]


##############################
#Room Views

class RoomDetailAPI(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]


# TODO: Consider SerializerMethodField (for displaying releted fields in proper format)
#  and UpdateRetrieveAPIView for List APIs
