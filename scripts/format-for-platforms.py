#!/usr/bin/env python3
"""
Format Jekyll blog posts for cross-posting to Substack and Medium.

Strips front matter, converts relative links to absolute URLs, and adds
platform-specific footers with canonical URLs.

No external dependencies — uses Python 3 standard library only.

Usage:
    python3 scripts/format-for-platforms.py _posts/2026-03-02-my-post.md
    python3 scripts/format-for-platforms.py _posts/2026-03-02-my-post.md --platform medium
    python3 scripts/format-for-platforms.py _posts/2026-03-02-my-post.md --platform substack
    python3 scripts/format-for-platforms.py _posts/2026-03-02-my-post.md --output-dir /tmp/formatted
"""

import argparse
import re
import sys
from pathlib import Path


def parse_front_matter(content):
    """Extract YAML front matter and body from a Jekyll markdown file."""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    front_matter_raw = parts[1].strip()
    body = parts[2].strip()

    metadata = {}
    for line in front_matter_raw.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            if value.startswith("[") and value.endswith("]"):
                items = value[1:-1].split(",")
                value = [item.strip().strip("'\"") for item in items if item.strip()]
            metadata[key] = value

    return metadata, body


def build_canonical_url(metadata, filename):
    """Build the canonical URL from post metadata and filename."""
    base_url = "https://humaine.studio"
    basename = Path(filename).stem
    match = re.match(r"(\d{4})-(\d{2})-(\d{2})-(.+)", basename)
    if not match:
        return None

    year, month, day, slug = match.groups()

    categories = metadata.get("categories", "")
    if isinstance(categories, list):
        category_path = "/".join(categories)
    elif isinstance(categories, str) and categories:
        categories = categories.strip("[]")
        cats = [c.strip().strip("'\"") for c in categories.split(",")]
        category_path = "/".join(cats)
    else:
        category_path = ""

    if category_path:
        return f"{base_url}/{category_path}/{year}/{month}/{day}/{slug}/"
    else:
        return f"{base_url}/posts/{year}/{month}/{day}/{slug}/"


def convert_relative_links(body, base_url="https://humaine.studio"):
    """Convert relative markdown links to absolute URLs."""
    def replace_link(match):
        text = match.group(1)
        url = match.group(2)
        if url.startswith("/") and not url.startswith("//"):
            return f"[{text}]({base_url}{url})"
        return match.group(0)

    return re.sub(r"\[([^\]]+)\]\((/[^)]+)\)", replace_link, body)


def select_medium_tags(tags):
    """Select up to 3 tags for Medium (max 25 chars each)."""
    if not tags:
        return []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.strip("[]").split(",")]
    valid = [t.strip().strip("'\"") for t in tags if len(t.strip().strip("'\"")) <= 25]
    return valid[:3]


def format_for_medium(metadata, body, canonical_url):
    """Format a Jekyll post for Medium (Import Story or manual paste)."""
    title = metadata.get("title", "Untitled")
    tags = select_medium_tags(metadata.get("tags", []))

    body = convert_relative_links(body)

    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(body)
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*Originally published at [humaine.studio]({canonical_url})*")

    formatted_content = "\n".join(lines)

    meta_lines = []
    meta_lines.append("=" * 60)
    meta_lines.append("MEDIUM PUBLISHING INFO")
    meta_lines.append("=" * 60)
    meta_lines.append(f"Title:         {title}")
    meta_lines.append(f"Tags:          {', '.join(tags)} (max 3)")
    meta_lines.append(f"Canonical URL: {canonical_url}")
    meta_lines.append("")
    meta_lines.append("OPTION A - Import Story (recommended):")
    meta_lines.append("  1. Medium > Profile > Stories > Import a story")
    meta_lines.append(f"  2. Paste: {canonical_url}")
    meta_lines.append("  3. Medium auto-sets canonical URL + imports content")
    meta_lines.append(f"  4. Add tags: {', '.join(tags)}")
    meta_lines.append("")
    meta_lines.append("OPTION B - Paste content below manually")
    meta_lines.append("=" * 60)
    meta_lines.append("")

    return "\n".join(meta_lines) + formatted_content, tags


def format_for_substack(metadata, body, canonical_url):
    """Format a Jekyll post for Substack publishing."""
    title = metadata.get("title", "Untitled")
    excerpt = metadata.get("excerpt", "")

    body = convert_relative_links(body)

    lines = []
    if excerpt:
        lines.append(f"*{excerpt}*")
        lines.append("")

    lines.append(body)
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        f"*This post was originally published at "
        f"[humaine.studio]({canonical_url}). "
        f"Subscribe to get new posts delivered to your inbox.*"
    )

    formatted_content = "\n".join(lines)

    meta_lines = []
    meta_lines.append("=" * 60)
    meta_lines.append("SUBSTACK PUBLISHING INFO")
    meta_lines.append("=" * 60)
    meta_lines.append(f"Title:         {title}")
    meta_lines.append(f"Subtitle:      {excerpt}")
    meta_lines.append(f"Canonical URL: {canonical_url}")
    meta_lines.append("  Set in: Settings > This post was originally")
    meta_lines.append("          published elsewhere > paste URL above")
    meta_lines.append("=" * 60)
    meta_lines.append("")

    return "\n".join(meta_lines) + formatted_content


def main():
    parser = argparse.ArgumentParser(
        description="Format Jekyll posts for cross-posting to Substack and Medium"
    )
    parser.add_argument("post_file", help="Path to Jekyll post (_posts/YYYY-MM-DD-title.md)")
    parser.add_argument("--platform", choices=["medium", "substack", "both"], default="both")
    parser.add_argument("--output-dir", help="Write formatted files here (default: stdout)")

    args = parser.parse_args()

    post_path = Path(args.post_file)
    if not post_path.exists():
        print(f"Error: File not found: {args.post_file}", file=sys.stderr)
        sys.exit(1)

    content = post_path.read_text(encoding="utf-8")
    metadata, body = parse_front_matter(content)
    canonical_url = build_canonical_url(metadata, args.post_file)

    if not canonical_url:
        print("Error: Could not build canonical URL from filename", file=sys.stderr)
        sys.exit(1)

    title = metadata.get("title", "Untitled")
    slug = post_path.stem

    if args.output_dir:
        Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    if args.platform in ("medium", "both"):
        medium_content, tags = format_for_medium(metadata, body, canonical_url)
        if args.output_dir:
            out = Path(args.output_dir) / f"{slug}-medium.md"
            out.write_text(medium_content, encoding="utf-8")
            print(f"Medium:   {out}")
        else:
            if args.platform == "both":
                print("\n" + "=" * 60)
                print("  MEDIUM VERSION")
                print("=" * 60 + "\n")
            print(medium_content)

    if args.platform in ("substack", "both"):
        substack_content = format_for_substack(metadata, body, canonical_url)
        if args.output_dir:
            out = Path(args.output_dir) / f"{slug}-substack.md"
            out.write_text(substack_content, encoding="utf-8")
            print(f"Substack: {out}")
        else:
            if args.platform == "both":
                print("\n" + "=" * 60)
                print("  SUBSTACK VERSION")
                print("=" * 60 + "\n")
            print(substack_content)

    print(f"\nPost:          {title}", file=sys.stderr)
    print(f"Canonical URL: {canonical_url}", file=sys.stderr)


if __name__ == "__main__":
    main()
