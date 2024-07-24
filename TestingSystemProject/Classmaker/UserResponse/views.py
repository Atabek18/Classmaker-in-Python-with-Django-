from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import (
    UserAnswerToMultipleChoiceModel,
    UserAsnwerToTrueFalseModel,
    UserAnswerToFreeTextModel,
    UserAnswerToMatchingModel,
    UserRegisterModel,
)
from django.forms.models import model_to_dict
from TestingSystem.models import (
    QuestionModel,
    TestModel,
    OptionModel,
    TrueFalseModel,
    FreeTextModel,
    MatchingModel,
)
from .forms import RegistrationForm
from django.utils.safestring import mark_safe
from AssignLinks.models import AssignLinkModel
import pytz
from django.utils import timezone
from datetime import datetime, time, timedelta
import requests


class TestPassUtils:
    def __init__(self, user, questions) -> None:
        self.uzb_zone = pytz.timezone("Asia/Tashkent")
        self.curr_dt = timezone.now().astimezone(self.uzb_zone)
        self.user = user
        self.questions = questions

    def _setTimerAvailability(self, data, time):
        datetimeset = self.uzb_zone.localize(
            datetime.combine(
                data,
                time,
            )
        )
        return datetimeset

    def _saveAnswers(self, data):
        for key in data:
            if key.startswith("question_"):
                val = data[key]
                if key.endswith("_multi") and val[0]:
                    model = UserAnswerToMultipleChoiceModel(
                        user=self.user,
                        question_based=self.questions[int(key.split("_")[1])],
                        answer_based=OptionModel.objects.get(pk=int(val[0])),
                    )
                    model.save()
                elif key.endswith("_truefalse") and val[0]:
                    model = UserAsnwerToTrueFalseModel(
                        user=self.user,
                        question_based=self.questions[int(key.split("_")[1])],
                        answer_based=True if val[0] == "true" else False,
                    )
                    model.save()
                elif key.endswith("_freetext") and val[0]:
                    model = UserAnswerToFreeTextModel(
                        user=self.user,
                        question_based=self.questions[int(key.split("_")[1])],
                        answer_based=val[0],
                    )
                    model.save()
                elif key.startswith("question_") and val[0] and "_matching" in key:
                    question_index = int(key.split("_")[1])
                    matching_index = int(key.split("_")[3])
                    response_pairs = val[:1]
                    left_items = []
                    right_items = []
                    for pair in response_pairs:
                        left, right = pair.split("_")
                        left_items.append(left)
                        right_items.append(right)
                    question = self.questions[question_index]
                    for left, right in zip(left_items, right_items):
                        model = UserAnswerToMatchingModel(
                            user=self.user,
                            question_based=question,
                            answer_based=MatchingModel.objects.filter(
                                question=question
                            )[matching_index],
                            left_item=left,
                            right_item=right,
                        )
                        model.save()

    def _assignQuestions(self):
        question_data = [
            {
                "question_type": (
                    "multi"
                    if question.options.all()
                    else (
                        "truefalse"
                        if question.truefalse.all()
                        else (
                            "freetext"
                            if question.freetext.all()
                            else "matching" if question.matching.all() else "unknown"
                        )
                    )
                ),
                "text": mark_safe(question.text),
                "options": (
                    [
                        {"id": str(option.id), "text": mark_safe(option.answer)}
                        for option in OptionModel.objects.filter(question=question)
                    ]
                    if question.options.all()
                    else []
                ),
                "pairs": (
                    [
                        {"left_item": match.left_item, "right_item": match.right_item}
                        for match in MatchingModel.objects.filter(question=question)
                    ]
                    if question.matching.all()
                    else []
                ),
            }
            for question in self.questions
        ]
        return question_data

    def _timeCalulatorHelper(self, milliseconds):
        seconds, milliseconds = divmod(milliseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return hours, minutes, seconds

    def _spentTimeCalculator(self, stricked_time, hours, minutes, seconds):
        time1 = timedelta(hours=0, minutes=stricked_time, seconds=0)
        time2 = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        result = time1 - time2
        total_seconds = result.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        result_time = time(int(hours), int(minutes), int(seconds))
        return result_time

    def _savePassNeedTime(self, time, startedDateTime, endedDateTime, limited_time):
        hours, minutes, seconds = self._timeCalulatorHelper(time)
        spent_time = self._spentTimeCalculator(limited_time, hours, minutes, seconds)
        usertimepass = UserRegisterModel(
            user=self.user,
            spent_time=spent_time,
            started_time=startedDateTime,
            ended_time=endedDateTime,
        )
        usertimepass.save()


class SavePassInfo(TestPassUtils):
    def __init__(self, user, questions) -> None:
        super(SavePassInfo, self).__init__(user, questions)

    def TimerAvailability(self, start_date_and_time: list, end_date_and_time: list):
        return self._setTimerAvailability(
            start_date_and_time[0], start_date_and_time[1]
        ), self._setTimerAvailability(end_date_and_time[0], end_date_and_time[1])

    def SaveAnsweredQuestions(self, data: dict) -> None:
        self._saveAnswers(data)

    def AssignGivenQuestions(self):
        return self._assignQuestions()

    def SaveNeededTime(self, time, startDateTime, endDateTime, limited_time) -> None:
        self._savePassNeedTime(time, startDateTime, endDateTime, limited_time)


def getUsersInfo(user):
    return dict(
        id=user["id"],
        name=user["name"],
        surname=user["surname"],
        email=user["email"],
        status=user["status"],
    )


def answer_question_view(request, assign_slug):
    assign_model = get_object_or_404(AssignLinkModel, slug_field=assign_slug)
    assign_users = [
        getUsersInfo(model_to_dict(i)) for i in assign_model.user_assign.all()
    ]
    random_questions = assign_model.test_MTO.test_random.all().order_by("order")
    questions = [question.question for question in random_questions]
    # saveFuntions = SavePassInfo(UserRegisterModel.objects.none(), questions)
    # question_data = saveFuntions.AssignGivenQuestions()
    startDT, endDT = [
        assign_model.availability_OTO.start_date,
        assign_model.availability_OTO.start_time,
    ], [
        assign_model.availability_OTO.end_date,
        assign_model.availability_OTO.end_time,
    ]
    limited_time = assign_model.limit_time_OTO.minute
    api_url = reverse("API_TEST:init_test")
    data = requests.get(
        "http://127.0.0.1:8000/" + api_url, params={"link_id": assign_model.id}
    )
    # start_datetime, end_datetime = saveFuntions.TimerAvailability(startDT, endDT)
    register_form = RegistrationForm()
    if request.method == "POST":
        pass
        # current_datetime = saveFuntions.curr_dt
        # if request.POST.get("BlockMe", None) == "Block" and not (
        #     start_datetime < current_datetime < end_datetime
        # ):
        #     return redirect(reverse("TestingSystem:dashboard"))
        # else:
        #     data = dict(request.POST)
        #     saveFuntions.SaveAnsweredQuestions(data=data)
        #     test_s_time = request.POST.get('test_started_datetime', False)
        #     test_e_time = request.POST.get('test_ended_datetime', False)
        #     time_difference = request.POST.get('time_difference', False)
        #     if all([time_difference, test_s_time, test_e_time]):
        #         parsed_s_datetime = datetime.fromisoformat(test_s_time)
        #         parsed_e_datetime = datetime.fromisoformat(test_e_time)
        #         saveFuntions.SaveNeededTime(int(time_difference), parsed_s_datetime, parsed_e_datetime, limited_time)
        #         return redirect(
        #             reverse(
        #                 "UserScore:score",
        #                 kwargs={"user_id": 1, "assign_slug": assign_slug},
        #             )
        #         )
    context = {
        "test_id": assign_model.test_MTO.id,
        "registerForm": register_form,
        "assign_slug": assign_slug,
        # "question_data": question_data,
        "link_id": assign_model.id,
        "assign_users": assign_users,
        # 'TestData':data.json(),
        # "start_datetime": start_datetime.isoformat(),
        # "end_datetime": end_datetime.isoformat(),
    }

    return render(request, "userresponse/user_response1.html", context)


def previews_questions(request, test_id):
    test = get_object_or_404(TestModel, id=test_id)
    questions = QuestionModel.objects.filter(test=test)
    question_data = [
        {
            "question_type": (
                "multi"
                if question.options.all()
                else (
                    "truefalse"
                    if question.truefalse.all()
                    else (
                        "freetext"
                        if question.freetext.all()
                        else "matching" if question.matching.all() else "unknown"
                    )
                )
            ),
            "text": mark_safe(question.text),
            "options": (
                [
                    {"id": str(option.id), "text": mark_safe(option.answer)}
                    for option in OptionModel.objects.filter(question=question)
                ]
                if question.options.all()
                else []
            ),
            "pairs": (
                [
                    {"left_item": match.left_item, "right_item": match.right_item}
                    for match in MatchingModel.objects.filter(question=question)
                ]
                if question.matching.all()
                else []
            ),
        }
        for question in questions
    ]
    context = {"question_data": question_data}
    return render(request, "userresponse/admin_preview.html", context)


# def registration_view(request, assign_slug):
#     assign_model = get_object_or_404(
#         AssignLinkModel, slug_field=assign_slug
#     )
#     if request.method == "OPTIONS":
#         response = JsonResponse({}, status=200)
#     elif request.method == "POST":
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.assign = assign_model
#             user.save()
#             response = JsonResponse({'main':'adasda'}, status=200)
#         else:
#             response = JsonResponse({'status_register':'Not valid'})
#     else:
#         response = JsonResponse({"error": "Method not allowed"}, status=405)

#     return response

# @csrf_exempt
# def init_test(request, test_id):
#     test = get_object_or_404(TestModel, pk=test_id)
#     questions = test.questions.all()
#     return JsonResponse({'questions':'[i for i in questions]'}, status=200)

# @csrf_exempt
# def start_test(request, test_id):
#     test = get_object_or_404(TestModel, pk=test_id)
#     questions = test.questions.all()


#     return JsonResponse({'questions':'[i for i in questions]'}, status=200)
def index(request):
    return render(request, "userresponse/admin_preview.html")
