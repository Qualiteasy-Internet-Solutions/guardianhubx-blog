#!/usr/bin/env python3
"""
Audit posts for featured snippet optimization potential.
Identify opportunities for definition, list, table, and Q&A snippets.
"""

import re
import yaml
from pathlib import Path

def load_post(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return None, ""
    fm = yaml.safe_load(match.group(1))
    return fm, content[match.end():]

def analyze_snippet_potential(body):
    """Score posts for different snippet types."""
    score = {'definition': 0, 'list': 0, 'table': 0, 'qa': 0}
    
    # Definition snippet: Intro paragraph with clear definition
    if re.search(r'^[A-Z].*?\b(es|es un|es la|significa|refers to)\b.*?\.$', body.split('\n')[0], re.MULTILINE):
        score['definition'] += 2
    
    # List snippets: Multiple bullet/numbered lists
    lists = len(re.findall(r'^[-*]\s+', body, re.MULTILINE))
    numbered = len(re.findall(r'^\d+\.\s+', body, re.MULTILINE))
    score['list'] += min(2, (lists + numbered) // 5)
    
    # Table snippets: Has comparison table
    if '|' in body and re.search(r'\|.*\|.*\|', body):
        score['table'] += 2
    
    # Q&A snippets: Questions in headings or body
    questions = len(re.findall(r'^\s*(\?|\*\*)?¿.*\?', body, re.MULTILINE))
    score['qa'] += min(2, questions // 2)
    
    return score

def main():
    base_path = Path('/Users/ignasinogues/Library/CloudStorage/OneDrive-Personal/qe/guardianhubx/guardianhubx-blog/content')
    
    results = []
    
    for lang_path in [base_path / 'es']:
        for md_file in sorted(lang_path.glob('*.md')):
            fm, body = load_post(md_file)
            if not fm or fm.get('draft'):
                continue
            
            slug = fm.get('slug', '')
            title = fm.get('title', '')
            
            score = analyze_snippet_potential(body)
            best_type = max(score, key=score.get)
            best_score = score[best_type]
            
            if best_score > 0:
                results.append({
                    'slug': slug,
                    'title': title,
                    'type': best_type,
                    'score': best_score,
                    'all_scores': score
                })
    
    # Sort by potential
    results.sort(key=lambda x: x['score'], reverse=True)
    
    print("\n=== Featured Snippet Potential ===\n")
    
    for snippet_type in ['definition', 'list', 'table', 'qa']:
        typed = [r for r in results if r['type'] == snippet_type]
        if typed:
            print(f"\n{snippet_type.upper()} SNIPPETS ({len(typed)} posts):")
            print("-" * 100)
            for r in typed[:5]:
                print(f"{r['slug'][:40]:40s} | {r['title'][:45]}")

if __name__ == '__main__':
    main()
