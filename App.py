import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "AN Downloader Server is running!"

@app.route("/api/download", methods=["POST"])
def download():
    data = request.get_json(silent=True) or {}
    url = data.get("url", "").strip()

    if not url.startswith(("https://", "http://")):
        return jsonify({"error": "सही वीडियो लिंक डालें"}), 400

    try:
        options = {
            "format": "best",
            "quiet": True,
            "noplaylist": True,
            "skip_download": True
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)

        return jsonify({
            "title": info.get("title", "Video"),
            "download_url": info.get("url")
        })

    except Exception as e:
        return jsonify({
            "error": "वीडियो लिंक नहीं खुला। दूसरा लिंक आज़माएँ।"
        }), 400

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
