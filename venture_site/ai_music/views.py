from django.shortcuts import render
from django.http import JsonResponse
import requests
import os

def ai_music_page(request):
    return render(request, "ai_music/ai_music.html")

def ai_generate_api(request):
    if request.method == "POST":
        prompt = request.POST.get("prompt", "")
        try:
            HF_API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
            headers = {"Authorization": f"Bearer {os.environ.get('HF_API_TOKEN', '')}"}

            response = requests.post(HF_API_URL, headers=headers, json={"inputs": prompt})

            if response.status_code == 200:
                audio_data = response.content
                return JsonResponse({"status": "success", "audio": len(audio_data)})
            else:
                print("DEBUG HF RESPONSE:", response.status_code, response.text)
                return JsonResponse({"status": "error", "details": response.text}, status=500)
        except Exception as e:
            print("ERROR:", str(e))
            return JsonResponse({"status": "error", "details": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)



