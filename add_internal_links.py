#!/usr/bin/env python3
"""
Add internal links to blog posts based on tag matching.
Links are added contextually to the first relevant paragraph that mentions a related topic.
"""

import os
import re
import yaml
from pathlib import Path
from collections import defaultdict

def load_post_metadata(filepath):
    """Extract front matter from markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract front matter
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return None, content

    fm_text = match.group(1)
    body = content[match.end():]

    try:
        fm = yaml.safe_load(fm_text)
        return fm, body
    except:
        return None, content

def get_post_info(filepath):
    """Extract post info: slug, tags, title."""
    fm, body = load_post_metadata(filepath)
    if not fm:
        return None

    return {
        'filepath': filepath,
        'slug': fm.get('slug', '').strip('/'),
        'title': fm.get('title', ''),
        'tags': [tag.lower().strip() for tag in fm.get('tags', [])],
        'body': body,
        'has_links': bool(re.search(r'\[.*?\]\(/blog/.*?\)', body))
    }

def find_related_posts(post_tags, all_posts, current_slug):
    """Find 2-3 related posts with matching tags."""
    tag_matches = defaultdict(int)

    for other in all_posts:
        if other['slug'] == current_slug:
            continue

        matches = len(set(post_tags) & set(other['tags']))
        if matches > 0:
            tag_matches[other['slug']] = {
                'title': other['title'],
                'matches': matches,
                'tags': other['tags']
            }

    # Sort by number of matching tags, take top 3
    sorted_matches = sorted(tag_matches.items(), key=lambda x: x[1]['matches'], reverse=True)
    return sorted_matches[:3]

def create_link(slug, title):
    """Create markdown link with title as anchor text."""
    return f"[{title}](/blog/{slug}/)"

def add_links_to_post(filepath, related_posts, language='es'):
    """Add internal links to the first relevant paragraph."""
    if not related_posts:
        return False

    fm, body = load_post_metadata(filepath)
    if not fm or fm.get('draft'):
        return False

    # Skip if already has internal links
    if re.search(r'\[.*?\]\(/blog/.*?\)', body):
        return False

    # Create link HTML
    links = [create_link(slug, info['title']) for slug, info in related_posts]
    link_text = f"\n\n**Lecturas relacionadas:**\n" + "\n".join([f"- {link}" for link in links])

    # Find first paragraph (after headers) to add links
    paragraphs = re.split(r'\n\n+', body)

    # Skip title paragraph and any single-line content
    for i, para in enumerate(paragraphs):
        # Skip headers, blockquotes, and short lines
        if para.strip().startswith(('#', '>', '`', '-', '*')) or len(para.strip()) < 50:
            continue

        # Found a good paragraph, insert links after it
        paragraphs.insert(i + 1, link_text.strip())
        body = '\n\n'.join(paragraphs)
        break
    else:
        # If no good paragraph found, append at end (before any closing CTA)
        if body.strip().endswith('>'):
            # Has a closing CTA block
            body = body + link_text
        else:
            body = body + link_text

    # Reconstruct file
    fm_lines = ['---']
    fm_lines.append(yaml.dump(fm, allow_unicode=True, sort_keys=False).strip())
    fm_lines.append('---')

    new_content = '\n'.join(fm_lines) + '\n\n' + body

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True

def main():
    base_path = Path('/Users/ignasinogues/Library/CloudStorage/OneDrive-Personal/qe/guardianhubx/guardianhubx-blog/content')

    for lang in ['es', 'ca']:
        lang_path = base_path / lang
        if not lang_path.exists():
            continue

        print(f"\n=== Processing {lang.upper()} posts ===\n")

        # Load all posts for tag matching
        all_posts = []
        for md_file in sorted(lang_path.glob('*.md')):
            info = get_post_info(md_file)
            if info:
                all_posts.append(info)

        # Process posts without links
        updated_count = 0
        for post in all_posts:
            if post['has_links']:
                continue

            related = find_related_posts(post['tags'], all_posts, post['slug'])
            if related:
                added = add_links_to_post(post['filepath'], related, lang)
                if added:
                    updated_count += 1
                    print(f"✓ {post['slug']}")
                    for slug, info in related:
                        print(f"  └─ linked to: {slug} ({info['matches']} tag matches)")

        print(f"\nUpdated {updated_count} posts in {lang.upper()}")

if __name__ == '__main__':
    main()
