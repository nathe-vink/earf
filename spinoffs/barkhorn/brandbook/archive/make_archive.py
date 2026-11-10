"""Writes the EARF Brand Archive (archive/index.html): the private record behind the Brand Book. No pictures; paths and
commits only. Built from the coordinator's Book audit (plan.md, book-items.json, surfaces-items.json, facts.json) and the
OWNER DECISIONS blocks of approved-renders.md, read from r46-owner-notes at NOTES, and the Book as published before the
rebuild (r47-brand 7d6b3d41, version 25). Republished whenever the Book changes; nothing in it is deleted.

    python3 archive/make_archive.py
"""
import html, json, os, re, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = '35b4cf3c9d74279800a72c43fc3c420302a027f8'           # r46-owner-notes, 2026-11-10
AUDIT = 'spinoffs/barkhorn/coordinator/book-audit-2026-11-10'
V25 = ('7d6b3d41cfbdf4341c4872a66ea4e37a02417bea', 'spinoffs/barkhorn/brandbook/book/index.html')
BOOK_VERSIONS = [('v22', '1794270136-2332', '38 files'), ('v23', '1794271571-295d', 'the audited Book'),
                 ('v24', '1794272741-39e1', 'r47-brand 804cc8aa'), ('v25', '1794275254-44ef', 'r47-brand 7d6b3d41; the idents out'),
                 ('v26', 'the rebuild of 10 November', 'r47-brand; the current overview and where it is going')]


def git(commit, path):
    root = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True, cwd=HERE).stdout.strip()
    return subprocess.run(['git', 'show', f'{commit}:{path}'], capture_output=True, text=True, cwd=root, check=True).stdout


def e(s):
    return html.escape(str(s), quote=False)


def section(plan, start, end):
    """A slice of plan.md between two headings, as preformatted text (verbatim)."""
    i = plan.index(start); j = plan.index(end, i + len(start)) if end else len(plan)
    return plan[i:j].rstrip()


