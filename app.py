import os
from flask import Flask, request
import google.generativeai as genai
app = Flask(__name__)
# জেমিনি এপিআই কনফিগারেশন
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
@app.route("/upload", methods=["POST"])
def upload_image():
  # সরাসরি রিকোয়েস্টের বডি থেকে বাইনারি ইমেজ ডেটা নেওয়া
  image_bytes = request.get_data()
  if not image_bytes or len(image_bytes) < 100:
    return "No image uploaded", 400
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
    return "ALERT", 200
  else:
    return "Ignored", 200
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
