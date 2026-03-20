# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
# ]
# ///

import argparse
import os
import requests

API = "https://api.agentmail.to/v0"


def send(to: str, subject: str, body: str) -> dict:
    hdr = {
        "Authorization": f"Bearer {os.environ['AGENTMAIL_API_KEY']}",
        "Content-Type": "application/json",
    }
    r = requests.post(
        f"{API}/inboxes/{os.environ['AGENTMAIL_INBOX_ID']}/messages/send",
        headers=hdr,
        json={"to": to, "subject": subject, "text": body},
        timeout=10,
    )
    r.raise_for_status()
    print(f"Sent: {r.json()['message_id']}")
    return r.json()


if __name__ == "__main__":
    if "AGENTMAIL_API_KEY" not in os.environ or "AGENTMAIL_INBOX_ID" not in os.environ:
        raise ValueError(
            "AGENTMAIL_API_KEY and AGENTMAIL_INBOX_ID environment variables are required"
        )
    p = argparse.ArgumentParser(description="Send an email using AgentMail API.")
    p.add_argument("to", help="Recipient email address")
    p.add_argument("subject", help="Email subject")
    p.add_argument("body", help="Email body")
    a = p.parse_args()
    send(a.to, a.subject, a.body)
