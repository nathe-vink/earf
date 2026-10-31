"""Strategic-partner pitch packs: two US Letter pages each, for Klipsch, Ace Hotel Group and Pro-Ject.

Content from R9 (r46-owner-notes a9aa15d3, spinoffs/barkhorn/research/2026-10-31/R9-strategic-partners.md): the
proposals (its table 1 and section E), the precedents (section A, C), the deal ranges (D1-D5). Facts about EARF from
earf.world (the press sheets). Pictures are renders and say so; they are replaced by the debut's photographs before
anything is sent. Run: python3 make_packs.py, then node ../launch/topdf.cjs <slug>.html out/<file>.pdf for each.
"""
import html, os

HERE = os.path.dirname(os.path.abspath(__file__))
STRIP = ''.join(f'<i style="background:{c}"></i>' for c in
                ('#C92118', '#E06718', '#E2AA15', '#367424', '#2584BE', '#5B3197', '#D5DFE0', '#57545F'))

CSS = """
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Sans:wght@400..700&display=block');
@page { size: Letter; margin: 0 }
* { box-sizing: border-box }
body { margin: 0; font-family: 'Instrument Sans', Arial, sans-serif; color: #1C1A18; -webkit-print-color-adjust: exact; print-color-adjust: exact }
.page { width: 8.5in; height: 11in; padding: .5in .55in .45in; position: relative; overflow: hidden; page-break-after: always; background: #F4F1EC; display: flex; flex-direction: column; gap: 13px }
.page.dark { background: #0E0D10; color: #EDE7DD }
.k { font-family: 'IBM Plex Mono', monospace; font-size: 7.5pt; letter-spacing: .13em; text-transform: uppercase; color: #5E5A53 }
.dark .k { color: #A79F93 }
.top { display: flex; justify-content: space-between; align-items: center }
.top img { height: 16px }
h1 { margin: 0; font-size: 34pt; line-height: .96; letter-spacing: -.035em; font-weight: 600 }
h2 { margin: 0; font-size: 17pt; line-height: 1.05; letter-spacing: -.02em; font-weight: 600 }
h3 { margin: 0 0 4px; font-size: 11pt; letter-spacing: -.01em }
p { margin: 0; font-size: 9.6pt; line-height: 1.48 }
.lede { font-size: 12pt; line-height: 1.42; color: #CFC8BD }
.pic { margin: 0 -.55in; height: 3.0in; overflow: hidden; position: relative } .pic img { width: 100%; height: 100%; object-fit: cover }
.pic .lbl { position: absolute; left: .55in; bottom: 8px; font-family: 'IBM Plex Mono', monospace; font-size: 7pt; letter-spacing: .12em; text-transform: uppercase; color: #fff; background: rgba(0,0,0,.45); padding: 3px 6px }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 18px }
.dark .card { background: #1A181C } .card { background: #ECE8E1; border-radius: 3px; padding: 11px 13px; display: grid; gap: 5px; align-content: start }
ul { margin: 0; padding-left: 14px; font-size: 9.2pt; line-height: 1.42; display: grid; gap: 2px }
.dark ul, .dark p { color: #DCD5CA }
table { border-collapse: collapse; width: 100%; font-size: 9pt; line-height: 1.4 }
th { text-align: left; font-family: 'IBM Plex Mono', monospace; font-size: 7pt; letter-spacing: .1em; text-transform: uppercase; color: #5E5A53; font-weight: 500; padding: 4px 6px 4px 0; border-bottom: 1px solid #1C1A18 }
td { padding: 6px 8px 6px 0; border-bottom: 1px solid #D6D0C6; vertical-align: top }
td:first-child { font-weight: 600; width: 24% }
.counsel { font-family: 'IBM Plex Mono', monospace; font-size: 6.6pt; letter-spacing: .08em; color: #A8321F; text-transform: uppercase }
.note { font-size: 8.2pt; color: #5E5A53; line-height: 1.45 }
.foot { margin-top: auto; display: flex; justify-content: space-between; font-family: 'IBM Plex Mono', monospace; font-size: 7pt; letter-spacing: .08em; text-transform: uppercase; color: #5E5A53 }
.dark .foot { color: #A79F93 }
.strip { position: absolute; left: 0; right: 0; bottom: 0; height: 5px; display: flex } .strip i { flex: 1 }
"""

