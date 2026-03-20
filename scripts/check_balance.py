# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
# ]
# ///

"""Check Vercel AI Gateway credit balance."""

import argparse
import os
import requests


def check() -> dict:
    r = requests.get(
        "https://ai-gateway.vercel.sh/v1/credits",
        headers={"Authorization": f"Bearer {os.environ['AI_GATEWAY_API_KEY']}"},
        timeout=10,
    )
    r.raise_for_status()
    c = r.json()
    print(f"Balance: ${c['balance']} | Used: ${c['total_used']}")
    return c


if __name__ == "__main__":
    if "AI_GATEWAY_API_KEY" not in os.environ:
        raise ValueError("AI_GATEWAY_API_KEY environment variable is required")
    p = argparse.ArgumentParser(description="Check Vercel AI Gateway credit balance.")
    p.parse_args()
    check()
