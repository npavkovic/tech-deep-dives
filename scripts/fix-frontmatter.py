#!/usr/bin/env python3
"""Add templateEngineOverride to all guide frontmatters."""

import re
from pathlib import Path

guides_dir = Path('guides')

for guide_file in guides_dir.glob('*.md'):
    content = guide_file.read_text(encoding='utf-8', errors='ignore')

    # Check if it already has templateEngineOverride
    if 'templateEngineOverride' in content:
        print(f"✓ {guide_file.name} - already has templateEngineOverride")
        continue

    # Find and update frontmatter
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if match:
        frontmatter = match.group(1)
        new_frontmatter = frontmatter + "\ntemplateEngineOverride: md"
        new_content = content.replace(
            f"---\n{frontmatter}\n---",
            f"---\n{new_frontmatter}\n---",
            1
        )
        guide_file.write_text(new_content, encoding='utf-8')
        print(f"✓ {guide_file.name} - added templateEngineOverride")
    else:
        print(f"✗ {guide_file.name} - no frontmatter found")

print("\nDone!")
