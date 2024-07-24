from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from GenerateSecureKeys.GenerateSlug import generate_secure_slug
from TestingSystem.models import TestModel
from .models import (
    AssignLinkModel,
)
from .forms import (
    AvailabilityModelForm,
    AttemptsModelForm,
    RestrictionsModelForm,
    Print_copy_paste_translateModelForm,
    DisplayEachQuestionModelForm,
    InstructionModelForm,
    LimitTimeModelForm,
    ResultsPageModelForm,
    PassMarkAndFeedbackModelForm,
    EmailResultsInstructorModelForm,
    TakerEmailSendModelForm,
    AssignLinkModelForm,
)
from Login.views import login_required_decorator
from .view_helper import *


@login_required_decorator
def ShowLinks(request, test_id, test_description):
    test = get_object_or_404(TestModel, pk=test_id, slug=test_description)
    if request.method == "POST":
        availability_form = AvailabilityModelForm(request.POST)
        attempts_form = AttemptsModelForm(request.POST)
        restrictions_form = RestrictionsModelForm(request.POST)
        print_copy_paste_translate_form = Print_copy_paste_translateModelForm(
            request.POST
        )
        display_each_question_form = DisplayEachQuestionModelForm(request.POST)
        instruction_form = InstructionModelForm(request.POST)
        limit_time_form = LimitTimeModelForm(request.POST)
        results_page_form = ResultsPageModelForm(request.POST)
        pass_mark_and_feedback_form = PassMarkAndFeedbackModelForm(request.POST)
        email_results_intructor_form = EmailResultsInstructorModelForm(request.POST)
        taker_email_send_form = TakerEmailSendModelForm(request.POST)
        assign_link_form = AssignLinkModelForm(request.POST)
        valid_values = [
            availability_form.is_valid(),
            attempts_form.is_valid(),
            restrictions_form.is_valid(),
            print_copy_paste_translate_form.is_valid(),
            display_each_question_form.is_valid(),
            instruction_form.is_valid(),
            limit_time_form.is_valid(),
            results_page_form.is_valid(),
            pass_mark_and_feedback_form.is_valid(),
            email_results_intructor_form.is_valid(),
            taker_email_send_form.is_valid(),
            assign_link_form.is_valid(),
        ]
        if all(valid_values):
            availability_model_save = availability_form.save()
            attempts_model_save = attempts_form.save()
            restrictions_model_save = restrictions_form.save()
            print_copy_paste_translate_model_save = (
                print_copy_paste_translate_form.save()
            )
            display_each_question_model_save = display_each_question_form.save()
            instruction_model_save = instruction_form.save()
            limit_time_model_save = limit_time_form.save()
            results_page_model_save = results_page_form.save()
            pass_mark_and_feedback_model_save = pass_mark_and_feedback_form.save()
            email_results_intructor_model = email_results_intructor_form.save()
            taker_email_send_model_save = taker_email_send_form.save()
            assign_link_model_save = assign_link_form.save(commit=False)

            assign_link_model_save.availability_OTO = availability_model_save
            assign_link_model_save.attempts_OTO = attempts_model_save
            assign_link_model_save.restrictions_OTO = restrictions_model_save
            assign_link_model_save.print_copy_paste_translate_OTO = (
                print_copy_paste_translate_model_save
            )
            assign_link_model_save.display_each_question_OTO = (
                display_each_question_model_save
            )
            assign_link_model_save.instruction_OTO = instruction_model_save
            assign_link_model_save.limit_time_OTO = limit_time_model_save
            assign_link_model_save.results_page_OTO = results_page_model_save
            assign_link_model_save.pass_mark_and_feedback_OTO = (
                pass_mark_and_feedback_model_save
            )
            assign_link_model_save.email_results_instructor_OTO = (
                email_results_intructor_model
            )
            assign_link_model_save.taker_email_send_OTO = taker_email_send_model_save
            assign_link_model_save.test_MTO = test
            assign_link_model_save.save()
            return redirect(
                reverse(
                    "Assign:edit-assign",
                    kwargs={
                        "assign_id": assign_link_model_save.id,
                        "test_description": test_description,
                    },
                )
            )

    else:
        availability_form = AvailabilityModelForm()
        attempts_form = AttemptsModelForm()
        restrictions_form = RestrictionsModelForm()
        print_copy_paste_translatef_form = Print_copy_paste_translateModelForm()
        display_each_question_form = DisplayEachQuestionModelForm()
        instruction_form = InstructionModelForm()
        limit_time_form = LimitTimeModelForm()
        results_page_form = ResultsPageModelForm()
        pass_mark_and_feedback_form = PassMarkAndFeedbackModelForm()
        email_results_intructor_form = EmailResultsInstructorModelForm()
        taker_email_send_form = TakerEmailSendModelForm()
        assign_link_form = AssignLinkModelForm()
    return render(
        request,
        "assignlinks/LinksShow.html",
        context={
            "form": availability_form,
            "attempts_form": attempts_form,
            "restrictions_form": restrictions_form,
            "print_copy_paste_translatef_form": print_copy_paste_translatef_form,
            "display_each_question_form": display_each_question_form,
            "instruction_form": instruction_form,
            "limit_time_form": limit_time_form,
            "results_page_form": results_page_form,
            "pass_mark_and_feedback_form": pass_mark_and_feedback_form,
            "email_results_intructor_form": email_results_intructor_form,
            "taker_email_send_form": taker_email_send_form,
            "assign_link_form": assign_link_form,
        },
    )


