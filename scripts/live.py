#!/usr/bin/env python3
"""Live cards for Hamna's profile, rebuilt every 6 hours by GitHub Actions and published to the `live` branch.

  greeting.svg         time-aware greeting from Karachi, current weather, Sagittarius-season countdown
  github-activity.svg  public numbers, a 30-day "fire" commit chart and the latest repositories
Standard library only. If a source fails, the previous card is kept.
"""
import argparse, datetime as dt, json, os, sys, urllib.request
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from theme import *

PKT = dt.timezone(dt.timedelta(hours=5))
USER = os.environ.get("GH_USER", "Hamnakhan123")
REPO = os.environ.get("GITHUB_REPOSITORY", f"{USER}/{USER}")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
UA = {"User-Agent": f"{USER}-live-cards"}
MON = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
WMO = {0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast", 45: "foggy", 48: "foggy", 51: "light drizzle",
       53: "drizzle", 55: "drizzle", 61: "light rain", 63: "rain", 65: "heavy rain", 80: "showers", 81: "showers",
       82: "heavy showers", 95: "thunderstorm", 96: "thunderstorm", 99: "thunderstorm"}
LANG = {"JavaScript": "#F7DF1E", "TypeScript": "#3178C6", "HTML": "#E34F26", "CSS": "#663399", "Python": "#3572A5", "PHP": "#777BB4", "Java": "#B07219"}

def get(url, headers=None):
    with urllib.request.urlopen(urllib.request.Request(url, headers={**UA, **(headers or {})}), timeout=30) as r:
        return json.loads(r.read().decode())

def gh(path):
    h = {"Accept": "application/vnd.github+json"}
    if TOKEN: h["Authorization"] = f"Bearer {TOKEN}"
    return get("https://api.github.com" + path, h)

def stamp(now):
    return f"UPDATED {now:%H:%M} PKT · {now.day} {MON[now.month-1].upper()} {now.year} · EVERY 6 H"

def season(now):
    d = now.date()
    start, end = dt.date(d.year, 11, 22), dt.date(d.year, 12, 21)
    if start <= d <= end:
        left = (end - d).days
        return "Sagittarius season is live", f"{left} day{'s' if left != 1 else ''} of fire left"
    nxt = start if d < start else dt.date(d.year + 1, 11, 22)
    n = (nxt - d).days
    return f"{n} days to Sagittarius season", "22 Nov – 21 Dec"

def greeting(now, wx):
    W, H = 1200, 160
    h = now.hour
    g = ("Good morning" if 5 <= h < 12 else "Good afternoon" if h < 17 else "Good evening" if h < 21 else "Good night") + " from Karachi"
    wd = "Monday Tuesday Wednesday Thursday Friday Saturday Sunday".split()[now.weekday()]
    s1, s2 = season(now)
    b = [f'<circle cx="100" cy="80" r="130" fill="url(#neb)"/><circle cx="1100" cy="80" r="140" fill="url(#nebv)"/>', stars(now.day, W, H, 28)]
    b.append(f'<circle cx="100" cy="80" r="52" fill="{CARD}" stroke="url(#fire)" stroke-width="2"/>')
    b.append(flame(100, 104, 1.0))
    b.append(f'<text class="in" x="180" y="72" font-size="34" font-weight="900" fill="url(#fs)">{esc(g)}</text>')
    b.append(f'<text class="in" x="182" y="104" font-size="16" fill="{INK}" style="animation-delay:.15s">{wd} · {now.day} {MON[now.month-1]} {now.year}  ·  thanks for stopping by ✦</text>')
    b.append(f'<g class="in" style="animation-delay:.3s"><rect x="182" y="118" width="430" height="28" rx="14" fill="{CARD}" stroke="{GOLD}" stroke-opacity=".6"/>'
             f'{archer(194, 123, .75, GOLD, 2.6)}<text x="222" y="137" font-size="13" font-weight="800" fill="{GOLD}">{esc(s1)}</text>'
             f'<text x="598" y="137" font-size="12" fill="{MUTED}" text-anchor="end">{esc(s2)}</text></g>')
    if wx:
        b.append(f'<text x="1160" y="70" font-size="36" font-weight="900" fill="url(#fire)" text-anchor="end">{wx["t"]:.0f}°C</text>')
        b.append(f'<text x="1160" y="96" font-size="14" font-weight="600" fill="{INK}" text-anchor="end">Karachi now · {esc(wx["desc"])}</text>')
    b.append(f'<text x="1160" y="138" font-size="10.5" letter-spacing="1" fill="{MUTED}" text-anchor="end">{stamp(now)}</text>')
    return frame(W, H, "".join(b))

