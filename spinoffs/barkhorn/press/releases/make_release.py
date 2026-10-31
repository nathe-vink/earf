"""RELEASE-MARCH.md's release text -> release-march.html (one US Letter page). Then:
node ../../brandbook/launch/topdf.cjs release-march.html out/earf-release-march.pdf out/earf-release-march.png"""
import re, html
s = open('RELEASE-MARCH.md').read()
body = s.split('\n---\n', 1)[1].split('\n---\n', 1)[0]
inl = lambda t: re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<i>\1</i>', re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', html.escape(t)))
out, lines, i = [], body.strip().split('\n'), 0
while i < len(lines):
    l = lines[i]
    if l.startswith('# '): out.append(f'<h1>{inl(l[2:])}</h1>')
    elif l.startswith('- '):
        items = []
        while i < len(lines) and (lines[i].startswith('- ') or lines[i].startswith('  ')):
            if lines[i].startswith('- '): items.append(lines[i][2:])
            else: items[-1] += ' ' + lines[i].strip()
            i += 1
        out.append('<ul>' + ''.join(f'<li>{inl(x)}</li>' for x in items) + '</ul>'); continue
    elif l.strip():
        para = [l]
        while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r'^(#|- )', lines[i + 1]): i += 1; para.append(lines[i])
        out.append(f'<p>{inl(" ".join(para))}</p>')
    i += 1
strip = ''.join(f'<i style="background:{c}"></i>' for c in ('#C92118','#E06718','#E2AA15','#367424','#2584BE','#5B3197','#D5DFE0','#57545F'))
css = """@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Sans:wght@400..700&display=block');
@page { size: Letter; margin: 0 } * { box-sizing: border-box }
body { margin: 0; font-family: 'Instrument Sans', Arial; color: #1C1A18; -webkit-print-color-adjust: exact; print-color-adjust: exact }
.page { width: 8.5in; height: 11in; padding: .45in .6in .4in; background: #F4F1EC; position: relative; display: flex; flex-direction: column; gap: 6px; overflow: hidden }
.top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px } .top img { height: 15px }
.k { font-family: 'IBM Plex Mono', monospace; font-size: 7pt; letter-spacing: .12em; text-transform: uppercase; color: #5E5A53 }
h1 { font-size: 21pt; line-height: 1.02; letter-spacing: -.025em; margin: 2px 0 4px; font-weight: 600 }
p { margin: 0; font-size: 8.5pt; line-height: 1.4 } ul { margin: 0; padding-left: 14px; font-size: 8.5pt; line-height: 1.38 }
p:first-of-type { font-family: 'IBM Plex Mono', monospace; font-size: 7.5pt; letter-spacing: .08em; text-transform: uppercase; color: #A8321F }
.strip { position: absolute; left: 0; right: 0; bottom: 0; height: 5px; display: flex } .strip i { flex: 1 }
.draft { position: absolute; right: .6in; bottom: .18in; font-family: 'IBM Plex Mono', monospace; font-size: 6.5pt; letter-spacing: .1em; color: #5E5A53; text-transform: uppercase }"""
doc = (f'<!doctype html><meta charset="utf-8"><title>EARF · Release, March 2027 (draft)</title><style>{css}</style>'
       f'<section class="page"><div class="top"><img src="../../brand/mark/earf-wordmark-black.svg" alt="EARF"><span class="k">Press release · draft · not for distribution</span></div>'
       f'{"".join(out)}<span class="draft">Draft 2026-10-31 · brackets and [COUNSEL] lines resolved before release</span><div class="strip">{strip}</div></section>')
open('release-march.html', 'w').write(doc)
