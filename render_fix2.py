import urllib.request, json

api_key = "rnd_szEpz4CEWUJrWwqq6ZrnC3jRdv0J"
headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}

req = urllib.request.Request("https://api.render.com/v1/services", headers=headers)
r = urllib.request.urlopen(req)
d = json.loads(r.read())
srv = d[0]["service"]
sd = srv["serviceDetails"]
sid = srv["id"]

print(f"Service: {srv['name']} ({sid})")

# Minimal PATCH - just the essential fields
body = {
    "serviceDetails": {
        "envSpecificDetails": sd.get("envSpecificDetails"),
        "healthCheckPath": sd.get("healthCheckPath", ""),
        "numInstances": sd.get("numInstances"),
    }
}

patch_headers = {**headers, "Content-Type": "application/json"}
data = json.dumps(body).encode()
patch_url = f"https://api.render.com/v1/services/{sid}"
req = urllib.request.Request(patch_url, data=data, headers=patch_headers, method="PATCH")
try:
    r = urllib.request.urlopen(req)
    print(f"PATCH response: {r.status}")
    resp = json.loads(r.read())
    s = resp.get("service", {}).get("serviceDetails", {}).get("envSpecificDetails", {})
    print(f"After patch - build: {s.get('buildCommand')}, start: {s.get('startCommand')}")
except urllib.error.HTTPError as e:
    print(f"PATCH failed: {e.code}")
    print(e.read().decode()[:500])
