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

### 1. Prepare Your Guide

Take your `-edited.md` file and add frontmatter at the top:

```yaml
---
layout: guide.njk
title: "Redis Deep Dive"
date: 2025-01-20
audio: redis.mp3
description: "A comprehensive guide to Redis"
---

[Your existing content here]
```

### 2. Add Files

```bash
# Copy guide
cp path/to/redis-edited.md guides/redis.md

# Copy podcast audio from NotebookLM
cp path/to/redis-podcast.mp3 audio/redis.mp3
```

### 3. Deploy

```bash
git add .
git commit -m "Add Redis guide"
git push
```

Netlify auto-builds and deploys.

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
