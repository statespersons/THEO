# /// script
# requires-python = ">=3.12"
# ///

import argparse
import os
import subprocess


def sync(schedule_file: str, repo: str, token: str) -> None:
    cron = ""
    with open(schedule_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            time, prompt = line.split(maxsplit=1)
            hour, minute = time.split(":")
            cmd = f'curl -m 10 -sf -X POST -H \'Authorization: token {token}\' -H \'Accept: application/vnd.github+json\' https://api.github.com/repos/{repo}/dispatches -d \'{{"event_type":"wake","client_payload":{{"prompt":"{prompt}"}}}}\''
            cron += f"{minute} {hour} * * * {cmd}\n"

    subprocess.run(["crontab", "-"], input=cron.encode(), check=True)
    print("Installed crontab:")
    subprocess.run(["crontab", "-l"])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Sync schedule to crontab.")
    p.add_argument("schedule_file", help="Path to schedule.txt")
    p.add_argument("--repo", default=os.environ.get("REPO"), help="GitHub repo")
    p.add_argument("--token", default=os.environ.get("REPO_PAT"), help="GitHub token")
    a = p.parse_args()
    if not a.repo or not a.token:
        p.error("REPO and REPO_PAT must be set in env or passed as arguments")
    sync(a.schedule_file, a.repo, a.token)
