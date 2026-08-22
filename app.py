import os
from flask import Flask, request
import google.generativeai as genai
app = Flask(__name__)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.7-flash")
@app.route("/upload", methods=["POST"])
def upload_image():
  image_bytes = request.get_data()
  if not image_bytes or len(image_bytes) < 100:
    return "No image uploaded", 400
  try:
    # প্রম্পটটি আরও শক্তিশালী করা হলো যাতে যেকোনো উপায়ে আসা মানুষ বা চোর ধরা পড়ে
    response = model.generate_content([
        (
            "Analyze this security camera image carefully. Is there any human,"
            " intruder, or suspicious person visible (even if their face is"
            " covered, or they are partially hidden/crouching)? Answer with only"
            " one word: TRUE or FALSE."
        ),
        {"mime_type": "image/jpeg", "data": image_bytes},
    ])
    result = response.text.strip().upper()
  except Exception as e:
    return str(e), 500
  if "TRUE" in result:
    return "ALERT", 200
  else:
    return "Ignored", 200
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
