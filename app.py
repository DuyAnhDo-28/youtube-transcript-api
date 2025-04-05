from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled, NoTranscriptFound, VideoUnavailable, CouldNotRetrieveTranscript
)

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ API phụ đề YouTube đang hoạt động!"

@app.route("/transcript/<video_id>")
def get_transcript(video_id):
    lang = request.args.get("lang", "en")

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
        text = " ".join([entry["text"] for entry in transcript])
        return jsonify({ "text": text })

    except VideoUnavailable:
        return jsonify({
            "error": f"Video '{video_id}' không khả dụng hoặc bị chặn.",
            "suggestion": "Hãy thử video khác hoặc kiểm tra URL."
        }), 404

    except TranscriptsDisabled:
        return jsonify({
            "error": f"Phụ đề đã bị tắt cho video '{video_id}'."
        }), 404

    except NoTranscriptFound:
        return jsonify({
            "error": f"Không tìm thấy phụ đề cho video '{video_id}' với ngôn ngữ '{lang}'.",
            "suggestion": "Thử video khác hoặc thêm ?lang=vi nếu có phụ đề tiếng Việt."
        }), 404

    except CouldNotRetrieveTranscript:
        return jsonify({
            "error": "Không thể lấy phụ đề do lỗi không xác định từ YouTube.",
            "suggestion": "Thử lại sau hoặc video không hỗ trợ phụ đề."
        }), 500

    except Exception as e:
        return jsonify({ "error": str(e) }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
