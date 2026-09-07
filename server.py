from flask import Flask, request, jsonify
import subprocess
import tempfile
import os

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

    script_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False
        ) as script:
            script.write(blender_code)
            script_path = script.name

        result = subprocess.run(
            [
                "blender",
                "--background",
                "--python",
                script_path
            ],
            capture_output=True,
            text=True,
            timeout=300
        )

        return jsonify({
            "success": result.returncode == 0,
            "message": "Blender code executed",
            "output": result.stdout[-5000:],
            "error": result.stderr[-5000:]
        })

    except subprocess.TimeoutExpired:
        return jsonify({
            "success": False,
            "error": "Blender timed out"
        }), 504

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:
        if script_path and os.path.exists(script_path):
            os.remove(script_path)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