def activity(now, user, repos, days):
    W, H = 1200, 360
    own = [r for r in repos if not r.get("fork") and r["name"] != USER]
    stars_n = sum(r["stargazers_count"] for r in repos)
    total = sum(days.values())
    b = [f'<circle cx="200" cy="40" r="220" fill="url(#neb)"/><circle cx="1050" cy="320" r="220" fill="url(#nebv)"/>', stars(7, W, H, 30)]
    b.append(f'<text x="40" y="50" font-size="13" font-weight="800" letter-spacing="4" fill="{GOLD}">LIVE FROM GITHUB</text>')
    b.append(f'<text x="40" y="82" font-size="26" font-weight="900" fill="url(#fs)">@{esc(USER)}</text>')
    langs = len({r.get("language") for r in own if r.get("language")})
    active = sum(1 for d, v in days.items() if v and (now.date() - d).days < 30)
    tiles = [("Public repos", user.get("public_repos", 0), FIRE), ("Commits · 30 days", total, GOLD),
             ("Languages", langs, VIOLET), ("Active days · 30", active, EMBER)]
    for i, (lab, val, c) in enumerate(tiles):
        x, y = 40 + (i % 2) * 165, 110 + (i // 2) * 110
        b.append(f'<g class="in" style="animation-delay:{.1*i:.1f}s"><rect x="{x}" y="{y}" width="150" height="96" rx="14" fill="{CARD}" stroke="{c}" stroke-opacity=".55"/>'
                 f'<text x="{x+18}" y="{y+52}" font-size="34" font-weight="900" fill="{c}">{val}</text>'
                 f'<text x="{x+18}" y="{y+78}" font-size="12" fill="{MUTED}">{esc(lab)}</text></g>')
    # 30-day fire chart
    cx, cy, cw, ch = 400, 110, 430, 206
    b.append(f'<rect x="{cx-16}" y="{cy}" width="{cw+32}" height="{ch}" rx="14" fill="{CARD}" stroke="{LINE}"/>')
    b.append(f'<text x="{cx}" y="{cy+28}" font-size="14" font-weight="800" fill="{INK}">Commit fire · last 30 days</text>')
    seq = [(now.date() - dt.timedelta(days=29 - i)) for i in range(30)]
    mx = max([days.get(d, 0) for d in seq] + [1])
    bw = cw / 30
    for i, d in enumerate(seq):
        v = days.get(d, 0)
        bh = 4 if v == 0 else 10 + (ch - 80) * v / mx
        x = cx + i * bw + 2
        fill = LINE if v == 0 else "url(#flameV)"
        b.append(f'<rect class="gr" style="animation-delay:{i*.03:.2f}s" x="{x:.1f}" y="{cy+ch-24-bh:.1f}" width="{bw-4:.1f}" height="{bh:.1f}" rx="3" fill="{fill}"><title>{d:%d %b}: {v}</title></rect>')
    b.append(f'<text x="{cx}" y="{cy+ch-8}" font-size="10.5" fill="{MUTED}">{seq[0]:%d %b}</text><text x="{cx+cw}" y="{cy+ch-8}" font-size="10.5" fill="{MUTED}" text-anchor="end">today</text>')
    # latest repos
    rx = 870
    b.append(f'<text x="{rx}" y="{cy+16}" font-size="14" font-weight="800" fill="{INK}">Latest repositories</text>')
    for i, r in enumerate(own[:4]):
        y = cy + 32 + i * 46
        lang = r.get("language") or "Code"
        pushed = dt.datetime.fromisoformat(r["pushed_at"].replace("Z", "+00:00")).astimezone(PKT)
        name = r["name"] if len(r["name"]) <= 26 else r["name"][:25] + "…"
        b.append(f'<g class="in" style="animation-delay:{.2+.1*i:.1f}s"><rect x="{rx}" y="{y}" width="290" height="38" rx="10" fill="{CARD}" stroke="{LINE}"/>'
                 f'<circle cx="{rx+16}" cy="{y+19}" r="5" fill="{LANG.get(lang, FIRE)}"/>'
                 f'<text x="{rx+30}" y="{y+17}" font-size="13" font-weight="700" fill="{INK}">{esc(name)}</text>'
                 f'<text x="{rx+30}" y="{y+31}" font-size="10.5" fill="{MUTED}">{esc(lang)} · {pushed.day} {MON[pushed.month-1]}</text></g>')
    b.append(f'<text x="1160" y="340" font-size="10.5" letter-spacing="1" fill="{MUTED}" text-anchor="end">{stamp(now)}</text>')
    return frame(W, H, "".join(b))

def fetch_weather():
    d = get("https://api.open-meteo.com/v1/forecast?latitude=24.8607&longitude=67.0011&current=temperature_2m,weather_code&timezone=Asia%2FKarachi")
    c = d["current"]
    return {"t": c["temperature_2m"], "desc": WMO.get(c["weather_code"], "fair")}

def fetch_github(now):
    user = gh(f"/users/{USER}")
    repos = gh(f"/users/{USER}/repos?per_page=100&sort=pushed")
    since = (now - dt.timedelta(days=30)).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
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
            if len(cs) < 100:
                break
    return user, repos, days

def keep_previous(out, name):
    try:
        url = f"https://raw.githubusercontent.com/{REPO}/live/{name}"
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
            open(os.path.join(out, name), "wb").write(r.read())
        print(f"kept previous {name}")
    except Exception as e:
        print(f"no previous {name}: {e}")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default="dist"); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    now = dt.datetime.now(PKT)
    try: wx = fetch_weather()
    except Exception as e: print("weather:", e); wx = None
    open(os.path.join(a.out, "greeting.svg"), "w").write(greeting(now, wx))
    try:
        open(os.path.join(a.out, "github-activity.svg"), "w").write(activity(now, *fetch_github(now)))
    except Exception as e:
        print("github:", e); keep_previous(a.out, "github-activity.svg")

if __name__ == "__main__":
    main()