def text_of(src):
    """An HTML block's visible text, its tags stripped."""
    t = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', src, flags=re.S)
    t = re.sub(r'<br\s*/?>|</(p|li|h\d|div|dt|dd|figcaption|tr)>', '\n', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = html.unescape(t).replace(' ', ' ')
    return '\n'.join(l.strip() for l in t.splitlines() if l.strip())


def rows(items, keep=('KEEP_CURRENT', 'KEEP_FORWARD')):
    out = []
    for it in items:
        if it['verdict'] in keep:
            continue
        out.append(f'<tr><td><code>{e(it["where"])}</code></td><td>{e(it["verdict"])}</td><td>{e(it["text"])}</td>'
                   f'<td>{e(it["why"])}</td><td>{e(it.get("rewrite") or "")}</td></tr>')
    return ('<div class="scroll"><table><thead><tr><th>Where</th><th>Verdict</th><th>Text, verbatim</th><th>Why</th>'
            '<th>What the Book says instead</th></tr></thead><tbody>' + ''.join(out) + '</tbody></table></div>'), len(out)


def main():
    plan = git(NOTES, f'{AUDIT}/plan.md')
    book = json.loads(git(NOTES, f'{AUDIT}/book-items.json'))
    surf = json.loads(git(NOTES, f'{AUDIT}/surfaces-items.json'))
    facts = json.loads(git(NOTES, f'{AUDIT}/facts.json'))
    ar = git(NOTES, 'spinoffs/barkhorn/coordinator/approved-renders.md').splitlines()
    i = next(k for k, l in enumerate(ar) if 'OWNER DECISIONS 10 Nov 02:15' in l)
    decisions = '\n'.join(ar[i - 6:])
    v25 = git(*V25)
    chap = {cid: text_of(m) for cid, m in re.findall(r'<section class="[^"]*" id="([a-z]+)">(.*?)</section>', v25, flags=re.S)}
    book_rows, nb = rows(book['items'])
    surf_rows, ns = rows(surf['items'])
    arch = section(plan, '## ARCHIVE OUTLINE', '## SURFACE FIXES')
    S = []
    S.append(('how', '0. How to read it', f'<p>Every entry is dated in UTC with its source. The owner\'s words are quoted verbatim with their send '
              f'times; a delivery time is in brackets where it differs. Sources: the coordinator\'s Book audit and plan '
              f'(<code>{AUDIT}/</code> on r46-owner-notes <code>{NOTES[:8]}</code>), the approved list\'s OWNER DECISIONS blocks '
              f'(<code>spinoffs/barkhorn/coordinator/approved-renders.md</code>, same commit), and the Book as published before the '
              f'rebuild (version 25, r47-brand <code>{V25[0][:8]}</code>). AR:n, WT n, README:n and RC:n are line references '
              f'as the plan defines them.</p>'))
    S.append(('log', '1. Decision log, and the archive\'s outline as the coordinator wrote it',
              f'<pre>{e(arch)}</pre>'))
    S.append(('since', '1b. The owner\'s decisions since the plan (approved-renders.md, verbatim)',
              f'<p>These win over the plan where they differ. In the rebuild of 10 November they settled: the rods, collars and sockets black; '
              f'eight colors, Smoke in as a neutral gray; the mark as the approved globe (A3) and the flat coins, in the speakers\' colors; '
              f'the bar shown as where EARF is going; the line kept, with "Globe is good." as the sign-off; the lamps\' light warm or '
              f'amber; Mantle on four black posts with satin edges, its base color and light still open.</p><pre>{e(decisions)}</pre>'))
    S.append(('record', '2. The facts of record as of 9 November (the Book\'s chapter 12, verbatim)', f'<pre>{e(chap.get("facts", ""))}</pre>'
              f'<h3>The audit\'s fact table</h3><h4>Current</h4><ul>' +
              ''.join(f'<li><b>{e(f["topic"])}.</b> {e(f["fact"])} <span class="src">{e(f["evidence"])}</span></li>' for f in facts['current']) +
              '</ul><h4>Forward</h4><ul>' +
              ''.join(f'<li>{e(f["direction"])} <span class="src">({e(f["status"])}; {e(f["evidence"])})</span></li>' for f in facts['forward']) +
              '</ul><h4>What the Book claimed that was never decided</h4><ul>' +
              ''.join(f'<li>{e(c)}</li>' for c in facts['book_claims_not_decided']) + f'</ul><p class="src">{e(facts["summary"])}</p>'))
    S.append(('chapters', '3. Chapters that left the Book, verbatim (version 25)',
              ''.join(f'<h3>{t}</h3><pre>{e(chap.get(c, ""))}</pre>' for c, t in
                      [('packaging', 'Packaging (was 09)'), ('ideas', 'Big ideas (was 10)'), ('press', 'Press kit (was 11), as it stood'),
                       ('parked', 'Parked plans'), ('names', 'The naming system, as it stood (Planet EARF, Mother EARF, the names in reserve, the model code)'),
                       ('applications', 'Applications, as it stood (the card, the rating plate, the paper, the signs, EARFcoin)'),
                       ('identity', 'Identity, as it stood'), ('color', 'Color, as it stood (Smoke held, the TruCast codes, the In light values)'),
                       ('voice', 'Voice, as it stood'), ('images', 'Image direction, as it stood'), ('position', 'Position, as it stood')])))
    S.append(('blocks', f'4. Every audited Book block not kept as it stood ({nb} of {len(book["items"])})', book_rows))
    S.append(('surfaces', f'5. Moved out of the other surfaces ({ns} of {len(surf["items"])})',
              '<p>The site preview, the live site, the press kit, launch, social and the deck, each row with its location and reason.</p>' + surf_rows))
    S.append(('checks', '6. The two verifiers\' checks of the plan, verbatim', f'<pre>{e(section(plan, "## OPEN QUESTIONS FOR THE OWNER", None))}</pre>'))
    S.append(('book', '7. The Book\'s own history', '<ul>' + ''.join(f'<li><b>{v}</b>: {e(i_)} ({e(n)})</li>' for v, i_, n in BOOK_VERSIONS) +
              '</ul><p>In the rebuild of 10 November the pictures were renamed (honest-front-* to tropos-front-*, from the tallr6 set with brass rods '
              'to the tallr7 set with black rods, r33-speaker-horn 370de3da) and these left the Book: card.jpg, plate.jpg, stationery.jpg, the three crate '
              'decals, idea-founding.jpg, idea-hotel.jpg, globe-paper.jpg and lockup-paper.jpg and lockup-night.jpg (the globe as rendered on 17 October, '
              'replaced by A3), globe-real.jpg ("as an object"), honest-ice-habitat.jpg (brass rods; its black-rods re-render had not landed), and the '
              'social.jpg of 9 November (its middle post read "where it began").</p>'))
    body = '\n'.join(f'<section id="{i_}"><h2>{t}</h2>{b}</section>' for i_, t, b in S)
    nav = ''.join(f'<a href="#{i_}">{e(t.split(" ", 1)[0])} {e(t.split(" ", 1)[1].split(",")[0].split("(")[0])}</a>' for i_, t, _ in S)
    page = TEMPLATE.replace('{{NAV}}', nav).replace('{{BODY}}', body)
    open(os.path.join(HERE, 'index.html'), 'w').write(page)
    print('archive/index.html', len(page) // 1024, 'KB;', nb, 'Book blocks,', ns, 'surface rows')


TEMPLATE = '''<title>EARF Brand Archive</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Sans:wght@400..700&display=swap">
<style>
:root { --bg: #F4F1EC; --fg: #1C1A18; --muted: #5E5A53; --rule: #D6D0C6; --warn: #8A1C10; --code: #ECE8E1;
  --sans: 'Instrument Sans', 'Helvetica Neue', Arial, sans-serif; --mono: 'IBM Plex Mono', 'Courier New', monospace }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg: #141312; --fg: #EDE7DD; --muted: #A79F93; --rule: #2E2B27; --warn: #F08A7A; --code: #1E1C1A; color-scheme: dark } }
:root[data-theme="dark"] { --bg: #141312; --fg: #EDE7DD; --muted: #A79F93; --rule: #2E2B27; --warn: #F08A7A; --code: #1E1C1A; color-scheme: dark }
* { box-sizing: border-box }
body { margin: 0; background: var(--bg); color: var(--fg); font: 400 16px/1.55 var(--sans) }
.wrap { max-width: 1100px; margin: 0 auto; padding-block: 40px 80px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)) }
h1 { font-size: clamp(30px, 5vw, 44px); letter-spacing: -.02em; margin: 0 0 8px; text-wrap: balance }
h2 { font-size: 24px; letter-spacing: -.01em; margin: 48px 0 12px; padding-top: 20px; border-top: 1px solid var(--rule); text-wrap: balance }
h3 { font-size: 18px; margin: 28px 0 8px } h4 { font: 500 12px/1.4 var(--mono); letter-spacing: .1em; text-transform: uppercase; color: var(--muted); margin: 20px 0 6px }
.internal { border: 2px solid var(--warn); color: var(--warn); padding: 14px 18px; border-radius: 4px; font-weight: 500; max-width: 80ch }
nav { display: flex; flex-wrap: wrap; gap: 6px 14px; margin: 18px 0 0; font: 500 12px/1.4 var(--mono); letter-spacing: .06em }
nav a { color: var(--muted) }
pre { white-space: pre-wrap; overflow-wrap: anywhere; background: var(--code); padding: 14px 16px; border-radius: 4px; font: 13px/1.55 var(--mono); max-width: 100% }
code { font: 13px var(--mono); overflow-wrap: anywhere }
.src { color: var(--muted); font-size: 13.5px }
li { margin-bottom: 6px }
.scroll { overflow-x: auto; max-width: 100%; border: 1px solid var(--rule); border-radius: 4px }
table { border-collapse: collapse; min-width: 900px; font-size: 13.5px }
th, td { text-align: left; vertical-align: top; padding: 8px 10px; border-bottom: 1px solid var(--rule) }
th { font: 500 11px/1.4 var(--mono); letter-spacing: .08em; text-transform: uppercase; color: var(--muted); position: sticky; top: 0; background: var(--bg) }
td:nth-child(3) { min-width: 26ch } td:nth-child(1) { width: 12ch }
</style>
<div class="wrap">
<h1>EARF Brand Archive</h1>
<p class="internal">Internal. For the EARF team only; not for investors, retailers, press, partners or customers. No stakeholder-facing page links here: not the Brand Book, the site, the press kit or the deck. Do not forward this link. The Brand Book is the current overview; this page is the record behind it.</p>
<nav aria-label="Sections">{{NAV}}</nav>
{{BODY}}
</div>
'''

if __name__ == '__main__':
    main()
