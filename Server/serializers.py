from .models import (
    Category,
    CommandHistory,
    Controller,
    Device,
    Error,
    InputDataHistory,
    Room)
from rest_framework.serializers import ModelSerializer, SerializerMethodField
# TODO:Order alphabetically

##############################
#Category Serializers


class CategoryDetailSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_id", "name", "type", "related_group"]


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_id", "name", "type"]


##############################
#CommandHistory Serializers


class OutputDataSerializer(ModelSerializer):
    # for Automatic Controllers
    class Meta:
        model = CommandHistory
        fields = ["device", "data", "datetime"]


##############################
#Controller Serializers


class ControllerAuthSerializer(ModelSerializer):
    class Meta:
        model = Controller
        fields = ["controller_id", "priority", "password"]


class ControllerUpdateSerializer(ModelSerializer):
    class Meta:
        model = Controller
        fields = ["name", "ip"]


class ControllerSerializer(ModelSerializer):
    class Meta:
        model = Controller
        fields = ["controller_id", "name", "ip", "priority"]


# TODO: Add Serializer for updating only password on Controller with Authentication
##############################
#Device Serializers

class DeviceChangeControllerSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = ["controller"]


class DeviceDetailSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = ["device_id", "name", "active", "error_state", "category", "room", "controller"]


class DeviceUpdateStateSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = ["active", "error_state"]


class DeviceSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = ["device_id", "name", "active", "error_state", "room"]


##############################
#Error Serializers

class ErrorCreateSerializer(ModelSerializer):
    class Meta:
        model = Error
        fields = ["name", "description"]


class ErrorUpdateSerializer(ModelSerializer):
    class Meta:
        model = Error
        fields = ["description"]


class ErrorSelectSerializer(ModelSerializer):
    class Meta:
        model = Error
        fields = ["error_id", "name", "description"]

##############################
#InputDataHistory Serializers


class InputDataSerializer(ModelSerializer):
    class Meta:
        model = InputDataHistory
        fields = ["device", "data", "datetime"]

##############################
# Room Serializers


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ["room_id", "name"]


# ControllerHistory only for main server

