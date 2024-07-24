from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from Login.views import login_required_decorator
from django.contrib import messages
from .models import (
    QuestionModel,
    TestModel,
    OptionModel,
    TrueFalseModel,
    FreeTextModel,
    CustomUser,
    MatchingModel,
    TestIntroductionModel,
)
from AssignLinks.models import AssignLinkModel
from django.core.mail import EmailMessage
from django.contrib.auth import update_session_auth_hash
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import (
    TestModelForm,
    OptionModelForm,
    QuestionModelForm,
    OptionModelFormSet,
    TrueFalseModelFormSet,
    TrueFalseModelForm,
    FreeTextModelFormSet,
    FreeTextModelForm,
    CustomPasswordChangeForm,
    CustomUserChangeForm,
    MatchingModelFormSet,
    MatchingModelForm,
    TestIntroductionModelForm,
)
from AssignLinks.views import Analyse, AnalyseUtils, SortBy, SortUtils
import numpy as np
from datetime import timedelta


@login_required_decorator
def home(request):
    if request.method == "POST":
        form = TestModelForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                create_question = reverse("TestingSystem:tests")
                return redirect(create_question)
            except:
                form.add_error(None, "Some problems with filling blank")
    else:
        form = TestModelForm()

    data = {"form": form}
    return render(request, "testingsystem/temp.html", data)


class CreateQuestionAndOptions:
    def __init__(self, request, test, qestion_type):
        self.request = request
        self.test = test
        self.type = qestion_type

    def DatabaseSave(self, QForm, OptionalFormSet):
        question_form = QForm(self.request.POST)
        formset = OptionalFormSet(self.request.POST)
        if question_form.is_valid() and formset.is_valid():
            question = question_form.save(commit=False)
            question.question_type = self.type
            question.save()
            question.test.add(self.test)
            formset_instances = formset.save(commit=False)
            for form in formset_instances:
                form.question = question
                form.save()
            return [question_form, formset, True]


@login_required_decorator
def CreateQuestionAndMultpleOptions(request, test_id, test_description):
    test = TestModel.objects.get(pk=test_id, slug=test_description)
    if request.method == "POST":
        CQAP = CreateQuestionAndOptions(request, test, "option")
        question_form, option_formset, is_valid = CQAP.DatabaseSave(
            QuestionModelForm, OptionModelFormSet
        )
        if is_valid:
            object_list = reverse(
                "TestingSystem:questions",
                kwargs={"test_id": test_id, "test_description": test_description},
            )
            messages.success(request, "Question and options added successfully!")
            return redirect(object_list)
    else:
        question_form = QuestionModelForm()
        option_formset = OptionModelFormSet(queryset=OptionModel.objects.none())
    return render(
        request,
        "testingsystem/main.html",
        {
            "question_form": question_form,
            "option_formset": option_formset,
            "slug": test.slug,
            "test_id": test_id,
            "id": request.GET.get("id", None),
        },
    )


@login_required_decorator
def CreateQuestionAndTrueFalseOptions(request, test_id, test_description):
    test = TestModel.objects.get(pk=test_id, slug=test_description)
    if request.method == "POST":
        CQAP = CreateQuestionAndOptions(request, test, "truefalse")
        question_form, truefalse_formset, is_valid = CQAP.DatabaseSave(
            QuestionModelForm, TrueFalseModelFormSet
        )
        if is_valid:
            object_list = reverse(
                "TestingSystem:questions",
                kwargs={"test_id": test_id, "test_description": test_description},
            )
            messages.success(request, "Question and options added successfully!")
            return redirect(object_list)

    else:
        question_form = QuestionModelForm()
        truefalse_formset = TrueFalseModelFormSet(
            queryset=TrueFalseModel.objects.none()
        )

    return render(
        request,
        "testingsystem/main.html",
        {
            "question_form": question_form,
            "option_formset": truefalse_formset,
            "slug": test.slug,
            "test_id": test_id,
        },
    )


