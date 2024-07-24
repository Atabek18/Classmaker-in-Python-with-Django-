from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import (
    AvailabilityModel,
    AttemptsModel,
    RestrictionsModel,
    Print_copy_paste_translateModel,
    DisplayEachQuestionModel,
    InstructionModel,
    LimitTimeModel,
    ResultsPageModel,
    PassMarkAndFeedbackModel,
    EmailResultsInstructorModel,
    TakerEmailSendModel,
    AssignLinkModel,
    NUMBER_CHOICES,
)
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class AvailabilityModelForm(forms.ModelForm):
    class Meta:
        model = AvailabilityModel
        fields = [
            "unavailable",
            "available",
            "start_date",
            "start_time",
            "end_date",
            "end_time",
        ]

    available = forms.BooleanField(
        label="Available", widget=forms.CheckboxInput(), initial=True
    )
    unavailable = forms.BooleanField(
        label="Unavailable", widget=forms.CheckboxInput(), required=False
    )
    start_date = forms.DateField(label="", widget=DatePickerInput(), required=False)
    end_date = forms.DateField(
        label="", widget=DatePickerInput(range_from="start_date"), required=False
    )
    start_time = forms.TimeField(
        label="", widget=TimePickerInput(options={"format": "hh:mm A"}), required=False
    )
    end_time = forms.TimeField(
        label="", widget=TimePickerInput(options={"format": "hh:mm A"}), required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_time"].widget.attrs["timezone"] = "Asia/Tashkent"
        self.fields["end_time"].widget.attrs["timezone"] = "Asia/Tashkent"


class AttemptsModelForm(forms.ModelForm):
    class Meta:
        model = AttemptsModel
        fields = "__all__"

    attempts = forms.IntegerField(
        validators=[MinValueValidator(0)], required=False, initial=1
    )
    unlimited = forms.BooleanField(required=False)


class RestrictionsModelForm(forms.ModelForm):
    class Meta:
        model = RestrictionsModel
        fields = "__all__"

    password = forms.CharField(
        label="",
        required=False,
        widget=forms.PasswordInput(attrs={"class": "restrict-class"}),
    )


class Print_copy_paste_translateModelForm(forms.ModelForm):
    class Meta:
        model = Print_copy_paste_translateModel
        fields = "__all__"

    allow_print = forms.BooleanField(required=False)
    allow_copy = forms.BooleanField(required=False)
    allow_paste = forms.BooleanField(required=False)
    allow_translation = forms.BooleanField(required=False)


class LimitTimeModelForm(forms.ModelForm):
    minute = forms.IntegerField(
        initial=0,
        validators=[MinValueValidator(0), MaxValueValidator(1440)],
        widget=forms.NumberInput(attrs={"class": "limit-class", "required": "true"}),
        required=True,
        label="",
    )

    class Meta:
        model = LimitTimeModel
        fields = ["minute"]

    def __init__(self, *args, **kwargs) -> None:
        super(LimitTimeModelForm, self).__init__(*args, **kwargs)

        if "instance" in kwargs and kwargs["instance"] is not None:
            minute = kwargs["instance"].minute
            if minute:
                if minute >= 0:
                    self.fields["minute"].initial = int(minute)
                else:
                    self.fields["minute"].initial = 0
        else:
            self.fields["minute"].initial = 0


class DisplayEachQuestionModelForm(forms.ModelForm):
    class Meta:
        model = DisplayEachQuestionModel
        fields = ["selected_number", "randomize", "must_answer"]

    selected_number = forms.ChoiceField(choices=NUMBER_CHOICES, widget=forms.Select())
    randomize = forms.BooleanField(required=False)
    must_answer = forms.BooleanField(initial=True)


class PassMarkAndFeedbackModelForm(forms.ModelForm):
    class Meta:
        model = PassMarkAndFeedbackModel
        fields = ["pass_mark", "send_completed_message", "send_not_completed_message"]

    pass_mark = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        widget=forms.NumberInput(attrs={"class": "pass-mark-stp"}),
        label="",
        required=True,
    )
    send_completed_message = CKEditorUploadingWidget()
    send_not_completed_message = CKEditorUploadingWidget()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["send_completed_message"].required = False
        self.fields["send_not_completed_message"].required = False
        self.fields["send_completed_message"].label = ""
        self.fields["send_not_completed_message"].label = ""


class InstructionModelForm(forms.ModelForm):
    class Meta:
        model = InstructionModel
        fields = "__all__"

    pre_test_guidelines = forms.BooleanField(
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "pre-test-guidelines"}),
    )


class EmailResultsInstructorModelForm(forms.ModelForm):
    class Meta:
        model = EmailResultsInstructorModel
        fields = "__all__"

    off = forms.BooleanField(initial=True, required=False)
    score = forms.BooleanField(required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "creator-email"}))


class ResultsPageModelForm(forms.ModelForm):
    class Meta:
        model = ResultsPageModel
        fields = "__all__"

    points = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "res-point"})
    )
    persentage = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "res-persentage"})
    )
    feedback = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "res-feedback"})
    )
    reveal_correct_answers = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "res-reveal"})
    )


class TakerEmailSendModelForm(forms.ModelForm):
    class Meta:
        model = TakerEmailSendModel
        fields = "__all__"

    point = forms.BooleanField(required=False)
    percentage = forms.BooleanField(required=False)
    feedback = forms.BooleanField(required=False)
    graded = forms.BooleanField(required=False)
    reveal_correct_answers = forms.BooleanField(required=False)


class AssignLinkModelForm(forms.ModelForm):
    class Meta:
        model = AssignLinkModel
        fields = ["assign_name"]

    assign_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "assign-name-input",
                "placeholder": "Assign name ...",
            }
        ),
        required=False,
        label="",
    )

    def __init__(self, *args, **kwargs) -> None:
        super(AssignLinkModelForm, self).__init__(*args, **kwargs)
        if "instance" in kwargs and kwargs["instance"] is not None:
            assign_name = kwargs["instance"].assign_name
            if assign_name:
                self.fields["assign_name"].required = False
                self.fields["assign_name"].widget.attrs["value"] = assign_name
        else:
            self.fields["assign_name"].required = True
