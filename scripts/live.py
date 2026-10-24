#!/usr/bin/env python3
"""Live cards for Hamna's profile, rebuilt every 6 hours by GitHub Actions and published to the `live` branch.

  desk.svg       "Lecturer's Desk": today's date (PKT), a rotating CS tip for students,
                 a Sagittarius-season ring and this week's commit count
  buildlog.svg   "Build Log": 5-week contribution heatmap, ring gauges and the latest repositories
Standard library only. If GitHub is unreachable, the previous card is kept.
"""
import argparse, datetime as dt, json, math, os, sys, urllib.request
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from theme import *

PKT = dt.timezone(dt.timedelta(hours=5))
USER = os.environ.get("GH_USER", "Hamnakhan123")
REPO = os.environ.get("GITHUB_REPOSITORY", f"{USER}/{USER}")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
UA = {"User-Agent": f"{USER}-live-cards"}
MON = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
DAYS = "Monday Tuesday Wednesday Thursday Friday Saturday Sunday".split()
LANG = {"JavaScript": "#F7DF1E", "TypeScript": "#3178C6", "HTML": "#E34F26", "CSS": "#663399", "Python": "#3572A5", "PHP": "#777BB4", "Java": "#B07219"}

TIPS = [  # (topic, line 1, line 2)
    ("Data Structures", "A stack is LIFO, a queue is FIFO.", "Pick the one that matches how your data leaves."),
    ("Big-O", "Binary search halves the problem each step,", "so a million items need only about 20 checks."),
    ("Debugging", "Read the error message twice before changing code.", "It usually tells you the line and the reason."),
    ("Git", "Commit small and often, with clear messages.", "Your future self is your most important teammate."),
    ("Recursion", "Every recursive function needs a base case,", "or it will call itself until the stack overflows."),
    ("Web Dev", "Build mobile-first, then scale up the layout.", "Most of your users are on a phone."),
    ("Linked Lists", "Inserting at the head of a linked list is O(1),", "no shifting needed, unlike an array."),
    ("Clean Code", "Name variables for what they mean, not their type.", "totalMarks beats x or arr2 every time."),
    ("Trees", "In a BST, left < node < right.", "An in-order traversal prints it sorted."),
    ("Problem Solving", "Solve it on paper with a small example first.", "Then translate each step into code."),
    ("Hashing", "Hash maps give O(1) average lookups,", "trading a little memory for a lot of speed."),
    ("Practice", "Ten minutes of daily coding beats", "a five-hour session once a week."),
]

def get(url, headers=None):
    with urllib.request.urlopen(urllib.request.Request(url, headers={**UA, **(headers or {})}), timeout=30) as r:
        return json.loads(r.read().decode())

def gh(path):
    h = {"Accept": "application/vnd.github+json"}
    if TOKEN: h["Authorization"] = f"Bearer {TOKEN}"
    return get("https://api.github.com" + path, h)

def foot(now):
    return f"REFRESHED {now:%H:%M} PKT · {now.day} {MON[now.month-1].upper()} {now.year}"

def arc(cx, cy, r, frac, color, sw=8):
    frac = max(0.0, min(1.0, frac))
    c = 2 * math.pi * r
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINE}" stroke-width="{sw}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" '
            f'stroke-dasharray="{c*frac:.1f} {c:.1f}" transform="rotate(-90 {cx} {cy})">'
            f'<animate attributeName="stroke-dasharray" from="0 {c:.1f}" to="{c*frac:.1f} {c:.1f}" dur="1.4s" fill="freeze"/></circle>')

def season(now):
    d = now.date()
    start, end = dt.date(d.year, 11, 22), dt.date(d.year, 12, 21)
    if start <= d <= end:
        return "SEASON", "live", (d - start).days / 29, f"{(end-d).days}d of fire left"
    nxt = start if d < start else dt.date(d.year + 1, 11, 22)
    prev_end = dt.date(nxt.year - 1, 12, 21)
    n = (nxt - d).days
    return f"{n}", "days to go", 1 - n / max((nxt - prev_end).days, 1), "season starts 22 Nov"

