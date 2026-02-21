#!/usr/bin/env python3
"""Fix image paths missing uploads/ prefix in cover front matter."""

import os
import re

def fix_image_paths_in_dir(directory):
    fixed = 0
    for filename in os.listdir(directory):
        if not filename.endswith('.md'):
            continue

        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Pattern: image: <anything without "uploads/" >
        # Match lines like: image: filename.webp (but not image: uploads/filename.webp or image: "uploads/...)
        pattern = r'(\s+image:\s+)(["\']?)(?!uploads/)([a-zA-Z0-9\-\.]+\.webp|[a-zA-Z0-9\-\.]+\.jpg)(["\']?)'

        def replace_func(match):
            indent = match.group(1)
            quote1 = match.group(2)
            filename = match.group(3)
            quote2 = match.group(4)
            return f'{indent}{quote1}uploads/{filename}{quote2}'

        content = re.sub(pattern, replace_func, content)

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {filename}")
            fixed += 1
        else:
            # Check if already has uploads/
            if 'image: "uploads/' in content or "image: 'uploads/" in content:
                pass  # Already correct
            elif 'image:' in content:
                # Has image but pattern didn't match - might be a different format
                print(f"⚠️  {filename} — image found but pattern didn't match")

    return fixed

# Fix Spanish posts
es_fixed = fix_image_paths_in_dir('content/es')
print(f"\n✓ Spanish: Fixed {es_fixed} posts")

# Fix Catalan posts
ca_fixed = fix_image_paths_in_dir('content/ca')
print(f"✓ Catalan: Fixed {ca_fixed} posts")

print(f"\n✓ Total fixed: {es_fixed + ca_fixed} posts")
