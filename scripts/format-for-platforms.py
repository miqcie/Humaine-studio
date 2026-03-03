#!/usr/bin/env python3
"""
Format Jekyll blog posts for cross-posting to Substack and Medium.

Reads a Jekyll markdown post, strips front matter, and generates
platform-specific formatted versions ready for publishing.

Usage:
    python3 scripts/format-for-platforms.py _posts/2026-03-02-my-post.md
    python3 scripts/format-for-platforms.py _posts/2026-03-02-my-post.md --platform medium
    python3 scripts/format-for-platforms.py _posts/2026-03-02-my-post.md --platform substack
    python3 scripts/format-for-platforms.py _posts/2026-03-02-my-post.md --output-dir /tmp/formatted
"""

import argparse
import os
import re
import sys
import textwrap
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

    # Simple YAML parsing (no external deps needed for flat front matter)
    metadata = {}
    for line in front_matter_raw.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            # Strip quotes
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            # Parse arrays: [tag1, tag2, tag3]
            if value.startswith("[") and value.endswith("]"):
                items = value[1:-1].split(",")
                value = [item.strip().strip("'\"") for item in items if item.strip()]
            metadata[key] = value

    return metadata, body


def build_canonical_url(metadata, filename):
    """Build the canonical URL from post metadata and filename."""
    base_url = "https://humaine.studio"

    # Extract date and slug from filename (YYYY-MM-DD-title.md)
    basename = Path(filename).stem
    match = re.match(r"(\d{4})-(\d{2})-(\d{2})-(.+)", basename)
    if not match:
        return None

    year, month, day, slug = match.groups()

    # Check for categories in front matter
    categories = metadata.get("categories", "")
    if isinstance(categories, list):
        category_path = "/".join(categories)
    elif isinstance(categories, str) and categories:
        # Handle [cat1, cat2] format that wasn't parsed as list
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
    # Match markdown links with relative paths: [text](/path/)
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
    # Filter to 25 chars max, take first 3
    valid = [t.strip().strip("'\"") for t in tags if len(t.strip().strip("'\"")) <= 25]
    return valid[:3]


def format_for_medium(metadata, body, canonical_url, filename):
    """Format a Jekyll post for Medium publishing."""
    title = metadata.get("title", "Untitled")
    tags = select_medium_tags(metadata.get("tags", []))

    # Convert relative links to absolute
    body = convert_relative_links(body)

    # Build the formatted output
    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(body)
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        f"*Originally published at [humaine.studio]({canonical_url})*"
    )

    formatted_content = "\n".join(lines)

    # Build metadata summary for the publisher
    meta_lines = []
    meta_lines.append("=" * 60)
    meta_lines.append("MEDIUM PUBLISHING METADATA")
    meta_lines.append("=" * 60)
    meta_lines.append(f"Title:         {title}")
    meta_lines.append(f"Tags:          {', '.join(tags)} (max 3)")
    meta_lines.append(f"Canonical URL: {canonical_url}")
    meta_lines.append(f"Publish as:    Draft (review before publishing)")
    meta_lines.append(f"Content format: markdown")
    meta_lines.append("=" * 60)
    meta_lines.append("")

    return "\n".join(meta_lines) + formatted_content, tags


def format_for_substack(metadata, body, canonical_url, filename):
    """Format a Jekyll post for Substack publishing."""
    title = metadata.get("title", "Untitled")
    excerpt = metadata.get("excerpt", "")

    # Convert relative links to absolute
    body = convert_relative_links(body)

    # Build the formatted output with Substack-specific additions
    lines = []

    # Email-friendly opening hook (using excerpt if available)
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

    # Build metadata summary for the publisher
    meta_lines = []
    meta_lines.append("=" * 60)
    meta_lines.append("SUBSTACK PUBLISHING METADATA")
    meta_lines.append("=" * 60)
    meta_lines.append(f"Title:         {title}")
    meta_lines.append(f"Subtitle:      {excerpt}")
    meta_lines.append(f"Canonical URL: {canonical_url}")
    meta_lines.append(f"  Set in: Settings > This post was originally")
    meta_lines.append(f"          published elsewhere > paste URL above")
    meta_lines.append("=" * 60)
    meta_lines.append("")

    return "\n".join(meta_lines) + formatted_content


