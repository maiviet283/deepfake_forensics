from django.shortcuts import render
from .ai_image_web import detect_deepfake_from_image
import tempfile

def index(request):
    result = None

    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        
        # Lưu ảnh tạm để truyền vào hàm detect
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            for chunk in image_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        # Gửi ảnh đến API
        result = detect_deepfake_from_image(temp_file_path)
        result_value = result['result']['output']['aiProbability'] * 100

    return render(request, 'analyzer/index.html', {
        'result': result,
        'result_value': result_value
    })
