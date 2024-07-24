from django import forms
from django.forms import ModelForm, TextInput, EmailInput, Select, NumberInput
from .models import UserRegisterModel
from phonenumber_field.widgets import RegionalPhoneNumberWidget


class RegistrationForm(ModelForm):
    class Meta:
        model = UserRegisterModel
        fields = [
            "name",
            "surname",
            "email",
            "phone_number",
            "season_type",
            "season_number",
        ]

        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Atabek",
                    "required": "true",
                    "id": "name",
                }
            ),
            "surname": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Abduakimov",
                    "required": "true",
                    "id": "surname",
                }
            ),
            "email": EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "you@example.com",
                    "required": "true",
                    "id": "email",
                }
            ),
            "season_number": NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Please write your number of season",
                    "required": "true",
                    "id": "season_number",
                }
            ),
            "season_type": Select(
                attrs={
                    "class": "form-season",
                    "id": "season_type",
                    "placeholder": "Please write your season",
                    "required": "true",
                }
            ),
            "phone_number": RegionalPhoneNumberWidget(
                attrs={
                    "class": "form-control",
                    "placeholder": "+998 (**) ** ** ***",
                    "id": "phone_number",
                    "required": "true",
                },
                region="UZ",
            ),
        }
