# Python Code Execution Service

This service provides an API endpoint that executes arbitrary Python code in a sandboxed environment and returns the result.

## Features

- Executes Python code in a secure sandbox using nsjail
- Returns the result of the main() function along with stdout
- Input validation to ensure script contains a main() function
- Protection against potentially malicious code
- Support for common libraries like pandas and numpy

## Running Locally

To run the service locally:

```bash
docker build -t python-executor .
docker run -p 8080:8080 python-executor
```

## API Usage

### Execute Code

**Endpoint:** POST /execute

**Request Body:**
```json
{
  "script": "def main():\n    return {'message': 'Hello World'}"
}
```

**Response:**
```json
{
  "result": {"message": "Hello World"},
  "stdout": ""
}
```

### Example cURL Request

```bash
curl -X POST https://python-executor-abcxyz123.run.app/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n    import pandas as pd\n    import numpy as np\n    data = {\"A\": [1, 2, 3], \"B\": [4, 5, 6]}\n    df = pd.DataFrame(data)\n    return {\"sum\": int(np.sum(df[\"A\"]))}"}'
```

## Security Considerations

- The service uses nsjail to sandbox the Python execution environment
- Resource limits are enforced to prevent DoS attacks
- Basic validation checks prevent common malicious patterns
- File system access is restricted
- Network access is disabled

## Dependencies

- Flask: Web framework
- nsjail: Sandbox environment
- Python 3.9: Runtime environment
- pandas, numpy: Available libraries for scripts


Python Code Execution Service - Documentation
✅ Valid Usage and Expected Results
This service securely executes user-submitted Python scripts in a sandboxed environment using nsjail. It exposes a REST API that accepts code and returns its output, ensuring security and resource control.
Endpoint
POST https://kavish-cloudrun-project-94871636326.europe-west1.run.app/execute
Request Body (JSON)
{
  "script": "def main():\n  return {\"key\": \"value\"}"
}
Response Format
{
  "result": { ... },
  "returncode": 0,
  "stderr": "",
  "stdout": ""
}
Return success message
curl -X POST https://kavish-cloudrun-project-94871636326.europe-west1.run.app/execute -H "Content-Type: application/json" -d "{\"script\": \"def main():\n  return {\"status\": \"success\", \"message\": \"Hello from main!\"}\"}"
Response:
{"result":{"status":"success","message":"Hello from main!"},"returncode":0,"stderr":"","stdout":""}
Print in script, but still returns main()
curl -X POST https://kavish-cloudrun-project-94871636326.europe-west1.run.app/execute -H "Content-Type: application/json" -d "{\"script\": \"def main():\n  print(\\\"This should not be in output\\\")\n  return {\"result\": 123}\"}"
Response:
{"result":{"result":123},"returncode":0,"stderr":"","stdout":"This should not be in output\n"}
Loop and return dictionary
curl -X POST https://kavish-cloudrun-project-94871636326.europe-west1.run.app/execute -H "Content-Type: application/json" -d "{\"script\": \"def main():\n  data = {\"count\": 5}\n  for i in range(data[\"count\"]):\n    pass\n  return data\"}"
Response:
{"result":{"count":5},"returncode":0,"stderr":"","stdout":""}
File system access (may vary)
curl -X POST https://kavish-cloudrun-project-94871636326.europe-west1.run.app/execute -H "Content-Type: application/json" -d "{\"script\": \"def main():\n  import os\n  return os.listdir(\\"/\\")\"}"
Response:
{"result":["usr","app","bin",...],"returncode":0,"stderr":"","stdout":""}


❌ Invalid Usage and Fixes
No main() function
Script or Command:
def not_main():\n  return {\"msg\": \"no main function\"}
Output:
{"error":"Script must contain a 'main()' function."}
Fix:
Define a `main()` function.
main() returns a non-dict
Script or Command:
def main():\n  return 42
Output:
{"result":42,...}
Fix:
Add type check to ensure return value is a dictionary.
Syntax error in script
Script or Command:
def main(:\n  return {\"msg\": \"syntax error\"}
Output:
SyntaxError
Fix:
Fix function definition: def main():
Empty script
Script or Command:

Output:
{"error":"Script must contain a 'main()' function."}
Fix:
Provide a valid `main()` function.
Incorrect curl formatting (Windows CMD)
Script or Command:
curl -X POST http://localhost:8080/execute \ -H ...
Output:
curl: (3) URL rejected: Bad hostname
Fix:
Use single line without backslashes on Windows.
File access not restricted
Script or Command:
def main():\n  import os\n  return os.listdir(\"/\")
Output:
Shows system directories
Fix:
Restrict mounts and access in `nsjail.cfg`.
