#!/usr/bin/env python3
"""Build one mockup page per pick in a round.

    python3 mock/.harness/generate.py mock/.harness/rounds/09-minimal.py

The round module defines:
    ROUND     = dict(dir='navigation', title='Flat & minimal')
                dict(dir=..., dirs={'slug': 'theme', ...})   # per-pick override:
                                                             # a round's picks can
                                                             # land in several themes
    V         = {'slug': dict(NAME=..., TWCONFIG=..., ...), ...}
    TRANSFORM = {'slug': callable}          # optional, str -> str, pre-fill
"""
import os, re, sys, runpy

HARNESS = os.path.dirname(os.path.abspath(__file__))
MOCK = os.path.dirname(HARNESS)
if HARNESS not in sys.path:            # so round modules can `import models`
    sys.path.insert(0, HARNESS)


def theme_buttons(pairs):
    return "\n".join(
        '        <button data-theme-pick="%s" class="theme-btn rounded-[6px] px-3 py-1.5 '
        'text-xs font-semibold">%s</button>' % (key, label) for key, label in pairs)


def theme_captions(d):
    return "  const THEME_CAPTION = {\n%s\n  };" % "\n".join(
        "    '%s': '%s'," % (k, v.replace("'", "\\'")) for k, v in d.items())


def content_slots(name='content.html'):
    """Split a content pack on its `<!-- @@NAME@@ -->` markers."""
    path = os.path.join(HARNESS, name)
    if not os.path.exists(path):
        return {}
    parts = re.split(r'<!--\s*@@([A-Z_]+)@@\s*-->', open(path).read())
    return dict(zip(parts[1::2], (p.strip('\n') for p in parts[2::2])))


def build(round_module):
    mod = runpy.run_path(round_module)
    rnd, variants, transforms = mod['ROUND'], mod['V'], mod.get('TRANSFORM', {})
    template = open(os.path.join(HARNESS, rnd.get('template', 'template.html'))).read()
    default_pack = rnd.get('content', 'content.html')
    dirs = rnd.get('dirs', {})

    for slug, cfg in variants.items():
        cfg = dict(cfg)
        cfg.setdefault('SLUG', slug)
        cfg.setdefault('EXTRAJS', '')
        cfg.setdefault('ONSCREEN', '')   # text laid on the bare screen
        cfg['THEMEBTNS'] = theme_buttons(cfg.pop('THEMES'))
        cfg['THEMECAPTIONS'] = theme_captions(cfg['THEMECAPTIONS'])
        slots = content_slots(cfg.pop('CONTENT', default_pack))
        cfg.update(slots)

        out = template
        for name, body in slots.items():          # content first, so transforms
            out = out.replace('@@%s@@' % name, body)   # can reach screen markup
        if slug in transforms:
            out = transforms[slug](out)
        for key, value in cfg.items():
            out = out.replace('@@%s@@' % key, value)

        missing = sorted(set(re.findall(r'@@[A-Z_0-9]+@@', out)))
        if missing:
            sys.exit('%s: unfilled placeholders %s' % (slug, missing))
        outdir = os.path.join(MOCK, dirs.get(slug, rnd.get('dir', '')))
        os.makedirs(outdir, exist_ok=True)
        path = os.path.join(outdir, '%s.html' % slug)
        open(path, 'w').write(out)
        rel = os.path.relpath(path, os.path.dirname(MOCK))
        print('wrote %s (%d lines)' % (rel, len(out.splitlines())))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    build(sys.argv[1])
