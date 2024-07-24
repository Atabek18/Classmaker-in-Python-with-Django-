from typing import Any
from django.contrib.auth.base_user import AbstractBaseUser
from django.forms import (
    ModelForm,
    TextInput,
    Textarea,
    NumberInput,
    CheckboxInput,
)
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import modelformset_factory
from .models import (
    QuestionModel,
    OptionModel,
    TestModel,
    TrueFalseModel,
    FreeTextModel,
    MatchingModel,
    TestIntroductionModel,
)
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor_uploader.fields import RichTextUploadingFormField


class TestModelForm(ModelForm):
    class Meta:
        model = TestModel
        fields = ["title", "description"]

        widgets = {
            "title": TextInput(
                attrs={
                    "class": "form-test",
                    "placeholder": "Title",
                    "required": "true",
                }
            ),
            "description": Textarea(
                attrs={
                    "class": "form-test",
                    "placeholder": "Please about Test",
                    "rows": 7,
                }
            ),
        }

        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": "%(model_name)s's %(field_labels)s are not unique.",
            }
        }


class QuestionModelForm(ModelForm):
    class Meta:
        model = QuestionModel

        fields = ["text", "ranking"]

        widgets = {
            "ranking": NumberInput(
                attrs={
                    "class": "form-question-rank",
                    "placeholder": 1,
                    "required": "true",
                }
            ),
        }

        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": "%(model_name)s's %(field_labels)s are not unique.",
            }
        }

    text = RichTextUploadingFormField(
        label="",
        widget=CKEditorUploadingWidget(attrs={"class": "form-question"}),
        required=True,
    )


class OptionModelForm(ModelForm):
    class Meta:
        model = OptionModel

        fields = ["answer", "is_correct"]

        widgets = {
            "is_correct": CheckboxInput(attrs={"class": "form-correct"}),
        }

        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": "%(model_name)s's %(field_labels)s are not unique.",
            }
        }

    answer = RichTextUploadingFormField(
        label="",
        widget=CKEditorUploadingWidget(attrs={"class": "form-multiple"}),
        required=True,
    )


class TrueFalseModelForm(ModelForm):
    class Meta:
        model = TrueFalseModel

        fields = ["truefalse", "modify_truefalse_text"]

        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": "%(model_name)s's %(field_labels)s are not unique.",
            }
        }


class FreeTextModelForm(ModelForm):
    class Meta:
        model = FreeTextModel

        fields = ["freetext"]
        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": "%(model_name)s's %(field_labels)s are not unique.",
            }
        }

    freetext = RichTextUploadingFormField(
        label="",
        widget=CKEditorUploadingWidget(attrs={"class": "form-freetext"}),
        required=True,
    )


class MatchingModelForm(ModelForm):
    class Meta:
        model = MatchingModel
        fields = ["left_item", "right_item"]

    left_item = RichTextUploadingFormField(
        label="Left Item",
        widget=CKEditorUploadingWidget(attrs={"class": "form-control"}),
        required=True,
    )

    right_item = RichTextUploadingFormField(
        label="Right Item",
        widget=CKEditorUploadingWidget(attrs={"class": "form-control"}),
        required=True,
    )
    error_messages = {
        NON_FIELD_ERRORS: {
            "unique_together": "%(model_name)s's %(field_labels)s are not unique.",
        }
    }


class TestIntroductionModelForm(ModelForm):
    class Meta:
        model = TestIntroductionModel
        fields = ["text"]

    text = RichTextUploadingFormField(
        label="",
        widget=CKEditorUploadingWidget(attrs={"class": "form-intro"}),
        required=False,
    )
    error_messages = {
        NON_FIELD_ERRORS: {
            "unique_together": "%(model_name)s's %(field_labels)s are not unique.",
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].required = True


OptionModelFormSet = modelformset_factory(
    OptionModel, OptionModelForm, fields=("answer", "is_correct"), extra=4
)
TrueFalseModelFormSet = modelformset_factory(
    TrueFalseModel,
    TrueFalseModelForm,
    fields=("truefalse", "modify_truefalse_text"),
    extra=2,
)
FreeTextModelFormSet = modelformset_factory(
    FreeTextModel, FreeTextModelForm, fields=("freetext",), extra=1
)
MatchingModelFormSet = modelformset_factory(
    MatchingModel, MatchingModelForm, fields=("left_item", "right_item"), extra=4
)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "uploaded_image")

    uploaded_image = forms.ImageField(
        widget=forms.FileInput(
            attrs={"id": "imageUpload", "accept": ".png, .jpg, .jpeg"}
        ),
        required=False,
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form__input", "placeholder": "Username"}
        ),
        required=False,
        max_length=100,
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form__input", "placeholder": "Email"}),
        required=False,
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form__input", "placeholder": "Password"}
        ),
        required=False,
        max_length=100,
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        del self.fields["old_password"]
        del self.fields["new_password2"]
        self.fields["new_password1"].required = False
