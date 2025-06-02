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

# Python Code Execution Service

This service securely executes user-submitted Python scripts in a sandboxed environment using `nsjail`. It exposes a REST API that accepts code and returns its output, ensuring security and resource control.

---

## ✅ How to Use

### Endpoint

POST https://kavish-cloudrun-project-94871636326.europe-west1.run.app/execute


### Request Body (JSON)

```json
{
  "script": "def main():\n  return {\"key\": \"value\"}"
}
```
Response Format

```json
{
  "result": { ... },        // returned by main()
  "returncode": 0,
  "stderr": "",
  "stdout": ""              // captured output (e.g. print)
}
```

✅ Valid Example Commands
1. Return success message
```bash   
   curl -X POST https://kavish-cloudrun-project-94871636326.europe-west1.run.app/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n  return {\"status\": \"success\", \"message\": \"Hello from main!\"}"}'
```
```json
{"result":{"status":"success","message":"Hello from main!"},"returncode":0,"stderr":"","stdout":""}

```
2. Print in script, but still returns main()
```bash   
   curl -X POST https://kavish-cloudrun-project-94871636326.europe-west1.run.app/execute \
  -H "Content-Type: application/json" \
  -d "{\"script\": \"def main():\\n  print(\\\"This should not be in output\\\")\\n  return {\\\"result\\\": 123}\"}"

```
```json
{"result":{"result":123},"returncode":0,"stderr":"","stdout":"This should not be in output\n"}
```
3. Loop and return dictionary
```bash   
  curl -X POST https://kavish-cloudrun-project-94871636326.europe-west1.run.app/execute \
  -H "Content-Type: application/json" \
  -d "{\"script\": \"def main():\\n  data = {\\\"count\\\": 5}\\n  for i in range(data[\\\"count\\\"]):\\n    pass\\n  return data\"}"

```
```json
{"result":{"count":5},"returncode":0,"stderr":"","stdout":""}
```
4. File system access (may vary)
```bash   
  curl -X POST https://kavish-cloudrun-project-94871636326.europe-west1.run.app/execute \
  -H "Content-Type: application/json" \
  -d "{\"script\": \"def main():\\n  import os\\n  return os.listdir(\\\"/\\\")\"}"
```
```json
{"result":["usr","app","bin",...],"returncode":0,"stderr":"","stdout":""}
```
5. Invalid Script: Missing main() function
```bash   
   curl -X POST https://kavish-cloudrun-project-94871636326.europe-west1.run.app/execute \
  -H "Content-Type: application/json" \
  -d "{\"script\": \"def not_main():\\n  return {\\\"msg\\\": \\\"no main function\\\"}\"}"

```
```json
{ "error": "No main() function found"}
```   
6. Invalid Return Type: main() does not return a dictionary
 ```bash   
  curl -X POST https://kavish-cloudrun-project-94871636326.europe-west1.run.app/execute \
  -H "Content-Type: application/json" \
  -d "{\"script\": \"def main():\\n  return 42\"}"
```
```json
{"error": "main() must return a JSON-compatible dictionary"}
```   
7. Syntax Error in Script
 ```bash   
  curl -X POST https://kavish-cloudrun-project-94871636326.europe-west1.run.app/execute \
  -H "Content-Type: application/json" \
  -d "{\"script\": \"def main(:\\n  return {\\\"msg\\\": \\\"syntax error\\\"}\"}"
```
```json
{ "error": "<traceback showing syntax error>"}
```  
8. Empty Script
 ```bash   
  curl -X POST https://kavish-cloudrun-project-94871636326.europe-west1.run.app/execute \
  -H "Content-Type: application/json" \
  -d "{\"script\": \"\"}"
```
```json
{ "error": "No main() function found"}
```  
   