def desk(now, week_commits):
    W, H = 1200, 200
    topic, l1, l2 = TIPS[now.timetuple().tm_yday % len(TIPS)]
    big, small, frac, cap = season(now)
    b = [stars(now.day, W, H, 30), f'<circle cx="160" cy="100" r="200" fill="url(#neb)"/><circle cx="1060" cy="100" r="200" fill="url(#nebv)"/>']
    # date block
    b.append(f'<g class="in"><rect x="40" y="36" width="230" height="128" rx="18" fill="{CARD}" stroke="url(#fire)" stroke-width="1.5"/>'
             f'<text x="155" y="64" font-size="11" font-weight="800" letter-spacing="3" fill="{GOLD}" text-anchor="middle">LECTURER&apos;S DESK</text>'
             f'<text x="155" y="112" font-size="44" font-weight="900" fill="url(#fs)" text-anchor="middle">{now.day} {MON[now.month-1]}</text>'
             f'<text x="155" y="142" font-size="14" fill="{INK}" text-anchor="middle">{DAYS[now.weekday()]} · Karachi</text></g>')
    # tip
    b.append(f'<g class="in" style="animation-delay:.15s"><rect x="292" y="36" width="600" height="128" rx="18" fill="{CARD}" stroke="{LINE}"/>'
             f'{flame(326, 84, .55)}<text x="350" y="68" font-size="11" font-weight="800" letter-spacing="3" fill="{FIRE}">TIP OF THE DAY · {esc(topic.upper())}</text>'
             f'<text x="318" y="108" font-size="18" font-weight="700" fill="{INK}">{esc(l1)}</text>'
             f'<text x="318" y="136" font-size="15" fill="{MUTED}">{esc(l2)}</text></g>')
    # season ring + week
    b.append(f'<g class="in" style="animation-delay:.3s"><rect x="914" y="36" width="246" height="128" rx="18" fill="{CARD}" stroke="{LINE}"/>'
             f'{arc(976, 100, 38, frac, GOLD, 7)}<text x="976" y="104" font-size="{18 if len(big) <= 3 else 12}" font-weight="900" fill="{GOLD}" text-anchor="middle">{esc(big)}</text>'
             f'<text x="976" y="120" font-size="9" fill="{MUTED}" text-anchor="middle">{esc(small)}</text>'
             f'<text x="1030" y="78" font-size="11" font-weight="800" letter-spacing="1.5" fill="{VIOLET}">THIS WEEK</text>'
             f'<text x="1030" y="114" font-size="32" font-weight="900" fill="{INK}">{week_commits}</text>'
             f'<text x="1030" y="136" font-size="11" fill="{MUTED}">commits · {esc(cap)}</text></g>')
    b.append(f'<text x="1160" y="186" font-size="9.5" letter-spacing="1" fill="{MUTED}" text-anchor="end">{foot(now)}</text>')
    return frame(W, H, "".join(b))