@login_required_decorator
def CreateQuestionAndFreeTextOptions(request, test_id, test_description):
    test = TestModel.objects.get(pk=test_id, slug=test_description)
    if request.method == "POST":
        CQAP = CreateQuestionAndOptions(request, test, "freetext")
        question_form, freetext_formset, is_valid = CQAP.DatabaseSave(
            QuestionModelForm, FreeTextModelFormSet
        )
        if is_valid:
            object_list = reverse(
                "TestingSystem:questions",
                kwargs={"test_id": test_id, "test_description": test_description},
            )
            messages.success(request, "Question and options added successfully!")
            return redirect(object_list)  # Replace with the actual success URL
    else:
        question_form = QuestionModelForm()
        freetext_formset = FreeTextModelFormSet(queryset=FreeTextModel.objects.none())

    return render(
        request,
        "testingsystem/main.html",
        {
            "question_form": question_form,
            "option_formset": freetext_formset,
            "slug": test.slug,
            "test_id": test_id,
        },
    )


@login_required_decorator
def CreateQuestionAndMatchingOptions(request, test_id, test_description):
    test = TestModel.objects.get(pk=test_id, slug=test_description)
    if request.method == "POST":
        CQAP = CreateQuestionAndOptions(request, test, "matching")
        question_form, option_formset, is_valid = CQAP.DatabaseSave(
            QuestionModelForm, MatchingModelFormSet
        )
        if is_valid:
            object_list = reverse(
                "TestingSystem:questions",
                kwargs={"test_id": test_id, "test_description": test_description},
            )
            messages.success(request, "Question and options added successfully!")
            return redirect(object_list)
    else:
        question_form = QuestionModelForm()
        option_formset = MatchingModelFormSet(queryset=MatchingModel.objects.none())

    return render(
        request,
        "testingsystem/main.html",
        {
            "question_type": "matching",
            "question_form": question_form,
            "option_formset": option_formset,
            "slug": test.slug,
            "test_id": test_id,
            "id": request.GET.get("id", None),
        },
    )


class EditQuestionAndOptions:
    def __init__(self, request, question, options):
        self.request = request
        self.question = question
        self.options = options

    def DatabaseEdit(self, QForm, OptionalForm):
        form = QForm(self.request.POST, instance=self.question)
        option_forms = [
            OptionalForm(
                self.request.POST, instance=option, prefix=f"option_{option.uid}"
            )
            for option in self.options
        ]
        if form.is_valid() and all(of.is_valid() for of in option_forms):
            form.save()
            for option_form in option_forms:
                option_form.save()
            return [form, option_forms, True]


@login_required_decorator
def EditQuestionAndMultpleOptions(request, question_id, question_description):
    question = get_object_or_404(
        QuestionModel, pk=question_id, slug=question_description
    )
    options = OptionModel.objects.filter(question=question)
    if request.method == "POST":
        EQAO = EditQuestionAndOptions(request, question, options)
        form, option_forms, is_valid = EQAO.DatabaseEdit(
            QuestionModelForm, OptionModelForm
        )
        if is_valid:
            reverse_url = reverse("TestingSystem:tests")
            return redirect(reverse_url)
    else:
        form = QuestionModelForm(instance=question)
        option_forms = [
            OptionModelForm(instance=option, prefix=f"option_{option.uid}")
            for option in options
        ]
    return render(
        request,
        "testingsystem/question_edit.html",
        {
            "form": form,
            "option_forms": option_forms,
            "question_type": "options",
        },
    )


@login_required_decorator
def EditQuestionAndTrueFalseOptions(request, question_id, question_description):
    question = get_object_or_404(
        QuestionModel, pk=question_id, slug=question_description
    )
    options = TrueFalseModel.objects.filter(question=question)
    if request.method == "POST":
        EQAO = EditQuestionAndOptions(request, question, options)
        form, truefalse_forms, is_valid = EQAO.DatabaseEdit(
            QuestionModelForm, TrueFalseModelForm
        )
        if is_valid:
            reverse_url = reverse("TestingSystem:tests")
            return redirect(reverse_url)
    else:
        form = QuestionModelForm(instance=question)
        truefalse_forms = [
            TrueFalseModelForm(instance=option, prefix=f"option_{option.uid}")
            for option in options
        ]
    return render(
        request,
        "testingsystem/question_edit.html",
        {
            "form": form,
            "option_forms": truefalse_forms,
            "question_type": "truefalse",
        },
    )