@login_required_decorator
def ShowLinksEdit(request, assign_id, test_description):
    test = get_object_or_404(TestModel, slug=test_description)
    assign_link = get_object_or_404(AssignLinkModel, pk=assign_id)
    deleteCL = DeleteConfirmedLink(request.POST, "detele_link_id", assign_link)
    is_confirmed = deleteCL.DeleteLink()
    if is_confirmed:
        return redirect(reverse("TestingSystem:links-views"))
    copy = CopyLink(assign_link, "http://127.0.0.1:8000/start/online-test/{}/")
    copylink = copy.GivenLink()
    if request.method == "POST":
        assign_form = AssignLinkModelForm(request.POST, instance=assign_link)
        availability_form = AvailabilityModelForm(
            request.POST, instance=assign_link.availability_OTO
        )
        attempts_form = AttemptsModelForm(
            request.POST, instance=assign_link.attempts_OTO
        )
        restrictions_form = RestrictionsModelForm(
            request.POST, instance=assign_link.restrictions_OTO
        )
        print_copy_paste_translate_form = Print_copy_paste_translateModelForm(
            request.POST, instance=assign_link.print_copy_paste_translate_OTO
        )
        display_each_question_form = DisplayEachQuestionModelForm(
            request.POST, instance=assign_link.display_each_question_OTO
        )
        instruction_form = InstructionModelForm(
            request.POST, instance=assign_link.instruction_OTO
        )
        limit_time_form = LimitTimeModelForm(
            request.POST, instance=assign_link.limit_time_OTO
        )
        results_page_form = ResultsPageModelForm(
            request.POST, instance=assign_link.results_page_OTO
        )
        pass_mark_and_feedback_form = PassMarkAndFeedbackModelForm(
            request.POST, instance=assign_link.pass_mark_and_feedback_OTO
        )
        email_results_intructor_form = EmailResultsInstructorModelForm(
            request.POST, instance=assign_link.email_results_instructor_OTO
        )
        taker_email_send_form = TakerEmailSendModelForm(
            request.POST, instance=assign_link.taker_email_send_OTO
        )

        valid_values = all(
            [
                availability_form.is_valid(),
                attempts_form.is_valid(),
                restrictions_form.is_valid(),
                print_copy_paste_translate_form.is_valid(),
                display_each_question_form.is_valid(),
                instruction_form.is_valid(),
                limit_time_form.is_valid(),
                results_page_form.is_valid(),
                pass_mark_and_feedback_form.is_valid(),
                email_results_intructor_form.is_valid(),
                taker_email_send_form.is_valid(),
            ]
        )
        if valid_values:
            availability_model_save = availability_form.save()
            attempts_model_save = attempts_form.save()
            restrictions_model_save = restrictions_form.save()
            print_copy_paste_translate_model_save = (
                print_copy_paste_translate_form.save()
            )
            display_each_question_model_save = display_each_question_form.save()
            instruction_model_save = instruction_form.save()
            limit_time_model_save = limit_time_form.save()
            results_page_model_save = results_page_form.save()
            pass_mark_and_feedback_model_save = pass_mark_and_feedback_form.save()
            email_results_intructor_model = email_results_intructor_form.save()
            taker_email_send_model_save = taker_email_send_form.save()

    else:
        assign_form = AssignLinkModelForm(request.POST, instance=assign_link)
        availability_form = AvailabilityModelForm(instance=assign_link.availability_OTO)
        attempts_form = AttemptsModelForm(instance=assign_link.attempts_OTO)
        restrictions_form = RestrictionsModelForm(instance=assign_link.restrictions_OTO)
        print_copy_paste_translate_form = Print_copy_paste_translateModelForm(
            instance=assign_link.print_copy_paste_translate_OTO
        )
        display_each_question_form = DisplayEachQuestionModelForm(
            instance=assign_link.display_each_question_OTO
        )
        instruction_form = InstructionModelForm(instance=assign_link.instruction_OTO)
        limit_time_form = LimitTimeModelForm(instance=assign_link.limit_time_OTO)
        results_page_form = ResultsPageModelForm(instance=assign_link.results_page_OTO)
        pass_mark_and_feedback_form = PassMarkAndFeedbackModelForm(
            instance=assign_link.pass_mark_and_feedback_OTO
        )
        email_results_intructor_form = EmailResultsInstructorModelForm(
            instance=assign_link.email_results_instructor_OTO
        )
        taker_email_send_form = TakerEmailSendModelForm(
            instance=assign_link.taker_email_send_OTO
        )

    try:
        analyse_build = Analyse(assign_link)
        analyse_dict = analyse_build.Result()
        statistics_dict = analyse_build.Statistic()
        sortby = SortBy(analyse_dict)
        order_by = list(dict(request.GET).keys())
        order = list(dict(request.GET).values())
        if order_by and order:
            order_inverse = {"desc": False, "asc": True}[order[0][0]]
            sorted_result = sortby.sortDescAsc(order_by[0], order_inverse)
            sortorders = dict(order=order[0][0], order_by=order_by[0])
        else:
            sorted_result = sortby.sortDescAsc()
            sortorders = dict(order=False, order_by="percentage")
    except:
        statistics_dict = None
        sorted_result = None
        sortorders = None

    previous_url = request.session.get("previous_url", None)
    return render(
        request,
        "assignlinks/Settings.html",
        context={
            "test": test,
            "sort_orders": sortorders,
            "assign_name": assign_link.assign_name,
            "current_model": assign_link,
            "copylink": copylink,
            "previous_url": previous_url,
            "analyse_dict": sorted_result,
            "statistics_dict": statistics_dict,
            "assign_form": assign_form,
            "form": availability_form,
            "attempts_form": attempts_form,
            "restrictions_form": restrictions_form,
            "print_copy_paste_translate_form": print_copy_paste_translate_form,
            "display_each_question_form": display_each_question_form,
            "instruction_form": instruction_form,
            "limit_time_form": limit_time_form,
            "results_page_form": results_page_form,
            "pass_mark_and_feedback_form": pass_mark_and_feedback_form,
            "email_results_intructor": email_results_intructor_form,
            "taker_email_send_form": taker_email_send_form,
        },
    )
