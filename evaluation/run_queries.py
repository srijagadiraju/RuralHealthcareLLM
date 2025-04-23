"""
Robust query runner that
  * obeys Gemini free-tier 15 req/min limit
  * retries on 429 with server-suggested back-off
"""

import json, time, requests, pathlib, argparse
from google.protobuf.json_format import MessageToDict

API_URL  = "http://localhost:8000/generate-answer"     # change if deployed
OUT_FILE = pathlib.Path("responses.json")
MAX_RPM  = 15                                          # free-tier limit
MIN_DELAY = 60 / MAX_RPM                               # 4 seconds

def safe_call(query: str, max_retries: int = 5):
    tries = 0
    while tries < max_retries:
        try:
            r = requests.get(API_URL, params={"query": query}, timeout=40)
            if r.status_code == 429:
                # extract retry delay if FastAPI propagated it
                try:
                    delay = r.json().get("retry_delay", {}).get("seconds", MIN_DELAY)
                except Exception:
                    delay = MIN_DELAY
                delay = max(float(delay), MIN_DELAY)
                print(f"⚠  429 – sleeping {delay:.0f}s")
                time.sleep(delay)
                tries += 1
                continue

            r.raise_for_status()
            return r.json()

        except requests.exceptions.RequestException as e:
            print(f"✖  {query[:40]}… failed ({e}), retry {tries+1}/{max_retries}")
            time.sleep(2 ** tries)       # exponential back-off
            tries += 1
    return {"query": query, "error": "max_retries_exceeded", "context_used": []}

def main(qfile):
    queries = json.loads(pathlib.Path(qfile).read_text())
    out = []

    for i, q in enumerate(queries, 1):
        print(f"[{i:03}/{len(queries)}]  {q}")
        out.append(safe_call(q))
        time.sleep(MIN_DELAY)            # throttle to 15 rpm

    OUT_FILE.write_text(json.dumps(out, indent=2))
    print(f"✔ saved {len(out)} responses to {OUT_FILE}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--queries", default="queries.json")
    args = ap.parse_args()
    main(args.queries)
