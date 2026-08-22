import os
from flask import Flask, request
import google.generativeai as genai
import requests
app = Flask(__name__)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
@app.route("/upload", methods=["POST"])
def upload_image():
  if "image" not in request.files:
    return "No image uploaded", 400
  image_file = request.files["image"]
  image_bytes = image_file.read()
  try:
    response = model.generate_content([
        (
            "Is there a human visible in this image? Answer with only one word:"
            " TRUE or FALSE."
        ),
        {"mime_type": "image/jpeg", "data": image_bytes},
    ])
    result = response.text.strip().upper()
  except Exception as e:
    return str(e), 500
  if "TRUE" in result:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    files = {"photo": ("image.jpg", image_bytes)}
    data = {"chat_id": CHAT_ID, "caption": "সতর্কবার্তা! মানুষ শনাক্ত হয়েছে।"}
    requests.post(url, data=data, files=files)
    return "Alert sent", 200
  else:
    return "Ignored", 200
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
