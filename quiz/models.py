# # from django.db import models
# # import pandas as pd
# # from django.contrib.auth.models import User
# # from django.db.models import Sum
# # from django.db.models.signals import post_save
# # from django.dispatch import receiver


# # # Create your models here.
# # class Category(models.Model):
# #     name = models.CharField(max_length=15)

# #     class Meta:
# #         verbose_name_plural = 'Categories'

# #     def __str__(self):
# #         return self.name

# # class Quiz(models.Model):
# #     title = models.CharField(max_length=255)
# #     description = models.TextField()
# #     category = models.ForeignKey(Category, on_delete=models.CASCADE)
# #     quiz_file = models.FileField(upload_to='quiz/')
# #     created_at = models.DateTimeField(auto_now_add=True)
# #     updated_at = models.DateTimeField(auto_now=True)

# #     class Meta:
# #         verbose_name_plural = 'Quizzes'

# #     def __str__(self):
# #         return self.title

# #     # call the function on quiz save
# #     def save(self, *args, **kwargs):
# #         super().save(*args, **kwargs)
# #         if self.quiz_file:
# #             self.import_quiz_from_excel()

# #     # function to extract excel file
# #     def import_quiz_from_excel(self):
# #         # read the excel file
# #         df = pd.read_excel(self.quiz_file.path)

# #         # iterate over the each row
# #         for index, row in df.iterrows():
# #             # extract question text, choices and correct answer from the row
# #             question_text = row['Question']
# #             choice1 = row['A']
# #             choice2 = row['B'] 
# #             choice3 = row['C']
# #             choice4 = row['D']
# #             correct_answer = row['Answer']
# #             #their add the sugesstion rows and images rows

# #             # create the question object
# #             question = Question.objects.get_or_create(quiz=self, text=question_text)

# #             # create choices objects
# #             choice_1 = Choice.objects.get_or_create(question=question[0], text=choice1, is_correct=correct_answer == 'A')
# #             choice_2 = Choice.objects.get_or_create(question=question[0], text=choice2, is_correct=correct_answer == 'B')
# #             choice_4 = Choice.objects.get_or_create(question=question[0], text=choice4, is_correct=correct_answer == 'D')
# #             choice_3 = Choice.objects.get_or_create(question=question[0], text=choice3, is_correct=correct_answer == 'C')
 
# # class Question(models.Model):
# #     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
# #     text = models.TextField()

# #     def __str__(self):
# #         return self.text[:50]
    

# # class Choice(models.Model):
# #     question = models.ForeignKey(Question, on_delete=models.CASCADE)
# #     text = models.CharField(max_length=255)
# #     is_correct = models.BooleanField(default=False)

# #     def __str__(self):
# #         return f"{self.question.text[:50]}, {self.text[:20]}"

# # class SubmissionAnswer(models.Model):
# #     # Define fields here
# #     answer_text = models.TextField()
# #     # Other fields

# #     def __str__(self):
# #         return self.answer_text
    
# # class QuizSubmission(models.Model):
# #     user = models.ForeignKey(User, on_delete=models.CASCADE)
# #     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
# #     score = models.IntegerField()
# #     correct_answers = models.IntegerField(null=True, blank=True)  # Add this field
# #     wrong_answers = models.IntegerField(null=True, blank=True)  #add this field for grah
# #     submitted_at = models.DateTimeField(auto_now_add=True)
# #     answers = models.ManyToManyField(Question, through='SubmissionAnswer')
# #     def __str__(self):
# #         return f"{self.user}, {self.quiz.title}"

# # class UserRank(models.Model):
# #     user = models.OneToOneField(User, on_delete=models.CASCADE)
# #     rank = models.IntegerField(null=True, blank=True)
# #     total_score = models.IntegerField(null=True, blank=True)

# #     def __str__(self):
# #         return f"{self.rank}, {self.user.username}"

# # @receiver(post_save, sender=QuizSubmission)
# # def update_leaderboard(sender, instance, created, **kwargs):
# #     if created:
# #         update_leaderboard()



