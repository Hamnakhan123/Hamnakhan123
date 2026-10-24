"""Builds the numbered section headers (run once; output committed to assets/)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from theme import *

SECTIONS = [
    ("about", "01", "About Me", "Engineer · Lecturer · Builder · Organizer"),
    ("cosmic", "02", "Cosmic Blueprint", "Sagittarius · Fire element · Ruled by Jupiter"),
    ("journey", "03", "Journey", "From Software Engineering graduate to the lecture hall"),
    ("expertise", "04", "Expertise", "What I bring to every team and classroom"),
    ("stack", "05", "Tech Arsenal", "The tools I build and teach with"),
    ("projects", "06", "Featured Work", "Real products, shipped with passion"),
    ("teaching", "07", "Teaching", "Courses I teach at IoBM"),
    ("events", "08", "Events & Community", "Bringing people together around tech"),
    ("analytics", "09", "Live GitHub Analytics", "Refreshed automatically every 6 hours"),
]

def header(key, num, title, sub):
    W, H = 1200, 110
    b = [f'<circle cx="90" cy="55" r="120" fill="url(#neb)"/><circle cx="1110" cy="55" r="120" fill="url(#nebv)"/>', stars(num, W, H, 24)]
    b.append(f'<text class="in" x="48" y="76" font-size="58" font-weight="900" fill="url(#fs)">{num}</text>')
    b.append(f'<rect x="140" y="28" width="3" height="56" rx="1.5" fill="url(#flameV)"/>')
    b.append(f'<text class="in" x="166" y="58" font-size="30" font-weight="800" fill="{INK}" style="animation-delay:.1s">{esc(title)}</text>')
    b.append(f'<text class="in" x="167" y="84" font-size="14" font-weight="600" letter-spacing="1.5" fill="{MUTED}" style="animation-delay:.2s">{esc(sub.upper())}</text>')
    b.append(f'<path d="M640 58 H1040" stroke="url(#fire)" stroke-width="2" stroke-linecap="round" class="dr"/>')
    b.append(f'<circle cx="1040" cy="58" r="4" fill="{GOLD}"/><circle cx="1040" cy="58" r="4" fill="none" stroke="{GOLD}" class="ring"/>')
    b.append(flame(1100, 82, .8))
    b.append(f'<g class="zg">{archer(1128, 22, 1.0, GOLD, 2.4)}</g>')
    return frame(W, H, "".join(b))

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "assets"
    os.makedirs(out, exist_ok=True)
    for key, num, title, sub in SECTIONS:
        open(os.path.join(out, f"sec-{key}.svg"), "w").write(header(key, num, title, sub))
    print("ok")
