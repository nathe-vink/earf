"""A length proof: the concept's jury text set on three A4 pages (no logos), image slots where the bar lane's go.
Not the festival's template (behind a sign-in); it shows whether the text fits. Run: python3 proof.py, then print proof.html to A4 PDF (Chromium)"""
import html, re
s = open('CONCEPT.md').read()
body = s.split('\n---\n', 1)[1].rsplit('\n---\n', 1)[0]
inl = lambda t: re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<i>\1</i>', re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', html.escape(t)))
out, lines, i = [], body.strip().split('\n'), 0
while i < len(lines):
    l = lines[i]
    if l.startswith('## '): out.append(f'<h2>{inl(l[3:])}</h2>')
    elif l.startswith('[IMAGE'): out.append(f'<div class="img">{inl(l.strip("[]"))}</div>')
    elif l.startswith('|'):
        rows = []
        while i < len(lines) and lines[i].startswith('|'):
            if not re.match(r'^\|[-| ]+\|$', lines[i]): rows.append([c.strip() for c in lines[i].strip('|').split('|')])
            i += 1
        out.append('<table>' + ''.join('<tr>' + ''.join(f'<td>{inl(c)}</td>' for c in r) + '</tr>' for r in rows if any(r)) + '</table>'); continue
    elif l.startswith('- '):
        items = []
        while i < len(lines) and (lines[i].startswith('- ') or lines[i].startswith('  ')):
            if lines[i].startswith('- '): items.append(lines[i][2:])
            else: items[-1] += ' ' + lines[i].strip()
            i += 1
        out.append('<ul>' + ''.join(f'<li>{inl(x)}</li>' for x in items) + '</ul>'); continue
    elif l.strip():
        para = [l]
        while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r'^(##|\||- |\[IMAGE)', lines[i + 1]):
            i += 1; para.append(lines[i])
        out.append(f'<p>{inl(" ".join(para))}</p>')
    i += 1
title = '[TITLE]'
doc = f"""<!doctype html><meta charset="utf-8"><style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400..700&display=block');
@page {{ size: A4; margin: 16mm 17mm }} body {{ font-family: 'Instrument Sans', Arial; font-size: 9.6pt; line-height: 1.42; color: #1C1A18 }}
h1 {{ font-size: 20pt; margin: 0 0 2px; letter-spacing: -.02em }} .by {{ color: #5E5A53; margin: 0 0 8px }}
h2 {{ font-size: 12pt; margin: 10px 0 3px }} p {{ margin: 0 0 5px }} ul {{ margin: 0 0 5px; padding-left: 15px }}
table {{ border-collapse: collapse; width: 100%; font-size: 8.6pt; margin: 3px 0 6px }} td {{ border-bottom: 1px solid #D6D0C6; padding: 3px 6px 3px 0; vertical-align: top }}
td:first-child {{ width: 22%; font-weight: 600 }}
.img {{ height: 52mm; background: #ECE8E1; border: 1px dashed #B9B2A6; display: flex; align-items: center; justify-content: center; text-align: center; color: #5E5A53; font-size: 8.5pt; margin: 6px 0; padding: 0 20mm }}
</style><h1>{title}</h1><p class="by">[OWNER: full name] · San Francisco · a concept for Amsterdam Light Festival, Edition 16</p>{''.join(out)}"""
open('proof.html', 'w').write(doc)
