from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from quiz.models import QuizSession

# Create your views here.
class QuizSessionView(GenericAPIView):

    def post(self, request):

        user = request.user
        quiz_session = QuizSession.objects.create(user_id=user)
        quiz_session.save()
        return Response({
            "Quiz_session_id": quiz_session.uid,
            "Message": "New Quiz Sesssion Started"},
            status.HTTP_200_OK)