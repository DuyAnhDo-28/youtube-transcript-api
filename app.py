from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Transcript API hoạt động!"

@app.route("/transcript/<video_id>")
def get_transcript(video_id):
    lang = request.args.get("lang", "en")
    fallback_langs = [lang, "vi", "en", "en-US", "vi-VN", "auto"]

    for l in fallback_langs:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[l])
            full_text = " ".join([entry['text'] for entry in transcript])
            return jsonify({"text": full_text})
        except NoTranscriptFound:
            continue
        except TranscriptsDisabled:
            return jsonify({
                "error": "Video này đã tắt phụ đề.",
                "suggestion": "Hãy thử video khác."
            }), 403
        except VideoUnavailable:
            return jsonify({
                "error": "Video không tồn tại hoặc bị giới hạn khu vực."
            }), 404
        except Exception as e:
            return jsonify({
                "error": "Lỗi không xác định.",
                "details": str(e)
            }), 500

    return jsonify({
        "error": f"Không tìm thấy phụ đề cho video '{video_id}' với ngôn ngữ '{lang}'.",
        "suggestion": "Thử video khác hoặc thêm ?lang=vi nếu có phụ đề tiếng Việt."
    }), 404

@app.route("/debug/<video_id>")
def debug_languages(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        langs = [t.language_code for t in transcript_list]
        return jsonify({
            "available_languages": langs
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
