# Script to update image paths to prefix with /blog/uploads/
#
# Usage:
#   1. Place this script in the root of your blog source directory (e.g., blog-src/).
#   2. Run: python3 update_image_paths.py
#
# It will update:
# - Markdown image/link syntax: ](uploads/... or ](/uploads/... 
#     -> ](/blog/uploads/...
# - HTML src attributes: src="uploads/... or src="/uploads/... 
#     -> src="/blog/uploads/...
# - Frontmatter image fields: image: "uploads/... or image: "/uploads/... 
#     -> image: "/blog/uploads/...
#
# Processes all .md files recursively and prints modified files.

import re
from pathlib import Path

patterns = [
    # Markdown images/links: ](uploads/... or ](/uploads/... -> ](/blog/uploads/...
    (re.compile(r'\]\(\s*/?uploads/'), r'](/blog/uploads/'),
    # HTML src attributes: src="uploads/... or src="/uploads/... -> src="/blog/uploads/...
    (re.compile(r'(src=["\'])/?uploads/'), r'\1/blog/uploads/'),
    # Frontmatter image field: image: "uploads/... or image: "/uploads/... -> image: "/blog/uploads/...
    (re.compile(r'(image:\s*["\'])/?uploads/'), r'\1/blog/uploads/'),
]

updated_files = []

for md_file in Path('.').rglob('*.md'):
    text = md_file.read_text(encoding='utf-8')
    new_text = text
    for pattern, repl in patterns:
        new_text = pattern.sub(repl, new_text)
    if new_text != text:
        md_file.write_text(new_text, encoding='utf-8')
        updated_files.append(str(md_file))

print(f"Updated {len(updated_files)} file(s):")
for f in updated_files:
    print(" -", f)