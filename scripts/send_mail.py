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
        "Authorization": f"Bearer {os.environ.get('AGENTMAIL_API_KEY')}",
        "Content-Type": "application/json",
    }
    r = requests.post(
        f"{API}/inboxes/{os.environ.get('AGENTMAIL_INBOX_ID')}/messages/send",
        headers=hdr,
        json={"to": to, "subject": subject, "text": body},
    )
    r.raise_for_status()
    print(f"Sent: {r.json()['message_id']}")
    return r.json()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Send an email using AgentMail API.")
    p.add_argument("to", help="Recipient email address")
    p.add_argument("subject", help="Email subject")
    p.add_argument("body", help="Email body")
    a = p.parse_args()
    send(a.to, a.subject, a.body)
