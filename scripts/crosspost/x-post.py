# /// script
# dependencies = ["requests-oauthlib"]
# ///
"""Post a single approved tweet via the X API v2 (pay-per-use credits).

One-time setup:
  1. developer.x.com -> create app, enable OAuth 1.0a with Read & Write,
     buy pay-per-use credits (~$0.015/post, ~$0.22 if it contains a URL).
  2. Store the four secrets in 1Password, Developer Vault, item "X API":
     fields: consumer_key, consumer_secret, access_token, access_token_secret

Usage:
  uv run scripts/crosspost/x-post.py "post text with https://link"

Never pass keys on the command line; they load from 1Password at runtime.
"""
import subprocess
import sys

from requests_oauthlib import OAuth1Session


def op(field: str) -> str:
    return subprocess.run(
        ["op", "read", f"op://Developer Vault/X API/{field}"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1].strip():
        raise SystemExit('usage: uv run scripts/crosspost/x-post.py "post text"')
    text = sys.argv[1]
    if len(text) > 280:
        raise SystemExit(f"post is {len(text)} chars (max 280) — trim it")

    session = OAuth1Session(
        op("consumer_key"), op("consumer_secret"),
        op("access_token"), op("access_token_secret"),
    )
    r = session.post("https://api.x.com/2/tweets", json={"text": text})
    if r.status_code != 201:
        raise SystemExit(f"X API error {r.status_code}: {r.text}")
    tweet_id = r.json()["data"]["id"]
    print(f"posted: https://x.com/i/status/{tweet_id}")


if __name__ == "__main__":
    main()
