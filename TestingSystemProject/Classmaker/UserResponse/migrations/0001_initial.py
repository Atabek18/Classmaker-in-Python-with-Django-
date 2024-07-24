# Generated by Django 5.0.3 on 2024-04-09 17:35

import django.db.models.deletion
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("AssignLinks", "0001_initial"),
        ("TestingSystem", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserRegisterModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("surname", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, region="UZ"
                    ),
                ),
                (
                    "season_type",
                    models.CharField(
                        choices=[("MS", "Main-Season"), ("PS", "Pre-Season")],
                        max_length=2,
                    ),
                ),
                ("season_number", models.PositiveSmallIntegerField()),
                ("status", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "assign",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_assign",
                        to="AssignLinks.assignlinkmodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserAsnwerToTrueFalseModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("answer_based", models.UUIDField(blank=True, null=True)),
                (
                    "question_based",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="TestingSystem.questionmodel",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="UserResponse.userregistermodel",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserAnswerToMultipleChoiceModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("answer_based", models.UUIDField(blank=True, null=True)),
                (
                    "question_based",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="TestingSystem.questionmodel",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="UserResponse.userregistermodel",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserAnswerToMatchingModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("left_item", models.UUIDField(blank=True, null=True)),
                ("right_item", models.UUIDField(blank=True, null=True)),
                (
                    "question_based",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answer_matching_question",
                        to="TestingSystem.questionmodel",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_matching",
                        to="UserResponse.userregistermodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserAnswerToFreeTextModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "answer_based",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "question_based",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="TestingSystem.questionmodel",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="UserResponse.userregistermodel",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CurrentPageModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("current_page", models.PositiveIntegerField(default=0)),
                ("timestampt", models.DateTimeField()),
                (
                    "current_user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_current_page",
                        to="UserResponse.userregistermodel",
                    ),
                ),
            ],
        ),
    ]