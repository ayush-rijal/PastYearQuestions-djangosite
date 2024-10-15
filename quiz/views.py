from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from account.models import Profile
from .models import Quiz, Category
from django.db.models import Q
from quiz.models import QuizSubmission, SubmissionAnswer
from django.contrib import messages

# Create your views here.

@login_required
def all_quiz_view(request):

    quizzes = Quiz.objects.order_by('-created_at')
    categories = Category.objects.all()

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

@login_required
def quiz_view(request, quiz_id):

    quiz = get_object_or_404(Quiz, pk=quiz_id)

    if request.method == "POST":
        
        # Get the score
        score = int(request.POST.get('score', 0))
        
        # save the new quiz submission
        submission = QuizSubmission(user=request.user, quiz=quiz, score=score)
        submission.save()

        return redirect('quiz_result', submission_id=submission.id)

    return render(request, 'quiz.html', {'quiz': quiz})

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