import json, sys, os, time, re, shutil, subprocess, tempfile, glob, hashlib

sys.stdout.reconfigure(encoding="utf-8")

NET_CACHE = os.path.join(tempfile.gettempdir(), "sl_net.json")
NO_WIN = 0x08000000
CFG = os.environ.get("CLAUDE_CONFIG_DIR", os.path.expanduser("~/.claude"))
R, D, B = "\033[0m", "\033[2m", "\033[1m"
SEP = f" {D}│{R} "


def net_worker():
    info = {"ts": time.time()}
    try:
        ps = ("$r=Get-NetRoute -DestinationPrefix 0.0.0.0/0|Sort-Object RouteMetric|Select-Object -First 1;"
              "$a=Get-NetAdapter -InterfaceIndex $r.InterfaceIndex;"
              "$i=Get-NetIPAddress -InterfaceIndex $r.InterfaceIndex -AddressFamily IPv4|Select-Object -First 1;"
              "@{gw=$r.NextHop;name=$a.Name;desc=$a.InterfaceDescription;ip=$i.IPAddress}|ConvertTo-Json -Compress")
        o = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True,
                           text=True, timeout=15, creationflags=NO_WIN).stdout
        info.update(json.loads(o))
    except Exception:
        pass
    try:
        info["ext"] = subprocess.run(["curl.exe", "-s", "--max-time", "5", "https://api.ipify.org"],
                                     capture_output=True, text=True, timeout=8,
                                     creationflags=NO_WIN).stdout.strip()
    except Exception:
        pass
    ident = f"{info.get('desc', '')} {info.get('name', '')}"
    info["tether"] = bool(re.search(r"rndis|remote ndis|android|samsung|tether", ident, re.I)
                          or str(info.get("gw", "")).startswith("192.168.42."))
    adb = shutil.which("adb")
    if adb:
        try:
            o = subprocess.run([adb, "shell", "ip", "-4", "addr", "show", "ipsec0"], capture_output=True,
                               text=True, timeout=5, creationflags=NO_WIN).stdout
            m = re.search(r"inet (\d+\.\d+\.\d+\.\d+)", o)
            if m:
                info["phone_vpn"] = m.group(1)
        except Exception:
            pass
    tmp = NET_CACHE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(info, f)
    os.replace(tmp, NET_CACHE)


if "--net" in sys.argv:
    net_worker()
    sys.exit(0)

try:
    d = json.load(sys.stdin)
except Exception:
    d = {}


def g(o, *path):
    for p in path:
        if not isinstance(o, dict):
            return None
        o = o.get(p)
    return o


def bar(pct, n=10):
    pct = max(0, min(100, pct))
    f = round(pct * n / 100)
    return "█" * f + "░" * (n - f)


def color(pct):
    return "\033[32m" if pct < 50 else "\033[33m" if pct < 80 else "\033[31m"


def dot(pct):
    return "🟢" if pct < 50 else "🟡" if pct < 80 else "🔴"


def k(n):
    return f"{n / 1000:.1f}k" if n >= 1000 else str(int(n))


def effort():
    for path in (("effort", "level"), ("effort",), ("effort_level",), ("reasoning_effort",), ("model", "effort")):
        v = g(d, *path)
        if isinstance(v, str) and v:
            return v, False
    try:
        with open(os.path.join(CFG, "settings.json"), encoding="utf-8") as f:
            st = json.load(f)
        v = g(st, "modelSettings", g(d, "model", "id") or "", "effortLevel") or st.get("effortLevel")
        if isinstance(v, str) and v:
            return v, True
    except Exception:
        pass
    return None, False


