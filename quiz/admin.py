from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(QuizSession)
admin.site.register(Question)
admin.site.register(UserAttempt)
admin.site.register(UserResult)
