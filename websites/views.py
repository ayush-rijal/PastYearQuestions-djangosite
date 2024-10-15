from django.shortcuts import render
from .models import Slider

from django.http import JsonResponse
import openai

from .models import Chat

from django.utils import timezone

def slider_list(request):
    sliders = Slider.objects.all()
    context = {
        'sliders': sliders
    }
    return render(request, 'index.html', context)




openai_api_key = 'input-your-key'
openai.api_key = openai_api_key

def ask_openai(message):
    response = openai.ChatCompletion.create(
        model = "gpt-4",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    
    answer = response.choices[0].message.content.strip()
    return answer

# Create your views here.
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'quiz.html', {'chats': chats})

