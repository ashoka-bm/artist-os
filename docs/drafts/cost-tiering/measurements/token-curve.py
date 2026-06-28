#!/usr/bin/env python3
"""Generate a standalone per-turn token curve (context size + cumulative) for a
Claude Code or Codex session transcript, so runs can be compared before/after the
cost-tiering changes.

Usage:
  token-curve.py <transcript.jsonl> [out.html] [--title "label"]

Auto-detects format. Writes a self-contained HTML (Chart.js via CDN, light/dark
aware). The point: re-run on a future Queen-Bee-equivalent project and put the new
HTML next to the baseline in curves/ to see the area under the curve shrink.
"""
import json, sys, os

def _find(o, key, acc):
    if isinstance(o, dict):
        if isinstance(o.get(key), dict):
            acc[0] = o[key]
        for v in o.values():
            _find(v, key, acc)
    elif isinstance(o, list):
        for v in o:
            _find(v, key, acc)


def series(path):
    """Return (ctx_per_turn[], cumulative[]). ctx = approx context window that turn."""
    lines = [l for l in open(path, encoding="utf-8", errors="ignore").read().splitlines() if l.strip()]
    is_codex = any('"total_token_usage"' in l for l in lines)
    ctx, cum = [], []
    if is_codex:
        for l in lines:
            if '"total_token_usage"' not in l:
                continue
            try:
                o = json.loads(l)
            except Exception:
                continue
            tot = [None]; _find(o, "total_token_usage", tot)
            if tot[0] is None:
                continue
            last = [None]; _find(o, "last_token_usage", last)
            cum.append(tot[0].get("total_tokens", 0))
            ctx.append((last[0] or {}).get("input_tokens", 0))
    else:
        run = 0
        for l in lines:
            try:
                o = json.loads(l)
            except Exception:
                continue
            u = None
            m = o.get("message") if isinstance(o, dict) else None
            if isinstance(m, dict) and isinstance(m.get("usage"), dict):
                u = m["usage"]
            elif isinstance(o, dict) and isinstance(o.get("usage"), dict):
                u = o["usage"]
            if u and "output_tokens" in u:
                window = u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
                run += window + u.get("output_tokens", 0)
                ctx.append(window)
                cum.append(run)
    return ctx, cum


TEMPLATE = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ — token curve</title>
<style>
 :root{--bg:#fff;--fg:#1a1a18;--muted:#6b6a64;--surface:#faf9f5;--border:rgba(0,0,0,.12)}
 @media(prefers-color-scheme:dark){:root{--bg:#1d1c1a;--fg:#ece9e2;--muted:#a6a49b;--surface:#262522;--border:rgba(255,255,255,.14)}}
 body{margin:0;padding:24px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--fg)}
 .wrap{max-width:920px;margin:0 auto}h1{font-size:20px;font-weight:500}
 .cards{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:16px 0}
 .card{background:var(--surface);border-radius:8px;padding:12px 16px}.card .l{font-size:13px;color:var(--muted)}.card .v{font-size:24px;font-weight:500}
 .legend{display:flex;gap:16px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin-bottom:8px}
 .legend span{display:flex;align-items:center;gap:6px}
</style></head><body><div class="wrap">
<h1>__TITLE__</h1>
<div class="cards">
 <div class="card"><div class="l">peak context / turn</div><div class="v">__PEAK__</div></div>
 <div class="card"><div class="l">mean context / turn</div><div class="v">__MEAN__</div></div>
 <div class="card"><div class="l">total over __N__ turns</div><div class="v">__TOTAL__</div></div>
</div>
<div class="legend">
 <span><span style="width:14px;height:3px;background:#E24B4A"></span>context re-read / turn (left)</span>
 <span><span style="width:14px;height:10px;background:rgba(55,138,221,.25);border-top:2px solid #378ADD"></span>cumulative (right)</span>
 <span><span style="width:14px;height:0;border-top:2px dashed #BA7517"></span>target cap ~90k</span>
</div>
<div style="position:relative;width:100%;height:340px"><canvas id="c" role="img" aria-label="__ARIA__"></canvas></div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js" integrity="sha384-dug+JxfBvklEQdJ4AYuBBAIScUz0bVN73xpy273gcAwHjb3qI0fXmuYNaNfdyYJG" crossorigin="anonymous"></script>
<script>
const CTX=__CTX__,CUM=__CUM__,n=CTX.length,labels=CTX.map((_,i)=>i+1),cap=CTX.map(()=>90000);
const dark=matchMedia('(prefers-color-scheme:dark)').matches,tk=dark?'#a6a49b':'#5f5e5a',gr=dark?'rgba(255,255,255,.08)':'rgba(0,0,0,.08)';
new Chart(document.getElementById('c'),{type:'line',data:{labels,datasets:[
 {label:'context/turn',data:CTX,yAxisID:'y',borderColor:'#E24B4A',borderWidth:1.5,pointRadius:0,tension:.15},
 {label:'cumulative',data:CUM,yAxisID:'y1',borderColor:'#378ADD',backgroundColor:'rgba(55,138,221,.18)',borderWidth:2,pointRadius:0,fill:true,tension:.1},
 {label:'cap',data:cap,yAxisID:'y',borderColor:'#BA7517',borderWidth:1,borderDash:[6,4],pointRadius:0}
]},options:{responsive:true,maintainAspectRatio:false,interaction:{intersect:false,mode:'index'},
 plugins:{legend:{display:false}},scales:{
  x:{title:{display:true,text:'turn',color:tk},ticks:{color:tk,maxTicksLimit:9},grid:{color:gr}},
  y:{position:'left',title:{display:true,text:'context tokens / turn',color:tk},ticks:{color:tk,callback:v=>(v/1000).toFixed(0)+'k'},grid:{color:gr},min:0},
  y1:{position:'right',title:{display:true,text:'cumulative',color:tk},ticks:{color:tk,callback:v=>(v/1e6).toFixed(1)+'M'},grid:{drawOnChartArea:false},min:0}
}}});
</script></body></html>"""


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    title = "session"
    if "--title" in argv:
        title = argv[argv.index("--title") + 1]
    if not args:
        print("usage: token-curve.py <transcript.jsonl> [out.html] [--title T]", file=sys.stderr)
        return 1
    src = args[0]
    out = args[1] if len(args) > 1 else os.path.splitext(os.path.basename(src))[0] + "-curve.html"
    ctx, cum = series(src)
    if not ctx:
        print("no per-turn usage found", file=sys.stderr)
        return 1
    n = len(ctx)
    peak = max(ctx); mean = sum(ctx) // n; total = cum[-1]
    k = lambda v: f"{v/1000:.0f}k" if v < 1e6 else f"{v/1e6:.1f}M"
    html = (TEMPLATE
            .replace("__TITLE__", title)
            .replace("__N__", str(n))
            .replace("__PEAK__", k(peak)).replace("__MEAN__", k(mean)).replace("__TOTAL__", k(total))
            .replace("__ARIA__", f"{title}: per-turn context peaks at {k(peak)}, mean {k(mean)}, over {n} turns; cumulative reaches {k(total)}.")
            .replace("__CTX__", json.dumps(ctx)).replace("__CUM__", json.dumps(cum)))
    open(out, "w").write(html)
    print(f"wrote {out}  ({n} turns, peak {k(peak)}, mean {k(mean)}, total {k(total)})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
