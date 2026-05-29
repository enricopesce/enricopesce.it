# Repository Guidelines

## Project Structure & Module Organization

This repository is a Hugo static site for `www.enricopesce.it` using the PaperMod theme. Site-wide settings live in `config.yml`. Primary content is in `content/`, with blog posts organized as numbered bundles such as `content/posts/0020/index.md`; post-specific assets belong in that bundle's `static/` folder. Global static files are in `static/`. Custom Hugo layout overrides are in `layouts/`, while the upstream theme is vendored in `themes/PaperMod/`.

Generated output in `public/`, `resources/_gen/`, and `.hugo_build.lock` should not be treated as source.

## Build, Test, and Development Commands

- `./hugo server -D`: run the local development server and include drafts.
- `./hugo --gc --minify`: build the production site locally and clean unused generated resources.
- `./hugo --gc --minify --baseURL "https://www.enricopesce.it/"`: build with the production base URL.
- `./hugo new posts/0021/index.md`: create a new post bundle from `archetypes/default.md`; adjust the number to the next available post ID.

CI builds with Hugo extended through GitHub Actions and deploys pushes to `main` to GitHub Pages.

## Coding Style & Naming Conventions

Use Markdown for content and YAML for front matter/configuration. Keep YAML indentation to two spaces, quote strings when they contain punctuation, and prefer clear front matter keys such as `title`, `description`, `date`, `draft`, `cover`, and `keywords`. Keep post directories zero-padded and sequential (`0001`, `0002`, ...). Reference post-local cover images with `cover.relative: true` and paths like `static/example.svg`.

Avoid editing `themes/PaperMod/` for site-specific changes; prefer overrides in `layouts/` or assets under the site root.

## Testing Guidelines

There is no separate automated test suite. Validate changes by running `./hugo --gc --minify` before committing. For content or layout changes, also run `./hugo server -D` and inspect the affected page, archive listing, navigation, metadata, and asset loading in a browser.

## Commit & Pull Request Guidelines

Recent history uses short, imperative commit subjects, for example `Add OCI GenAI Python Starters post`, `Update PaperMod theme`, and `Replace direct GA with Google Tag Manager`. Follow that style and keep each commit focused.

Pull requests should include a concise summary, the validation command run, linked issue if relevant, and screenshots for visual/layout changes. Note any Hugo/theme version changes explicitly.

## Security & Configuration Tips

Do not commit secrets, private analytics credentials, or generated build output. Public configuration such as the Google Tag Manager container ID belongs in `config.yml`; environment-specific credentials should stay outside the repository.
