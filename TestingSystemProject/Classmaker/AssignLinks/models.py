from collections.abc import Iterable
from django.db import models
from GenerateSecureKeys.GenerateSlug import generate_secure_slug
from TestingSystem.models import (
    TestModel,
    TimeStampedBaseModel,
    TestQuestionRandomizeModel,
)
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.validators import MaxValueValidator, MinValueValidator
from ckeditor_uploader.fields import RichTextUploadingField

NUMBER_CHOICES = [(str(i), str(i)) for i in range(1, 11)]


# Setups
class AvailabilityModel(models.Model):
    unavailable = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    start_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return "time_managed"


class AttemptsModel(models.Model):
    attempts = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    unlimited = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.attempts}"


class RestrictionsModel(models.Model):
    password = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return self.password


class Print_copy_paste_translateModel(models.Model):
    allow_print = models.BooleanField(default=False)
    allow_copy = models.BooleanField(default=False)
    allow_paste = models.BooleanField(default=False)
    allow_translation = models.BooleanField(default=False)


# Taking the Test
class DisplayEachQuestionModel(models.Model):
    selected_number = models.CharField(max_length=2, choices=NUMBER_CHOICES)
    randomize = models.BooleanField(default=False)
    must_answer = models.BooleanField(default=True)

    def __str__(self) -> str:
        return "display_seted"


class InstructionModel(models.Model):
    pre_test_guidelines = models.BooleanField(default=True)


class LimitTimeModel(models.Model):
    minute = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1440)], default=0
    )

    def __str__(self) -> str:
        return f"{self.minute}"


# Test completion
class ResultsPageModel(models.Model):
    points = models.BooleanField(default=True)
    persentage = models.BooleanField(default=True)
    feedback = models.BooleanField(default=True)
    reveal_correct_answers = models.BooleanField(default=True)


class PassMarkAndFeedbackModel(models.Model):
    pass_mark = models.IntegerField()
    send_completed_message = RichTextUploadingField(blank=True, null=True)
    send_not_completed_message = RichTextUploadingField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.pass_mark}%"


class EmailResultsInstructorModel(models.Model):
    off = models.BooleanField(default=True)
    score = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self) -> str:
        return f"{self.email}"


class TakerEmailSendModel(models.Model):
    point = models.BooleanField(default=False)
    percentage = models.BooleanField(default=False)
    feedback = models.BooleanField(default=False)
    graded = models.BooleanField(default=False)
    reveal_correct_answers = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.point}"


# Connection all settings
class AssignLinkModel(TimeStampedBaseModel):
    availability_OTO = models.OneToOneField(
        AvailabilityModel,
        on_delete=models.CASCADE,
        related_name="assign_link_availability",
    )
    attempts_OTO = models.OneToOneField(
        AttemptsModel, on_delete=models.CASCADE, related_name="assign_link_attempts"
    )
    restrictions_OTO = models.OneToOneField(
        RestrictionsModel,
        on_delete=models.CASCADE,
        related_name="assign_link_restrictions",
    )
    print_copy_paste_translate_OTO = models.OneToOneField(
        Print_copy_paste_translateModel,
        on_delete=models.CASCADE,
        related_name="assign_link_print_copy_paste_translate",
    )
    display_each_question_OTO = models.OneToOneField(
        DisplayEachQuestionModel,
        on_delete=models.CASCADE,
        related_name="assign_link_display_each_question",
    )
    instruction_OTO = models.OneToOneField(
        InstructionModel, on_delete=models.CASCADE, related_name="instruction"
    )
    limit_time_OTO = models.OneToOneField(
        LimitTimeModel, on_delete=models.CASCADE, related_name="assign_link_limit_time"
    )

    results_page_OTO = models.OneToOneField(
        ResultsPageModel, on_delete=models.CASCADE, related_name="results_page"
    )
    pass_mark_and_feedback_OTO = models.OneToOneField(
        PassMarkAndFeedbackModel,
        on_delete=models.CASCADE,
        related_name="assign_link_pass_mark_and_feedback",
    )
    email_results_instructor_OTO = models.OneToOneField(
        EmailResultsInstructorModel,
        on_delete=models.CASCADE,
        related_name="assign_link_email_results_instructor",
    )
    taker_email_send_OTO = models.OneToOneField(
        TakerEmailSendModel,
        on_delete=models.CASCADE,
        related_name="assign_link_taker_email_send",
    )
    test_MTO = models.ForeignKey(
        TestModel, on_delete=models.CASCADE, related_name="assign_link_test"
    )
    assign_name = models.CharField(max_length=50)
    slug_field = models.SlugField(unique=True, max_length=100)

    def __str__(self):
        return "valid_secure"

    def save(self, *args, **kwargs):
        if not self.slug_field:
            self.slug_field = generate_secure_slug(self.test_MTO.title)
        super().save(*args, **kwargs)
