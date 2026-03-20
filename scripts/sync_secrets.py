# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pynacl",
#     "requests",
# ]
# ///

import argparse
import base64
import os
import requests
from nacl import encoding, public


def encrypt(pub_key: str, value: str) -> str:
    key = public.PublicKey(pub_key.encode(), encoding.Base64Encoder)
    return base64.b64encode(public.SealedBox(key).encrypt(value.encode())).decode()


def sync(repo: str) -> None:
    hdr = {
        "Authorization": f"token {os.environ['REPO_PAT']}",
        "Accept": "application/vnd.github+json",
    }
    pk_res = requests.get(
        f"https://api.github.com/repos/{repo}/actions/secrets/public-key",
        headers=hdr,
        timeout=10,
    )
    pk_res.raise_for_status()
    pk = pk_res.json()

    secrets = {}
    if os.path.exists(".env"):
        with open(".env") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    secrets[k.strip()] = v.strip().strip("'\"")

    for k, v in secrets.items():
        res = requests.put(
            f"https://api.github.com/repos/{repo}/actions/secrets/{k}",
            headers=hdr,
            json={"encrypted_value": encrypt(pk["key"], v), "key_id": pk["key_id"]},
            timeout=10,
        )
        res.raise_for_status()

    print(f"Synced {len(secrets)} secrets to {repo}")


if __name__ == "__main__":
    if "REPO_PAT" not in os.environ:
        raise ValueError("REPO_PAT environment variable is required")
    p = argparse.ArgumentParser(description="Sync secrets to a GitHub repository.")
    p.add_argument("repo", help="The GitHub repository (e.g., owner/repo)")
    a = p.parse_args()
    sync(a.repo)
