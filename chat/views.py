from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
from django.conf import settings
from GLIMMA_AI.models import UserResponse

def generate_prompt(user):
    user_responses = UserResponse.objects.filter(user=user)
    prompt_text = ""
    for response in user_responses:
        prompt_text += f"The user was asked '{response.question}', they replied with '{response.answer}'. "
    prompt_text += "Make them a hook based on this information provided. 7 words max"
    return prompt_text

def generate_prompt2(user):
    user_responses = UserResponse.objects.filter(user=user)
    prompt_text2 = ""
    for response in user_responses:
        prompt_text2 += f"The user was asked '{response.question}', they replied with '{response.answer}'. "
    prompt_text2 += "Make them a post based on this information provided."
    return prompt_text2

def chat(request):
    chats = Chat.objects.all()
    return render(request, 'GLIMMA_AI/chat.html', {'chats': chats, })

@csrf_exempt
def Ajax(request):
    if request.method == "GET" or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        personalized_prompt = generate_prompt(request.user)
        personalized_prompt2 = generate_prompt2(request.user)
        openai.api_key = settings.OPENAI_API_KEY

        context = {
            "role": "system",
            "content": ("You are an expert copywriter tasked with crafting exceptional social media content tailored for brands that align with Carl Jung's 12 primary archetypes (ranging from the Hero, known for bravery and action, to the Sage, known for wisdom and introspection, and so on)."
"Analyze the user's provided archetype and other data points."
"Create content that subtly resonates with these details but NEVER explicitly mention or reference the user's archetype, data, or give direct hints about their specific details."
"Your objective is to ensure the social media content deeply resonates with their audience while maintaining discretion about its origins."
"You will be provided additional details which you must adhere to strictly."
"For example, if a one-liner is requested, it should be a single, concise sentence without hashtags or direct references to the user's information."


            )
        }

        # Generate hook
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                context,
                {"role": "user", "content": f"{personalized_prompt}"}
            ],
            temperature=0.7
        )
        response = res.choices[0].message["content"]

        # Generate social media post
        post_prompt2 = f"Based on this information about the user: {personalized_prompt2}, craft a compelling social media post."
        post_res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                context,
                {"role": "user", "content": f"{post_prompt2}"}
            ],
            temperature=0.7
        )
        post_response = post_res.choices[0].message["content"]

        # Save both hook and post to the database
        chat = Chat.objects.create(text=personalized_prompt, gpt=response, post=post_response)

        return JsonResponse({'data': response, 'post_data': post_response})

    return JsonResponse({})

# Add any other views or functions below
