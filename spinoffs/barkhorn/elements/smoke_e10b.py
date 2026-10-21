"""Smoke, setting E10b: E10 (smoke_e10.py: the burnt-out sedan2) with the smoke the owner saw in the test and liked.

The owner, 2026-10-21, on the results page's smoke test (la_e9 against la_bw: E9's plume_a as live, and the same cache
with E10's render-time billow and warp): "That smoke looks good." E10 itself solves the smoke again (plume_d); this is
the other way there, E9's cache with the near fire's render given the test's billow (lumps on the lobes) and warp (the
lobes folded into one another), so the two can be dueled and shown side by side.
"""
import copy

import smoke_e10 as E

CACHE = 'renders/2026-10-21/barkhorn/plume/plume_a.npz'
NEAR = {'billow': [0.06, 0.6, 4.0], 'warp': [1.5, 1.2, 2.0]}         # la_bw's


def _swap(s):
    for p in s['set']['props']:
        if p.get('module') == 'plume':
            p['cache'] = CACHE
            if p.get('seed') == 3:
                p.update(NEAR)
    return s


def shot():
    s = _swap(E.shot())
    s['title'] = 'barkhorn, Smoke E10b, the bridge with the test smoke the owner liked and a burnt-out car'
    return s


def portrait():
    p = _swap(E.portrait())
    p['title'] = 'barkhorn, Smoke E10b, the bridge with the test smoke the owner liked and a burnt-out car (4:5)'
    return p
