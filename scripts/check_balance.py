# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
# ]
# ///

"""Check Vercel AI Gateway credit balance."""

import argparse, os, requests


def check() -> dict:
    r = requests.get(
        "https://ai-gateway.vercel.sh/v1/credits",
        headers={"Authorization": f"Bearer {os.environ['AI_GATEWAY_API_KEY']}"},
    )
    r.raise_for_status()
    c = r.json()
    print(f"Balance: ${c['balance']} | Used: ${c['total_used']}")
    return c


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Check Vercel AI Gateway credit balance.")
    p.parse_args()
    check()