def load(p):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def usage(tp):
    cp = os.path.join(tempfile.gettempdir(), "sl3_" + hashlib.md5(tp.encode()).hexdigest()[:12] + ".json")
    fresh = {"off": 0, "skills": {}, "mcps": {}, "hooks": {}, "ag": {}, "agt": 0}
    st = load(cp) or {}
    if "off" not in st:
        st = dict(fresh)
    try:
        size = os.path.getsize(tp)
        if size < st["off"]:
            st = dict(fresh)
        if size > st["off"]:
            with open(tp, "rb") as f:
                f.seek(st["off"])
                chunk = f.read()
            end = chunk.rfind(b"\n") + 1
            for line in chunk[:end].splitlines():
                if b'"tool_use"' not in line and b'"hookEvent"' not in line and b'"tool_result"' not in line:
                    continue
                try:
                    obj = json.loads(line)
                    msg = obj.get("message")
                    items = msg.get("content") if isinstance(msg, dict) else None
                    att = obj.get("attachment")
                    if isinstance(att, dict) and att.get("hookEvent"):
                        ev = att["hookEvent"]
                        st["hooks"][ev] = st["hooks"].get(ev, 0) + 1
                except Exception:
                    continue
                for it in items if isinstance(items, list) else []:
                    if isinstance(it, dict) and it.get("type") == "tool_result":
                        st["ag"].pop(it.get("tool_use_id"), None)
                        continue
                    if not isinstance(it, dict) or it.get("type") != "tool_use":
                        continue
                    n = it.get("name") or ""
                    if n == "Agent":
                        st["ag"][it.get("id")] = 1
                        st["agt"] += 1
                    elif n == "Skill":
                        s = (it.get("input") or {}).get("skill")
                        if s:
                            st["skills"][s] = st["skills"].get(s, 0) + 1
                    elif n.startswith("mcp__"):
                        srv = n.split("__")[1]
                        for pre in ("claude_ai_", "plugin_"):
                            if srv.startswith(pre):
                                srv = srv[len(pre):]
                        st["mcps"][srv] = st["mcps"].get(srv, 0) + 1
            st["off"] += end
            with open(cp, "w", encoding="utf-8") as f:
                json.dump(st, f)
    except Exception:
        pass
    return st["skills"], st["mcps"], st.get("hooks", {}), len(st["ag"]), st["agt"]


def perm_mode():
    for path in (("permission_mode",), ("permissionMode",), ("mode",), ("output_style", "permission_mode")):
        v = g(d, *path)
        if isinstance(v, str) and v:
            return v, False
    st = load(os.path.join(CFG, "settings.json"))
    v = st.get("defaultMode") or st.get("defaultPermissionMode")
    return (v, True) if isinstance(v, str) and v else (None, False)


def configured_hooks(cwd):
    events = set()

    def add(h):
        if isinstance(h, dict):
            events.update(e for e, v in h.items() if v)

    gs = load(os.path.join(CFG, "settings.json"))
    add(gs.get("hooks"))
    if cwd:
        for n in ("settings.json", "settings.local.json"):
            add(load(os.path.join(cwd, ".claude", n)).get("hooks"))
    enabled = {e for e, v in (gs.get("enabledPlugins") or {}).items() if v}
    inst = load(os.path.join(CFG, "plugins", "installed_plugins.json")).get("plugins") or {}
    for key in enabled:
        for e in inst.get(key) or []:
            ip = e.get("installPath") if isinstance(e, dict) else None
            if ip:
                add(load(os.path.join(ip, "hooks", "hooks.json")).get("hooks"))
    return sorted(events)


def fmt(items, n=3):
    top = sorted(items.items(), key=lambda x: -x[1])
    s = ", ".join(f"{a}{D}×{v}{R}" for a, v in top[:n])
    return s + (f" {D}+{len(top) - n}{R}" if len(top) > n else "")


HOOK_SHORT = {"SessionStart": "SS", "SessionEnd": "End", "UserPromptSubmit": "UPS", "PreToolUse": "Pre",
              "PostToolUse": "Post", "Stop": "Stop", "SubagentStop": "SubStop", "Notification": "Notif",
              "PreCompact": "PreCmp"}


def remote_status():
    sid = d.get("session_id")
    for p in glob.glob(os.path.join(CFG, "sessions", "*.json")):
        s = load(p)
        if sid and s.get("sessionId") == sid:
            return "📡 RC \033[32m✅\033[0m" if s.get("bridgeSessionId") else f"📡 RC {D}off{R}"
    return f"📡 RC {D}?{R}"


def net_line():
    info = load(NET_CACHE)
    now = time.time()
    if now - info.get("ts", 0) > 45 and now - info.get("spawned", 0) > 30:
        info["spawned"] = now
        try:
            with open(NET_CACHE, "w", encoding="utf-8") as f:
                json.dump(info, f)
            subprocess.Popen([sys.executable, os.path.abspath(__file__), "--net"],
                             stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             creationflags=0x00000008 | NO_WIN, close_fds=True)
        except Exception:
            pass
    loc, ext = info.get("ip") or "…", info.get("ext") or "…"
    vpn = info.get("phone_vpn")
    if info.get("tether"):
        via = "📱 phone" + (f" → 🏠 home gateway \033[32m✅{R}" if vpn else f" \033[33m(home VPN off){R}")
    else:
        via = f"🖥️ direct {D}({info.get('name') or '…'}){R}" + (f" {D}phone VPN ready{R}" if vpn else "")
    return SEP.join([f"🌐 {loc} {D}→{R} {ext}", via, remote_status()])


