import os, json, requests

START, END = "2024-05-08", "2024-05-13"
SOURCES = [
    ("https://ccmc.gsfc.nasa.gov/DONKI-API/get/", {}),
    ("https://api.nasa.gov/DONKI/", {"api_key": os.environ.get("NASA_API_KEY", "DEMO_KEY")}),
]

def fetch(kind):
    for base, extra in SOURCES:
        params = {"startDate": START, "endDate": END, **extra}
        try:
            r = requests.get(base + kind, params=params, timeout=20)
            r.raise_for_status()
            print(kind, "OK from", base)
            return r.json()
        except (requests.RequestException, ValueError) as e:
            print(kind, "failed from", base, "->", e)
    return []

if __name__ == "__main__":
    data = {k: fetch(k) for k in ("FLR", "CME", "GST")}
    os.makedirs("data", exist_ok=True)
    with open("data/donki_archive.json", "w") as f:
        json.dump(data, f, indent=2)
    for k, v in data.items():
        print(k, len(v), "events")
    for ev in data["FLR"]:
        print(ev.get("beginTime"), ev.get("classType"))