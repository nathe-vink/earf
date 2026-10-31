# The waitlist: three ways to run it (for the owner's choice)

Round 47, 2026-10-31, `r47-site-next`. The form is built and switched off (`WAITLIST = False` in `web.py`); its privacy
notice is `policies-draft.md` section 4. Nothing below has been signed up for: no account is open anywhere. Prices are
from public pages and third-party summaries read on 2026-10-31; confirm each on the provider's own pricing page before
choosing.

What the form sends: an email address, and up to five ticks (Tropos, Hemisphere, Core, Mantle, Planet EARF). A hidden
field catches bots. The site has no cookies or analytics today, and keeps none with the form.

| | **1. Buttondown** (recommended) | **2. Kit** (formerly ConvertKit) | **3. Our own: a Vercel function and a database** |
|---|---|---|---|
| Cost now | Free to 100 subscribers; from about **$9 a month** to about 1,000 | Free "Newsletter" plan to **10,000 subscribers** (paid Creator from about $39 a month) | Free tiers: Vercel's functions, and a Postgres database (Neon, 0.5 to 1 GB) through the Vercel Marketplace |
| Cost at 5,000 | About $29 a month (summaries disagree above 1,000) | $0 on the free plan | $0 to store; **sending is extra** (a mail API such as Postmark or Resend, from about $15 a month) |
| What it holds | Address, ticks as tags, sign-up time and source, opens and clicks if tracking is on (it can be turned off) | Address, ticks as tags, sign-up form, opens and clicks | Exactly what we store: address, ticks, time. Nothing else |
| Where | United States: AWS us-west-2 (Oregon), per its sub-processor list; mail through Postmark and Mailgun | United States (Kit's own statement to confirm; its sub-processor list was not reachable from here) | Wherever we put it: Vercel and Neon both offer US West (near SF) |
| Double opt-in, unsubscribe, CAN-SPAM footer | Built in | Built in | Ours to build |
| Sending the first email | Its editor (Markdown), our domain once DNS is set | Its editor, our domain once DNS is set | Write and send through the mail API; nothing to compose in |
| The form on the site | Posts to Buttondown's embed URL; no script, no cookie | Posts to Kit's form endpoint (or its script, which sets cookies; we'd use the plain POST) | Posts to `/api/waitlist` on our own domain |
| Leaving it later | CSV export | CSV export | It's our table |
| Fit | Small, plain, privacy-minded, no tracking by default, cheapest for a list that starts small | The most free headroom; built for creators, heavier, more marketing features than we need | Most control and the least third-party data, but we own deliverability, consent records and the unsubscribe flow |

Mailchimp was looked at too: since early 2026 its free plan holds 250 contacts and 500 sends a month with its branding,
Essentials from about $13 a month for 500 contacts, and unsubscribed contacts count toward the limit. Nothing it does
here beats the two above.

**Recommendation: Buttondown.** It holds the least, tracks nothing unless asked, and the site needs no script. Kit if the
owner expects the list to pass a few thousand before launch and wants it free.

## To switch it on (after the owner's choice)

1. The owner opens the account (not a session: no account is opened here) and gives the form's endpoint.
2. In `web.py`: `WAITLIST_ACTION` = the endpoint; `WAITLIST_FIELD` = its field name (`email` for both providers);
   `PRIVACY_DATE` = the day; fill the three `[OWNER: ...]` in `PRIVACY` (provider, location, address); `WAITLIST = True`.
3. `python3 web.py`, the sweep, and the coordinator's yes before it goes to main.
4. earf.world has no mail records yet (`launch-readiness.md`): sending from the domain needs its DNS (SPF, DKIM) set up
   at the provider's instruction first.

## Sources

- Buttondown sub-processors (hosting AWS us-west-2): https://buttondown.com/legal/subprocessors
- Buttondown pricing summaries: https://toolradar.com/tools/buttondown/pricing, https://pricingsaas.com/companies/buttondown
- Kit pricing: https://www.emailvendorselection.com/kit-pricing/, https://costbench.com/software/marketing-automation/convertkit/free-plan/
- Mailchimp pricing: https://mailmeteor.com/blog/mailchimp-pricing, https://costbench.com/software/marketing-automation/mailchimp/free-plan
- Neon pricing: https://neon.com/pricing
