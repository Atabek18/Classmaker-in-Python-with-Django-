from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import UserResponseScore
from TestingSystem.models import QuestionModel
from UserResponse.models import (
    UserAnswerToMultipleChoiceModel,
    UserAsnwerToTrueFalseModel,
    UserAnswerToFreeTextModel,
    UserAnswerToMatchingModel,
    UserRegisterModel,
)
from AssignLinks.models import AssignLinkModel
from TestingSystem.models import MatchingModel
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def score(request, user_id, assign_slug):
    assign_model = get_object_or_404(AssignLinkModel, slug_field=assign_slug)
    user = get_object_or_404(UserRegisterModel, pk=user_id)
    mo_questions = user.user_multiple.all()
    tf_questions = user.user_truefalse.all()
    fr_questions = user.user_freetext.all()
    mch_questions = user.user_matching.all()
    questions = []
    for mo in mo_questions:
        question = mo.question_based
        answers = []
        question_type = "options"
        if mo.answer_based.is_correct:
            for option in question.options.all():
                is_correct = True if option.is_correct else None
                answers.append({option.answer: is_correct})
        else:
            for option in question.options.all():
                is_correct = True if option.is_correct else False if mo.answer_based == option else None
                answers.append({option.answer: is_correct})
        question_data = {
            "question": question,
            "type": question_type,
            "answers": answers,
        }
        questions.append(question_data)

    for tf in tf_questions:
        question = tf.question_based
        question_type = "true_false"
        if tf.answer_based:
            if tf.question_based.truefalse.first().true:
                answers = {'True': True, 'False': None}
            else:
                answers = {'True': False, 'False': True}
        else:
            if tf.question_based.truefalse.first().false:
                answers = {'True': None, 'False': True}
            else:
                answers = {'True': True, 'False': False}
        question_data = {
            "question": question,
            "type": question_type,
            "answers": [answers],
        }
        questions.append(question_data)


    for fr in fr_questions:
        question = fr.question_based
        question_type = "free_text"
        if fr.answer_based == question.freetext.first().freetext:
            answers = [{fr.answer_based: True}]
        else:
            answers = [{fr.answer_based: False, question.freetext.first().freetext: True}]

        question_data = {
            "question": question,
            "type": question_type,
            "answers": answers,
        }

        questions.append(question_data)

    pair_data = {i.question_based: {'user_pairs': []} for i in mch_questions}
    for mch in mch_questions:
        pair_data[mch.question_based]['user_pairs'].append({mch.answer_based:{mch.left_item: mch.right_item}})
    for model, matchings in pair_data.items():
        exmaple = dict()
        correct_answers = model.matching.all()
        user_p = matchings['user_pairs']
        exmaple['question'] = model
        exmaple['type'] = 'matching'
        exmaple['answers'] = []
        for match in user_p:
            up_model, modify = list(match.items())[0]
            user_left_item, user_right_item = list(modify.items())[0]
            is_valid = correct_answers.filter(pk=up_model.id, left_item=user_left_item, right_item=user_right_item).exists()
            exmaple['answers'].append(dict(left_item=user_left_item, right_item=user_right_item, is_correct=is_valid))
        questions.append(exmaple)
    

    # for tf in tf_questions:
    #     if tf.answer_based:
    #         if tf.question_based.truefalse.first().true:
    #             show_answers[tf.question_based.id] = dict(model=[tf], is_correct=[True])
    #         else:
    #             show_answers[tf.question_based.id] = dict(model=[tf], is_correct=[False])
    #     else:
    #         if tf.question_based.truefalse.first().false:
    #             show_answers[tf.question_based.id] = dict(model=[tf], is_correct=[True])
    #         else:
    #             show_answers[tf.question_based.id] = dict(
    #                 model=[tf], is_correct=[False]
    #             )

    # for fr in fr_questions:
    #     if fr.answer_based == fr.question_based.freetext.first().freetext:
    #         show_answers[fr.question_based.id] = dict(model=[fr], is_correct=[True])
    #     else:
    #         show_answers[fr.question_based.id] = dict(model=[fr], is_correct=[False])


    # user_pairs, correct_pairs = {i.question_based.id: [] for i in mch_questions}, {
    #     i.question_based.id: [] for i in mch_questions
    # }

    # for mch in mch_questions:
    #     user_pairs[mch.question_based.id].append({mch: {mch.left_item: mch.right_item}})
    #     correct_pairs[mch.question_based.id].append(
    #         {mch: {mch.answer_based.left_item: mch.answer_based.right_item}}
    #     )


    # for user_pair, correct_pair in zip(user_pairs.items(), correct_pairs.items()):
    #     (user_pair_id, answers_user), (correct_pair_id, answers_correct) = (
    #         user_pair,
    #         correct_pair,
    #     )
        
    #     answers_user_matched, answers_correct_matched = [
    #         list(au.items()) for au in answers_user
    #     ], [list(ac.items()) for ac in answers_correct]
    #     all_correted = []
    #     for aum, acm in zip(answers_user_matched, answers_correct_matched):
    #         if not aum[0][1] == acm[0][1]:
    #             all_correted.append(False)
    #         else:
    #             all_correted.append(True)
    #     if all(all_correted) and user_pair_id == correct_pair_id:
    #         show_answers[correct_pair_id] = dict(
    #             model=[i[0][0] for i in answers_user_matched], is_correct=all_correted
    #         )
    #     else:
    #         show_answers[correct_pair_id] = dict(
    #             model=[i[0][0] for i in answers_user_matched], is_correct=all_correted
    #         )

    given_questions = (
        user.assign.test_foreign.test_random.all().order_by("order")
        if assign_model.display_each_question.randomize
        else user.assign.test_foreign
    )
    answer_questions = []
    for random_q in given_questions:
        matching_question = [q for q in questions if q['question'].id == random_q.id]
        if matching_question:
            answer_questions.append(matching_question[0])

    # answer_questions = dict()
    # for random_q in given_questions:
    #     if questions.get(random_q.id, None):
    #         answer_questions[random_q.id] = questions.get(random_q.id, None)

    # data = []
    # for i, j in answer_questions.items():
    #     question_data = {
    #         "question": j["model"][0].question_based.text,
    #         "type": "options"
    #         if j["model"][0].question_based.options.all()
    #         else "truefalse"
    #         if j["model"][0].question_based.truefalse.all()
    #         else "matching"
    #         if j["model"][0].question_based.matching.all()
    #         else "freetext",
    #     }

    #     if all(j["is_correct"]):
    #         if question_data["type"] == "options":
    #             question_data["answers"] = [
    #                 {i.answer: True if i.is_correct else None}
    #                 for i in j["model"][0].question_based.options.all()
    #             ]
    #         elif question_data["type"] == "truefalse":
    #             question_data["answers"] = [
    #                 {
    #                     "True": True if i.true else None,
    #                     "False": True if i.false else None,
    #                 }
    #                 for i in j["model"][0].question_based.truefalse.all()
    #             ]
    #         elif question_data["type"] == "matching":
    #             question_data["answers"] = [
    #                 {
    #                     "left_item": option.left_item,
    #                     "right_item": option.right_item,
    #                     "is_selected": True,
    #                 }
    #                 for option in j["model"]
    #             ]
    #         else:
    #             question_data["answers"] = [
    #                 {i.answer_based: True}
    #                 for i in j["model"][0].question_based.freetext.all()
    #             ]
    #     else:
    #         if question_data["type"] == "options":
    #             question_data["answers"] = [
    #                 {
    #                     i: False
    #                     if i.answer == j["model"][0].answer_based.answer
    #                     else True
    #                     if i.is_correct
    #                     else None
    #                 }
    #                 for i in j["model"][0].question_based.options.all()
    #             ]
    #         elif question_data["type"] == "truefalse":
    #             question_data["answers"] = [
    #                 {
    #                     "True": True if i.true else False,
    #                     "False": True if i.false else False,
    #                 }
    #                 for i in j["model"][0].question_based.truefalse.all()
    #             ]
    #         elif question_data["type"] == "matching":
    #             question_data["answers"] = [
    #                 {
    #                     "left_item": option.left_item,
    #                     "right_item": option.right_item,
    #                     "is_selected": corrects,
    #                 }
    #                 for option, corrects in zip(j["model"], j["is_correct"])
    #             ]
    #         else:
    #             question_data["answers"] = [
    #                 {i.freetext: True, j["model"][0].answer_based: False}
    #                 for i in j["model"][0].question_based.freetext.all()
    #             ]

    #     data.append(question_data)
    return render(request, "userscore/score.html", {"data": answer_questions})


