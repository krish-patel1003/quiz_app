from django.urls import path
from quiz.views import *

urlpatterns = [
    path('quiz-sesion', QuizSessionView.as_view(), name="start-quiz-session"),
    path('list-quiz-questions', QuestionListView.as_view(), name="list-quiz-questions"),
    path('attempt', UserAttemptView.as_view(), name='attempt'),
    path('user-result', UserResultView.as_view(), name='user-result')

]