#!/usr/bin/env python3
"""
Jekyll to Nextra migration script for SeoGO.
- Renames overview.md -> index.md in each chapter directory
- Strips Jekyll-specific frontmatter keys (section_id, section, nav_order, layout, anchor_headings)
- Fixes .md links in markdown content
- Generates _meta.js files for Nextra navigation
"""

import os
import re
import glob

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'content')


def parse_frontmatter(filepath):
    """Parse YAML frontmatter and return (frontmatter_dict, full_text)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    match = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not match:
        return {}, text

    fm = {}
    for line in match.group(1).strip().split('\n'):
        # Simple YAML parsing for flat key: value pairs
        m = re.match(r'^(\w[\w_-]*):\s*(.*)', line)
        if m:
            key = m.group(1)
            val = m.group(2).strip().strip('"').strip("'")
            if val.isdigit():
                val = int(val)
            fm[key] = val

    return fm, text


def strip_frontmatter(text):
    """Remove Jekyll-specific keys from frontmatter, keep only title."""
    match = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not match:
        return text

    body = text[match.end():]
    fm_lines = match.group(1).strip().split('\n')

    jekyll_keys = {'section_id', 'section', 'nav_order', 'layout', 'anchor_headings'}
    new_lines = []
    for line in fm_lines:
        m = re.match(r'^(\w[\w_-]*):', line)
        if m and m.group(1) in jekyll_keys:
            continue
        new_lines.append(line)

    if not new_lines:
        return body.lstrip('\n')

    return '---\n' + '\n'.join(new_lines) + '\n---' + body


def fix_md_links(text):
    """Replace .md) with ) in markdown links, also .md#anchor) -> #anchor)."""
    # [text](file.md) -> [text](file)
    text = re.sub(r'\]\(([^)]+?)\.md\)', r'](\1)', text)
    # [text](file.md#anchor) -> [text](file#anchor)
    text = re.sub(r'\]\(([^)]+?)\.md#', r'](\1#', text)
    return text


def escape_js_string(s):
    """Escape single quotes in JS string values."""
    return s.replace("'", "\\'")


def generate_meta_js(entries):
    """Generate _meta.js content from list of (key, title) tuples."""
    lines = ['export default {']
    for key, title in entries:
        lines.append(f"  '{key}': '{escape_js_string(title)}',")
    lines.append('}')
    return '\n'.join(lines) + '\n'


def process_chapter(dirpath):
    """Process a single chapter directory. Returns (dir_basename, chapter_title, nav_order)."""
    dirname = os.path.basename(dirpath)
    overview_path = os.path.join(dirpath, 'overview.md')
    index_path = os.path.join(dirpath, 'index.md')

    chapter_title = dirname
    chapter_nav_order = 99

    # Collect all files and their frontmatter
    files_data = []
    for filepath in sorted(glob.glob(os.path.join(dirpath, '*.md'))):
        filename = os.path.basename(filepath)
        fm, text = parse_frontmatter(filepath)

        if filename == 'overview.md':
            chapter_title = fm.get('title', dirname)
            chapter_nav_order = fm.get('nav_order', 99)

            # Rename overview.md -> index.md
            print(f"  Renaming {filepath} -> {index_path}")
            os.rename(filepath, index_path)
            filepath = index_path
            filename = 'index.md'

        # Strip frontmatter and fix links
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        text = strip_frontmatter(text)
        text = fix_md_links(text)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)

        # Collect for _meta.js
        nav_order = fm.get('nav_order', 99)
        title = fm.get('title', filename.replace('.md', ''))
        key = filename.replace('.md', '')
        if key == 'index':
            # index should come first
            files_data.append((-1, key, '章节概述'))
        else:
            files_data.append((nav_order, key, title))

    # Sort by nav_order
    files_data.sort(key=lambda x: x[0])
    entries = [(key, title) for _, key, title in files_data]

    # Generate _meta.js
    meta_content = generate_meta_js(entries)
    meta_path = os.path.join(dirpath, '_meta.js')
    print(f"  Writing {meta_path}")
    with open(meta_path, 'w', encoding='utf-8') as f:
        f.write(meta_content)

    return dirname, chapter_title, chapter_nav_order


def process_quick_start():
    """Process the quick-start.md file."""
    filepath = os.path.join(CONTENT_DIR, 'quick-start.md')
    if not os.path.exists(filepath):
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    text = strip_frontmatter(text)
    text = fix_md_links(text)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"  Processed {filepath}")


def main():
    print("=== SeoGO Jekyll -> Nextra Migration ===\n")

    # Process quick-start.md
    print("Processing quick-start.md...")
    process_quick_start()

    # Process each chapter directory
    chapters = []
    for dirpath in sorted(glob.glob(os.path.join(CONTENT_DIR, '*/'))):
        dirname = os.path.basename(dirpath.rstrip('/'))
        if dirname.startswith('.') or dirname == 'scripts':
            continue
        print(f"\nProcessing {dirname}/...")
        name, title, nav_order = process_chapter(dirpath.rstrip('/'))
        chapters.append((nav_order, name, title))

    # Sort chapters by nav_order
    chapters.sort(key=lambda x: x[0])

    # Generate top-level _meta.js
    print("\nGenerating top-level _meta.js...")
    top_entries = [
        ('index', 'SEO 出海全流程教程'),
        ('quick-start', 'SEO 出海速成指南'),
    ]
    for _, name, title in chapters:
        top_entries.append((name, title))

    meta_content = generate_meta_js(top_entries)
    meta_path = os.path.join(CONTENT_DIR, '_meta.js')
    with open(meta_path, 'w', encoding='utf-8') as f:
        f.write(meta_content)
    print(f"  Written {meta_path}")

    print("\n=== Migration complete! ===")
    print(f"Processed {sum(1 for _ in glob.glob(os.path.join(CONTENT_DIR, '**/*.md'), recursive=True))} markdown files")


if __name__ == '__main__':
    main()
