from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
import google.generativeai as genai
import os
from hair import settings



def index(request):
    return render(request, 'index.html')


@csrf_exempt
@require_POST
def generate_hairstyle(request):
    # Get the uploaded image and user details from the request
    image = request.FILES.get('image')
    name = request.POST.get('name')
    email = request.POST.get('email')
    preferences = request.POST.get('preferences', '')

    # Save the uploaded image to a temporary location
    temp_image_path = os.path.join(settings.MEDIA_ROOT, 'temp_image.jpg')
    with open(temp_image_path, 'wb+') as temp_file:
        for chunk in image.chunks():
            temp_file.write(chunk)


    genai.configure(api_key=settings.GOOGLE_GENERATIVE_AI_KEY)        

    # Upload the image to Google Generative AI
    sample_file = genai.upload_file(path=temp_image_path, display_name=f"{name}'s Image")

    # Set the model
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

    # Generate the hairstyle recommendation
    prompt = f"Recommend a hairstyle that fits this face shape and head shape for {name}, with preferences: {preferences}. NOTE: ALWAYS RECOMMEND A HAIRSTYLE NO MATTER WHAT"
    response = model.generate_content([prompt, sample_file])

    # Clean up the temporary image file
    os.remove(temp_image_path)

    # Return the recommendation as a JSON response
    return JsonResponse({'recommendation': response.text})

# Create your views here.
