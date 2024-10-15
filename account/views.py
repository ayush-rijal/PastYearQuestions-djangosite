from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from .models import Profile
from quiz.models import QuizSubmission, Question

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user.username)
    
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            # Check if username exists
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('register')
            # Check if email exists
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('register')
            else:
                # Create user
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'User created successfully')

                # Log in the user and redirect to profile
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # Create profile for new user 
                user_model = User.objects.get(username=username) 
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()
                return redirect('profile', username=username)
        else:
            messages.error(request, "Passwords do not match")
            return redirect('register')  # Corrected the redirect target here
    context = {}
    return render(request, "register.html", context)

# def profile(request, username):
#     user_object2 = get_object_or_404(User, username=username)
@login_required (login_url= "login")
#     user_profile2 = get_object_or_404(Profile, user=user_object2)
#     #profile user
#     user_object2 = User.objects.get(username = username)
#     user_profile2  = Profile.objects.get (user = user_object2)
#     #request user
#     user_object = User.objects.get(username = request.user)
#     user_profile = Profile.objects.get(user = user_object)
#     #get all quiz submitted by user
#     submissions = QuizSubmission.objects.filter(user = user_object)
#     context = {"user_profile": user_profile, "user_profile2" : user_profile2, "submissions" : submissions}
#     return render (request, "profile.html",  context ) 
def profile(request, username):
    user_object2 = get_object_or_404(User, username=username)
    user_profile2 = get_object_or_404(Profile, user=user_object2)
    
    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)
    
    # Get all quiz submissions by the logged-in user
    submissions = QuizSubmission.objects.filter(user=user_object)

    for submission in submissions:
        correct_answers = 0
        wrong_answers = 0
        for question in submission.quiz.question_set.all():
            user_answer = submission.submitted_answer_for_question(question)
            correct_answer = question.choice_set.filter(is_correct=True).first().text  # Assuming each question has one correct answer
            if user_answer == correct_answer:
                correct_answers += 1
            else:
                wrong_answers += 1
        
        # Store these values in the submission object for use in the template
        submission.correct_answers = correct_answers
        submission.wrong_answers = wrong_answers

    context = {
        "user_profile": user_profile,
        "user_profile2": user_profile2,
        "submissions": submissions
    }

    return render(request, "profile.html", context)

@login_required(login_url='login')
def edit_profile(request):
    user_object = request.user
    user_profile = user_object.profile

    if request.method == "POST":
        # Image
        profile_img = request.FILES.get('profile_img')
        if profile_img:
            user_profile.profile_img = profile_img
            user_profile.save()

        # Email
        email = request.POST.get('email')
        if email and email != user_object.email:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already used. Choose a different one!")
                return redirect('edit_profile')
            else:
                user_object.email = email
                user_object.save()

        # Username
        username = request.POST.get('username')
        if username and username != user_object.username:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken. Choose a unique one!")
                return redirect('edit_profile')
            else:
                user_object.username = username
                user_object.save()

        # First name and Last name
        user_object.first_name = request.POST.get('firstname', user_object.first_name)
        user_object.last_name = request.POST.get('lastname', user_object.last_name)
        user_object.save()

        # Location, Bio, Gender
        user_profile.location = request.POST.get('location', user_profile.location)
        user_profile.gender = request.POST.get('gender', user_profile.gender)
        user_profile.bio = request.POST.get('bio', user_profile.bio)
        user_profile.save()

        return redirect('profile', username=user_object.username)

    context = {"user_profile": user_profile}
    return render(request, 'profile-edit.html', context)

    
@login_required(login_url='login')
def cancel_profile_update(request):

    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == "POST":
        user_profile.delete()
        user_object.delete()
        return redirect('logout')



    context = {"user_profile": user_profile}
    return render(request, 'confirm.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user.username)

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('profile', username)
        else:
            messages.info(request, 'Credentials Invalid!')
            return redirect('login')

    return render(request, "login.html")

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')