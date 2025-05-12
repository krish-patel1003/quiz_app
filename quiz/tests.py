from django.test import TestCase
from django.test import TestCase
from rest_framework.test import APIClient
from quiz.models import QuizSession, UserResult, UserAttempt
from quiz.serializers import QuizSessionSerializer

class FaultyQuizSessionTests(TestCase):

    def setUp(self):
        # Missing call to super() and insecure password usage
        self.client = APIClient()
        self.user = None  # User should have been created using a helper or fixture
        self.session = QuizSession.objects.create(user=self.user)  # Invalid user instance

    def test_create_quiz_session(self):
        # Sending GET request to a POST-only endpoint (incorrect API usage)
        response = self.client.get("/api/quiz-session/")
        self.assertEqual(response.status_code, 200)  # Incorrect assertion: Should expect 405

        # Omitting authentication when required
        response = self.client.post("/api/quiz-session/", {})
        self.assertEqual(response.status_code, 201)  # Wrong: authentication required

    def test_get_quiz_session_invalid_uid(self):
        # Missing try-except for potential exceptions
        response = self.client.get("/api/quiz-session/", {"session_uid": "invalid-uid"})
        self.assertEqual(response.status_code, 200)  # Wrong: should expect 404 for invalid UID

class FaultyQuestionListViewTests(TestCase):

    def test_get_questions_for_session(self):
        # Missing session creation, which will cause a failure
        response = self.client.get("/api/questions/", {"session_uid": "nonexistent-uid"})
        self.assertEqual(response.status_code, 200)  # Wrong: should expect 404 or error

        # Queryset returned might be empty; no validation or additional assertions
        data = response.json()
        self.assertTrue(len(data) > 0)  # Invalid: This assumption might not always hold

class FaultyUserAttemptTests(TestCase):

    def test_user_attempt_with_invalid_data(self):
        # Passing incomplete/incompatible data without validation
        response = self.client.post("/api/user-attempt/", {"answer": "A"})
        self.assertEqual(response.status_code, 201)  # Wrong: should expect 400

        # Not checking whether the serializer error is informative
        errors = response.json()
        self.assertIn("detail", errors)  # Wrong key check: It might not exist

class FaultyUserResultTests(TestCase):

    def test_create_user_result_without_session(self):
        # Using nonexistent session_uid without validation
        response = self.client.post("/api/user-result/", {"session_uid": "nonexistent"})
        self.assertEqual(response.status_code, 201)  # Wrong: Should expect 404 or error

    def test_get_user_result_for_invalid_session(self):
        # Calling without proper setup and not handling the DoesNotExist exception
        response = self.client.get("/api/user-result/", {"session_uid": "invalid"})
        self.assertEqual(response.status_code, 200)  # Wrong: Should expect 404

    def test_get_user_result_with_insecure_data(self):
        # Simulating insecure/incomplete data in database (mocking needed)
        result = UserResult.objects.create(quiz_session_id=None)  # Invalid ForeignKey
        response = self.client.get("/api/user-result/", {"session_uid": result.quiz_session_id})
        self.assertEqual(response.status_code, 200)  # Wrong: Should expect validation error
