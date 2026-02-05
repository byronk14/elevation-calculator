import requests
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


def calculate_elevation(lat, lon):
    """Get elevation for a single point using Open-Elevation API."""
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    response = requests.get(url, timeout=10)
    data = response.json()
    return data["results"][0]["elevation"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/elevation", methods=["POST"])
def get_elevation_difference():
    data = request.get_json()
    lat1 = data.get("lat1")
    lon1 = data.get("lon1")
    lat2 = data.get("lat2")
    lon2 = data.get("lon2")

    if not all([lat1, lon1, lat2, lon2]):
        return jsonify({"error": "Missing coordinates"}), 400

    try:
        elevation1 = calculate_elevation(lat1, lon1)
        elevation2 = calculate_elevation(lat2, lon2)
        difference = abs(elevation1 - elevation2)

        return jsonify({
            "elevation1": elevation1,
            "elevation2": elevation2,
            "difference": difference
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
