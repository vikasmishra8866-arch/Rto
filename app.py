import os
import requests
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

TARGET_API_BASE = "https://cjpindia.vercel.app/api/vehicle-details/"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/vehicle/<vehicle_no>", methods=["GET"])
def get_vehicle_details(vehicle_no):
    vehicle_no = str(vehicle_no).strip().upper()
    target_url = f"{TARGET_API_BASE}{vehicle_no}"
    
    headers = {
        "User-Agent": USER_AGENTS[0],
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://cjpindia.vercel.app/"
    }
    
    try:
        response = requests.get(target_url, headers=headers, timeout=18)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({
                "error": "Upstream service error",
                "status_code": response.status_code,
                "message": response.text
            }), response.status_code
    except requests.exceptions.Timeout:
        return jsonify({"error": "Gateway timeout", "message": "API took too long to respond."}), 504
    except Exception as e:
        return jsonify({"error": "Internal proxy error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