# # def update_leaderboard():
# #     # Count the sum of scores for all users
# #     user_scores = (QuizSubmission.objects.values('user').annotate(total_score=Sum('score')).order_by('-total_score'))

# #     # Update rank based on the sorted list
# #     rank = 1
# #     for entry in user_scores:
# #         user_id = entry['user']
# #         total_score = entry['total_score']

# #         user_rank, created = UserRank.objects.get_or_create(user_id=user_id)
# #         user_rank.rank = rank
# #         user_rank.total_score = total_score
# #         user_rank.save()

# #         rank += 1

# from django.db import models
# import pandas as pd
# from django.contrib.auth.models import User
# from django.db.models import Sum
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# class Category(models.Model):
#     name = models.CharField(max_length=15)

#     class Meta:
#         verbose_name_plural = 'Categories'

#     def __str__(self):
#         return self.name

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
#                 question_text = row['Question']
#                 choices = {
#                     'A': row['A'],
#                     'B': row['B'],
#                     'C': row['C'],
#                     'D': row['D']
#                 }
#                 correct_answer = row['Answer']

#                 question, _ = Question.objects.get_or_create(quiz=self, text=question_text)

#                 for choice_key, choice_text in choices.items():
#                     is_correct = (choice_key == correct_answer)
#                     Choice.objects.get_or_create(question=question, text=choice_text, is_correct=is_correct)
#         except Exception as e:
#             print(f"Error importing quiz: {e}")

# class Question(models.Model):
#     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
#     text = models.TextField()

#     def __str__(self):
#         return self.text[:50]

# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     text = models.CharField(max_length=255)
#     is_correct = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.question.text[:50]}, {self.text[:20]}"


# class QuizSubmission(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
#     score = models.IntegerField()
#     correct_answers = models.IntegerField(null=True, blank=True)
#     wrong_answers = models.IntegerField(null=True, blank=True)
#     submitted_at = models.DateTimeField(auto_now_add=True)
#     answers = models.ManyToManyField(Question, through='SubmissionAnswer')

#     def __str__(self):
#         return f"{self.user}, {self.quiz.title}"

#     def submitted_answer_for_question(self, question):
#         try:
#             return self.submissionanswer_set.get(question=question).answer_text
#         except SubmissionAnswer.DoesNotExist:
#             return None


# class SubmissionAnswer(models.Model):
#     quiz_submission = models.ForeignKey(QuizSubmission, on_delete=models.CASCADE)
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     answer_text = models.TextField()

#     def __str__(self):
#         return f"Submission ID: {self.quiz_submission.id}, Question ID: {self.question.id}, Answer: {self.answer_text}"

# class UserRank(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     rank = models.IntegerField(null=True, blank=True)
#     total_score = models.IntegerField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.rank}, {self.user.username}"

# @receiver(post_save, sender=QuizSubmission)
# def update_leaderboard(sender, instance, created, **kwargs):
#     if created:
#         update_leaderboard()


# def update_leaderboard():
#     user_scores = (QuizSubmission.objects.values('user')
#                    .annotate(total_score=Sum('score'))
#                    .order_by('-total_score'))

#     rank = 1
#     for entry in user_scores:
#         user_id = entry['user']
#         total_score = entry['total_score']

#         user_rank, created = UserRank.objects.get_or_create(user_id=user_id)
#         user_rank.rank = rank
#         user_rank.total_score = total_score
#         user_rank.save()

#         rank += 1


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
            for index, row in df.iterrows():
                question_text = row['Question']
                choices = {
                    'A': row['A'],
                    'B': row['B'],
                    'C': row['C'],
                    'D': row['D']
                }
                correct_answer = row['Answer']

                question, _ = Question.objects.get_or_create(quiz=self, text=question_text)

                for choice_key, choice_text in choices.items():
                    is_correct = (choice_key == correct_answer)
                    Choice.objects.get_or_create(question=question, text=choice_text, is_correct=is_correct)
        except Exception as e:
            print(f"Error importing quiz: {e}")

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text[:50]

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
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