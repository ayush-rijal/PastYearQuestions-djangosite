

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from account.models import Profile
from .models import Quiz, Category, Question, Choice, QuizSubmission, SubmissionAnswer, SubjectCategory
from django.db.models import Q
from django.contrib import messages
from .models import Question,Quiz,Choice
from .serializers import QuestionSerializer,ChoiceSerializer,QuizSerializer
from rest_framework import status

#####
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

@login_required
def all_quiz_view(request):

    quizzes = Quiz.objects.order_by('-created_at')
    categories = Category.objects.all()
    # subject_categories=SubjectCategory.objects.all()

    context = {"quizzes": quizzes, "categories": categories}
    return render(request, 'all-quiz.html', context)

@login_required
def search_view(request, category):

    # search by search bar
    if request.GET.get('q') != None:
        q = request.GET.get('q')
        query = Q(title__icontains=q) | Q(description__icontains=q)
        quizzes = Quiz.objects.filter(query).order_by('-created_at')
    
    # search by category
    elif category != " ":
        quizzes = Quiz.objects.filter(category__name=category).order_by('-created_at')
    
    else:
        quizzes = Quiz.objects.order_by('-created_at')


    categories = Category.objects.all()

    context = {"quizzes": quizzes, "categories": categories}
    return render(request, 'all-quiz.html', context)

# @login_required

# def quiz_view(request, quiz_id):

#     quiz = get_object_or_404(Quiz, pk=quiz_id)


#     return render(request, 'quiz.html', {'quiz': quiz})



# @login_required
# def questions_by_subject_category(request,subjectcategory_id):
#     print(f"View called for category ID: {subjectcategory_id}")  # Debug print
#     subject_category=get_object_or_404(SubjectCategory,id=subjectcategory_id)
#     print("Rendering quiz for category:", subject_category.name)
#     questions=subject_category.questions.all() 

#     if not questions.exists():
#         messages.warning(request,"No questions available for this category")
#         return redirect('all_quiz')

#     subject_categories=SubjectCategory.objects.all() 
#     print(subject_categories) # Debug print to check categories
#      # Render the quiz page with the first question of the selected category
#     return render(request,'quiz.html',
#                   {'quiz':questions,
#                    'subject_category':subject_category,
#                    'subject_categories':subject_categories})

    
#     print(subject_categories)  # This should print the list of categories 


# @login_required
# def quiz_view(request, quiz_id, subjectcategory_id=None):
#     quiz = get_object_or_404(Quiz, pk=quiz_id)
    
#     # Fetch all subject categories related to the quiz
#     subject_categories = SubjectCategory.objects.all()
    
#     if subjectcategory_id:
#         # If a subject category is provided, filter questions by that category
#         subject_category = get_object_or_404(SubjectCategory, id=subjectcategory_id)
#         questions = subject_category.questions.filter(quiz=quiz)
#     else:
#         # Default to showing all questions for the quiz
#         questions = quiz.question_set.all()

#     if not questions.exists():
#         messages.warning(request, "No questions available for this category")
#         return redirect('all_quiz')

#     context = {
#         'quiz': quiz,
#         'questions': questions,
#         'subject_categories': subject_categories,
#         'selected_category': subjectcategory_id
#     }
    
#     return render(request, 'quiz.html', context)
 

# @login_required
# def quiz_view(request, quiz_id, subjectcategory_id=None):
#     quiz = get_object_or_404(Quiz, pk=quiz_id)
    
#     # Fetch all subject categories related to the quiz
#     subject_categories = SubjectCategory.objects.filter(quiz=quiz)
#     # subject_categories 

#     if subjectcategory_id:
#      # If a subject category is provided, filter questions by that category
#         subject_category = get_object_or_404(SubjectCategory, id=subjectcategory_id)
#         questions = subject_category.question_set.filter(quiz=quiz).order_by('id')
        
#     # Calculate the starting index for this category
#         previous_questions_count = Question.objects.filter(
#             quiz=quiz, 
#             subject_category__id__lt=subjectcategory_id
#         ).count()
        
