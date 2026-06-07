"""Start server, test email lookup, print any errors."""
import threading, time, json, urllib.request, urllib.error, sys

# Start server in background
from app.main import app
import uvicorn

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="debug")

t = threading.Thread(target=run_server, daemon=True)
t.start()
time.sleep(3)

# Make test request
url = "http://127.0.0.1:8001/api/email/lookup"
body = json.dumps({"email": "test@gmail.com"}).encode()
req = urllib.request.Request(url, data=body, method="POST", headers={"Content-Type": "application/json"})

try:
    r = urllib.request.urlopen(req, timeout=15)
    data = json.loads(r.read())
    print(f"SUCCESS: {data.get('email')} - risk: {data.get('risk_score')}")
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:1000]}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
