from rest_framework import serializers
from quiz.models import *
from accounts.models import *


class QuestionSerializer(serializers.Serializer):
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
        return questions
    
class UserAttemptSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = UserAttempt
        fields = ['uid', 'quiz_session_id', 'question', 'user_response', 'is_correct']

    def create(self, validated_data):
        question_data = validated_data.pop('question')
        question = Question.objects.get(uid=question_data['uid'])
        user_attempt = UserAttempt.objects.create(question=question, **validated_data)
        return user_attempt
    
class UserResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResult
        fields = ['uid', 'quiz_session_id', 'total_questions', 'questions_answered_correct', 'questions_answered_wrong']