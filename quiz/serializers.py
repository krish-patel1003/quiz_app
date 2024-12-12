from rest_framework import serializers
from quiz.models import *
from accounts.models import *


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['uid', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'answer']

class QuizSessionSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = QuizSession
        fields = ['uid', 'created_at', 'started_at', 'questions']

    def get_questions(self, obj):
        questions = QuizSessionQuestion.get_questions_for_session(obj)
        return QuestionSerializer(instance=questions, many=True).data

    
class UserAttemptSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAttempt
        fields = ['uid', 'quiz_session_id', 'question_id', 'user_response', 'is_correct']
        extra_kwargs = {
            "uid": {"read_only": True},
            "is_correct": {"read_only": True}
        }

    def create(self, validated_data):
        user_attempt = UserAttempt.objects.create(**validated_data)
        return user_attempt
    
class UserResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResult
        fields = ['uid', 'quiz_session_id', 'total_questions', 'questions_answered_correct', 'questions_answered_wrong']
        read_only_fields = ('uid', 'total_questions', 'questions_answered_correct', 'questions_answered_wrong',)