@login_required_decorator
def EditQuestionAndFreeTextOptions(request, question_id, question_description):
    question = get_object_or_404(
        QuestionModel, pk=question_id, slug=question_description
    )
    options = FreeTextModel.objects.filter(question=question)
    if request.method == "POST":
        EQAO = EditQuestionAndOptions(request, question, options)
        form, freetext_forms, is_valid = EQAO.DatabaseEdit(
            QuestionModelForm, FreeTextModelForm
        )
        if is_valid:
            reverse_url = reverse("TestingSystem:tests")
            return redirect(reverse_url)
    else:
        form = QuestionModelForm(instance=question)
        freetext_forms = [
            FreeTextModelForm(instance=option, prefix=f"option_{option.uid}")
            for option in options
        ]
    return render(
        request,
        "testingsystem/question_edit.html",
        {
            "form": form,
            "option_forms": freetext_forms,
            "question_type": "freetext",
        },
    )


@login_required_decorator
def EditQuestionAndMatchingOptions(request, question_id, question_description):
    question = get_object_or_404(
        QuestionModel, pk=question_id, slug=question_description
    )
    options = MatchingModel.objects.filter(question=question)

    if request.method == "POST":
        EQAO = EditQuestionAndOptions(request, question, options)
        form, matching_forms, is_valid = EQAO.DatabaseEdit(
            QuestionModelForm, MatchingModelForm
        )
        if is_valid:
            reverse_url = reverse("TestingSystem:tests")
            return redirect(reverse_url)
    else:
        form = QuestionModelForm(instance=question)
        matching_forms = [
            MatchingModelForm(instance=option, prefix=f"option_{option.uid}")
            for option in options
        ]
    return render(
        request,
        "testingsystem/question_edit.html",
        {
            "form": form,
            "option_forms": matching_forms,
            "question_type": "matching",
        },
    )


@login_required_decorator
def TestViews(request):
    user_profile = request.user
    test = TestModel.objects.all()
    if request.method == "GET":
        if request.GET.get("alpabetical", None) == "True":
            sorted_test = test.order_by("title")
        elif request.GET.get("resent", None) == "True":
            sorted_test = test.order_by("-created_at")
        else:
            sorted_test = test
    else:
        sorted_test = test
    request.session["previous_url"] = request.path
    return render(
        request,
        "testingsystem/Test.html",
        {"objects": sorted_test, "user_profile": user_profile},
    )


# @login_required_decorator
# def main_page(request):
#     user_profile = request.user
#     return render(
#         request, "testingsystem/Main_Page.html", {"user_profile": user_profile}
#     )


