from django.shortcuts import render
from PIL import Image, ImageChops, ImageEnhance
import os
from django.core.files.storage import default_storage
from django.conf import settings

def error_level_analysis(img_path, quality=90):
    original = Image.open(img_path).convert('RGB')
    
    # Lưu ảnh tạm thời với chất lượng nén
    temp_path = img_path + ".resaved.jpg"
    original.save(temp_path, 'JPEG', quality=quality)

    # Mở lại ảnh đã nén
    resaved = Image.open(temp_path)

    # Trừ ảnh gốc và ảnh nén
    diff = ImageChops.difference(original, resaved)

    # Tăng độ tương phản
    extrema = diff.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    scale = 255.0 / max_diff if max_diff != 0 else 1
    diff = ImageEnhance.Brightness(diff).enhance(scale)

    # Lưu ảnh ELA
    ela_path = img_path + ".ela.jpg"
    diff.save(ela_path)

    return ela_path

def index(request):
    result_path = None
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        file_path = default_storage.save('tmp/' + image_file.name, image_file)
        full_path = default_storage.path(file_path)

        # Phân tích ảnh
        ela_result = error_level_analysis(full_path)
        result_path = ela_result.replace(settings.MEDIA_ROOT, settings.MEDIA_URL).replace("\\", "/")

    return render(request, 'analyzer/index.html', {
        'ela_image': result_path
    })
