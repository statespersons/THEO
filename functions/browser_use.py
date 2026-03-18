# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
# ]
# ///

import argparse, json, os, time, requests

API = "https://api.browser-use.com/api/v2"


def get_headers():
    return {"X-Browser-Use-API-Key": os.environ.get("BROWSER_USE_API_KEY", "")}


def browser_subagent(task: str, url: str | None = None) -> dict:
    proxy = None
    if os.environ.get("PROXY_HOST"):
        proxy = {
            "host": os.environ["PROXY_HOST"],
            "port": int(os.environ["PROXY_PORT"])
            if os.environ.get("PROXY_PORT")
            else None,
            "username": os.environ.get("PROXY_USER"),
            "password": os.environ.get("PROXY_PASS"),
        }

    body = {
        "task": task,
        "sessionSettings": {
            "profileId": os.environ.get("BROWSER_USE_PROFILE_ID"),
            "customProxy": proxy,
        },
    }
    if url:
        body["startUrl"] = url

    hdr = get_headers()
    res = requests.post(f"{API}/tasks", json=body, headers=hdr)
    res.raise_for_status()
    tid = res.json()["id"]
    print(f"Task {tid} started")

    while True:
        time.sleep(5)
        r = requests.get(f"{API}/tasks/{tid}/status", headers=hdr)
        r.raise_for_status()
        if r.json()["status"] in ("finished", "stopped"):
            break

    detail_res = requests.get(f"{API}/tasks/{tid}", headers=hdr)
    detail_res.raise_for_status()
    detail = detail_res.json()
    os.makedirs("browser-use-traces", exist_ok=True)
    with open(f"browser-use-traces/{tid}.json", "w") as f:
        json.dump(detail, f, indent=2)
    print(f"{detail['status']} | {detail.get('output', 'None')}")
    return detail


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Run a task using the browser-use API.")
    p.add_argument("task", help="The task for the browser subagent to perform")
    p.add_argument("--url", "-u", help="Optional starting URL", default=None)
    a = p.parse_args()
    browser_subagent(a.task, a.url)
