#!/usr/bin/env python3
"""
Add a guide to the Tech Deep Dives site.

Takes an -edited.md file and optionally an audio file, generates frontmatter,
and copies everything to the right place.

Usage:
    python scripts/add-guide.py path/to/redis-edited.md [--audio path/to/redis.mp3] [--date 2025-01-20]
"""

import argparse
import os
import re
import shutil
from datetime import datetime
from pathlib import Path


def extract_title_from_markdown(content):
    """Extract the first H1 heading from markdown content."""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None


def extract_description(content):
    """Extract a description from the content (first paragraph after title)."""
    # Remove frontmatter if it exists
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    # Find first H1
    lines = content.split('\n')

    # Skip empty lines and title
    start_idx = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('# '):
            start_idx = i + 1
            break

    # Find first substantial paragraph
    paragraphs = []
    current_para = []

    for line in lines[start_idx:]:
        stripped = line.strip()

        # Skip headings, code blocks, lists
        if (stripped.startswith('#') or
            stripped.startswith('```') or
            stripped.startswith('-') or
            stripped.startswith('*') or
            stripped.startswith('>')):
            if current_para:
                break
            continue

        if stripped:
            current_para.append(stripped)
        elif current_para:
            # End of paragraph
            para_text = ' '.join(current_para)
            if len(para_text) > 50:  # Must be substantial
                return para_text
            current_para = []

    # Last resort: join what we have
    if current_para:
        para_text = ' '.join(current_para)
        if len(para_text) > 50:
            return para_text

    return None


def generate_frontmatter(title, date, audio_filename, description):
    """Generate YAML frontmatter."""
    frontmatter = "---\n"
    frontmatter += "layout: guide.njk\n"
    frontmatter += f'title: "{title}"\n'
    frontmatter += f"date: {date}\n"
    if audio_filename:
        frontmatter += f"audio: {audio_filename}\n"
    if description:
        # Escape quotes in description
        description = description.replace('"', '\\"')
        frontmatter += f'description: "{description}"\n'
    # Disable Liquid processing to prevent {{ }} in code blocks from being interpreted
    frontmatter += "templateEngineOverride: md\n"
    frontmatter += "---\n"
    return frontmatter


def main():
    parser = argparse.ArgumentParser(description='Add a guide to Tech Deep Dives')
    parser.add_argument('markdown_file', help='Path to -edited.md file')
    parser.add_argument('--audio', help='Path to audio file (optional)')
    parser.add_argument('--date', help='Publication date (YYYY-MM-DD, default: today)')
    parser.add_argument('--title', help='Override title (default: extracted from markdown)')
    parser.add_argument('--description', help='Override description (default: auto-generated)')

    args = parser.parse_args()

    # Validate inputs
    md_path = Path(args.markdown_file)
    if not md_path.exists():
        print(f"Error: {md_path} not found")
        return 1

    # Read markdown content with error handling for encoding issues
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Try with latin-1 encoding as fallback
        with open(md_path, 'r', encoding='latin-1') as f:
            content = f.read()

    # Remove existing frontmatter if present
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    # Extract/set metadata
    title = args.title or extract_title_from_markdown(content)
    if not title:
        print("Error: Could not extract title. Use --title to specify manually.")
        return 1

    description = args.description or extract_description(content)

    date = args.date or datetime.now().strftime('%Y-%m-%d')

    # Handle audio
    audio_filename = None
    if args.audio:
        audio_path = Path(args.audio)
        if not audio_path.exists():
            print(f"Warning: Audio file {audio_path} not found")
        else:
            audio_filename = audio_path.name
            # Copy audio file
            audio_dest = Path('audio') / audio_filename
            audio_dest.parent.mkdir(exist_ok=True)
            shutil.copy2(audio_path, audio_dest)
            print(f"✓ Copied audio to {audio_dest}")

    # Generate slug from title
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

    # Generate new content with frontmatter
    frontmatter = generate_frontmatter(title, date, audio_filename, description)
    new_content = frontmatter + "\n" + content

    # Write to guides directory
    guides_dir = Path('guides')
    guides_dir.mkdir(exist_ok=True)
    output_path = guides_dir / f"{slug}.md"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✓ Created guide at {output_path}")
    print(f"\nMetadata:")
    print(f"  Title: {title}")
    print(f"  Date: {date}")
    if audio_filename:
        print(f"  Audio: {audio_filename}")
    if description:
        print(f"  Description: {description[:80]}...")

    print(f"\nNext steps:")
    print(f"  npm start                    # Preview locally")
    print(f"  git add guides/ audio/")
    print(f"  git commit -m 'Add {title} guide'")
    print(f"  git push")

    return 0


if __name__ == '__main__':
    exit(main())