def send_email_view(*, from_email: str, to_email: list[str], userInfo: dict) -> bool:
    subject = "Astrum Test"
    message = render_to_string("userscore/email_template.html", userInfo)
    email = EmailMessage(subject, message, from_email, to=to_email)
    email.content_subtype = "html"
    try:
        email.send()
        return True
    except:
        return False


def TestRanks(model):
    allQuestion = model.questions.all()
    ranks = 0
    for i in allQuestion:
        ranks += i.ranking
    return ranks


def UserScoreResults(request, user_id, assign_slug):
    assign_model = get_object_or_404(AssignLinkModel, slug_field=assign_slug)
    user = get_object_or_404(UserRegisterModel, pk=user_id)
    score = 0
    ranks = TestRanks(assign_model.test_foreign)
    mo_questions = user.user_multiple.all()
    tf_questions = user.user_truefalse.all()
    fr_questions = user.user_freetext.all()
    mch_questions = user.user_matching.all()
    for mo in mo_questions:
        if mo.answer_based.is_correct:
            score += mo.question_based.ranking

    for tf in tf_questions:
        if tf.answer_based:
            if tf.question_based.truefalse.first().true:
                score += tf.question_based.ranking
        else:
            if tf.question_based.truefalse.first().false:
                score += tf.question_based.ranking

    for fr in fr_questions:
        if fr.answer_based == fr.question_based.freetext.first().freetext:
            score += fr.question_based.ranking

    # user_pairs, correct_pairs = {i.question_based.id:[] for i in mch_questions}, {i.question_based.id:[] for i in mch_questions}
    # for mch in mch_questions:
    #     user_pairs[mch.question_based.id].append(dict(mch={mch.left_item: mch.right_item}))
    #     correct_pairs[mch.question_based.id].append({mch:{mch.answer_based.left_item: mch.answer_based.right_item}})
    # for user_pair, correct_pair in zip(user_pairs.items(), correct_pairs.items()):
    #     (user_pair_id, answers_user), (correct_pair_id, answers_correct) = user_pair, correct_pair
    #     answers_user_matched,  answers_correct_matched = [list(au.items()) for au in answers_user], [list(ac.items()) for ac in answers_correct]
    #     all_correted = []
    #     for aum, acm in zip(answers_user_matched, answers_correct_matched):
    #         if not aum[0][1] == acm[0][1]:
    #             all_correted.append(False)
    #         else:
    #             all_correted.append(True)
    #     question_point = Question.objects.get(pk=correct_pair_id)
    #     if all(all_correted) and user_pair_id == correct_pair_id:
    #         score += question_point.ranking

    pair_data = {i.question_based: {'user_pairs': []} for i in mch_questions}
    for mch in mch_questions:
        pair_data[mch.question_based]['user_pairs'].append({mch.answer_based:{mch.left_item: mch.right_item}})
    for model, matchings in pair_data.items():
        correct_answers = model.matching.all()
        user_p = matchings['user_pairs']
        for match in user_p:
            up_model, modify = list(match.items())[0]
            user_left_item, user_right_item = list(modify.items())[0]
            is_valid = correct_answers.filter(pk=up_model.id, left_item=user_left_item, right_item=user_right_item).exists()
            if not is_valid:
                break
        if is_valid:
            score+=model.ranking


    persentage = (score / ranks) * 100
    is_passed = (
        True
        if assign_model.test_completion.pass_mark <= round(persentage, 1)
        else False
    )
    feedback = (
        assign_model.test_completion.send_completed_message
        if is_passed
        else assign_model.test_completion.send_not_completed_message
    )
    try:
        model = UserResponseScore(
            user=user,
            score=score,
            ranks=ranks,
            persentage=round(persentage, 1),
            is_passed=is_passed,
        )
        model.save()
    except:
        pass
    data = {
        "user_id": user.id,
        "assign_slug": assign_model.slug_field,
        "name": user.name,
        "surname": user.surname,
        "score": score,
        "ranks": ranks,
        "percentage": persentage,
        "duration": "",
        "started": "",
        "finished": "",
        "feedback": feedback,
    }
    is_sended = send_email_view(
        from_email="your-email@example.com", to_email=[user.email], userInfo=data
    )
    return render(request, "userscore/UserScore.html", data)





