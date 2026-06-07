import subprocess, time, json, urllib.request, urllib.error, sys

proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8002"],
    cwd="D:\\email look\\email-insight\\backend",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
time.sleep(4)

url = "http://127.0.0.1:8002/api/email/lookup"
body = json.dumps({"email": "test@gmail.com"}).encode()
req = urllib.request.Request(url, data=body, method="POST", headers={"Content-Type": "application/json"})

try:
    r = urllib.request.urlopen(req, timeout=15)
    data = json.loads(r.read())
    print("SUCCESS:", data.get("email"), "- risk:", data.get("risk_score"))
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"HTTP {e.code}: {body[:500]}")
except Exception as e:
    print(f"ERROR: {e}")

time.sleep(1)
# Read server stderr for errors
proc.terminate()
stderr = proc.stderr.read()
if "Traceback" in stderr:
    print("\n=== SERVER ERROR ===")
    print(stderr[-2000:])
else:
    print("\nNo traceback in server output")
