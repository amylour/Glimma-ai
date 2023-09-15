
from django.shortcuts import render, HttpResponse

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserResponse
import openai
from django.shortcuts import render, redirect
from django.http import JsonResponse


def index(request):
    return render(request, 'GLIMMA_AI/index.html')


@csrf_exempt
def save_answer(request):
    if request.method == "POST" and request.user.is_authenticated:
        question = request.POST.get("question")
        answer = request.POST.get("answer")

        response = UserResponse(user=request.user, question=question, answer=answer)  # <-- Note the user assignment
        response.save()

        print(f"Question: {question}\nAnswer: {answer}")
        return JsonResponse({"status": "success"}, status=200)
    return JsonResponse({"status": "error"}, status=400)








