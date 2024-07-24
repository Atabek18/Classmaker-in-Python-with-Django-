from django.contrib import admin
from .models import (
    QuestionModel,
    OptionModel,
    FreeTextModel,
    TrueFalseModel,
    TestModel,
    CustomUser,
)

admin.site.register(QuestionModel)
admin.site.register(OptionModel)
admin.site.register(FreeTextModel)
admin.site.register(TrueFalseModel)
admin.site.register(TestModel)
admin.site.register(CustomUser)
