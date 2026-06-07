import urllib.request, json

headers = {
    "apikey": "sb_publishable_3qrj8vX-u6sximQuTpSJXw_LhHBHycU",
    "Authorization": "Bearer sb_publishable_3qrj8vX-u6sximQuTpSJXw_LhHBHycU",
}

urls = [
    "https://api.supabase.com/v1/projects",
    "https://api.supabase.co/v1/projects",
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        r = urllib.request.urlopen(req, timeout=10)
        data = json.loads(r.read())
        print(f"{url}: OK")
        for p in data:
            print(f"  Name: {p.get('name')}")
            print(f"  Ref: {p.get('ref')}")
            print(f"  Region: {p.get('region')}")
            print(f"  Org: {p.get('organization_id')}")
        break
    except urllib.error.HTTPError as e:
        print(f"{url}: HTTP {e.code} {e.read().decode()[:200]}")
    except Exception as e:
        print(f"{url}: {e}")
