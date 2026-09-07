from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Coli Blender API is running!"

@app.route("/render", methods=["POST"])
def render():
    data = request.get_json()

    blender_code = data.get("blender_code")

    if not blender_code:
        return jsonify({
            "success": False,
            "error": "No blender_code received"
        }), 400

    return jsonify({
        "success": True,
        "message": "Blender code received"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
