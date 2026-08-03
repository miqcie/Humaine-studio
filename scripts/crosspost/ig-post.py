# /// script
# dependencies = ["requests"]
# ///
"""Publish a share card to Instagram via the Meta Graph API.

One-time setup:
  1. Convert the Instagram account to business/creator and link it to a
     Facebook page.
  2. developers.facebook.com -> create app -> add Instagram Graph API ->
     generate a long-lived access token with instagram_basic +
     instagram_content_publish.
  3. Store in 1Password, Developer Vault, item "Meta Graph API":
     fields: access_token, ig_user_id

The image must be a PUBLIC https URL (merge the liftout card into the site
first; use its humaine.studio URL).

Usage:
  uv run scripts/crosspost/ig-post.py <image-url> "approved caption"
"""
import subprocess
import sys
import time

import requests

GRAPH = "https://graph.facebook.com/v21.0"


def op(field: str) -> str:
    return subprocess.run(
        ["op", "read", f"op://Developer Vault/Meta Graph API/{field}"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit('usage: uv run scripts/crosspost/ig-post.py <image-url> "caption"')
    image_url, caption = sys.argv[1], sys.argv[2]
    token, ig_user = op("access_token"), op("ig_user_id")

    r = requests.post(f"{GRAPH}/{ig_user}/media", data={
        "image_url": image_url, "caption": caption, "access_token": token,
    })
    if r.status_code != 200:
        raise SystemExit(f"container error {r.status_code}: {r.text}")
    container = r.json()["id"]

    # Media containers process async; poll briefly before publishing.
    for _ in range(10):
        s = requests.get(f"{GRAPH}/{container}", params={
            "fields": "status_code", "access_token": token,
        }).json().get("status_code")
        if s == "FINISHED":
            break
        if s == "ERROR":
            raise SystemExit("Instagram rejected the media container")
        time.sleep(3)

    r = requests.post(f"{GRAPH}/{ig_user}/media_publish", data={
        "creation_id": container, "access_token": token,
    })
    if r.status_code != 200:
        raise SystemExit(f"publish error {r.status_code}: {r.text}")
    print(f"published: media id {r.json()['id']}")


if __name__ == "__main__":
    main()
