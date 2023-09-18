from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
from django.conf import settings

# This function will generate a personalized prompt for the user
# by fetching their past responses to questions.
def generate_prompt(user):
    user_responses = UserResponse.objects.filter(user=user)
    prompt_text = ""

    # Iterate through each response and format it into the prompt.
    for response in user_responses:
        prompt_text += f"The user was asked '{response.question}', they replied with '{response.answer}'. "

    prompt_text += "Make them a hook based on this information provided."
    return prompt_text

# This view displays the chat interface.
def chat(request):
    chats = Chat.objects.all()
    return render(request, 'GLIMMA_AI/chat.html', {'chats': chats, })

# The main view that communicates with the GPT-3 API.
@csrf_exempt
def Ajax(request):
    # Handle both regular GET requests and AJAX requests.
    if request.method == "GET" or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        personalized_prompt = generate_prompt(request.user)
        print(personalized_prompt)

        # Setting the OpenAI API key.
        openai.api_key = settings.OPENAI_API_KEY

        # Pre-defined context setup for GPT-3.
        context = {
            "role": "system",
            "content": (
                "You are an expert copywriter tasked with crafting exceptional social media content tailored "
                "for brands that align with Carl Jung's 12 primary archetypes [...]")
        }

        # Send the personalized prompt to the GPT-3 API.
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                context,
                {"role": "user", "content": f"{personalized_prompt}"}
            ],
            temperature=0.7
        )

        response = res.choices[0].message["content"]
        print(response)

        # Save the chat in the database.
        chat = Chat.objects.create(text=personalized_prompt, gpt=response)
        return JsonResponse({'data': response, })

    return JsonResponse({})