cwd = g(d, "workspace", "current_dir") or d.get("cwd")

# riga 1: sessione e limiti
l1 = []
m = g(d, "model", "display_name") or g(d, "model", "id")
if m:
    e, from_cfg = effort()
    tag = f" ⚡{B}{e}{R}{D}{'*' if from_cfg else ''}{R}" if e else ""
    l1.append(f"🤖 {B}{m}{R}{tag}")

limits = []
for name, path in (("ctx", ("context_window", "used_percentage")),
                   ("5h", ("rate_limits", "five_hour", "used_percentage")),
                   ("7d", ("rate_limits", "seven_day", "used_percentage"))):
    v = g(d, *path)
    if v is not None:
        limits.append((v, name))
if limits:
    top, top_name = max(limits)
    tg = "OK" if top < 50 else "HIGH" if top < 80 else "CRITICAL"
    l1.append(f"{dot(top)} {color(top)}{B}LIMITS {top:.0f}% {tg}{R} {D}({top_name}){R}")

if cwd:
    l1.append(f"📁 {os.path.basename(cwd.rstrip(chr(92) + '/')) or cwd}")

for key, icon, label in (("five_hour", "⏳", "5h"), ("seven_day", "📅", "7d")):
    p = g(d, "rate_limits", key, "used_percentage")
    if p is not None:
        s = f"{icon}{label} {color(p)}{bar(p, 6)} {p:.0f}%{R}"
        ra = g(d, "rate_limits", key, "resets_at")
        if isinstance(ra, (int, float)):
            mins = int((ra - time.time()) // 60)
            if mins > 0:
                s += f"{D}↻{mins // 60}h{mins % 60:02d}m{R}"
        l1.append(s)

cost = g(d, "cost", "total_cost_usd")
if cost is not None:
    l1.append(f"💰${cost:.2f}")
dur = g(d, "cost", "total_duration_ms")
if dur:
    mins = int(dur // 60000)
    l1.append("🕒" + (f"{mins // 60}h{mins % 60:02d}m" if mins >= 60 else f"{mins}m"))
a, r = g(d, "cost", "total_lines_added"), g(d, "cost", "total_lines_removed")
if a or r:
    l1.append(f"✏️\033[32m+{a or 0}{R}/\033[31m-{r or 0}{R}")
if d.get("exceeds_200k_tokens"):
    l1.append("⚠️ \033[31m>200k\033[0m")

# riga 2: /context + skill + MCP + hook
l2 = []
cw = d.get("context_window") if isinstance(d.get("context_window"), dict) else {}
size, pct, cu = cw.get("context_window_size"), cw.get("used_percentage"), cw.get("current_usage")
if size:
    used = 0
    if isinstance(cu, dict):
        used = sum(cu.get(x) or 0 for x in ("input_tokens", "output_tokens",
                                             "cache_creation_input_tokens", "cache_read_input_tokens"))
    if not used and pct is not None:
        used = pct * size / 100
    p = pct if pct is not None else used * 100 / size
    f = round(min(p, 100) * 10 / 100)
    l2.append(f"📊 {color(p)}{'⛁' * f}{R}{D}{'⛶' * (10 - f)}{R} {k(used)}/{k(size)} {D}free {k(max(size - used, 0))}{R}")

tp = d.get("transcript_path")
sk, mc, hk, ag_open, ag_tot = usage(tp) if tp else ({}, {}, {}, 0, 0)
pm, pm_cfg = perm_mode()
if pm:
    l1.insert(1 if l1 else 0, f"🛡️ {B}{pm}{R}{D}{'*' if pm_cfg else ''}{R}")
l1.insert(2 if len(l1) > 1 else len(l1), f"👥 {B if ag_open else D}{ag_open}{R}{D} active/{ag_tot} launched{R}")
l2.append(f"🧩 {fmt(sk) if sk else D + '—' + R}")
l2.append(f"🔌 {fmt(mc) if mc else D + '—' + R}")
names = sorted(set(configured_hooks(cwd)) | set(hk))
if names:
    l2.append("🪝 " + " ".join(
        f"{HOOK_SHORT.get(n, n)}{D}×{hk[n]}{R}" if n in hk else f"{D}{HOOK_SHORT.get(n, n)}{R}" for n in names))

# riga 3: rete + remote control
print("\n".join([SEP.join(l1), SEP.join(l2), net_line()]))
