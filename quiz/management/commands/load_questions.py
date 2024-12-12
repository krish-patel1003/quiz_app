import json
from django.core.management.base import BaseCommand
from quiz.models import Question
import os

class Command(BaseCommand):
    help = "Load questions from a JSON file into the database"

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of this file
        file_path = os.path.join(base_dir, "..", "..", "data", "questions.json")

        try:
            with open(file_path, 'r') as file:
                questions = json.load(file)

                for question in questions:
                    question_text = question["question_text"]
                    option_a = question["option_a"]
                    option_b = question["option_b"]
                    option_c = question["option_c"]
                    option_d = question["option_d"]
                    answer = question["answer"]

                    Question.objects.create(
                        question_text=question_text,
                        option_a=option_a,
                        option_b=option_b,
                        option_c=option_c,
                        option_d=option_d,
                        answer=answer
                    )

                self.stdout.write(self.style.SUCCESS(f"Successfully added {len(questions)} questions to the database."))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR("File not found. Please provide a valid file path."))
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR("Invalid JSON format. Please provide a properly formatted JSON file."))
