
from flask import Flask, request, jsonify
import secrets

app = Flask(__name__)

api_keys = {
    secrets.token_hex(16): "Consumer 1",
    secrets.token_hex(16): "Consumer 2",
    secrets.token_hex(16): "Consumer 3"
}

print("\n========== ROOTSOFTWARE API KEYS ==========")
for key, consumer in api_keys.items():
    print(consumer, ":", key)
print("===========================================\n")


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "RootSoftware API is running"})


@app.route("/process", methods=["POST"])
def process_text():

    key = request.headers.get("X-API-Key")

    if not key or key not in api_keys:
        return jsonify({"error": "Missing or Invalid API Key"}), 401

    data = request.get_json(silent=True)

    if not data or not isinstance(data.get("text"), str) or not data.get("text").strip():
        return jsonify({"error": "Text is required"}), 400

    text = data["text"]

    return jsonify({
        "consumer": api_keys[key],
        "original_text": text,
        "processed_text": text.upper(),
        "status": "Success"
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5001, use_reloader=False)