@login_required_decorator
def QuestionView(request, test_id, test_description):
    test = get_object_or_404(TestModel, pk=test_id, slug=test_description)
    questions = QuestionModel.objects.filter(test=test)
    previous_intro = TestIntroductionModel.objects.first()
    if request.method == "GET":
        deletequestionId = request.GET.get("questionIdDelete", None)
        if deletequestionId is not None:
            try:
                dquestion_instance = QuestionModel.objects.get(
                    pk=int(deletequestionId.split("-")[0])
                )
                test.questions.remove(dquestion_instance)
            except QuestionModel.DoesNotExist:
                print("Question not found.")
    if request.method == "POST":
        deleteTestId = request.POST.get("status", None)
        if deleteTestId is not None and "Delete this Test" == deleteTestId:
            test.delete()
            reverse_url = reverse("TestingSystem:tests")
            return redirect(reverse_url)

        form = (
            TestIntroductionModelForm(
                request.POST,
                instance=previous_intro,
                prefix=f"option_{previous_intro.id}",
            )
            if previous_intro
            else TestIntroductionModelForm(request.POST)
        )
        if form.is_valid():
            model = form.save(commit=False)
            model.test = test
            model.save()

        update_test_name = request.POST.get("update_test_name", None)
        if update_test_name is not None:
            test.title = update_test_name
            test.save()

        duplicate_test_name = request.POST.get("duplicate_test_name", None)
        duplicate_questions = request.POST.get("duplicate_questions", None)
        if duplicate_test_name is not None and duplicate_questions is not None:
            if duplicate_questions == "yes":
                duplicated_test = test.duplicate_test(duplicate_test_name, "Copies")
            elif duplicate_questions == "no":
                duplicated_test = test.duplicate_test(duplicate_test_name, "Same")
            reverse_url = reverse("TestingSystem:tests")
            return redirect(reverse_url)

    q_and_a = [
        {
            "Q_ID": question.id,
            "Q_N": idx + 1,
            "question_description": question.slug,
            "text": question.text,
            "ranking": question.ranking,
            "qtype": question.question_type,
            "answers": [
                answers
                for answers in list(question.options.all())
                + list(question.freetext.all())
                + list(question.truefalse.all())
                + list(question.matching.all())
            ],
        }
        for idx, question in enumerate(questions)
    ]
    form = (
        TestIntroductionModelForm(
            instance=previous_intro, prefix=f"option_{previous_intro.id}"
        )
        if previous_intro
        else TestIntroductionModelForm()
    )
    context = {
        "test_name": test.title,
        "slug": test.slug,
        "test_id": test.id,
        "questions": q_and_a,
        "assign_items": test.assign_link_test.all(),
        "form": form,
    }
    return render(request, "testingsystem/EditTest.html", context=context)


def send_email_view(request):
    if request.method == "POST":
        subject = request.POST.get("subject")
        from_email = "your-email@example.com"  # Replace with your sender email
        to_email = request.POST.get("to_email")  # The recipient's email
        message = render_to_string("testingsystem/email_template.html")
        email = EmailMessage(subject, message, from_email, to=[to_email])
        email.content_subtype = "html"
        email.send()
        return render(
            request,
            "testingsystem/new_content.html",
            {"message": "Email sent successfully!"},
        )
    return render(request, "testingsystem/initial_content.html")


