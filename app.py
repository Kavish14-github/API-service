from flask import Flask, request, jsonify
import tempfile
import subprocess
import os
import json
import uuid

app = Flask(__name__)

def run_script_safely(script: str):
    script_id = str(uuid.uuid4())
    script_path = f"/tmp/script_{script_id}.py"
    output_path = f"/tmp/output_{script_id}.json"

    try:
        # Wrap the script to extract only return value of main()
        with open(script_path, "w") as f:
            f.write(script)
            f.write("\n\n")
            f.write("import json\n")
            f.write("try:\n")
            f.write("    result = main()\n")
            f.write("    with open('" + output_path + "', 'w') as out:\n")
            f.write("        json.dump(result, out)\n")
            f.write("except Exception as e:\n")
            f.write("    with open('" + output_path + "', 'w') as out:\n")
            f.write("        json.dump({'error': str(e)}, out)\n")

        # Run the script with timeout (10 seconds)
        result = subprocess.run(
            ["python3", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )

        # Load result if created
        if os.path.exists(output_path):
            with open(output_path) as f:
                output = json.load(f)
        else:
            output = {"error": "No output returned."}

        return {
            "returncode": result.returncode,
            "stdout": result.stdout.decode(),
            "stderr": result.stderr.decode(),
            "result": output
        }

    finally:
        # Clean up
        if os.path.exists(script_path):
            os.remove(script_path)
        if os.path.exists(output_path):
            os.remove(output_path)

@app.route("/execute", methods=["POST"])
def execute():
    data = request.get_json()
    script = data.get("script")

    if not script or "def main" not in script:
        return jsonify({"error": "Script must contain a 'main()' function."}), 400

    result = run_script_safely(script)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
