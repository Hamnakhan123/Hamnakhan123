"""Shared Sagittarius x Fire palette and SVG helpers for Hamna's profile cards."""
BG, CARD, CARD2, LINE = "#0A0716", "#150F2A", "#1C1436", "#2E2150"
FIRE, GOLD, VIOLET, EMBER, INK, MUTED = "#FF6B1A", "#FCD34D", "#A78BFA", "#F43F5E", "#F5EEFF", "#A99BC9"
FONT = "'Segoe UI','Poppins',Ubuntu,'Helvetica Neue',Arial,sans-serif"

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

DEFS = f'''<linearGradient id="fire" x1="0" x2="1"><stop offset="0" stop-color="{FIRE}"/><stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
<linearGradient id="fs" x1="0" x2="1"><stop offset="0" stop-color="{FIRE}"/><stop offset=".33" stop-color="{GOLD}"/><stop offset=".66" stop-color="{VIOLET}"/><stop offset="1" stop-color="{FIRE}"/><animateTransform attributeName="gradientTransform" type="translate" values="-1 0;0 0" dur="6s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="flameV" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{EMBER}"/><stop offset=".5" stop-color="{FIRE}"/><stop offset="1" stop-color="{GOLD}"/></linearGradient>
<radialGradient id="neb"><stop offset="0" stop-color="{FIRE}" stop-opacity=".28"/><stop offset="1" stop-color="{FIRE}" stop-opacity="0"/></radialGradient>
<radialGradient id="nebv"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".28"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
<style>
text{{font-family:{FONT}}}
.in{{animation:in .9s cubic-bezier(.2,.8,.2,1) both}}@keyframes in{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:none}}}}
.pu{{animation:pu 3s ease-in-out infinite}}@keyframes pu{{50%{{opacity:.25}}}}
.fla{{transform-box:fill-box;transform-origin:50% 100%;animation:fla 1.1s ease-in-out infinite alternate}}@keyframes fla{{to{{transform:scaleY(1.2) scaleX(.88)}}}}
.dr{{stroke-dasharray:1200;stroke-dashoffset:1200;animation:dr 2.4s ease-out forwards}}@keyframes dr{{to{{stroke-dashoffset:0}}}}
.gr{{transform-box:fill-box;transform-origin:50% 100%;animation:gr 1s cubic-bezier(.2,.8,.2,1) both}}@keyframes gr{{from{{transform:scaleY(0)}}}}
.zg{{transform-box:fill-box;transform-origin:center;animation:zg 4s ease-in-out infinite}}@keyframes zg{{50%{{transform:scale(1.12) rotate(-8deg)}}}}
.ring{{transform-box:fill-box;transform-origin:center;animation:rg 2s ease-out infinite}}@keyframes rg{{to{{transform:scale(3);opacity:0}}}}
</style>'''

def frame(w, h, body, border=True):
    b = f'<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="17" fill="none" stroke="url(#fire)" stroke-opacity=".45" stroke-width="1.5"/>' if border else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{DEFS}</defs>'
            f'<rect width="{w}" height="{h}" rx="18" fill="{BG}"/>{body}{b}</svg>')

def archer(x, y, k=1.0, color="url(#fire)", sw=2.6):
    return (f'<g transform="translate({x},{y}) scale({k})" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round"><path d="M2 22 L22 2 M10 2 H22 V14 M5 11 L13 19"/></g>')

def flame(cx, by, s=1.0, delay=0):
    """Animated flame whose base sits at (cx, by)."""
    return (f'<g class="fla" style="animation-delay:{delay}s"><path transform="translate({cx},{by}) scale({s})" '
            f'd="M0 -48 C20 -26 22 -8 12 2 C6 8 -6 8 -12 2 C-22 -8 -16 -24 -6 -30 C-6 -20 -2 -16 2 -14 C2 -26 -2 -38 0 -48 Z" fill="url(#flameV)"/>'
            f'<path transform="translate({cx},{by}) scale({s})" d="M0 -20 C8 -12 9 -4 5 1 C2 4 -3 4 -5 1 C-8 -4 -5 -12 0 -20 Z" fill="{GOLD}"/></g>')

def stars(seed, w, h, n=30):
    import random
    r = random.Random(seed)
    out = []
    for _ in range(n):
        out.append(f'<circle cx="{r.randint(8, w-8)}" cy="{r.randint(8, h-8)}" r="{r.uniform(.5, 1.5):.1f}" '
                   f'fill="{r.choice(["#fff", "#fff", GOLD, VIOLET])}" class="pu" style="animation-delay:{r.uniform(0, 3):.1f}s"/>')
    return "".join(out)