def buildlog(now, user, repos, days):
    W, H = 1200, 380
    own = [r for r in repos if not r.get("fork") and r["name"] != USER]
    today = now.date()
    start = today - dt.timedelta(days=today.weekday() + 28)  # Monday, 5 weeks back
    grid = [start + dt.timedelta(days=i) for i in range(35)]
    vals = [days.get(d, 0) for d in grid if d <= today]
    mx = max(vals + [1])
    b = [stars(9, W, H, 30), f'<circle cx="250" cy="300" r="240" fill="url(#neb)"/><circle cx="1000" cy="40" r="220" fill="url(#nebv)"/>']
    b.append(f'<text x="40" y="52" font-size="12" font-weight="800" letter-spacing="4" fill="{GOLD}">BUILD LOG</text>'
             f'<text x="40" y="82" font-size="24" font-weight="900" fill="url(#fs)">What I&apos;ve been shipping</text>')
    # heatmap 7 rows x 5 cols
    gx, gy, cs = 70, 112, 26
    for r, lab in enumerate("MTWTFSS"):
        b.append(f'<text x="{gx-16}" y="{gy + r*(cs+6) + 18}" font-size="10" fill="{MUTED}" text-anchor="middle">{lab}</text>')
    for i, d in enumerate(grid):
        col, row = i // 7, i % 7
        x, y = gx + col * (cs + 6), gy + row * (cs + 6)
        if d > today:
            b.append(f'<rect x="{x}" y="{y}" width="{cs}" height="{cs}" rx="6" fill="none" stroke="{LINE}" stroke-dasharray="3 3"/>')
            continue
        v = days.get(d, 0)
        if v == 0:
            fill, op = CARD2, 1
        else:
            t = v / mx
            fill, op = (EMBER if t < .34 else FIRE if t < .67 else GOLD), .55 + .45 * t
        ring = f'<rect x="{x-2}" y="{y-2}" width="{cs+4}" height="{cs+4}" rx="8" fill="none" stroke="{GOLD}" stroke-width="1.5"/>' if d == today else ""
        b.append(f'<rect class="in" style="animation-delay:{i*.02:.2f}s" x="{x}" y="{y}" width="{cs}" height="{cs}" rx="6" fill="{fill}" fill-opacity="{op:.2f}"><title>{d:%d %b}: {v} commits</title></rect>{ring}')
    # gauges
    total = sum(days.get(d, 0) for d in grid if d <= today)
    active = sum(1 for d in grid if d <= today and days.get(d, 0))
    langs = len({r.get("language") for r in own if r.get("language")})
    gauges = [(total, "commits · 5 wks", min(total / 150, 1), FIRE), (active, "active days", active / 35, GOLD),
              (user.get("public_repos", 0), "public repos", min(user.get("public_repos", 0) / 12, 1), VIOLET), (langs, "languages", min(langs / 6, 1), EMBER)]
    for i, (v, lab, f, c) in enumerate(gauges):
        cx = 330 + (i % 2) * 150
        cy = 150 + (i // 2) * 125
        b.append(f'<g class="in" style="animation-delay:{.2+i*.1:.1f}s">{arc(cx, cy, 42, f, c, 7)}'
                 f'<text x="{cx}" y="{cy+8}" font-size="24" font-weight="900" fill="{INK}" text-anchor="middle">{v}</text>'
                 f'<text x="{cx}" y="{cy+64}" font-size="11" fill="{MUTED}" text-anchor="middle">{lab}</text></g>')
    # timeline of latest repos
    tx = 640
    b.append(f'<text x="{tx}" y="112" font-size="13" font-weight="800" letter-spacing="2" fill="{INK}">LATEST REPOSITORIES</text>')
    b.append(f'<path d="M{tx+8} 132 V{132 + 46*3}" stroke="url(#fire)" stroke-width="2" class="dr"/>')
    for i, r in enumerate(own[:4]):
        y = 132 + i * 46
        lang = r.get("language") or "Code"
        p = dt.datetime.fromisoformat(r["pushed_at"].replace("Z", "+00:00")).astimezone(PKT)
        desc = (r.get("description") or "").strip()
        sub = f"{lang} · updated {p.day} {MON[p.month-1]}" + (f" · {desc[:38]}…" if len(desc) > 38 else f" · {desc}" if desc else "")
        b.append(f'<g class="in" style="animation-delay:{.3+i*.12:.2f}s"><circle cx="{tx+8}" cy="{y}" r="7" fill="{BG}" stroke="{LANG.get(lang, FIRE)}" stroke-width="3"/>'
                 f'<text x="{tx+28}" y="{y+5}" font-size="15" font-weight="800" fill="{INK}">{esc(r["name"])}</text>'
                 f'<text x="{tx+28}" y="{y+23}" font-size="11.5" fill="{MUTED}">{esc(sub)}</text></g>')
    b.append(f'<text x="1160" y="364" font-size="9.5" letter-spacing="1" fill="{MUTED}" text-anchor="end">{foot(now)}</text>')
    return frame(W, H, "".join(b))

def fetch_github(now):
    user = gh(f"/users/{USER}")
    repos = gh(f"/users/{USER}/repos?per_page=100&sort=pushed")
    since = (now - dt.timedelta(days=40)).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    days = Counter()
    for r in repos:
        if r.get("fork"): continue
        for page in range(1, 6):
            try:
                cs = gh(f"/repos/{r['full_name']}/commits?author={USER}&since={since}&per_page=100&page={page}")
            except Exception:
                break
            for c in cs:
                days[dt.datetime.fromisoformat(c["commit"]["author"]["date"].replace("Z", "+00:00")).astimezone(PKT).date()] += 1
            if len(cs) < 100: break
    return user, repos, days

def keep_previous(out, name):
    try:
        with urllib.request.urlopen(urllib.request.Request(f"https://raw.githubusercontent.com/{REPO}/live/{name}", headers=UA), timeout=20) as r:
            open(os.path.join(out, name), "wb").write(r.read())
    except Exception as e:
        print(f"no previous {name}: {e}")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default="dist"); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    now = dt.datetime.now(PKT)
    try:
        user, repos, days = fetch_github(now)
        monday = now.date() - dt.timedelta(days=now.weekday())
        week = sum(v for d, v in days.items() if d >= monday)
        open(os.path.join(a.out, "buildlog.svg"), "w").write(buildlog(now, user, repos, days))
    except Exception as e:
        print("github:", e); week = 0; keep_previous(a.out, "buildlog.svg")
    open(os.path.join(a.out, "desk.svg"), "w").write(desk(now, week))

if __name__ == "__main__":
    main()
