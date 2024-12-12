from django.db import models
import uuid
from accounts.models import CustomUser
import random

OPTION_CHOICE = [
    ('A', 'Option A'),
    ('B', 'Option B'),
    ('C', 'Option C'),
    ('D', 'Option D'),
]

class BaseAbstract(models.Model):

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = True)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)
    
    class Meta:
        abstract = True

class QuizSession(BaseAbstract):

    user = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)

    def add_random_questions(self, question_count=10):
        all_question_ids = Question.objects.values_list("uid", flat=True)
        selected_question_ids = random.sample(list(all_question_ids), min(question_count, len(all_question_ids)))

        for question_id in selected_question_ids:
            QuizSessionQuestion.objects.create(
                quiz_session_id=self,
                question_id=question_id
            )

    def get_questions(self):
        return self.questions.select_related("question").all()

    def get_user_attempts(self):
        return UserAttempt.objects.filter(quiz_session_id=self.id)

    def get_results(self):
        result, created = UserResult.objects.get_or_create(quiz_session_id=self)
        if created:
            result.evaluate_attempt()
        return result

class Question(BaseAbstract):

    question_text = models.TextField(null=False, blank=False)
    option_a = models.TextField(null=False, blank=False)
    option_b = models.TextField(null=False, blank=False)
    option_c = models.TextField(null=False, blank=False)
    option_d = models.TextField(null=False, blank=False)
    answer = models.CharField(max_length=1, choices=OPTION_CHOICE)

    def __str__(self):
        return self.question_text

class QuizSessionQuestion(BaseAbstract):
    quiz_session_id = models.ForeignKey(QuizSession, on_delete=models.CASCADE, related_name="questions")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("quiz_session_id", "question")

    @staticmethod
    def get_questions_for_session(quiz_session):
        session_questions = QuizSessionQuestion.objects.filter(quiz_session_id=quiz_session).select_related("question")
        question_queryset = session_questions.values_list('question', flat=True)  # Get just the 'question' field
        questions = Question.objects.filter(uid__in=question_queryset)  # Filter actual Question objects
        return questions
        

class UserAttempt(BaseAbstract):

    quiz_session_id = models.ForeignKey(QuizSession, null=False, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, null=False, on_delete=models.CASCADE)
    user_response = models.CharField(max_length=1, null=False, blank=False, choices=OPTION_CHOICE)
    is_correct = models.BooleanField(default=False)

    class Meta:
        unique_together = ("quiz_session_id", "question_id")

    def check_answer(self):
        return self.user_response == self.question_id.answer
    
    def save(self, *args, **kwargs):
        self.is_correct = self.check_answer()
        super().save(*args, **kwargs)
    
class UserResult(BaseAbstract):

    quiz_session_id = models.ForeignKey(QuizSession, null=False, on_delete=models.CASCADE)
    total_questions = models.IntegerField(null=True)
    questions_answered_wrong = models.IntegerField(null=True)
    questions_answered_correct = models.IntegerField(null=True)

    def get_quiz_question_list(self):
        questions = UserAttempt.objects.filter(quiz_session_id=self.quiz_session_id).values('question_id')
        print("---->", questions)
        return Question.objects.filter(id__in=[i for i in questions.values_list('uid', flat=True)])

    def get_questions_answered_correct(self):
        return UserAttempt.objects.filter(quiz_session_id=self.quiz_session_id, is_correct=True).count()

    def get_questions_answered_wrong(self):
        return UserAttempt.objects.filter(quiz_session_id=self.quiz_session_id, is_correct=False).count()

    def evaluate_attempt(self):
        attempt = UserAttempt.objects.filter(quiz_session_id=self.quiz_session_id)
        total_questions = attempt.count()
        correct_answers = attempt.filter(is_correct=True).count()
        incorrect_answers = total_questions - correct_answers

        self.total_questions = total_questions
        self.questions_answered_correct = correct_answers
        self.questions_answered_wrong = incorrect_answers

        self.save()    