from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from account.models import Profile
from quiz.models import UserRank, Quiz, QuizSubmission, Question,Category
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime
from .models import Message, Blog
from django.db.models import Count, Q
import math
from django.db.models.functions import ExtractYear
from django.http import JsonResponse
from django.utils.safestring import mark_safe
import re
from .models import BlogPost, Comment
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required



# Create your views here.
def home(request):

    leaderboard_users = UserRank.objects.order_by('rank')[:3]
    categories=Category.objects.all()

    if request.user.is_authenticated:
        # request user
        user_object = User.objects.get(username=request.user)
        try:
             user_profile = Profile.objects.get(user=user_object)
        except Profile.DoesNotExist:
            user_profile=None     
       
        context = {"user_profile": user_profile, "leaderboard_users": leaderboard_users, "categories":categories} # Add categories to context
    else:
        context = {"leaderboard_users": leaderboard_users, "categories":categories} # Pass categories and leaderboard data when user is not authenticated

    return render(request, 'index.html', context)


@login_required(login_url="login")
def leaderboard_view(request):

    user_object = User.objects.get(username=request.user)
    try:
        user_profile = Profile.objects.get(user=user_object)
    except Profile.DoesNotExist:
        user_profile=None


    leaderboard_users = UserRank.objects.order_by('rank')

    context = {"leaderboard_users": leaderboard_users, "user_profile": user_profile}
    return render(request, "leaderboard.html", context)


def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
@login_required(login_url='login')
def dashboard_view(request):

    user_object = User.objects.get(username=request.user)
    try:
        user_profile = Profile.objects.get(user=user_object)
    except Profile.DoesNotExist:
        user_profile=None


    # Total Number
    total_users = User.objects.all().count()
    total_quizzes = Quiz.objects.all().count()
    total_quiz_submit = QuizSubmission.objects.all().count()
    total_questions = Question.objects.all().count()

    # today_numbers
    today_users = User.objects.filter(date_joined__date=datetime.date.today()).count()
    today_quizzes_objs = Quiz.objects.filter(created_at__date=datetime.date.today())
    today_quizzes = Quiz.objects.filter(created_at__date=datetime.date.today()).count()
    today_quiz_submit = QuizSubmission.objects.filter(submitted_at__date=datetime.date.today()).count()
    today_questions = 0
    for quiz in today_quizzes_objs:
        today_questions += quiz.question_set.count()

    # Gain %
    gain_users = gain_percentage(total_users, today_users)
    gain_quizzes = gain_percentage(total_quizzes, today_quizzes)
    gain_quiz_submit = gain_percentage(total_quiz_submit, today_quiz_submit)
    gain_questions = gain_percentage(total_questions, today_questions)

    # Inbox Messages
    messages = Message.objects.filter(created_at__date=datetime.date.today()).order_by('-created_at')


    context = {"user_profile": user_profile, 
               "total_users": total_users,
               "total_quizzes": total_quizzes,
               "total_quiz_submit": total_quiz_submit,
               "total_questions": total_questions,
               "today_users":today_users,
               "today_quizzes":today_quizzes,
               "today_quiz_submit":today_quiz_submit,
               "today_questions":today_questions,
               "gain_users": gain_users,
               "gain_quizzes": gain_quizzes,
               "gain_quiz_submit": gain_quiz_submit,
               "gain_questions": gain_questions,
               "messages": messages,
               }
    return render(request, "dashboard.html", context)

def gain_percentage(total, today):
    if total > 0 and today > 0:
        gain = math.floor((today *100)/total)
        return gain

def about_view(request):
    return render(request, "about.html")
def blogs_view(request):

    year_blog_count = Blog.objects.annotate(year=ExtractYear('created_at')).values('year').annotate(count=Count('id')).order_by('-year').filter(status='public')

    blogs = Blog.objects.filter(status='public').order_by('-created_at')

    if request.user.is_authenticated:
        # request user
        user_object = User.objects.get(username=request.user)
        user_profile = Profile.objects.get(user=user_object)
        context = {"user_profile": user_profile, "year_blog_count": year_blog_count, "blogs": blogs}
    else:
        context = {"year_blog_count": year_blog_count, "blogs": blogs}
    return render(request, "blogs.html", context)

@login_required(login_url='login')
def blog_view(request, blog_id):
    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    blog = get_object_or_404(Blog, id=blog_id)
    
    recommended_blogs = Blog.objects.filter(status='public').exclude(id=blog_id).order_by('-created_at')[:3]

    context = {
        "user_profile": user_profile,
        "blog": blog,
        "recommended_blogs": recommended_blogs
    }
    return render(request, "blog.html", context)

@login_required(login_url='login')
def contact_view(request):

    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == "POST":
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if subject is not None and message is not None:
            form = Message.objects.create(user=request.user, subject=subject, message=message)
            form.save()
            messages.success(request, "We got your message. We will resolve your query soon.")
            return redirect('profile', request.user.username)
        
        else:
            return redirect('contact')
    
    context = {"user_profile": user_profile}
    return render(request, "contact-us.html", context)

@user_passes_test(is_superuser)
@login_required(login_url='login')
def message_view(request, id):

    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    message = Message.objects.filter(id=int(id)).first()
    if not message.is_read:
        message.is_read = True
        message.save()

    context = {"user_profile": user_profile, "message": message}
    return render(request, "message.html", context)


def terms_conditions_view(request):

    if request.user.is_authenticated:
        # request user
        user_object = User.objects.get(username=request.user)
        user_profile = Profile.objects.get(user=user_object)
        context = {"user_profile": user_profile}
    else:
        context = {}
    return render(request, "terms-conditions.html", context)

@login_required(login_url='login')
def downloads_view(request):

    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)
    
    context = {"user_profile": user_profile}
    return render(request, "downloads.html", context)

def search_users_view(request):

    query = request.GET.get('q')

    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query) 
        ).order_by('date_joined')

    else:
        users = []

    if request.user.is_authenticated:
        # request user
        user_object = User.objects.get(username=request.user)
        user_profile = Profile.objects.get(user=user_object)
        context = {"user_profile": user_profile, "query": query, "users": users}
    else:
        context = {"query": query, "users": users}
    return render(request, "search-users.html", context)



def post_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    comments = post.comments.filter(parent=None)
    return render(request, 'blog.html', {'post': post, 'comments': comments})

@require_POST
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    parent_id = request.POST.get('parent_id')
    content = request.POST.get('content')
    
    if parent_id:
        parent_comment = get_object_or_404(Comment, id=parent_id)
        comment = Comment.objects.create(post=post, user=request.user, content=content, parent=parent_comment)
    else:
        comment = Comment.objects.create(post=post, user=request.user, content=content)
    
    return JsonResponse({
        'status': 'success',
        'comment_id': comment.id,
        'user': comment.user.username,
        'content': comment.content,
        'created_at': comment.created_at.strftime('%B %d, %Y, %I:%M %p'),
    })

@require_POST
@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    # Implement like functionality here
    return JsonResponse({'status': 'success', 'likes': comment.likes})