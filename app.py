from flask import Flask, request, Response
import requests
import xml.etree.ElementTree as ET
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Transcript API hoạt động!"

@app.route("/transcript/<video_id>")
def get_transcript(video_id):
    lang = request.args.get("lang", "en")
    url = f"https://video.google.com/timedtext?lang={lang}&v={video_id}"

    try:
        response = requests.get(url)
        if response.status_code != 200 or not response.text.strip():
            raise Exception("Transcript not found or video unavailable")

        root = ET.fromstring(response.content)
        texts = []

        for child in root.findall("text"):
            line = child.text or ""
            line = (line
                .replace("&amp;", "&")
                .replace("&#39;", "'")
                .replace("&quot;", '"')
                .replace("&lt;", "<")
                .replace("&gt;", ">"))
            texts.append(line)

        full_text = " ".join(texts)

        return Response(
            json.dumps({"text": full_text}, ensure_ascii=False),
            content_type="application/json; charset=utf-8"
        )

    except Exception as e:
        error = {
            "error": f"Không tìm thấy phụ đề cho video '{video_id}' với ngôn ngữ '{lang}'.",
            "suggestion": "Thử video khác hoặc thêm ?lang=vi nếu có phụ đề tiếng Việt."
        }
        return Response(
            json.dumps(error, ensure_ascii=False),
            content_type="application/json; charset=utf-8"
        )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
