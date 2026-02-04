# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Hugo static site for the blog at www.enricopesce.it, using the PaperMod theme.

## Common Commands

```bash
# Local development server
./hugo server -D

# Build for production
./hugo --gc --minify

# Build with specific base URL (as used in CI)
./hugo --gc --minify --baseURL "https://www.enricopesce.it/"
```

## Updating the Theme

```bash
rm -fr themes/PaperMod/
git clone https://github.com/adityatelange/hugo-PaperMod themes/PaperMod --depth=1
```

## Architecture

- **config.yml**: Main Hugo configuration (site settings, menus, params)
- **content/posts/**: Blog posts organized in numbered directories (0001/, 0002/, etc.)
  - Each post folder contains `index.md` and optionally a `static/` folder for assets
- **layouts/**: Custom layout overrides
  - `_default/_markup/render-link.html`: External links open in new tab with nofollow
  - `shortcodes/plotly.html`: Embed Plotly charts via iframe

## Deployment

Pushes to `main` trigger GitHub Actions workflow (`.github/workflows/hugo.yaml`) which builds and deploys to GitHub Pages. Uses Hugo extended version 0.146.7.
