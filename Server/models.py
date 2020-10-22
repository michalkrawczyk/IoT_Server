from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from model_utils import Choices
from datetime import timedelta
from Server.model_utils.CustomMethods import generate_random_string


class Controller(models.Model):
    controller_id = models.SmallAutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=100, default="Unnamed")
    ip = models.GenericIPAddressField(verbose_name="IP Address", help_text="IPv4 or IPv6 as String")  # change to mac address?
    priority = models.PositiveSmallIntegerField(unique=True)
    password = models.CharField(max_length=200)

    salt = models.CharField(max_length=10, unique=True, default=generate_random_string(5))

    def __str__(self):
        return "{}:{}[{}]".format(self.controller_id, self.ip, self.priority)

    class Meta:
        verbose_name_plural = "4. Controllers"
        ordering = ['-priority']


class Room(models.Model):
    # Describes where's device
    room_id = models.SmallAutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=100, verbose_name="Room")
    room_channel = models.CharField(max_length=100, null=True, blank=True,
                                    help_text="In case of MQTT channels for each room")

    def __str__(self):
        return "{}:{} - channel: {}".format(self.room_id, self.name, self.room_channel)

    class Meta:
        verbose_name_plural = "3. Rooms"


class Category(models.Model):
    # Describes device's category - That allows to take proper calculation set for each device type
    category_id = models.SmallAutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=100, verbose_name="Category Name")

    TYPES = Choices("In", "Out", "I/O")
    type = models.CharField(max_length=3, choices=TYPES)

    related_group = models.CharField(max_length=100, default="None",
                                     help_text="Tells Interpreter how should threat devices from that category")

    def __str__(self):
        return "{}:[{}]{}".format(self.category_id, self.type, self.name)

    class Meta:
        verbose_name_plural = "2. Categories"


class Error(models.Model):
    error_id = models.SmallAutoField(primary_key=True, verbose_name="Error Code")
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{}:{}".format(self.error_id, self.name)

    class Meta:
        verbose_name_plural = "{ Errors }"


class Device(models.Model):
    device_id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=100)

    active = models.BooleanField(default=False,
                                 verbose_name="Is Active",
                                 help_text="Is Device Turned On?")
    error_state = models.ForeignKey(Error, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                                    verbose_name="Error Code",
                                    help_text="0 if working without any error")

    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 help_text="What is category of this device (e.g. RGB Lamp)?")
    room = models.ForeignKey(Room,
                             on_delete=models.SET_NULL,
                             help_text="In which room is this device?", null=True, blank=True)
    controller = models.ForeignKey(Controller, on_delete=models.SET_NULL, null=True, blank=True, default=None,
                                   help_text="Who is now controlling that device?")

    def __str__(self):
        active_str = "Active" if self.active else "Deactivated"
        return "{}:{}[{}]".format(self.device_id, self.name, active_str)

    class Meta:
        verbose_name_plural = "1. Devices"


class InputDataHistory(models.Model):
    data_id = models.BigAutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    data = models.CharField(max_length=50)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = "[History] Data received from Input Devices"


class CommandHistory(models.Model):
    command_id = models.BigAutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    command = models.CharField(max_length=50)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = "[History] Commands for Output Devices"


class ControllerHistory(models.Model):
    request_id = models.BigAutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    controller = models.ForeignKey(Controller, on_delete=models.SET_NULL, null=True)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    timeout = models.DurationField(default=timedelta(seconds=10.0), null=True, help_text="Timeout in microseconds")

    class Meta:
        verbose_name_plural = "[History] Requests to control devices"


@receiver(post_save, sender=Controller)
def salt_update(sender, instance, created, **kwargs):
    if created:
        instance.salt = "{}{}".format(instance.salt, instance.controller_id)
        instance.save()