@login_required_decorator
def profile(request):
    superuser = get_object_or_404(CustomUser, pk=request.user.id)
    if request.method == "POST":
        user_form = CustomUserChangeForm(
            request.POST, request.FILES, instance=superuser
        )
        password_form = CustomPasswordChangeForm(request.user, request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Profile updated successfully.")
            if password_form.is_valid():
                new_password = password_form.cleaned_data["new_password1"]
                if new_password:
                    password_form.save()
                    update_session_auth_hash(request, superuser)
                    messages.success(request, "Password updated successfully.")
                else:
                    messages.info(request, "Password remains unchanged.")
            return redirect("TestingSystem:dashboard")
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        user_form = CustomUserChangeForm(instance=superuser)
        password_form = CustomPasswordChangeForm(request.user)

    return render(
        request,
        "testingsystem/profileEdit.html",
        {
            "user_profile": superuser,
            "user_form": user_form,
            "password_form": password_form,
        },
    )


@login_required_decorator
def QuestionsView(request):
    questions = QuestionModel.objects.all()
    user = request.user
    filter_data = {}
    if request.method == "GET":
        filterQueryValue = request.GET.get("filter_query", "")
        filterStatusValue = request.GET.get("filter_status", "")
        filterQtypeValue = request.GET.get("filter_qtype", "")

        permanetlyDeleteId = request.GET.get("permanetdelete", "")
        filter_data = {
            "filter_query": filterQueryValue,
            "filter_status": filterStatusValue,
            "filter_qtype": filterQtypeValue,
        }
        if filterQueryValue:
            questions = questions.filter(text__startswith=filterQueryValue)
        if filterQtypeValue:
            questions = questions.filter(question_type=filterQtypeValue)
        if permanetlyDeleteId:
            dlQuestion = QuestionModel.objects.filter(pk=int(permanetlyDeleteId))
            dlQuestion.delete()
            return redirect(reverse("TestingSystem:questions-views"))

    elif request.method == "POST":
        selectTestId = request.POST.get("test_id", None)
        duplicateQuestionId, duplicateQTestId = request.POST.get(
            "dpq_question_id", None
        ), request.POST.get("dpq_test_id", None)
        if selectTestId is not None:
            test = get_object_or_404(TestModel, pk=selectTestId)
            return redirect(
                reverse(
                    "TestingSystem:create-multiple",
                    kwargs={
                        "test_id": int(selectTestId),
                        "test_description": test.slug,
                    },
                )
            )
        elif duplicateQuestionId is not None and duplicateQTestId is not None:
            dpQuestion = questions.get(id=int(duplicateQuestionId))
            dpTest = TestModel.objects.get(id=int(duplicateQTestId))
            dpQuestion.duplicate_question(dpTest)
            return redirect(
                reverse(
                    "TestingSystem:questions",
                    kwargs={"test_id": dpTest.id, "test_description": dpTest.slug},
                )
            )

    q_and_a = [
        {
            "Q_ID": question.id,
            "Q_N": idx + 1,
            "question_description": question.slug,
            "text": question.text,
            "ranking": question.ranking,
            "qtype": question.question_type,
            "tests": question.test.all(),
            "answers": [
                answers
                for answers in list(question.options.all())
                + list(question.freetext.all())
                + list(question.truefalse.all())
                + list(question.matching.all())
            ],
        }
        for idx, question in enumerate(questions)
    ]
    uniqueTests = TestModel.objects.all()
    return render(
        request,
        "testingsystem/QuestionBank.html",
        context={
            "questions": q_and_a,
            "user_profile": user,
            "tests": uniqueTests,
            "filter_data": filter_data,
        },
    )


@login_required_decorator
def LinksView(request):
    assign = AssignLinkModel.objects.all()
    user = request.user
    if request.method == "GET":
        if request.GET.get("alpabetical", None) == "True":
            sorted_test = assign.order_by("assign_name")
        elif request.GET.get("resent", None) == "True":
            sorted_test = assign.order_by("-created_at")
        else:
            sorted_test = assign
    else:
        sorted_test = assign
    request.session["previous_url"] = request.path
    return render(
        request,
        "testingsystem/Links.html",
        {"objects": sorted_test, "user_profile": user},
    )


@login_required_decorator
def Dashboard(request):
    user = request.user
    return render(request, "testingsystem/Dashboard.html", {"user_profile": user})


@login_required_decorator
def StatisticsByTest(request):
    tests = TestModel.objects.all()
    test_statistics = dict()
    for test in tests:
        analyse_utils = AnalyseUtils(None)
        links = test.assign_link_test.all()
        avarege_percentage_by_link, avarege_score_by_link, mean_duration_by_link = (
            [],
            [],
            [],
        )
        for link in links:
            analyse_build = Analyse(link)

            avarege_by_link = analyse_build.Statistic()

            avarege_percentage_by_link.append(avarege_by_link["avarege_percentage"])

            avarege_score_by_link.append(avarege_by_link["avarege_score"])

            mean_duration_by_link.append(
                timedelta(
                    hours=int(avarege_by_link["mean_duration"].split(":")[0]),
                    minutes=int(avarege_by_link["mean_duration"].split(":")[1]),
                    seconds=int(avarege_by_link["mean_duration"].split(":")[2]),
                )
            )
        test_statistic = dict(
            avarege_percentage=np.mean(avarege_percentage_by_link),
            avarege_score=np.mean(avarege_score_by_link),
            mean_duration=analyse_utils._durationsAvarege(mean_duration_by_link),
        )

        test_statistics[test] = test_statistic
    try:
        order_by = [*request.GET][0]
    except:
        order_by = None

    sortby = SortBy(test_statistics)
    order = request.GET.get(order_by, None)
    if order_by and order:
        order_inverse = {"desc": False, "asc": True}[order]
        sorted_result = sortby.sortDescAsc(order_by, order_inverse)
        sortorders = dict(order=order, order_by=order_by)
    else:
        sorted_result = sortby.sortDescAsc(order_by="avarege_percentage")
        sortorders = dict(order=False, order_by="avarege_percentage")
    context = {
        "statistics": sorted_result,
        "responce": "Test",
        "sort_orders": sortorders,
    }
    return render(request, "testingsystem/statistics.html", context=context)


@login_required_decorator
def StatisticsByLinks(request):
    links = AssignLinkModel.objects.all()
    link_statistics = dict()
    for link in links:
        analyse_build = Analyse(link)
        avarege_by_link = analyse_build.Statistic()
        link_statistics[link] = avarege_by_link
    try:
        order_by = [*request.GET][0]
    except:
        order_by = None
    sortby = SortBy(link_statistics)
    order = request.GET.get(order_by, None)

    if order_by and order:
        order_inverse = {"desc": False, "asc": True}[order]
        sorted_result = sortby.sortDescAsc(order_by, order_inverse)
        sortorders = dict(order=order, order_by=order_by)
    else:
        sorted_result = sortby.sortDescAsc(order_by="avarege_percentage")
        sortorders = dict(order=False, order_by="avarege_percentage")
    context = {
        "statistics": sorted_result,
        "responce": "Link",
        "sort_orders": sortorders,
    }
    return render(request, "testingsystem/statistics.html", context=context)


@login_required_decorator
def StatisticsByQuestions(request, test_id, test_description):
    test = get_object_or_404(TestModel, pk=test_id, slug=test_description)
    questions = test.questions.all()
    test_statistics = dict()
    for test in questions:
        analyse_utils = AnalyseUtils(None)
        links = test.assign_link.all()
        avarege_persentage_by_link, avarege_score_by_link, mean_duration_by_link = (
            [],
            [],
            [],
        )
        for link in links:
            analyse_build = Analyse(link)

            avarege_by_link = analyse_build.Statistic()

            avarege_persentage_by_link.append(avarege_by_link["avarege_persentage"])

            avarege_score_by_link.append(avarege_by_link["avarege_score"])

            mean_duration_by_link.append(
                timedelta(
                    hours=int(avarege_by_link["mean_duration"].split(":")[0]),
                    minutes=int(avarege_by_link["mean_duration"].split(":")[1]),
                    seconds=int(avarege_by_link["mean_duration"].split(":")[2]),
                )
            )
        test_statistic = dict(
            avarege_persentage=np.mean(avarege_persentage_by_link),
            avarege_score=np.mean(avarege_score_by_link),
            mean_duration=analyse_utils._durationsAvarege(mean_duration_by_link),
        )

        test_statistics[test] = test_statistic

    context = {"statistics": test_statistics}
    return render(request, "testingsystem/statistics.html", context=context)


@login_required_decorator
def StatsHome(request):
    return render(request, "testingsystem/StatsHome.html")


def main(request):
    return render(request, "index.html")


import hmac
import hashlib
import base64
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def verify_payload(payload, header_hmac_signature):
    webhook_secret = "YOUR_CLASSMARKER_WEBHOOK_SECRET_PHRASE"
    dig = hmac.new(
        webhook_secret.encode(), msg=payload, digestmod=hashlib.sha256
    ).digest()
    calculated_signature = base64.b64encode(dig).decode().encode("ascii", "ignore")

    if "," in header_hmac_signature:
        header_hmac_signature = header_hmac_signature.split(",")[0]

    return hmac.compare_digest(calculated_signature, header_hmac_signature)


@csrf_exempt
def webhook_view(request):
    print("Received webhook request")

    hmac_header = request.META.get("HTTP_X_CLASSMARKER_HMAC_SHA256")

    if verify_payload(request.body, hmac_header):
        print("200")
        return HttpResponse("OK", status=200)
    else:
        print("400")
        return HttpResponse("Fail", status=400)
