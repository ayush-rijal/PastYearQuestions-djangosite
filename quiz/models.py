

from django.db import models
import pandas as pd
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=15)
    image_url=models.URLField(max_length=200, blank=True, null=True) # Add field for image URL
    icon=models.CharField(max_length=50, blank=True, null=True) # Add field for icon (its being that blue line between image and title of category slider)



    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

# class Quiz(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     quiz_file = models.FileField(upload_to='quiz/')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name_plural = 'Quizzes'

#     def __str__(self):
#         return self.title

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         if self.quiz_file:
#             self.import_quiz_from_excel()
          

#     def import_quiz_from_excel(self):
#         try:
#             df = pd.read_excel(self.quiz_file.path)
#             for index, row in df.iterrows():
#                 try:

#                     question_text = row['Question']
#                     print(f"Processing question: {question_text}")  # Debug print
#                     choices = {
#                     'A': row['A'],
#                     'B': row['B'],
#                     'C': row['C'],
#                     'D': row['D']
#                     }
#                     correct_answer = row['Answer']
#                     # Check for missing data in the question, choices, or correct answer
#                     if not question_text or any(pd.isna(choice) for choice in choices.values()) or pd.isna(correct_answer):
#                         raise ValueError(f"Missing data in row {index}: Question or choices are incomplete.")


#                     question, _ = Question.objects.get_or_create(quiz=self, text=question_text)

#                     for choice_key, choice_text in choices.items():
#                         is_correct = (choice_key == correct_answer)
#                         print(f"Creating choice: {choice_text}, Is Correct: {is_correct}")  # Debug print
#                         Choice.objects.get_or_create(question=question, text=choice_text, is_correct=is_correct)
#                 except Exception as e:
#                     print(f"Error processing row {index}:{e}") 
                           
#         except Exception as e:
#             print(f"Error importing quiz: {e}")
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quiz_file = models.FileField(upload_to='quiz/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Check if the quiz_file field has changed or if it's a new object
        if self.pk is None or not Quiz.objects.filter(pk=self.pk, quiz_file=self.quiz_file).exists():
            super().save(*args, **kwargs)
            if self.quiz_file:
                self.import_quiz_from_excel()
        else:
            # Just save without re-importing from the file
            super().save(*args, **kwargs)

    def import_quiz_from_excel(self):
        try:
            df = pd.read_excel(self.quiz_file.path)
            for index, row in df.iterrows():
                try:
                    question_text = row['Question']
                    print(f"Processing question: {question_text}")  # Debug print
                    choices = {
                        'A': row['A'],
                        'B': row['B'],
                        'C': row['C'],
                        'D': row['D']
                    }
                    correct_answer = row['Answer']
                    # Check for missing data in the question, choices, or correct answer
                    if not question_text or any(pd.isna(choice) for choice in choices.values()) or pd.isna(correct_answer):
                        raise ValueError(f"Missing data in row {index}: Question or choices are incomplete.")

                    # Create or update the question
                    question, _ = Question.objects.get_or_create(quiz=self, text=question_text)

                    for choice_key, choice_text in choices.items():
                        is_correct = (choice_key == correct_answer)
                        print(f"Creating choice: {choice_text}, Is Correct: {is_correct}")  # Debug print
                        # Create or update choices based on the question
                        Choice.objects.get_or_create(question=question, text=choice_text, defaults={'is_correct': is_correct})

                except Exception as e:
                    print(f"Error processing row {index}: {e}") 
                           
        except Exception as e:
            print(f"Error importing quiz: {e}")


    
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text[:50]

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.text[:50]}, {self.text[:20]}"


class QuizSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    correct_answers = models.IntegerField(null=True, blank=True)
    wrong_answers = models.IntegerField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    answers = models.ManyToManyField(Question, through='SubmissionAnswer')

    def __str__(self):
        return f"{self.user}, {self.quiz.title}"

    def submitted_answer_for_question(self, question):
        try:
            return self.submissionanswer_set.get(question=question).answer_text
        except SubmissionAnswer.DoesNotExist:
            return None


class SubmissionAnswer(models.Model):
    quiz_submission = models.ForeignKey(QuizSubmission, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()

    def __str__(self):
        return f"Submission ID: {self.quiz_submission.id}, Question ID: {self.question.id}, Answer: {self.answer_text}"

class UserRank(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.IntegerField(null=True, blank=True)
    total_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.rank}, {self.user.username}"

@receiver(post_save, sender=QuizSubmission)
def update_leaderboard(sender, instance, created, **kwargs):
    if created:
        update_leaderboard()


def update_leaderboard():
    user_scores = (QuizSubmission.objects.values('user')
                   .annotate(total_score=Sum('score'))
                   .order_by('-total_score'))

    rank = 1
    for entry in user_scores:
        user_id = entry['user']
        total_score = entry['total_score']

        user_rank, created = UserRank.objects.get_or_create(user_id=user_id)
        user_rank.rank = rank
        user_rank.total_score = total_score
        user_rank.save()

        rank += 1