from datetime import datetime, timedelta, timezone
import time
import pytz
from rest_framework import status
from UserResponse.models import (
    UserAnswerToMultipleChoiceModel,
    UserAsnwerToTrueFalseModel,
    UserAnswerToFreeTextModel,
    CurrentPageModel,
)
from TestingSystem.models import QuestionModel, TestQuestionRandomizeModel


class API_HELPER_JSON:
    def __init__(self, student, questions, total_page) -> None:
        self.st = student
        self.qt = questions
        self.tp = total_page
        self.total_questions = len(self.qt)

    def _get_contents(self, id, sub_type, question, user_answer) -> dict:
        contents = {
            "id": id,
            "type": "question",
            "sub_type": sub_type,
            "question": question,
            "user_answer": user_answer,
        }
        return contents

    def _modify_current_page(self, next_page, cp_model):
        current_page = cp_model.current_page
        modify_current_page = False
        if next_page == True and next_page is not None:
            if current_page < self.tp:
                modify_current_page = current_page + 1
        else:
            if current_page > 1:
                modify_current_page = current_page - 1
        if modify_current_page is not False:
            cp_model.current_page = modify_current_page
            cp_model.save()
            return modify_current_page
        return current_page

    def _get_test_progress_response(self):
        return {
            "state": "test_in_progress",
            "data": {
                "test": {
                    "total_pages": self.tp,
                    "current_page": 1,
                    "num_of_questions": self.total_questions,
                    "previous_page": 0,
                    "timeout_timestamp": None,
                    "remaining_time": 0,
                }
            },
            "language": [],
            "token": None,
        }

    def _save_rt_answers(self, answer, question_type, question):
        user = self.st
        if answer is not None:
            try:
                if question_type == "truefalse":
                    UserAsnwerToTrueFalseModel.create_or_update_answer(
                        user=user, question=question, answer=answer
                    )
                elif question_type == "option":
                    UserAnswerToMultipleChoiceModel.create_or_update_answer(
                        user=user, question=question, answer=answer
                    )
                elif question_type == "freetext":
                    UserAnswerToFreeTextModel.create_or_update_answer(
                        user=user, question=question, answer=answer
                    )
            except:
                return status.HTTP_404_NOT_FOUND
        else:
            return status.HTTP_404_NOT_FOUND

    def StatusFinished(self):
        questions = self.qt
        student = self.st
        question_feedback = {}
        data = {"pages": []}

        for idx, question in enumerate(questions):
            content = self._get_contents(
                question.id, question.question_type, question.text, ""
            )
            each_question_analysis = {}

            if question.truefalse.exists():
                content["options"] = [
                    {"id": tf.uid.hex, "content": tf.modify_truefalse_text}
                    for tf in question.truefalse.all()
                ]
                non_null_answer_truefalse = UserAsnwerToTrueFalseModel.objects.filter(
                    user=student, question_based=question
                ).first()
                if non_null_answer_truefalse:
                    content["user_answer"] = non_null_answer_truefalse.answer_based.hex
                    correct_answer, point, percentage = (
                        non_null_answer_truefalse.get_truefalse_feedback()
                    )
                    each_question_analysis.update(
                        {
                            "correct_answer": correct_answer,
                            "point_scored": point,
                            "point_percentage": percentage,
                            "point_available": question.ranking,
                        }
                    )

            elif question.freetext.exists():
                non_null_answer_freetext = UserAnswerToFreeTextModel.objects.filter(
                    user=student, question_based=question
                ).first()
                if non_null_answer_freetext:
                    content["user_answer"] = non_null_answer_freetext.answer_based
                    correct_answer, point, percentage = (
                        non_null_answer_freetext.get_freetext_feedback()
                    )
                    each_question_analysis.update(
                        {
                            "correct_answer": correct_answer,
                            "point_scored": point,
                            "point_percentage": percentage,
                            "point_available": question.ranking,
                        }
                    )

            elif question.options.exists():
                content["options"] = [
                    {"id": option.uid.hex, "content": option.answer}
                    for option in question.options.all()
                ]
                non_null_answer_multiplechoice = (
                    UserAnswerToMultipleChoiceModel.objects.filter(
                        user=student, question_based=question
                    )
                )
                if non_null_answer_multiplechoice:
                    answers = []
                    points = 0
                    percentages = 0
                    for answer in non_null_answer_multiplechoice:
                        answers.append(answer.answer_based.hex)
                        correct_answer, point, percentage = (
                            answer.get_multiplechoice_feedback()
                        )
                        each_question_analysis.update(
                            {
                                "correct_answer": correct_answer,
                                "point_scored": point,
                                "point_percentage": percentage,
                                "point_available": question.ranking,
                            }
                        )
                        points += point
                        percentages += percentage
                    content["user_answer"] = answers

            elif question.matching.exists():
                content["options"] = {
                    "matches": [
                        {"id": m.uid.hex, "content": m.right_item}
                        for m in question.matching.all()
                    ],
                    "clues": [
                        {"id": m.uid.hex, "content": m.left_item}
                        for m in question.matching.all()
                    ],
                }

            each_question_analysis.update(
                {
                    "question_id": str(question.id),
                    "feedback": "",
                    "has_bookmarked": False,
                     }
            )

            question_feedback[f"{question.id}"] = each_question_analysis
            data["pages"].append(
                {
                    "page": idx + 1,
                    "prev_question_count": idx,
                    "contents": [content],
                }
            )

        test_data = {
            "result": {
                "test_sections": [data],
                "test_feedback": "",
                "points_scored": 1,
                "points_available": 5,
                "points_percentage": 20,
                "date_started": "Sat 20 Jan '24 21:07",
                "date_finished": "Sat 20 Jan '24 21:10",
                "duration_in_sec": 192,
                "duration": "00:03:12",
                "question_feedback": question_feedback,
            },
            "user": {
                "first_name": student.name,
                "last_name": student.surname,
                "email": student.email,
            },
        }
        return test_data

    def StatusContinue(self):
        questions = self.qt
        student = self.st
        current_page = CurrentPageModel.objects.get(current_user=student)
        data = {"pages": []}
        for idx, question in enumerate(questions):
            content = self._get_contents(
                question.id, question.question_type, question.text, ""
            )
            if question.truefalse.exists():
                content["options"] = [
                    {"id": tf.uid.hex, "content": tf.modify_truefalse_text}
                    for tf in question.truefalse.all()
                ]
                non_null_answer_truefalse = UserAsnwerToTrueFalseModel.objects.filter(
                    user=student, question_based=question
                )
                if non_null_answer_truefalse.exists():
                    answer = non_null_answer_truefalse.first()
                    content["user_answer"] = answer.answer_based.hex

            elif question.freetext.exists():
                non_null_answer_freetext = UserAnswerToFreeTextModel.objects.filter(
                    user=student, question_based=question
                )
                if non_null_answer_freetext.exists():
                    answer = non_null_answer_freetext.first()
                    content["user_answer"] = answer.answer_based

            elif question.options.exists():
                content["options"] = [
                    {"id": option.uid.hex, "content": option.answer}
                    for option in question.options.all()
                ]
                non_null_answer_multiplechoice = (
                    UserAnswerToMultipleChoiceModel.objects.filter(
                        user=student, question_based=question
                    )
                )
                if non_null_answer_multiplechoice.exists():
                    content["user_answer"] = [
                        answer.answer_based.hex
                        for answer in non_null_answer_multiplechoice
                    ]

            elif question.matching.exists():
                content["options"] = {
                    "matches": [
                        {"id": m.uid.hex, "content": m.right_item}
                        for m in question.matching.all()
                    ],
                    "clues": [
                        {"id": m.uid.hex, "content": m.left_item}
                        for m in question.matching.all()
                    ],
                }
            data["pages"].append(
                {
                    "page": idx + 1,
                    "prev_question_count": idx,
                    "contents": [content],
                }
            )
        test_data = {
            "test": {
                "total_pages": self.tp,
                "current_page": current_page.current_page,
                "num_of_questions": len(questions),
                "sections": [data],
            },
            "user": {
                "first_name": student.name,
                "last_name": student.surname,
                "email": student.email,
            },
        }
        return test_data


