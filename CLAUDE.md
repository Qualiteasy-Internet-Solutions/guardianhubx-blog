# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GuardianHubX Blog — a bilingual (Spanish/Catalan) cybersecurity blog built with **Hugo** using the **PaperMod** theme (git submodule). The blog is a subsite of guardianhubx.com, served under the `/blog/` path.

## Build & Development Commands

```bash
# Local development server
hugo server -D

# Build for production
hugo

# Fix image paths (prefix with /blog/uploads/)
python3 fix_leading_slash.py
```

The site builds to `public/` (gitignored). The PaperMod theme is a git submodule at `themes/PaperMod` — after cloning, run `git submodule update --init`.

## Architecture

- **Config**: `config.toml` — multilingual setup with `es` (default) and `ca` languages
- **Content**: `content/es/` and `content/ca/` — blog posts as Markdown files
- **Layouts**: `layouts/` overrides PaperMod partials (header, footer, favicons, extend_head, list)
- **i18n**: `i18n/es.yaml` and `i18n/ca.yaml` — translation strings for UI elements
- **Static assets**: `static/css/custom.css`, `static/js/language.js`, `static/uploads/` (images)

## Content Conventions

Blog posts follow this naming pattern: `YYYYMMDD-slug-in-language.md`

Front matter fields for posts:
```yaml
title: "Post title"
author: "GuardianHubX"
date: YYYY-MM-DDT09:00:00+00:00
draft: false
slug: "url-slug"
type: "blog"
categories: ["Ciberseguridad"]
tags: ["Tag1", "Tag2"]
description: "Meta description"
cover:
  image: "uploads/image-name.webp"
  alt: "Alt text"
  caption: "Fuente: GuardianHubX"
translationKey: "shared-key-between-es-and-ca"
```

- `translationKey` links Spanish and Catalan versions of the same post
- Images go in `static/uploads/` and are referenced as `uploads/filename.webp` in front matter
- All image paths must be prefixed with `/blog/` for production (use `fix_leading_slash.py` if needed)

## Deployment

Pushes to `main` trigger a GitHub Actions workflow (`.github/workflows/trigger-main-deploy.yml`) that dispatches a `blog-updated` event to the main site repo (`guardianhubx.github.io`), which handles the actual build and deploy. A daily scheduled deploy also runs at 04:05 UTC.

## Layout Customizations

The `layouts/partials/header.html` is heavily customized: it includes Google Tag Manager, Cookiebot consent, a language switcher, Bootstrap navbar matching the main guardianhubx.com site, and breadcrumb navigation. Changes to this file should preserve the integration with the main site's design.

## SEO

SEO is handled by PaperMod's `head.html` partial (in the theme, not overridden locally). It auto-generates:

- **Canonical URLs**: from `.Permalink` or overridable via `canonicalURL` in front matter
- **Meta robots**: `index, follow` when `params.env = "production"` (set in `config.toml`); `noindex, nofollow` otherwise. Per-page opt-out with `robotsNoIndex: true` in front matter
- **Meta description**: from front matter `description`, falls back to `.Summary`
- **Meta keywords**: from front matter `keywords`, falls back to `tags`
- **Open Graph**: og:title, og:description, og:image (from `cover.image`), og:locale, article timestamps, article:tag (first 6 tags)
- **Twitter Cards**: `summary_large_image` when cover image exists, `summary` otherwise
- **JSON-LD structured data**: `Organization` on homepage, `BreadcrumbList` + `BlogPosting` on post pages (includes headline, description, author, dates, wordCount, inLanguage, image)
- **hreflang**: auto-generated `<link rel="alternate" hreflang>` tags for all translations (ES/CA linking)
- **RSS**: per-language feeds, linked via `<link rel="alternate">` in head
- **Sitemap**: auto-generated per-language sitemaps (`/sitemap.xml`, `/es/sitemap.xml`, `/ca/sitemap.xml`), referenced in `robots.txt`

### SEO notes

- Google Search Console is validated at domain level (no per-site verification tag needed).
- Google Analytics is handled via GTM (GTM-584VRJ97) in `layouts/partials/header.html`, not via Hugo's built-in analytics config.
- Cover images use absolute path format (`uploads/image.webp`) — OG/Twitter image URLs depend on `canonifyURLs = true` to resolve correctly to the full `https://guardianhubx.com/blog/uploads/...` path.

# My Project Rules
- ALWAYS use Haiku model for simple tasks.
- ASK for permission before running broad audits or reading more than 5 files.
- WARNING: We are on a tight token budget. Be concise.
- **DO NOT auto-commit changes** — User will commit manually. Only stage changes with `git add` and prepare commit messages if requested.
