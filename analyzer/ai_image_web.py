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

        if data.get("code") == 100000:
            request_id = data["result"]["request_id"]
            url_result = f"https://api.decopy.ai/api/decopy/ai-image-detector/get-job/{request_id}"

            time.sleep(1)

            result_response = requests.get(url_result)
            result_data = result_response.json()

            aiProbability = result_data['result']['output']['aiProbability'] * 100
            predictedResults = result_data['result']['output']['predictedResults']

            return ({
                'aiProbability':aiProbability,
                'predictedResults': predictedResults
            })
        
        else:
            print("Upload failed.")
            return None
    except Exception as e:
        print("Error:", str(e))
        return None