EARF_IS = ("EARF makes hi-fi and light in San Francisco, in cast acrylic tinted all the way through, in eight colours "
           "from Ember to Smoke. Tropos is a powered horn loudspeaker; Mantle, a record player whose plinth floats over "
           "a base lit at its edge; Hemisphere, a pendant; Core, a cordless table lamp. The first pair of Tropos played "
           "for the first time at our debut in San Francisco on 19 January 2027, in FOG Design+Art week.")

PACKS = [
    dict(slug='klipsch', who='Klipsch', file='earf-pitch-klipsch',
         title='A numbered horn edition, built in Hope.',
         pic='../../site/img/macro-horn.jpg', pos='50% 50%',
         proposal="A Klipsch × EARF edition of a Heritage model, built by Klipsch in Hope, with an EARF cast-acrylic horn "
                  "surround, baffle or stands in one of our tints: about 100 numbered pairs. EARF sells it direct in the "
                  "United States; Klipsch dealers sell it everywhere else, as with the kO-R2.",
         why=["The kO-R1 (2024): 100 pairs at $8,498, built in Hope with Devon Turnbull of OJAS, and sold out.",
              "The kO-R2 (2026): 600 numbered pairs at $11,998, “handcrafted in Hope”, “sold direct from Ojas” in "
              "the US, through authorised retailers in Europe, launched at Milan Design Week with USM and Karimoku.",
              "Klipsch’s sound in other people’s objects and rooms: La-Z-Boy’s AudioLuxe furniture, and the "
              "Equipment Room at Hotel Magdalena, Austin (October 2026).",
              "EARF brings what OJAS brought: a designer’s object, a colour, a room to launch it in. The tint is new."],
         theirs=["The Heritage model and its engineering", "The build in Hope: quality, warranty, certification",
                 "Its dealers outside the US", "Its press, and a show stand"],
         ours=["The acrylic parts’ design, drawn and specified", "The eight tints, and approval of each cast",
               "The US direct channel and the launch: a listening room, a Session record",
               "The design press (Wallpaper*, Dezeen, Core77 on our list)"],
         terms=[("Structure", "Klipsch builds. EARF buys finished pairs at a transfer price and sells them direct in the US, "
                              "keeping the retail margin; Klipsch’s dealers sell elsewhere."),
                ("Royalty", "On Klipsch’s own sales: 3–7% of net wholesale, 5% common for consumer products. "
                            "Net defined, with listed deductions only."),
                ("Fee", "A development fee for the design work, recoupable against royalty. Advances in this field are "
                        "small or none."),
                ("Edition", "About 100 numbered pairs, capped; the tint and the numbering EARF’s to approve."),
                ("Control", "EARF approves colour, material and finish, and the use of its name; credit on the product."),
                ("Term", "1–3 years, renewable; a sell-off of 30–180 days; rights revert if not launched in 12–18 "
                         "months."),
                ("Prices", "A suggested retail price only: a licensor can’t set resale prices in California."),
                ("Reports", "Quarterly statements, about three months in arrears; audit rights.")],
         when=[("The debut, 19 January", "The first pair plays; photographed and filmed"),
               ("1–4 weeks after", "This letter, with the photographs and a short listening video"),
               ("About 12 weeks after", "A meeting at Milan Design Week, 13–18 April, where the kO-R2 launched"),
               ("About 16 weeks after", "HIGH END, Vienna, 6–9 May: the pair measured and heard"),
               ("Then", "If both want it: design and tooling, about 12–18 months to an edition")],
         route='pr@klipsch.com (its press office), asking for the note to be passed to product partnerships'),
    dict(slug='ace', who='Ace Hotel Group', file='earf-pitch-ace-hotel',
         title='A listening corner for one Ace lobby.',
         pic='../../site/img/room-1440.jpg', pos='50% 55%',
         proposal="A season-long EARF listening corner in one Ace lobby: a numbered pair of Tropos, a Mantle record player "
                  "and Hemisphere pendants, in a tint chosen for the room, with listening sessions through the season. "
                  "It starts as a residency and becomes a purchase if it works for Ace. Beside it, an Ace × EARF edition "
                  "of Core, our cordless lamp, for the rooms or the shop.",
         why=["Ace has treated sound as part of the building: Devon Turnbull built the lobby system at Ace Hotel New York.",
              "Tivoli made a co-branded radio for Ace Sydney’s rooms; Ace set the brief and the silkscreen.",
              "Elsewhere, hotels now commission listening rooms: OJAS’s Listening Room at Patina Osaka; the Equipment "
              "Room at Hotel Magdalena, Austin, with Klipsch.",
              "A corner is smaller than a room: one season, one tint, no construction."],
         theirs=["The lobby, and the guests in it", "The programme: who plays, and when",
                 "Its shop, for the Core edition", "Photography and its own channels"],
         ours=["The system: Tropos, Mantle, Hemisphere, installed and tuned",
               "The Sessions: one album, start to finish, on set nights", "Core in an Ace tint, numbered",
               "Service through the season"],
         terms=[("Residency", "A season (about three months): EARF installs and services; Ace hosts and programmes. A "
                              "residency fee or a loan [to agree]."),
                ("Purchase", "At the end, Ace may buy the corner: 50% on order, the balance on installation, as "
                             "commissions usually run."),
                ("Core edition", "Ace buys a numbered run (for example 100) at wholesale, about 40–50% of retail."),
                ("Co-brand", "“Ace × EARF” on the Core edition, under a licence of 1–3 years; each approves the "
                             "other’s use of its name."),
                ("IP", "EARF keeps the design; a credit line such as “The Listening Corner by EARF”."),
                ("Care", "Insurance and liability for loaned equipment in a public lobby; a service contract if bought."),
                ("Prices", "A suggested retail price for the shop only: no resale price set (California).")],
         when=[("The debut, 19 January", "The pieces seen working, photographed"),
               ("2–5 weeks after", "This letter, with the photographs (February)"),
               ("About 12 weeks after", "A meeting in Milan, 13–18 April, or at the property"),
               ("Mid-2027", "The residency opens, in a city Ace chooses"),
               ("With the Core run", "The Ace edition of Core, numbered (est. autumn 2027)")],
         route='business@acehotel.com (Atelier Ace business inquiries); press@acehotel.com in copy'),
    dict(slug='project', who='Pro-Ject Audio Systems', file='earf-pitch-pro-ject',
         title='A tinted-acrylic edition, made under licence.',
         pic='../../site/img/tt-violet-dusk-1200.jpg', pos='50% 50%',
         proposal="A Pro-Ject turntable built in Pro-Ject’s own factory with an EARF cast-acrylic plinth and platter, "
                  "in a few of our tints, numbered: about 50 to 100 in each. Pro-Ject sells it through its dealers; EARF "
                  "sells it direct and launches it with a listening event in San Francisco. Mantle, our own record player, "
                  "stays separate.",
         why=["Pro-Ject already makes editions “under license”: its Harley-Davidson turntable is “Manufactured by "
              "Pro-Ject … under license from Harley-Davidson”.",
              "Its Artist Collection runs with partners from Metallica and The Rolling Stones to Third Man Records.",
              "It sells an acrylic deck already, the 6 PerspeX, and builds its turntables in its own Czech factory.",
              "Its home is about 35 km north of Vienna, where HIGH END meets on 6–9 May."],
         theirs=["The deck: motor, bearing, arm, and their engineering", "The factory, quality control, certification",
                 "Its dealers, worldwide", "Its stand at HIGH END"],
         ours=["The plinth and platter, designed in cast acrylic", "The tints, and approval of each cast",
               "The US launch: a listening event, a Session record", "Direct sales, and the design press"],
         terms=[("Structure", "A licence: Pro-Ject manufactures; EARF licenses the design and the tint. EARF buys units at "
                              "a transfer price for its direct sales."),
                ("Royalty", "3–7% of net wholesale on Pro-Ject’s sales, 5% common; net defined."),
                ("Fee", "A development fee, recoupable; a minimum guarantee from the second year."),
                ("Edition", "50–100 numbered per tint, in a few tints; the edition capped."),
                ("Control", "EARF approves colour, material and finish; the tint system stays EARF’s own, and "
                            "exclusivity covers this edition only."),
                ("Term", "1–3 years; sell-off 30–180 days; reversion if not launched in 12–18 months, or if "
                         "production stops."),
                ("Prices", "A suggested retail price only; channel terms, not resale prices (California)."),
                ("Reports", "Quarterly statements; audit rights.")],
         when=[("The debut, 19 January", "Mantle and the tints seen; photographed"),
               ("3–8 weeks after", "This letter, through Pro-Ject’s contact form (February to March)"),
               ("About 16 weeks after", "A meeting at HIGH END, Vienna, 6–9 May"),
               ("Then", "If both want it: design and tooling, about 12–18 months to an edition")],
         route="the contact form at project-audio.com/en/contact/"),
]


