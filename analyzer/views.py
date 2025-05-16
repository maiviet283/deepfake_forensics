import json
from django.shortcuts import render
from .decopy_ai import check_image_ai_decopy
from .wasit_ai import check_image_ai_wasitai
from .combine_ai_results import combine_ai_results
from .models import Image

def index(request):
    result_decopy = None
    result_waist = None
    result_final = None
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
            result_decopy = check_image_ai_decopy(temp_file_path)
            result_waist = check_image_ai_wasitai(temp_file_path)

            isItAi_decopy = result_decopy.get('isItAi') if result_decopy else None
            isItAi_waist = result_waist.get('isItAi') if result_waist else None
            prob_decopy = result_decopy.get('probability') if result_decopy else None
            prob_waist = result_waist.get('probability') if result_waist else None

            result_final = combine_ai_results(isItAi_decopy, isItAi_waist, prob_decopy, prob_waist)

            # Cập nhật kết quả vào bản ghi Image
            try:
                if result_final:
                    image_instance.result = (
                        'F' if result_final.get('isItAi') == 'Ảnh Được Tạo Bằng AI' else
                        'R' if result_final.get('isItAi') == 'Ảnh Thật' else
                        'N'
                    )
                    image_instance.probability = result_final.get('probability', 0)
                    image_instance.save()
            except Exception as e:
                print(f"Error updating result and probability: {e}")

    return render(request, 'analyzer/index.html', {
        'image_url': image_url,
        'result_metadata': metadata,
        'result_decopy': result_decopy,
        'result_waist': result_waist,
        'result_final': result_final
    })
