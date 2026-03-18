# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pynacl",
#     "requests",
# ]
# ///

import argparse, base64, os, requests
from nacl import encoding, public


def encrypt(pub_key: str, value: str) -> str:
    key = public.PublicKey(pub_key.encode(), encoding.Base64Encoder)
    return base64.b64encode(public.SealedBox(key).encrypt(value.encode())).decode()


def sync(repo: str):
    hdr = {
        "Authorization": f"token {os.environ['REPO_PAT']}",
        "Accept": "application/vnd.github+json",
    }
    pk = requests.get(
        f"https://api.github.com/repos/{repo}/actions/secrets/public-key", headers=hdr
    ).json()

    secrets = {}
    if os.path.exists(".env"):
        for line in open(".env"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                secrets[k.strip()] = v.strip()

    for k, v in secrets.items():
        requests.put(
            f"https://api.github.com/repos/{repo}/actions/secrets/{k}",
            headers=hdr,
            json={"encrypted_value": encrypt(pk["key"], v), "key_id": pk["key_id"]},
        )

    print(f"Synced {len(secrets)} secrets to {repo}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Sync secrets to a GitHub repository.")
    p.add_argument("repo", help="The GitHub repository (e.g., owner/repo)")
    a = p.parse_args()
    sync(a.repo)
