# Tech Deep Dives

Minimal blog + podcast feed for technical deep dive guides.

## Tech Stack

- **11ty** (Eleventy) - Static site generator
- **Google Fonts** - IBM Plex Sans (nav/links) + Libre Baskerville (articles)
- **Netlify** - Hosting with auto-deploy

## Setup

```bash
npm install
npm start    # Run dev server at http://localhost:8080
npm run build # Build for production
```

## Adding New Content

### Automated (Recommended)

Use the script to auto-generate frontmatter and copy files:

```bash
# With audio
python scripts/add-guide.py path/to/redis-edited.md --audio path/to/redis.mp3

# Without audio (audio can be added later)
python scripts/add-guide.py path/to/redis-edited.md

# Custom date and metadata
python scripts/add-guide.py path/to/redis-edited.md \
  --audio path/to/redis.mp3 \
  --date 2025-01-20 \
  --title "Custom Title" \
  --description "Custom description"
```

The script will:
- Extract title from the first H1 heading
- Auto-generate a description from the first paragraph
- Generate frontmatter with all metadata
- Copy files to the correct locations
- Show you the git commands to run

Then just:
```bash
git add guides/ audio/
git commit -m "Add Redis guide"
git push
```

### Manual

If you prefer to do it manually:

1. Add frontmatter to your `-edited.md`:
```yaml
---
layout: guide.njk
title: "Redis Deep Dive"
date: 2025-01-20
audio: redis.mp3
description: "A comprehensive guide to Redis"
---
```

2. Copy files:
```bash
cp redis-edited.md guides/redis.md
cp redis.mp3 audio/
```

3. Push:
```bash
git add . && git commit -m "Add Redis guide" && git push
```

## Customizing Design

Edit `/css/style.css` - all styles are in one file with CSS variables at the top for easy theming.

## Podcast Feed

The RSS feed is available at `/feed.xml` for podcast apps.

## Project Structure

```
tech-deep-dives/
├── guides/              # Your -edited.md files (with frontmatter added)
├── audio/               # MP3 files from NotebookLM
├── css/
│   └── style.css       # All styles - edit this!
├── _includes/
│   ├── layout.njk      # Base layout
│   └── guide.njk       # Guide page template
├── index.njk           # Homepage (lists all guides)
├── feed.njk            # Podcast RSS feed
└── .eleventy.js        # 11ty config
```

## Netlify Setup

1. Create new site from Git
2. Build command: `npm run build`
3. Publish directory: `_site`
4. Auto-deploys on push to main