def li(xs):
    return '<ul>' + ''.join(f'<li>{html.escape(x)}</li>' for x in xs) + '</ul>'


def build(p):
    terms = ''.join(f'<tr><td>{html.escape(a)}</td><td>{html.escape(b)} <span class="counsel">for counsel</span></td></tr>'
                    for a, b in p['terms'])
    when = ''.join(f'<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td></tr>' for a, b in p['when'])
    return f"""<!doctype html><meta charset="utf-8"><title>EARF · A proposal for {html.escape(p['who'])}</title>
<style>{CSS}</style>
<section class="page dark">
  <div class="top"><img src="../../brand/mark/earf-wordmark-white.svg" alt="EARF"><span class="k">A proposal for {html.escape(p['who'])} · draft · confidential</span></div>
  <h1>{html.escape(p['title'])}</h1>
  <p class="lede">{html.escape(EARF_IS)}</p>
  <div class="pic"><img src="{p['pic']}" alt="" style="object-position:{p['pos']}"><span class="lbl">Render · replaced by a photograph from the debut before sending</span></div>
  <div><span class="k">What we propose</span><p style="font-size:11pt;line-height:1.45;margin-top:4px">{html.escape(p['proposal'])}</p></div>
  <div class="cols">
    <div class="card"><span class="k">Why {html.escape(p['who'])}</span>{li(p['why'])}</div>
    <div style="display:grid;gap:10px;align-content:start">
      <div class="card"><span class="k">{html.escape(p['who'])} brings</span>{li(p['theirs'])}</div>
      <div class="card"><span class="k">EARF brings</span>{li(p['ours'])}</div>
    </div>
  </div>
  <div class="foot"><span>Draft for discussion; nothing here is an offer</span><span>earf.world · [contact line]</span></div>
  <div class="strip">{STRIP}</div>
</section>
<section class="page">
  <div class="top"><img src="../../brand/mark/earf-wordmark-black.svg" alt="EARF"><span class="k">Terms in outline · the timeline</span></div>
  <h2>How it could work.</h2>
  <p class="note">An outline to discuss, not an offer. The ranges are those typical in published sources for licensed and
  co-branded design (furniture, lighting, consumer products); none of it is agreed, and every line is for counsel.</p>
  <table><tr><th>Term</th><th>In outline</th></tr>{terms}</table>
  <h2 style="margin-top:6px">When.</h2>
  <table><tr><th>From the debut</th><th>What</th></tr>{when}</table>
  <div class="cols" style="margin-top:4px;grid-template-columns:1fr 1fr 1fr">
    <div><h3>What we’d send next</h3><p>Photographs and a short film from the debut; drawings of the parts we’d
    design; samples of the eight tints in cast sheet; an edition sheet with sizes, colours and lead times.</p></div>
    <div><h3>What stays EARF\u2019s own</h3><p>Tropos, Mantle and the tint system. An edition is designed around them
    and licensed for its own run; nothing here licenses EARF\u2019s products or its colours beyond it.</p></div>
    <div><h3>Who</h3><p>[Your name], founder, EARF, San Francisco. [contact line].<br>Through {html.escape(p['route'])}.</p></div>
  </div>
  <div class="foot"><span>Draft · terms for counsel · figures are ranges, not proposals of price</span><span>earf.world</span></div>
  <div class="strip">{STRIP}</div>
</section>
"""


if __name__ == '__main__':
    for p in PACKS:
        with open(os.path.join(HERE, p['slug'] + '.html'), 'w') as f:
            f.write(build(p))
        print(p['slug'], p['file'])
