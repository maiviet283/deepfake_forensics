import requests
import time

def check_image_ai_decopy(image_path):
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
                break 

        if not result_data or "output" not in result_data.get("result", {}):
            return {"error": "Deepfake detection failed"}

        ai_probability = result_data['result']['output']['aiProbability'] * 100
        ai_probability = round(ai_probability, 2)

        if ai_probability > 50:
            ai_probability = (ai_probability-50) * 2
        elif ai_probability < 50:
            ai_probability = ai_probability * 2
        else:
            ai_probability = 50

        if result_data['result']['output']['predictedResults'] == 'real':
            predicted_results = 'Ảnh Thật'
        else : predicted_results = 'Ảnh Được Tạo Bằng AI'

        return {
            'isItAi': predicted_results,
            'probability': ai_probability,
        }

    except Exception as e:
        print("Error:", str(e))
        return {"error": str(e)}
