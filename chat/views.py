from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai

# This function will generate a personalized prompt for the user
# by fetching their past responses to questions.
def generate_prompt(user):
    # Fetch the user's responses from the database.
    user_responses = UserResponse.objects.filter(user=user)

    # Initialize an empty string to build the prompt.
    prompt_text = ""

    # Iterate through each of the user's responses.
    for response in user_responses:
        # Append each question and its corresponding answer to the prompt.
        prompt_text += f"The user was asked '{response.question}', they replied with '{response.answer}'. "

    # Append the final instruction to the prompt.
    prompt_text += "Make them a hook based on this information provided."

    return prompt_text

# This view is responsible for displaying the chat.
def chat(request):
    chats = Chat.objects.all()
    return render(request, 'GLIMMA_AI/chat.html', {
        'chats': chats,
    })

# This is the main view that communicates with the GPT-3 API.
@csrf_exempt
def Ajax(request):
    # Check if the incoming request is an Ajax request.
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        # Generate the personalized prompt using the current user's data.
        personalized_prompt = generate_prompt(request.user)

        # Print the generated prompt for debugging purposes.
        print(personalized_prompt)

        # Your OpenAI API key.
        openai.api_key = "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"

        # Pre-defined context setup for GPT-3.
        context = {
            "role": "system",
            "content": ("You are an expert copywriter tasked with crafting exceptional social media content tailored "
                        "for brands that align with Carl Jung's 12 primary archetypes (ranging from the Hero, known for "
                        "bravery and action, to the Sage, known for wisdom and introspection, and so on). Analyze the user's "
                        "provided archetype and other data points. Create content that subtly resonates with these details but "
                        "NEVER explicitly mention or reference the user's archetype, data, or give direct hints about their specific "
                        "details. Your objective is to ensure the social media content deeply resonates with their audience while "
                        "maintaining discretion about its origins. You will be provided additional details which you must adhere to "
                        "strictly. For example, if a one-liner is requested, it should be a single, concise sentence without hashtags "
                        "or direct references to the user's information.")
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

        # Extract the response content from the GPT-3 API response.
        response = res.choices[0].message["content"]

        # Print the response for debugging purposes.
        print(response)

        # Create a new Chat object and save it to the database.
        chat = Chat.objects.create(
            text = personalized_prompt,
            gpt = response
        )

        # Return the GPT-3 response as a JsonResponse.
        return JsonResponse({'data': response,})

    # If the request is not an Ajax request, return an empty JsonResponse.
    return JsonResponse({})