#         starting_index = previous_questions_count + 1
#     else:
#         # Default to showing all questions for the quiz
#         questions = quiz.question_set.all().order_by('subject_category__id', 'id')
#         starting_index = 1

#     if not questions.exists():
#         messages.warning(request, "No questions available for this category")
#         return redirect('all_quiz')

#     # Calculate total questions and questions per category
#     total_questions = quiz.question_set.count()
#     questions_per_category = {
#         category.id: category.question_set.filter(quiz=quiz).count()
#         for category in subject_categories
#     }

#     context = {
#         'quiz': quiz,
#         'questions': questions,
#         'subject_categories': subject_categories,
#         'selected_category': subjectcategory_id,
#         'starting_index': starting_index,
#         'total_questions': total_questions,
#         'questions_per_category': questions_per_category,
#     }
    
#     return render(request, 'quiz.html',context)



@login_required
def quiz_view(request, quiz_id, subjectcategory_id=None):
    # Fetch the quiz object
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    
    # Get all subject categories for the quiz
    subject_categories = SubjectCategory.objects.filter(quiz=quiz).distinct()
    
    # Handle case when no subject category is selected; redirect to the first category
    if not subjectcategory_id and subject_categories.exists():
        subjectcategory_id = subject_categories.first().id
        return redirect('quiz', quiz_id=quiz_id, subjectcategory_id=subjectcategory_id)
    
    # Fetch the selected subject category
    subject_category = get_object_or_404(SubjectCategory, pk=subjectcategory_id)
    
    # # Save the current category in the session to retain progress
    # if request.session.get('current_subject_category') != subjectcategory_id:
    #     request.session['current_subject_category'] = subjectcategory_id

    # Retrieve questions for the selected subject category
    questions = subject_category.question_set.filter(quiz=quiz).order_by('id')

    # Find the next category
    
    # Calculate the starting index for the current subject category
    starting_index = (
        Question.objects.filter(quiz=quiz, subject_category__in=subject_categories.filter(id__lt=subjectcategory_id)).count()
        + 1
    )

    # Check if there are no questions for this category
    if not questions.exists():
        messages.warning(request, "No questions available for this category.")
        return redirect('all_quiz')

    # Fetch the current question index from the session
    

    # Prepare the context for the template
    context = {
        'quiz': quiz,
        'questions': questions,
        'subject_categories': subject_categories,
        'selected_category': subjectcategory_id,
        'starting_index':starting_index,
        
    }

    return render(request, 'quiz.html', context)




#########this is the final correct api
@api_view(['GET'])
@login_required
def quiz_api_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)

    response_data = []
    for question in questions:
        question_data = QuestionSerializer(question).data
        question_data['choices'] = ChoiceSerializer(Choice.objects.filter(question=question), many=True).data
        response_data.append(question_data)

    return Response(response_data, status=status.HTTP_200_OK)

    # Get the quiz object or return a 404 error if not found
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    # Serialize the quiz data along with its category and questions
    serializer = QuizSerializer(quiz)

    # Return the serialized data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)



@login_required
def quiz_result_view(request, submission_id):
    submission = get_object_or_404(QuizSubmission, pk=submission_id, user=request.user)
    user_answers = SubmissionAnswer.objects.filter(quiz_submission=submission)

    question_data = []
    for question in submission.quiz.question_set.all():
        correct_answer = question.choice_set.filter(is_correct=True).first()
        user_answer_submission = user_answers.filter(question=question).first()
        
        user_answer = None
        if user_answer_submission:
            user_answer = question.choice_set.filter(text=user_answer_submission.answer_text).first()
        
        question_data.append({
            'question': question,
            'user_answer': user_answer,
            'correct_answer': correct_answer,
        })

    context = {
        'submission': submission,
        'question_data': question_data,
    }
    
    # Debug print statements
    for item in question_data:
        print(f"Question: {item['question'].text}")
        print(f"Correct Answer: {item['correct_answer'].text if item['correct_answer'] else 'No correct answer'}")
        print(f"User Answer: {item['user_answer'].text if item['user_answer'] else 'No user answer'}")
        print("---")

    return render(request, 'quiz-result.html', context)






