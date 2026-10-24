"""Refreshes the dynamic sections of the profile README (runs daily via GitHub Actions)."""
import datetime as dt, json, os, re, urllib.request

USER = "Hamnakhan123"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
PKT = dt.timezone(dt.timedelta(hours=5))

def gh(path):
    req = urllib.request.Request("https://api.github.com" + path, headers={"Accept": "application/vnd.github+json", "User-Agent": USER})
    if TOKEN:
        req.add_header("Authorization", "Bearer " + TOKEN)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def ago(iso):
    d = dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    if d.days >= 30: return f"{d.days // 30} mo ago"
    if d.days >= 1: return f"{d.days}d ago"
    h = d.seconds // 3600
    return f"{h}h ago" if h else "just now"

def recent_repos():
    repos = [r for r in gh(f"/users/{USER}/repos?sort=pushed&per_page=20") if r["name"] != USER and not r.get("fork")][:4]
    rows = ["| 🏹 Repository | 📝 About | 🔥 Language | ⭐ | 🕒 Updated |", "|:--|:--|:--:|:--:|:--:|"]
    for r in repos:
        desc = (r.get("description") or "—").replace("|", "/")[:70]
        rows.append(f"| [**{r['name']}**]({r['html_url']}) | {desc} | {r.get('language') or '—'} | {r['stargazers_count']} | {ago(r['pushed_at'])} |")
    return "\n".join(rows)

ICONS = {"PushEvent": "🔥", "CreateEvent": "✨", "WatchEvent": "⭐", "ForkEvent": "🍴", "IssuesEvent": "🎯", "PullRequestEvent": "🏹", "IssueCommentEvent": "💬", "ReleaseEvent": "🚀", "PublicEvent": "🌍"}

def activity():
    out = []
    for e in gh(f"/users/{USER}/events/public?per_page=30"):
        t, repo, p = e["type"], e["repo"]["name"], e.get("payload", {})
        link = f"[{repo.split('/')[-1]}](https://github.com/{repo})"
        if t == "PushEvent":
            n = p.get("size") or len(p.get("commits", [])) or 1
            msg = f"Pushed {n} commit{'s' if n != 1 else ''} to {link}"
        elif t == "CreateEvent":
            msg = f"Created {p.get('ref_type', 'repository')} in {link}"
        elif t == "PullRequestEvent":
            msg = f"{p.get('action', 'updated').capitalize()} a pull request in {link}"
        elif t == "IssuesEvent":
            msg = f"{p.get('action', 'updated').capitalize()} an issue in {link}"
        elif t == "WatchEvent":
            msg = f"Starred {link}"
        elif t == "ForkEvent":
            msg = f"Forked {link}"
        elif t == "ReleaseEvent":
            msg = f"Released a new version of {link}"
        else:
            continue
        out.append(f"{ICONS.get(t, '✦')} {msg} · <sub>{ago(e['created_at'])}</sub>")
        if len(out) == 5: break
    return "<br/>\n".join(out) if out else "✦ Charging up the next project… stay tuned."

QUOTES = [
    "“Aim for the stars; even an arrow that falls short lands among them.” ♐",
    "“Code is fire: handle it with passion, shape it with patience.” 🔥",
    "“Jupiter teaches that knowledge only grows when it is shared.” 🪐",
    "“The best way to learn is to teach.” — Frank Oppenheimer",
    "“First, solve the problem. Then, write the code.” — John Johnson",
    "“Simplicity is the soul of efficiency.” — Austin Freeman",
    "“Every expert was once a beginner. Keep shooting arrows.” 🏹",
    "“Make it work, make it right, make it fast.” — Kent Beck",
    "“Adventure is the archer's compass: explore one new tech every week.” ✨",
    "“Talk is cheap. Show me the code.” — Linus Torvalds",
]

def quote(now):
    return f"> {QUOTES[now.timetuple().tm_yday % len(QUOTES)]}"

def replace(text, key, body):
    return re.sub(rf"(<!--{key}:START-->).*?(<!--{key}:END-->)", lambda m: f"{m.group(1)}\n{body}\n{m.group(2)}", text, flags=re.S)

def main():
    now = dt.datetime.now(PKT)
    with open("README.md", encoding="utf-8") as f:
        text = f.read()
    for key, fn in (("RECENT_REPOS", recent_repos), ("ACTIVITY", activity)):
        try:
            text = replace(text, key, fn())
        except Exception as exc:  # keep the previous content if the API hiccups
            print(f"skip {key}: {exc}")
    text = replace(text, "QUOTE", quote(now))
    text = replace(text, "UPDATED", f"<sub>🔄 Auto-updated by GitHub Actions · {now:%d %b %Y, %I:%M %p} PKT</sub>")
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == "__main__":
    main()
