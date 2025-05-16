import requests
import time

def check_image_ai_decopy(image_path):
    url_upload = "https://api.decopy.ai/api/decopy/ai-image-detector/create-job"

    try:
        with open(image_path, "rb") as f:
            files = {'image': (image_path.split('/')[-1], f, 'image/jpeg')}
            response = requests.post(url_upload, files=files)

        if response.status_code != 200:
            print("Upload HTTP error:", response.status_code, response.text)
            return {"error": "Upload HTTP error"}

        data = response.json()
        if data.get("code") != 100000 or "result" not in data:
            print("Upload failed:", data)
            return {"error": "Upload failed or API error"}

        request_id = data["result"]["request_id"]
        url_result = f"https://api.decopy.ai/api/decopy/ai-image-detector/get-job/{request_id}"

        # Chờ phản hồi API
        attempts = 10
        result_data = None
        for _ in range(attempts):
            time.sleep(2)  # Tăng thời gian chờ để đảm bảo task hoàn tất
            result_response = requests.get(url_result)

            if result_response.status_code != 200:
                print("Result HTTP error:", result_response.status_code, result_response.text)
                continue

            try:
                result_data = result_response.json()
            except Exception as e:
                print("Failed to parse JSON:", e, result_response.text)
                continue

            # Nếu kết quả đã sẵn sàng
            result = result_data.get("result")
            if isinstance(result, dict) and result.get("output"):
                break
            else:
                print("Waiting for result...", result_data.get("message", {}))

        if not isinstance(result_data.get("result"), dict) or "output" not in result_data["result"]:
            return {"error": "Deepfake detection failed or still processing after attempts"}

        output = result_data["result"]["output"]
        ai_probability = output['aiProbability'] * 100
        ai_probability = round(ai_probability, 2)

        # Tăng độ lệch từ 50%
        if ai_probability > 50:
            ai_probability = (ai_probability - 50) * 2
        elif ai_probability < 50:
            ai_probability = (50 - ai_probability) * 2
        else:
            ai_probability = 50

        predicted_results = 'Ảnh Thật' if output['predictedResults'] == 'real' else 'Ảnh Được Tạo Bằng AI'

        return {
            'isItAi': predicted_results,
            'probability': ai_probability,
        }

    except Exception as e:
        print("Error:", str(e))
        return {"error": str(e)}

# Gọi thử
a = check_image_ai_decopy(r'D:\IMAGES\Screenshot 2025-05-14 154814.png')
print(a)