def analyse(id):
    user = get_object_or_404(UserRegisterModel, pk=id)
    mo_questions = user.user_multiple.all()
    tf_questions = user.user_truefalse.all()
    fr_questions = user.user_freetext.all()
    mch_questions = user.user_matching.all()
    {
    "state": "test_complete",
    "data": {
        "result": {
            "test_sections": [
                {
                    "pages": [
                        {
                            "page": 1,
                            "prev_question_count": 0,
                            "contents": [
                                {
                                    "id": 34888237,
                                    "type": "question",
                                    "sub_type": "truefalse",
                                    "question": "asdfasdfa",
                                    "user_answer": "be0250beec44a920e03ff29776bc1756",
                                    "options": [
                                        {
                                            "id": "be0250beec44a920e03ff29776bc1756",
                                            "content": "True"
                                        },
                                        {
                                            "id": "5aa0b14581d27e64dfe91c1f474780b8",
                                            "content": "False"
                                        }
                                    ],
                                }
                            ]
                        },
                        {
                            "page": 3,
                            "prev_question_count": 2,
                            "contents": [
                                {
                                    "id": 35023834,
                                    "type": "question",
                                    "sub_type": "multiplechoice",
                                    "question": "asdad",
                                    "user_answer": "60ae8025111af3db10d930b536c05bb8",
                                    "options": [
                                        {
                                            "id": "60ae8025111af3db10d930b536c05bb8",
                                            "content": "2"
                                        },
                                        {
                                            "id": "2be2dafc350d8fcc16a1575623a30706",
                                            "content": "4"
                                        },
                                        {
                                            "id": "39bafdd9c4ca353e5d22ed0b8dbbbb0a",
                                            "content": "3"
                                        },
                                        {
                                            "id": "037218e767c860789c1360883b41dd19",
                                            "content": "1"
                                        }
                                    ],
                                }
                            ]
                        },
                        {
                            "page": 4,
                            "prev_question_count": 3,
                            "contents": [
                                {
                                    "id": 35025166,
                                    "type": "question",
                                    "sub_type": "freetext",
                                    "category": None,
                                    "question": "sfsafsasdf",
                                    "user_answer": "sadasda",
                                    "has_bookmarked": False,
                                    "points": None,
                                }
                            ]
                        },
                        {
                            "page": 5,
                            "prev_question_count": 4,
                            "contents": [
                                {
                                    "id": 35025236,
                                    "type": "question",
                                    "sub_type": "matching",
                                    "category": None,
                                    "question": "Match the options below:",
                                    "user_answer": {
                                        "user_answer": {
                                            "402c3862b0366152f654c5ff8fdb2956": "18378d7a513b5b6dc8a20b5445a13068",
                                            "2adf4f76eacf8f5c412186c9fba40d38": "ae669082d865302ff9dc94df2cf4bb47",
                                            "dbba6bc8fd89b885275a5e1de369a9ab": "d3ab9434978a9d7f434edd2bb729afac"
                                        }
                                    },
                                    "has_bookmarked": False,
                                    "points": None,
                                    "matching_style": "Multimedia",
                                    "options": {
                                        "matches": [
                                            {
                                                "id": "18378d7a513b5b6dc8a20b5445a13068",
                                                "content": "asdfasdfadsf"
                                            },
                                            {
                                                "id": "ae669082d865302ff9dc94df2cf4bb47",
                                                "content": "asdf"
                                            },
                                            {
                                                "id": "d3ab9434978a9d7f434edd2bb729afac",
                                                "content": "asdfdasf"
                                            }
                                        ],
                                        "clues": [
                                            {
                                                "id": "402c3862b0366152f654c5ff8fdb2956",
                                                "content": "asdas"
                                            },
                                            {
                                                "id": "2adf4f76eacf8f5c412186c9fba40d38",
                                                "content": "asdfa"
                                            },
                                            {
                                                "id": "dbba6bc8fd89b885275a5e1de369a9ab",
                                                "content": "asdfasf"
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    ],
                    "settings": []
                }
            ],
            "test_feedback": "",
            "points_scored": 1,
            "points_available": 5,
            "points_percentage": 20,
            "date_started": "Sat 20 Jan '24 21:07",
            "date_finished": "Sat 20 Jan '24 21:10",
            "duration_in_sec": 192,
            "duration": "00:03:12",
            "question_feedbacks": {
                "34888237": {
                    "question_id": 34888237,
                    "feedback": "",
                    "point_scored": 1,
                    "point_percentage": 100,
                    "correct_answer": "be0250beec44a920e03ff29776bc1756",
                    "full_mark": True,
                    "point_available": 1,
                    "has_bookmarked": False
                },
                "35023629": {
                    "question_id": 35023629,
                    "feedback": "",
                    "point_scored": 0,
                    "point_percentage": 0,
                    "correct_answer": "bfbc4aa81b6f1ae5696f43f03ce5165b",
                    "full_mark": True,
                    "point_available": 1,
                    "has_bookmarked": False
                },
                "35023834": {
                    "question_id": 35023834,
                    "feedback": "",
                    "point_scored": 0,
                    "point_percentage": 0,
                    "correct_answer": "2be2dafc350d8fcc16a1575623a30706",
                    "full_mark": False,
                    "point_available": 1,
                    "has_bookmarked": False
                },
                "35025166": {
                    "question_id": 35025166,
                    "feedback": "",
                    "point_scored": 0,
                    "point_percentage": 0,
                    "correct_answer": [
                        "qwqewq",
                        "121qqweq",
                        "qwadas"
                    ],
                    "full_mark": False,
                    "point_available": 1,
                    "has_bookmarked": False
                },
                "35025236": {
                    "question_id": 35025236,
                    "feedback": "",
                    "point_scored": 0,
                    "point_percentage": 0,
                    "correct_answer": {
                        "402c3862b0366152f654c5ff8fdb2956": "ae669082d865302ff9dc94df2cf4bb47",
                        "2adf4f76eacf8f5c412186c9fba40d38": "d3ab9434978a9d7f434edd2bb729afac",
                        "dbba6bc8fd89b885275a5e1de369a9ab": "18378d7a513b5b6dc8a20b5445a13068"
                    },
                    "full_mark": False,
                    "point_available": 1,
                    "has_bookmarked": False
                }
            },
            "pass": True,
        },
        "user": {
            "first_name": "Atabek",
            "last_name": "Abduakimov",
            "email": None,
        }
    },
    "language": [],
    "token": null
}
