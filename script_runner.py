import sys
import importlib.util
import json
import traceback

def run(script_path):
    try:
        spec = importlib.util.spec_from_file_location("user_script", script_path)
        user_script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_script)

        if not hasattr(user_script, "main"):
            raise AttributeError("No main() function found")

        result = user_script.main()

        if not isinstance(result, dict):
            raise TypeError("main() must return a JSON-compatible dictionary")

        print(json.dumps({"result": result, "stdout": ""}))
    except Exception as e:
        print(json.dumps({"result": None, "stdout": traceback.format_exc()}))
        sys.exit(1)

if __name__ == "__main__":
    run(sys.argv[1])
