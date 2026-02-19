from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
import tempfile
import os

app = Flask(__name__)
CORS(app)

print("Loading Whisper model...")
model = whisper.load_model("base")
print("Model ready.")


@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    ext = os.path.splitext(file.filename)[1] if file.filename else ".webm"

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        result = model.transcribe(tmp_path)
        return jsonify({"text": result["text"]})
    finally:
        os.unlink(tmp_path)


if __name__ == "__main__":
    app.run(port=5000, debug=False)
