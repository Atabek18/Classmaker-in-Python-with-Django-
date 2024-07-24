from django.db import models
from TestingSystem.models import QuestionModel
from django.db import models
from AssignLinks.models import AssignLinkModel
from phonenumber_field.modelfields import PhoneNumberField


class UserRegisterModel(models.Model):
    assign = models.ForeignKey(
        AssignLinkModel, on_delete=models.CASCADE, related_name="user_assign"
    )
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = PhoneNumberField(region="UZ")
    Season = [
        ("MS", "Main-Season"),
        ("PS", "Pre-Season"),
    ]
    season_type = models.CharField(max_length=2, choices=Season)
    season_number = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.surname} - {self.season_type}-{self.season_number}"


class CurrentPageModel(models.Model):
    current_user = models.OneToOneField(
        UserRegisterModel, on_delete=models.CASCADE, related_name="user_current_page"
    )
    current_page = models.PositiveIntegerField(default=0)
    timestampt = models.DateTimeField(null=True, blank=True)


class BaseUserAnswerModel(models.Model):
    user = models.ForeignKey(UserRegisterModel, on_delete=models.CASCADE)
    question_based = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
    answer_based = None

    @classmethod
    def create_or_update_answer(cls, user, question, answer):
        model, created = cls.objects.get_or_create(
            user=user, question_based=question, defaults={"answer_based": answer}
        )
        if not created and model.answer_based != answer:
            model.answer_based = answer
            model.save()
        return model, created

    def _get_point_and_percentage(self, is_correct):
        point = self.question_based.ranking if is_correct else 0
        percentage = round(point / self.question_based.ranking, 2) * 100
        return point, percentage

    class Meta:
        abstract = True


class UserAnswerToMultipleChoiceModel(BaseUserAnswerModel):

    answer_based = models.UUIDField(blank=True, null=True)

    def get_multiplechoice_feedback(self):
        current_options = self.question_based.options
        get_answered_multiplechoice = current_options.get(uid=self.answer_based.hex)
        get_correct_answer = [
            correct_answer.hex
            for correct_answer in current_options.filter(is_correct=True).values_list(
                "uid", flat=True
            )
        ]
        is_correct = get_answered_multiplechoice.is_correct
        point, percentage = self._get_point_and_percentage(is_correct)
        return get_correct_answer, point, percentage


class UserAsnwerToTrueFalseModel(BaseUserAnswerModel):
    answer_based = models.UUIDField(blank=True, null=True)

    def get_truefalse_feedback(self):
        current_options = self.question_based.truefalse
        get_answered_truefalse = current_options.get(uid=self.answer_based.hex)
        get_correct_answer = current_options.get(truefalse=True).uid.hex
        is_correct = get_answered_truefalse.truefalse
        point, percentage = self._get_point_and_percentage(is_correct)
        return get_correct_answer, point, percentage


class UserAnswerToFreeTextModel(BaseUserAnswerModel):

    answer_based = models.CharField(max_length=100, blank=True, null=True)

    def get_freetext_feedback(self):
        current_options = self.question_based.freetext.all()
        is_correct = current_options.filter(freetext=self.answer_based).exists()
        point, percentage = self._get_point_and_percentage(is_correct)
        return (
            list(current_options.values_list("freetext", flat=True)),
            point,
            percentage,
        )


class UserAnswerToMatchingModel(models.Model):
    user = models.ForeignKey(
        UserRegisterModel, on_delete=models.CASCADE, related_name="user_matching"
    )
    question_based = models.ForeignKey(
        QuestionModel, on_delete=models.CASCADE, related_name="answer_matching_question"
    )
    left_item = models.UUIDField(blank=True, null=True)
    right_item = models.UUIDField(blank=True, null=True)
