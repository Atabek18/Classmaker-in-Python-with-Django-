from django.db import models
import random
from GenerateSecureKeys.GenerateSlug import generate_slugs
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField


class UIDBaseModel(models.Model):
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    class Meta:
        abstract = True


class TimeStampedBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TestManager(models.Manager):
    def create_duplicate_test(self, original_test, test_name=None, method="Same"):
        """
        Create a duplicate test with associated questions.
        Parameters:
        - original_test: The original test instance to duplicate.
        - test_name: Optional name for the duplicated test.
        - method: 'Same' to associate questions with the duplicated test, 'Copies' to create new question copies.
        """

        method = test_name if test_name else original_test.title + " (Copy)"
        new_test = self.create(
            title=method,
            description=original_test.description,
            slug=generate_slugs(method),
        )

        if method == "Copies":
            for question in original_test.questions.all():
                new_question = question.duplicate_question(new_test)
        elif method == "Same":
            for question in self.questions.all():
                question.test.add(new_test)

        return new_test


class TestModel(TimeStampedBaseModel):
    title = models.CharField(max_length=50)
    description = models.TextField()
    slug = models.SlugField(unique=True, max_length=200)

    objects = TestManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slugs(self.title)
        super().save(*args, **kwargs)

    def duplicate_test(self, test_name=None, method="Same"):
        return self.objects.create_duplicate_test(self, test_name, method)


class TestQuestionRandomizeModel(TimeStampedBaseModel):
    user = models.ForeignKey(
        "UserResponse.UserRegisterModel",
        on_delete=models.CASCADE,
        related_name="user_random",
    )
    test = models.ForeignKey(
        TestModel, on_delete=models.CASCADE, related_name="test_random"
    )
    question = models.ForeignKey(
        "QuestionModel", on_delete=models.CASCADE, related_name="question_random"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("user", "test", "question")
        indexes = [models.Index(fields=["user", "test", "order"])]

    def __str__(self):
        return f"{self.question} (Order: {self.order})"

    # @classmethod
    # def randomize_questions(cls, test_instance):
    #     questions = list(test_instance.questions.all())
    #     random.shuffle(questions)
    #     for index, question in enumerate(questions):
    #         test_question, created = cls.objects.get_or_create(
    #             test=test_instance, question=question
    #         )
    #         test_question.order = index + 1
    #         test_question.save()

    @classmethod
    def randomize_questions(cls, user_instance, test_instance):
        questions = list(test_instance.questions.all())
        random.shuffle(questions)
        objects_to_create = [
            cls(
                user=user_instance,
                test=test_instance,
                question=question,
                order=index + 1,
            )
            for index, question in enumerate(questions)
        ]
        cls.objects.bulk_create(objects_to_create, ignore_conflicts=True)


class QuestionManager(models.Manager):
    def create_question(self, self_item, test):
        new_question = QuestionModel.objects.create(
            text=self_item.text,
            ranking=self_item.ranking,
            slug=generate_slugs(self_item.text + "-copy"),
            question_type=self_item.question_type,
        )
        new_question.test.add(test)
        for option in self_item.options.all():
            new_option = option.duplicate_option(new_question)
        for truefalse in self_item.truefalse.all():
            new_truefalse = truefalse.duplicate_truefalse(new_question)
        for freetext in self_item.freetext.all():
            new_freetext = freetext.duplicate_freetext(new_question)
        for matching in self_item.matching.all():
            new_matching = matching.duplicate_matching(new_question)
        new_question.save()

        return new_question


class QuestionModel(TimeStampedBaseModel):
    test = models.ManyToManyField(TestModel, related_name="questions", blank=True)
    text = RichTextUploadingField(blank=True, null=True)
    ranking = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=200)
    question_type = models.CharField(max_length=10)

    objects = QuestionManager()

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slugs(self.text)
        super().save(*args, **kwargs)

    def duplicate_question(self, test):
        return self.objects.create_question(self, test)


class OptionModel(UIDBaseModel, TimeStampedBaseModel):
    question = models.ForeignKey(
        QuestionModel, on_delete=models.CASCADE, related_name="options"
    )
    answer = RichTextUploadingField(blank=True, null=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return mark_safe(self.answer)

    def duplicate_option(self, question):
        return self.objects.create(
            question=question, answer=self.answer, is_correct=self.is_correct
        )


class TrueFalseModel(UIDBaseModel, TimeStampedBaseModel):
    question = models.ForeignKey(
        QuestionModel, on_delete=models.CASCADE, related_name="truefalse"
    )
    truefalse = models.BooleanField(default=False)
    modify_truefalse_text = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.question}"

    def duplicate_truefalse(self, question):
        return self.objects.create(
            question=question,
            truefalse=self.truefalse,
            modify_truefalse_text=self.modify_truefalse_text,
        )


class FreeTextModel(UIDBaseModel, TimeStampedBaseModel):
    question = models.ForeignKey(
        QuestionModel, on_delete=models.CASCADE, related_name="freetext"
    )
    freetext = RichTextUploadingField(blank=True, null=True)

    def __str__(self):
        return self.freetext

    def duplicate_freetext(self, question):
        return self.objects.create(question=question, freetext=self.freetext)


class MatchingModel(UIDBaseModel, TimeStampedBaseModel):
    question = models.ForeignKey(
        QuestionModel, on_delete=models.CASCADE, related_name="matching"
    )
    left_item = RichTextUploadingField(blank=True, null=True)
    right_item = RichTextUploadingField(blank=True, null=True)

    def __str__(self):
        return f"{self.left_item} -> {self.right_item}"

    def duplicate_freetext(self, question):
        return self.objects.create(
            question=question, left_item=self.left_item, right_item=self.right_item
        )


class TestIntroductionModel(TimeStampedBaseModel):
    test = models.OneToOneField(
        TestModel, on_delete=models.CASCADE, related_name="test_intro"
    )
    text = RichTextUploadingField(blank=True, null=True)

    def __str__(self) -> str:
        return "valid_intro"


class CustomUser(AbstractUser):
    uploaded_image = models.ImageField(
        upload_to="testingsystem/img/", blank=True, null=True
    )
