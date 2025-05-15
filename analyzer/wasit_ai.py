import requests
import mimetypes

def check_image_ai_wasitai(image_path):
    url = "https://wasitai.com/api/images/check-is-it-ai"

    try:
        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type:
            mime_type = 'image/jpeg'  # fallback

        with open(image_path, 'rb') as f:
            files = {
                'file': (image_path.split('/')[-1], f, mime_type)  # phải dùng 'file'
            }
            response = requests.post(url, files=files)

        if response.status_code != 200:
            print("Upload failed:", response.status_code, response.text)
            return {"error": f"Request failed with status code {response.status_code}"}

        data = response.json()

        probability = 0
        if data.get('isItAi') == True:
            isItAi = 'Ảnh Được Tạo Bằng AI'
            if data.get('classificationSliderBlock') == 1:
                probability = 50
            elif data.get('classificationSliderBlock') == 2:
                probability = 100
        else: 
            isItAi = 'Ảnh Thật'
            if data.get('classificationSliderBlock') == 1:
                probability = 50
            elif data.get('classificationSliderBlock') == 2:
                probability = 100

        return {
            'isItAi': isItAi,
            'description': data.get('classificationDescription'),
            'probability': probability,
        }

    except Exception as e:
        print("Error:", str(e))
        return {"error": str(e)}
