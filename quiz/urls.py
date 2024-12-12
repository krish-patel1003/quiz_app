from django.urls import path
from quiz.views import QuizSessionView

urlpatterns = [
    path('start-quiz-sesion', QuizSessionView.as_view(), name="start-quiz-session")
]