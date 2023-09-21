from django.shortcuts import render
from django.http import JsonResponse
from .models import UserResponse
from django.contrib.auth.decorators import login_required
import json


def index(request):
    """ Return the home page """

    return render(request, 'GLIMMA_AI/index.html')


@login_required
def display_quiz(request):
    # Sample questions and options
    questions = {
        'What is your favorite color?': ['Red', 'Green', 'Blue'],
        'Which animal do you prefer?': ['Cat', 'Dog', 'Bird'],
        'What is your 2nd favorite color?': ['Red', 'Green', 'Blue'],
        'What is your favorite city?': "input_field",
        'Which is your favourite time of day?': ['Morning', 'Afternoon', 'Evening', 'Night'],
        'Which came first?': ['Chicken', 'Egg'],
        # Add more questions as needed
    }

    return render(request, 'GLIMMA_AI/quiz.html', {'questions': questions})


@login_required
def save_answer(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            question = data.get('question')
            answer = data.get('answer')

            user_response = UserResponse(
                user=request.user,
                question=question,
                answer=answer
            )
            user_response.save()

            return JsonResponse({'status': 'success'})

        return JsonResponse({'status': 'error'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
