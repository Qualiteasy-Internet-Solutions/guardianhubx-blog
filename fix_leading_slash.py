import re
from pathlib import Path

# Script para quitar la barra inicial de rutas de imagen en Markdown.
# Uso:
#   python3 fix_leading_slash.py

patterns = [
    # Markdown images/links: ](/foo -> ](foo
    (re.compile(r'\]\(/'), r']('),
    # HTML src attributes: src="/foo -> src="foo
    (re.compile(r'src=["\']/'), r'src="'),
    # Frontmatter image: image: "/foo -> image: "foo
    (re.compile(r'image:\s*["\']/'), r'image: "'),
]

updated = []

for md in Path('.').rglob('*.md'):
    text = md.read_text(encoding='utf-8')
    new = text
    for pat, rep in patterns:
        new = pat.sub(rep, new)
    if new != text:
        md.write_text(new, encoding='utf-8')
        updated.append(str(md))

print(f"Actualizados {len(updated)} archivo(s):")
for f in updated:
    print(" •", f)