# from django.contrib import admin
# from .models import Category, Quiz, Question, Choice, QuizSubmission, UserRank
# from unfold.admin import ModelAdmin as UnfoldModelAdmin

# class CategoryAdmin(UnfoldModelAdmin):
#     pass

# class QuizAdmin(UnfoldModelAdmin):
#     pass

# class QuestionAdmin(UnfoldModelAdmin):  
#     pass

# class ChoiceAdmin(UnfoldModelAdmin):  # or use admin.ModelAdmin if you prefer
#     list_display = ('question', 'text', 'is_correct')

# class QuizSubmissionAdmin(UnfoldModelAdmin):
#     pass

# class UserRankAdmin(UnfoldModelAdmin):
#     pass

# # Register your models here.
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Quiz, QuizAdmin)
# admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice, ChoiceAdmin)
# admin.site.register(QuizSubmission, QuizSubmissionAdmin)
# admin.site.register(UserRank, UserRankAdmin)

from django.contrib import admin
from .models import Category, Quiz, Question, Choice, QuizSubmission, UserRank
from unfold.admin import ModelAdmin as UnfoldModelAdmin

class CategoryAdmin(UnfoldModelAdmin):
     list_display = ('name', 'image_url', 'icon')  # Show these fields in the admin list view

class QuizAdmin(UnfoldModelAdmin):
    pass

class QuestionAdmin(UnfoldModelAdmin):
    pass

class ChoiceAdmin(UnfoldModelAdmin):  # or use admin.ModelAdmin if you prefer
    list_display = ('question', 'text', 'is_correct')

class QuizSubmissionAdmin(UnfoldModelAdmin):
    pass

class UserRankAdmin(UnfoldModelAdmin):
    pass

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(QuizSubmission, QuizSubmissionAdmin)
admin.site.register(UserRank, UserRankAdmin)