class AssignUtils:
    def __init__(self, model) -> None:
        self.model = model
        self.is_randomize = self.model.display_each_question_OTO.randomize
        self.default_questions = self.model.test_MTO.questions.all()

    def _randomize(self, user_instance) -> None:
        if self.is_randomize:
            test_instance = self.model.test_MTO
            TestQuestionRandomizeModel.randomize_questions(user_instance, test_instance)

    def _setup_display_settings(self) -> int:
        amount_num_questions = len(self.default_questions)
        display_per_page_questions = (
            self.model.display_each_question_OTO.selected_number
        )
        if display_per_page_questions.isdigit():
            display_per_page_questions = int(display_per_page_questions)
        rest_question_page = (
            1 if amount_num_questions % display_per_page_questions else 0
        )
        total_pages = (
            amount_num_questions // display_per_page_questions
        ) + rest_question_page
        return total_pages


class RandomizeTest(AssignUtils):
    def __init__(self, model, user_instance) -> None:
        super(RandomizeTest, self).__init__(model)
        self.user_instance = user_instance

    def randomize(self) -> None:
        user = self.user_instance
        self._randomize(user)

    def get_randomized_questions_for_student_or_manual(self):
        """Retrieves the randomized question order saved for a student-test combination.

        Args:
            student: The student instance.
            test: The test instance.

        Returns:
            A list of QuestionModel instances in the randomized order, or an empty list if not found.
        """

        try:
            if self.is_randomize:
                randomized_question_order = TestQuestionRandomizeModel.objects.filter(
                    user=self.user_instance, test=self.model.test_MTO
                ).order_by("order")
                question_ids = [item.question_id for item in randomized_question_order]
                questions = QuestionModel.objects.filter(id__in=question_ids)
                return questions
            return self.default_questions
        except TestQuestionRandomizeModel.DoesNotExist:
            return (
                self.default_questions
            )  # No randomized order found for this student-test combination

    def get_total_pages(self):
        return self._setup_display_settings()


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


class SavePassInfo(TestPassUtils):
    def __init__(self, user, questions) -> None:
        super(SavePassInfo, self).__init__(user, questions)

    def TimerAvailability(self, start_date_and_time: list, end_date_and_time: list):
        return self._setTimerAvailability(
            start_date_and_time[0], start_date_and_time[1]
        ), self._setTimerAvailability(end_date_and_time[0], end_date_and_time[1])

    def SaveNeededTime(self, time, startDateTime, endDateTime, limited_time) -> None:
        self._savePassNeedTime(time, startDateTime, endDateTime, limited_time)
