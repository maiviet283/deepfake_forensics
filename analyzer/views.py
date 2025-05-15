from django.shortcuts import render
from .ai_image_web import detect_deepfake_from_image
from .models import Image
import json

def index(request):
    result_detect_deepfake_from_image = None
    image_instance = None
    metadata = None

    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        metadata_json = request.POST.get("image_metadata")

        metadata = json.loads(metadata_json)
        
        image_instance = Image.objects.create(image=image_file)
        temp_file_path = image_instance.image.path

        # Gọi AI Detector
        result_detect_deepfake_from_image = detect_deepfake_from_image(temp_file_path)


    return render(request, 'analyzer/index.html', {
        'image_url': image_instance.image.url if image_instance else None,
        'result_detect': result_detect_deepfake_from_image, # AI Detector
        'result_metadata' : metadata,
    })
