from django.contrib import admin
from .models import Category, Quiz, Question, Choice, QuizSubmission, UserRank
from unfold.admin import ModelAdmin as UnfoldModelAdmin

class CategoryAdmin(UnfoldModelAdmin):
    list_display = ('name', 'image_url')  # Display the name and image URL
    search_fields = ('name',)  # Allow search by category name

class QuizAdmin(UnfoldModelAdmin):
    list_display = ('title', 'category', 'created_at')  # Display quiz title, category, and creation date
    search_fields = ('title', 'category__name')  # Allow search by quiz title and category name
    list_filter = ('category', 'created_at')  # Add filters for category and creation date
    fieldsets = (
        (None, {'fields': ('title', 'description', 'category', 'quiz_file')}),
        ('Dates', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    readonly_fields = ('created_at', 'updated_at')  # Make these fields read-only

class QuestionAdmin(UnfoldModelAdmin):
    list_display = ('text', 'quiz')  # Display the question text and associated quiz
    search_fields = ('text',)  # Allow search by question text
    list_filter = ('quiz',)  # Add a filter for the quiz

class ChoiceAdmin(UnfoldModelAdmin):
    list_display = ('question', 'text', 'is_correct')  # Display the question, choice text, and if it's correct
    list_filter = ('is_correct',)  # Filter by correct/incorrect choices
    search_fields = ('question__text', 'text')  # Allow search by question text and choice text

class QuizSubmissionAdmin(UnfoldModelAdmin):
    list_display = ('user', 'quiz', 'score', 'submitted_at')  # Display user, quiz, score, and submission date
    search_fields = ('user__username', 'quiz__title')  # Allow search by username and quiz title
    list_filter = ('quiz', 'submitted_at')  # Add filters for quiz and submission date

class UserRankAdmin(UnfoldModelAdmin):
    pass  # Keep it as is for now, but could add `list_display` if needed later

# Register your models with UnfoldModelAdmin
admin.site.register(Category, CategoryAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(QuizSubmission, QuizSubmissionAdmin)
admin.site.register(UserRank, UserRankAdmin)
