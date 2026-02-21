#!/usr/bin/env python3
"""Add leading slash to image paths."""

import os

def fix_images_in_dir(directory):
    fixed = 0
    for filename in os.listdir(directory):
        if not filename.endswith('.md'):
            continue

        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Replace "  image: uploads/" with "  image: /uploads/"
        content = content.replace('  image: uploads/', '  image: /uploads/')

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed += 1

    return fixed

# Fix Spanish posts
es_fixed = fix_images_in_dir('content/es')
print(f"✓ Spanish: Fixed {es_fixed} posts")

# Fix Catalan posts
ca_fixed = fix_images_in_dir('content/ca')
print(f"✓ Catalan: Fixed {ca_fixed} posts")

print(f"\n✓ Total: {es_fixed + ca_fixed} posts with leading slash added to image paths")
