from flask import Flask, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Transcript API Flask is running!"

@app.route("/transcript/<video_id>")
def get_transcript(video_id):
    lang = "en"
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
        text = " ".join([entry["text"] for entry in transcript])
        return jsonify({"text": text})
    except TranscriptsDisabled:
        return jsonify({"error": "Phụ đề bị tắt với video này."}), 404
    except NoTranscriptFound:
        return jsonify({
            "error": f"Không tìm thấy phụ đề cho video '{video_id}' với ngôn ngữ '{lang}'.",
            "suggestion": "Hãy thử ngôn ngữ khác như ?lang=vi nếu video có phụ đề tiếng Việt."
        }), 404
    except VideoUnavailable:
        return jsonify({"error": "Video không khả dụng hoặc bị xóa."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
