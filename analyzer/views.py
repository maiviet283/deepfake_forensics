import json
from django.shortcuts import render
from .ai_image_web import detect_deepfake_from_image
from .models import Image

def index(request):
    result_detect = None
    metadata = None
    image_url = None

    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        metadata_json = request.POST.get("image_metadata", "")

        # Kiểm tra nếu metadata rỗng hoặc sai định dạng JSON
        try:
            metadata = json.loads(metadata_json) if metadata_json else {"error": "No metadata received"}
        except json.JSONDecodeError:
            metadata = {"error": "Invalid JSON format"}

        # Lưu ảnh vào database
        try:
            image_instance = Image.objects.create(image=image_file)
            temp_file_path = image_instance.image.path
            image_url = image_instance.image.url
        except Exception as e:
            print(f"Error saving image: {e}")
            metadata["error"] = "Failed to save image"

        # Gọi AI Detector nếu ảnh được lưu thành công
        if temp_file_path:
            result_detect = detect_deepfake_from_image(temp_file_path)

    return render(request, 'analyzer/index.html', {
        'image_url': image_url,
        'result_detect': result_detect,
        'result_metadata': metadata,
    })