def format_medium_api_json(metadata, body, canonical_url):
    """Generate the JSON payload for the Medium API (if token available)."""
    import json

    title = metadata.get("title", "Untitled")
    tags = select_medium_tags(metadata.get("tags", []))

    # Convert relative links to absolute
    body = convert_relative_links(body)

    # Build content with title and footer
    content = f"# {title}\n\n{body}\n\n---\n\n"
    content += f"*Originally published at [humaine.studio]({canonical_url})*"

    payload = {
        "title": title,
        "contentFormat": "markdown",
        "content": content,
        "canonicalUrl": canonical_url,
        "tags": tags,
        "publishStatus": "draft",
        "notifyFollowers": False,
        "license": "all-rights-reserved",
    }

    return json.dumps(payload, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Format Jekyll posts for cross-posting to Substack and Medium"
    )
    parser.add_argument(
        "post_file",
        help="Path to the Jekyll post file (_posts/YYYY-MM-DD-title.md)",
    )
    parser.add_argument(
        "--platform",
        choices=["medium", "substack", "both"],
        default="both",
        help="Target platform (default: both)",
    )
    parser.add_argument(
        "--output-dir",
        help="Directory to write formatted files (default: prints to stdout)",
    )
    parser.add_argument(
        "--api-json",
        action="store_true",
        help="Also generate Medium API JSON payload",
    )

    args = parser.parse_args()

    # Read the post file
    post_path = Path(args.post_file)
    if not post_path.exists():
        print(f"Error: File not found: {args.post_file}", file=sys.stderr)
        sys.exit(1)

    content = post_path.read_text(encoding="utf-8")
    metadata, body = parse_front_matter(content)

    if not metadata:
        print("Warning: No front matter found in post", file=sys.stderr)

    # Build canonical URL
    canonical_url = build_canonical_url(metadata, args.post_file)
    if not canonical_url:
        print(
            "Error: Could not determine canonical URL from filename",
            file=sys.stderr,
        )
        sys.exit(1)

    title = metadata.get("title", "Untitled")
    slug = post_path.stem

    # Format for requested platforms
    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    if args.platform in ("medium", "both"):
        medium_content, tags = format_for_medium(
            metadata, body, canonical_url, args.post_file
        )

        if args.output_dir:
            medium_path = Path(args.output_dir) / f"{slug}-medium.md"
            medium_path.write_text(medium_content, encoding="utf-8")
            print(f"Medium version written to: {medium_path}")
        else:
            if args.platform == "both":
                print("\n" + "=" * 60)
                print("  MEDIUM VERSION")
                print("=" * 60 + "\n")
            print(medium_content)

        # Generate API JSON if requested
        if args.api_json:
            api_json = format_medium_api_json(metadata, body, canonical_url)
            if args.output_dir:
                json_path = Path(args.output_dir) / f"{slug}-medium-api.json"
                json_path.write_text(api_json, encoding="utf-8")
                print(f"Medium API JSON written to: {json_path}")
            else:
                print("\n" + "=" * 60)
                print("  MEDIUM API JSON PAYLOAD")
                print("=" * 60 + "\n")
                print(api_json)

    if args.platform in ("substack", "both"):
        substack_content = format_for_substack(
            metadata, body, canonical_url, args.post_file
        )

        if args.output_dir:
            substack_path = Path(args.output_dir) / f"{slug}-substack.md"
            substack_path.write_text(substack_content, encoding="utf-8")
            print(f"Substack version written to: {substack_path}")
        else:
            if args.platform == "both":
                print("\n" + "=" * 60)
                print("  SUBSTACK VERSION")
                print("=" * 60 + "\n")
            print(substack_content)

    # Summary
    print("\n" + "=" * 60, file=sys.stderr)
    print(f"Post:          {title}", file=sys.stderr)
    print(f"Canonical URL: {canonical_url}", file=sys.stderr)
    if args.platform in ("medium", "both"):
        print(f"Medium tags:   {', '.join(tags)}", file=sys.stderr)
    print("=" * 60, file=sys.stderr)


if __name__ == "__main__":
    main()
