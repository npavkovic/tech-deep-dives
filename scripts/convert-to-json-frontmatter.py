#!/usr/bin/env python3
"""Convert all guides from YAML frontmatter to JSON frontmatter."""

import json
import re
from pathlib import Path

def parse_simple_yaml(yaml_content):
    """Simple YAML parser for our structured frontmatter."""
    data = {}
    for line in yaml_content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # Match key: value
        match = re.match(r'^([^:]+):\s*(.*)$', line)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()

            # Remove quotes if present
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]

            # Handle escaped quotes
            value = value.replace('\\"', '"')

            data[key] = value

    return data

guides_dir = Path('guides')

for guide_file in guides_dir.glob('*.md'):
    content = guide_file.read_text(encoding='utf-8', errors='ignore')

    # Check if it already has JSON frontmatter
    if content.startswith('---json'):
        print(f"✓ {guide_file.name} - already JSON")
        continue

    # Extract YAML frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        print(f"✗ {guide_file.name} - no frontmatter found")
        continue

    yaml_content = match.group(1)
    markdown_content = match.group(2)

    # Parse YAML
    try:
        data = parse_simple_yaml(yaml_content)
    except Exception as e:
        print(f"✗ {guide_file.name} - parse error: {e}")
        continue

    # Convert to JSON frontmatter
    json_frontmatter = "---json\n"
    json_frontmatter += json.dumps(data, indent=2, ensure_ascii=False)
    json_frontmatter += "\n---\n"

    # Write back
    new_content = json_frontmatter + markdown_content
    guide_file.write_text(new_content, encoding='utf-8')

    print(f"✓ {guide_file.name} - converted to JSON")

print("\nDone!")
