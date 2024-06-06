from django import forms

from .models import Device, User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "is_active"]


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ["mac_address", "user", "device_type"]
