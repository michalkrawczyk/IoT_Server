from django.contrib import admin
from django.contrib.auth.models import Group
# Register your models here.

from .models import (
    Controller,
    Room,
    Category,
    Error,
    Device,
    InputDataHistory,
    CommandHistory,
    ControllerHistory
)


class ControllerAdmin(admin.ModelAdmin):
    list_display = ["controller_id", "name", "ip", "priority"]
    list_display_links = ["controller_id", "name"]
    readonly_fields = ["controller_id"]
    fieldsets = (
        (None, {"fields": (
            "controller_id",
            "ip",
            "password",
                    )
                }),
        ("Advanced", {"fields": (
            "salt",
            "priority"
        ), "classes": ["collapse"]
        })
    )
    search_fields = ["ip", "name"]

    def set(self, obj):
        return obj.set
    set.admin_order_field = ["controller_id", "ip", "priority"]


class RoomAdmin(admin.ModelAdmin):
    readonly_fields = ["room_id"]
    fieldsets = (
        (None, {"fields": (
            "room_id",
            "name"
        )
        }),
        ("Optional (MQTT)", {"fields": (
            "room_channel",
        )
        })
    )
    search_fields = ["room_id", "name", "room_channel"]


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ["category_id"]
    list_filter = ["category_id", "type"]
    search_fields = ["category_id", "name"]


class ErrorAdmin(admin.ModelAdmin):
    search_fields = ["error_id", "name"]


class DeviceAdmin(admin.ModelAdmin):
    list_display = ["device_id", "name", "active", "error_state", "category", "room", "controller"]
    list_display_links = ["name", "error_state", "category", "room", "controller"]
    list_filter = ("active", "category", "room", "controller", "error_state")
    readonly_fields = ["device_id"]
    fieldsets = (
        (None, {"fields": (
            "device_id",
            "name"
        )
        }),
        ("Classification Settings", {"fields": (
            "category",
            "room"
        )
        }),
        ("Activity", {"fields": (
            "active",
            "error_state",
            "controller",
        ),
            "classes": ["collapse"]
        })
    )
    search_fields = ["device_id", "name"]


class InputDataAdmin(admin.ModelAdmin):
    list_display = ["data_id", "device", "data", "datetime"]
    readonly_fields = ["data_id", "device", "data", "datetime"]
    list_display_links = ["data_id", "device"]
    list_filter = ["device", "datetime"]


class OutputDataAdmin(admin.ModelAdmin):
    list_display = ["command_id", "device", "command", "datetime"]
    readonly_fields = ["command_id", "device", "command", "datetime"]
    list_display_links = ["command_id", "device"]
    list_filter = ["device", "datetime"]


class ControllerHistoryAdmin(admin.ModelAdmin):
    list_display = ["request_id", "device", "controller", "datetime", "timeout"]
    readonly_fields = ["request_id", "device", "controller", "datetime", "timeout"]
    list_display_links = ["request_id", "device", "controller"]
    list_filter = ["device", "controller", "datetime"]


admin.site.site_header = "IoT Server - Admin Panel"

admin.site.register(Controller, ControllerAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Error, ErrorAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(InputDataHistory, InputDataAdmin)
admin.site.register(CommandHistory, OutputDataAdmin)
admin.site.register(ControllerHistory, ControllerHistoryAdmin)

admin.site.unregister(Group)
