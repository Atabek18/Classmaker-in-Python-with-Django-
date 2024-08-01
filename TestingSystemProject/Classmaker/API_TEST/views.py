from datetime import timedelta
from django.shortcuts import get_object_or_404, render
import pytz
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from AssignLinks.models import AssignLinkModel
from .view_helper import API_HELPER_JSON, RandomizeTest
from .serializers import UserRegisterModel
from UserResponse.models import (
    CurrentPageModel,
)
from django.urls import reverse
from TestingSystem.models import QuestionModel
from .authentication import JWTAuthentication
from .serializers import UserRegisterModelSerializer
from .permission import IsJWTTokenProvided
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect


class UserINFOListAPIView(APIView, JWTAuthentication):
    def post(self, request, *args, **kwargs):
        quiz_id = request.GET.get("quiz_id")
        assign_model = get_object_or_404(AssignLinkModel, slug_field=quiz_id)
        serializer = UserRegisterModelSerializer(data=request.data)
        if serializer.is_valid():
            modify_user_link = serializer.save(
                assign=assign_model, status="user_registered"
            )
            token = self.generate_student_token(modify_user_link)
            response_data = {
                "user": serializer.data,
                "token": token,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.utils import timezone


class StartListAPIView(APIView, JWTAuthentication):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsJWTTokenProvided]

    def post(self, request, *args, **kwargs):
        token = self.update_token()

        user_model = request.user
        user_model.status = "test_in_progress"
        user_model.save()

        quiz_id = self.get_anything_from_token("quiz_id")
        assign_model = get_object_or_404(AssignLinkModel, slug_field=quiz_id)
        availability = assign_model.availability_OTO
        attempts = assign_model.attempts_OTO
        restrictions = assign_model.restrictions_OTO
        print_copy_paste_translate = assign_model.print_copy_paste_translate_OTO
        display_each_question = assign_model.display_each_question_OTO
        instruction = assign_model.instruction_OTO
        limit_time = assign_model.limit_time_OTO
        results_page = assign_model.results_page_OTO
        pass_mark_and_feedback = assign_model.pass_mark_and_feedback_OTO
        email_results_instructor = assign_model.email_results_instructor_OTO
        taker_email_send = assign_model.taker_email_send_OTO
        test = assign_model.test_MTO
        uzb_zone = pytz.timezone("Asia/Tashkent")
        curr_dt = timezone.now().astimezone(uzb_zone) + timedelta(
            minutes=limit_time.minute
        )
        current_page_custom = CurrentPageModel(
            current_user=user_model, current_page=1, timestampt=curr_dt
        )
        current_page_custom.save()
        assign_tools = RandomizeTest(assign_model, user_model)
        assign_tools.randomize()
        questions = assign_tools.get_randomized_questions_for_student_or_manual()
        total_pages = assign_tools.get_total_pages()
        api_helper = API_HELPER_JSON(user_model, questions, total_pages)
        test_data = api_helper.StatusContinue()
        response_data = {
            "state": "test_in_progress",
            "settings": {
                "test": {
                    "test_type": "links",
                    "link_id": assign_model.id,
                    "test_id": test.id,
                    "time_limits": limit_time.minute * 60,
                    "display_time_limit": None,
                    "resume_later": False,
                    "display_points": False,
                    "questions_per_page": display_each_question.selected_number,
                    "must_answer_question": True,
                    "correct_to_continue": False,
                    "allow_click_previous": True,
                    "display_feedback_during_test": False,
                    "text_copy_allowed": False,
                    "text_paste_allowed": False,
                    "text_spell_check_allowed": False,
                    "browser_translation_allowed": False,
                    "print_allowed": False,
                    "timeout_timestamp": int(curr_dt.timestamp()),
                    "remaining_time": limit_time.minute * 60,
                    "passmark": pass_mark_and_feedback.pass_mark,
                    "num_of_questions": None,
                    "display_pretest_instruction": True,
                    "display_result_score": taker_email_send.point,
                    "display_results_incorrect_questions_only": True,
                },
            },
            "data": test_data,
            "token": token,
        }
        return Response(response_data, status=status.HTTP_200_OK)

