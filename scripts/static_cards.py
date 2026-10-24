"""Static cards for Hamna's faculty-style profile (run once; output committed to assets/)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from theme import *

ICONS = {  # 24x24 line icons
    "cap": "M2 9 L12 4 L22 9 L12 14 Z M6 11 V16 C6 18 18 18 18 16 V11 M22 9 V15",
    "book": "M4 4 H10 C11 4 12 5 12 6 V20 C12 19 11 18 10 18 H4 Z M20 4 H14 C13 4 12 5 12 6 V20 C12 19 13 18 14 18 H20 Z",
    "path": "M5 19 C5 12 19 14 19 5 M5 19 m-2 0 a2 2 0 1 0 4 0 a2 2 0 1 0 -4 0 M19 5 m-2 0 a2 2 0 1 0 4 0 a2 2 0 1 0 -4 0",
    "spark": "M12 2 L14 9 L21 12 L14 15 L12 22 L10 15 L3 12 L10 9 Z",
    "code": "M8 7 L3 12 L8 17 M16 7 L21 12 L16 17 M14 4 L10 20",
    "rocket": "M12 3 C16 6 17 11 15 16 H9 C7 11 8 6 12 3 Z M9 16 L6 19 M15 16 L18 19 M12 9 m-1.5 0 a1.5 1.5 0 1 0 3 0 a1.5 1.5 0 1 0 -3 0",
    "people": "M8 11 m-3 0 a3 3 0 1 0 6 0 a3 3 0 1 0 -6 0 M16 11 m-3 0 a3 3 0 1 0 6 0 a3 3 0 1 0 -6 0 M2 20 C2 16 14 16 14 20 M10 20 C10 16 22 16 22 20",
    "chart": "M4 20 V10 M10 20 V4 M16 20 V13 M22 20 H2",
    "star": "M12 3 L14.6 9 L21 9.5 L16 13.6 L17.6 20 L12 16.6 L6.4 20 L8 13.6 L3 9.5 L9.4 9 Z",
}
def icon(name, x, y, k=1.0, c=GOLD, sw=1.8):
    return f'<path transform="translate({x},{y}) scale({k})" d="{ICONS[name]}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'

HEADERS = [
    ("faculty", "cap", "Faculty Profile", "Junior Lecturer · Institute of Business Management"),
    ("teaching", "book", "Teaching", "Courses, labs and how I teach"),
    ("courses", "book", "Open Course Library", "Free, session-wise study material for students"),
    ("journey", "path", "Academic & Professional Path", "Every step that shaped me"),
    ("expertise", "spark", "Expertise", "Where engineering meets education"),
    ("stack", "code", "Technical Toolkit", "What I build and teach with"),
    ("projects", "rocket", "Selected Projects", "Shipped, deployed and documented"),
    ("events", "people", "Events & Community", "Bringing people together around tech"),
    ("cosmic", "star", "Beyond the Code", "The Sagittarius behind the screen"),
    ("dashboard", "chart", "Live Dashboard", "Auto-refreshed by GitHub Actions"),
]

def header(key, ic, title, sub):
    """Centered ribbon header with an arrow that flies in under the title."""
    W, H = 1200, 120
    b = [stars(key, W, H, 26), f'<circle cx="600" cy="60" r="200" fill="url(#neb)" opacity=".6"/>']
    b.append(f'<path d="M90 60 H398" stroke="{LINE}" stroke-width="1.5"/><path d="M802 60 H1110" stroke="{LINE}" stroke-width="1.5"/>')
    b.append(f'<path d="M90 60 H398" stroke="url(#fire)" stroke-width="2" class="dr"/><path d="M1110 60 H802" stroke="url(#fire)" stroke-width="2" class="dr"/>')
    b.append(f'<g class="in"><rect x="410" y="18" width="380" height="84" rx="42" fill="{CARD}" stroke="url(#fire)" stroke-width="1.5"/>'
             f'<circle cx="452" cy="60" r="26" fill="{CARD2}" stroke="{GOLD}" stroke-opacity=".5"/>{icon(ic, 440, 48, 1.0)}</g>')
    size = 22 if len(title) <= 18 else 19
    b.append(f'<text class="in" x="492" y="58" font-size="{size}" font-weight="800" fill="{INK}" style="animation-delay:.1s">{esc(title)}</text>')
    b.append(f'<text class="in" x="493" y="80" font-size="10.5" font-weight="600" letter-spacing=".6" fill="{MUTED}" style="animation-delay:.2s">{esc(sub)}</text>')
    b.append(f'<g class="zg">{archer(1130, 47, 1.05, GOLD, 2.3)}</g>{flame(70, 76, .55)}')
    return frame(W, H, "".join(b), border=False)

def faculty():
    W, H = 1200, 440
    b = [f'<circle cx="230" cy="220" r="260" fill="url(#neb)"/><circle cx="1050" cy="80" r="240" fill="url(#nebv)"/>', stars("fac", W, H, 40)]
    # ID card
    b.append(f'<g class="in"><rect x="50" y="50" width="340" height="340" rx="24" fill="{CARD}" stroke="url(#fire)" stroke-width="2"/>'
             f'<rect x="50" y="50" width="340" height="70" rx="24" fill="url(#fire)" opacity=".18"/>'
             f'<text x="220" y="92" font-size="13" font-weight="800" letter-spacing="4" fill="{GOLD}" text-anchor="middle">FACULTY · IoBM</text>'
             f'<circle cx="220" cy="190" r="56" fill="{CARD2}" stroke="url(#fire)" stroke-width="3"/>'
             f'<text x="220" y="207" font-size="44" font-weight="900" fill="url(#fs)" text-anchor="middle">HZ</text>'
             f'<text x="220" y="282" font-size="24" font-weight="900" fill="{INK}" text-anchor="middle">Hamna Zahid Khan</text>'
             f'<text x="220" y="308" font-size="14" font-weight="700" fill="{FIRE}" text-anchor="middle">Junior Lecturer · Lab Engineer</text>'
             f'<text x="220" y="332" font-size="12.5" fill="{MUTED}" text-anchor="middle">Institute of Business Management, Karachi</text>'
             f'<g transform="translate(150,350)">{archer(0, 0, .7, GOLD, 2.6)}<text x="26" y="14" font-size="11" font-weight="700" letter-spacing="1.5" fill="{GOLD}">SAGITTARIUS · FIRE</text></g></g>')
    rows = [
        ("cap", FIRE, "EDUCATION", "BS Software Engineering · Jinnah University for Women", "Master's (in progress) · NED University of Engineering & Technology"),
        ("book", GOLD, "TEACHING AT IoBM", "Data Structures · Programming Fundamentals · ICT labs", "Hands-on, project-first labs with real-world examples"),
        ("code", VIOLET, "INDUSTRY EXPERIENCE", "10Pearls SHINE · MERN-stack internship (2025)", "Aptech · Faculty, Web Development & Programming"),
        ("spark", EMBER, "INTERESTS", "Web engineering · Software engineering · Data science", "Student mentoring · Tech events & community building"),
    ]
    for i, (ic, c, t, l1, l2) in enumerate(rows):
        y = 50 + i * 88
        b.append(f'<g class="in" style="animation-delay:{.15+i*.12:.2f}s"><rect x="420" y="{y}" width="730" height="76" rx="16" fill="{CARD}" stroke="{c}" stroke-opacity=".45"/>'
                 f'<circle cx="462" cy="{y+38}" r="22" fill="{CARD2}" stroke="{c}" stroke-opacity=".6"/>{icon(ic, 450, y+26, 1.0, c)}'
                 f'<text x="500" y="{y+24}" font-size="11" font-weight="800" letter-spacing="2.5" fill="{c}">{t}</text>'
                 f'<text x="500" y="{y+46}" font-size="15" font-weight="700" fill="{INK}">{esc(l1)}</text>'
                 f'<text x="500" y="{y+66}" font-size="12.5" fill="{MUTED}">{esc(l2)}</text></g>')
    return frame(W, H, "".join(b))

def philosophy():
    W, H = 1200, 220
    b = [stars("phil", W, H, 30), f'<circle cx="600" cy="110" r="300" fill="url(#nebv)" opacity=".7"/>']
    b.append(f'<text class="in" x="600" y="70" font-size="12" font-weight="800" letter-spacing="5" fill="{GOLD}" text-anchor="middle">MY TEACHING PHILOSOPHY</text>')
    b.append(f'<text class="in" x="600" y="115" font-size="26" font-weight="800" fill="url(#fs)" text-anchor="middle" style="animation-delay:.1s">Light the spark, then let students aim their own arrows.</text>')
    b.append(f'<text class="in" x="600" y="150" font-size="15" fill="{INK}" text-anchor="middle" style="animation-delay:.2s">I teach code the way I build it: hands-on, curious and connected to real products,</text>')
    b.append(f'<text class="in" x="600" y="174" font-size="15" fill="{INK}" text-anchor="middle" style="animation-delay:.25s">so every lab ends with something students can run, share and be proud of.</text>')
    for i, x in enumerate((470, 600, 730)):
        b.append(f'<circle cx="{x}" cy="198" r="3" fill="{[FIRE, GOLD, VIOLET][i]}" class="pu" style="animation-delay:{i*.4}s"/>')
    return frame(W, H, "".join(b))

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "assets"
    os.makedirs(out, exist_ok=True)
    for key, ic, t, s in HEADERS:
        open(os.path.join(out, f"h-{key}.svg"), "w").write(header(key, ic, t, s))
    open(os.path.join(out, "faculty.svg"), "w").write(faculty())
    open(os.path.join(out, "philosophy.svg"), "w").write(philosophy())
    print("ok")
