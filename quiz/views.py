from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from quiz.models import QuizSession
from quiz.serializers import *

# Create your views here.
class QuizSessionView(APIView):

    def post(self, request):
        user = request.user
        session = QuizSession.objects.create(user=user)
        session.add_random_questions()
        serializers = QuizSessionSerializer(session)
        return Response(serializers.data, status=status.HTTP_201_CREATED)
        

    def get(self, request, session_uid):
        try:
            session = QuizSession.objects.get(uid=session_uid)
            serializer = QuizSessionSerializer(session)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except QuizSession.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

class QuestionListView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserAttemptView(APIView):
    def post(self, request):
        serializer = UserAttemptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserResultView(APIView):
    def get(self, request, session_uid):
        try:
            result = UserResult.objects.get(quiz_session_id__uid=session_uid)
            serializer = UserResultSerializer(result)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserResult.DoesNotExist:
            return Response({"error": "Result not found"}, status=status.HTTP_404_NOT_FOUND)