
from django.db import models
import pandas as pd
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=15)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

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
        super().save(*args, **kwargs)
        if self.quiz_file:
            self.import_quiz_from_excel()

    def import_quiz_from_excel(self):
        try:
            df = pd.read_excel(self.quiz_file.path)
            df.columns = df.columns.str.strip()  # Strip whitespace from column names
            for index, row in df.iterrows():
                try:
                    question_text = str(row['Question']).strip()
                    choices = {
                        'A': str(row['A']).strip(),
                        'B': str(row['B']).strip(),
                        'C': str(row['C']).strip(),
                        'D': str(row['D']).strip()
                    }
                    correct_answer = row['Answer'].strip()
                    subject_category_name = str(row['SubjectCategory']).strip()

                    # Check for missing data
                    if not question_text or any(pd.isna(choice) for choice in choices.values()) or pd.isna(correct_answer):
                        raise ValueError(f"Missing data in row {index}: Question or choices are incomplete.")

                    # Get or create the subject category linked to the current quiz
                    subject_category, created = SubjectCategory.objects.get_or_create(
                        name=subject_category_name,
                        quiz=self  # Ensure the subject category is linked to the current quiz
                    )
                    print(f"{'Created' if created else 'Retrieved'} subject category: {subject_category.name}")

                    # Create the question
                    question, created = Question.objects.get_or_create(
                        quiz=self,  # Link to the current quiz
                        text=question_text,
                        subject_category=subject_category  # Link to the subject category
                    )
                    print(f"{'Created' if created else 'Retrieved'} question: {question.text}")

                    # Create choices
                    for choice_key, choice_text in choices.items():
                        is_correct = (choice_key == correct_answer)
                        Choice.objects.get_or_create(question=question, text=choice_text, is_correct=is_correct)
                        print(f"Choice created: {choice_text}, Is Correct: {is_correct}")

                except Exception as e:
                    print(f"Error processing row {index}: {e}, Row data: {row}")

        except Exception as e:
            print(f"Error importing quiz: {e}")

class SubjectCategory(models.Model):
    name = models.CharField(max_length=100)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='subject_categories')  # Link to the quiz

    class Meta:
        verbose_name_plural = 'SubjectCategories'

    def __str__(self):
        return f"{self.quiz.title}, {self.name}"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    subject_category = models.ForeignKey(SubjectCategory, on_delete=models.CASCADE)

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