class InitTestListAPIView(APIView, JWTAuthentication):
    def get(self, request, *args, **kwargs):
        return Response({"everything": "ok"}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        quiz_id = request.GET.get("quiz_id")
        student = self.get_student()
        assign_model = get_object_or_404(AssignLinkModel, slug_field=quiz_id)
        availability = assign_model.availability_OTO
        attempts = assign_model.attempts_OTO
        restrictions = assign_model.restrictions_OTO
        print_copy_paste_translate = assign_model.print_copy_paste_translate_OTO
        display_each_question = assign_model.display_each_question_OTO
        instruction = assign_model.instruction_OTO
        limit_time = assign_model.limit_time_OTO
        results_page = assign_model.results_page_OTO
        pass_mark_and_feedback = assign_model.pass_mark_and_feedback_OTO
        email_results_instructor = assign_model.email_results_instructor_OTO
        taker_email_send = assign_model.taker_email_send_OTO
        test = assign_model.test_MTO
        assign_tools = RandomizeTest(assign_model, student)
        questions = assign_tools.get_randomized_questions_for_student_or_manual()
        total_pages = assign_tools.get_total_pages()
        api_helper = API_HELPER_JSON(student, questions, total_pages)
        response_data = {
            "state": "",
            "settings": {
                "test": {
                    "test_type": "links",
                    "link_id": assign_model.id,
                    "test_id": test.id,
                    "time_limits": limit_time.minute,
                    "display_time_limit": None,
                    "resume_later": False,
                    "display_points": False,
                    "questions_per_page": display_each_question.selected_number,
                    "must_answer_question": True,
                    "correct_to_continue": False,
                    "allow_click_previous": True,
                    "display_feedback_during_test": False,
                    "text_copy_allowed": False,
                    "text_paste_allowed": False,
                    "text_spell_check_allowed": False,
                    "browser_translation_allowed": False,
                    "print_allowed": False,
                    "passmark": pass_mark_and_feedback.pass_mark,
                    "num_of_questions": None,
                    "display_pretest_instruction": True,
                    "display_result_score": taker_email_send.point,
                    "display_results_incorrect_questions_only": True,
                },
            },
            "data": [],
            "token": "",
        }

        token = self.generate_quiz_token(quiz_id)
        try:
            test_intro = test.test_intro.text
        except:
            test_intro = None
        test_state = "test_intro"
        test_data = {
            "test_intro": {
                "num_of_questions": 5,
                "test_instruction": test_intro,
                "attempts_allowed": attempts.attempts,
            },
            "user": {
                "first_name": "Atabek",
                "last_name": "Abduakimov",
                "email": "",
            },
        }
        if student is not None:
            token = self.generate_student_token(student)
            if student.status == "test_in_progress":
                test_data = api_helper.StatusContinue()
            elif student.status == "test_complete":
                test_data = api_helper.StatusFinished()
        response_data["data"] = test_data
        response_data["state"] = student.status if student else test_state
        response_data["token"] = token
        return Response(response_data, status=status.HTTP_200_OK)


class ContinueListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsJWTTokenProvided]

    def post(self, request, *args, **kwargs):
        user = request.user
        test_id = request.GET.get("test_id", None)
        link_id = request.GET.get("link_id", None)
        test_status = request.data.get("status", None)
        next_page = request.data.get("next_page", None)
        question_id = request.data.get("answers")[0].get("question_id", None)
        question_type = request.data.get("answers")[0].get("type", None)
        answer = request.data.get("answers")[0].get("answer", None)
        question = get_object_or_404(QuestionModel, pk=int(question_id))
        link = get_object_or_404(AssignLinkModel, pk=int(link_id))
        change_current_page = CurrentPageModel.objects.get(current_user=user)
        assign_tools = RandomizeTest(link, user)
        questions = assign_tools.get_randomized_questions_for_student_or_manual()
        total_pages = assign_tools.get_total_pages()
        api_helper = API_HELPER_JSON(user, questions, total_pages)
        save_status = api_helper._save_rt_answers(answer, question_type, question)
        if save_status == status.HTTP_404_NOT_FOUND:
            return Response(status=save_status)
        response_data = None
        if test_status == "continue":
            response_data = api_helper._get_test_progress_response()
            mcp = api_helper._modify_current_page(next_page, change_current_page)
            response_data["data"]["test"]["current_page"] = mcp
        elif test_status == "complete":
            response_data = {
                "state": "test_complete",
                "data": api_helper.StatusFinished(),
            }
            user.status = "test_complete"
            user.save()
        return Response(response_data, status=status.HTTP_200_OK)


from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def get_csrf_token(request):
    csrf_token = get_token(request)
    if csrf_token != None:
        return JsonResponse({"csrftoken": csrf_token})
    return Response(data={}, status=status.HTTP_400_BAD_REQUEST)
