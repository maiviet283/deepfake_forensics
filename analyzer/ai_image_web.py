import requests
import time

def detect_deepfake_from_image(image_path):
    """
    Gửi ảnh đến API decopy.ai để phân tích deepfake và trả về kết quả.
    
    :param image_path: Đường dẫn tới file ảnh cần phân tích
    :return: dict kết quả nếu thành công, hoặc None nếu thất bại
    """
    url_upload = "https://api.decopy.ai/api/decopy/ai-image-detector/create-job"

    try:
        with open(image_path, "rb") as f:
            files = {'image': (image_path.split('/')[-1], f, 'image/jpeg')}
            response = requests.post(url_upload, files=files)

        data = response.json()
        if data.get("code") != 100000 or "result" not in data:
            print("Upload failed:", data)
            return {"error": "Upload failed or API error"}

        request_id = data["result"]["request_id"]
        url_result = f"https://api.decopy.ai/api/decopy/ai-image-detector/get-job/{request_id}"

        # Chờ phản hồi API một cách linh hoạt
        attempts = 5
        result_data = None
        for _ in range(attempts):
            time.sleep(1)  # Đợi 1 giây trước mỗi lần thử
            result_response = requests.get(url_result)
            result_data = result_response.json()
            if result_data.get("result", {}).get("output"):
                break  # Thoát vòng lặp khi nhận dữ liệu hợp lệ

        if not result_data or "output" not in result_data.get("result", {}):
            return {"error": "Deepfake detection failed"}

        ai_probability = result_data['result']['output']['aiProbability'] * 100
        predicted_results = result_data['result']['output']['predictedResults']

        return {
            'aiProbability': ai_probability,
            'predictedResults': predicted_results
        }

    except Exception as e:
        print("Error:", str(e))
        return {"error": str(e)}
