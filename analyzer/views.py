from django.shortcuts import render, HttpResponse
from .ai_image_web import detect_deepfake_from_image
import tempfile

def index(request):
    result_detect_deepfake_from_image = None
    temp_file_path = None

    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        
        # Lưu ảnh tạm để truyền vào hàm detect
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            for chunk in image_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        result_detect_deepfake_from_image = detect_deepfake_from_image(temp_file_path)

    return render(request, 'analyzer/index.html', {
        'image_url': temp_file_path,
        'result_detect': result_detect_deepfake_from_image,
    })
