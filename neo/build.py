#!/usr/bin/env python3
"""Build neo/index.html — experimental Project Atlas redesign of lyf266.github.io.
Reads neo/projects.json (extracted from main index.html), applies copy fixes,
and renders a single self-contained page at /neo/.
"""
import json, re, html as htmllib

P = json.load(open('neo/projects.json', encoding='utf-8'))

# ---------------------------------------------------------------- copy fixes
# (zh_old, zh_new, en_old, en_new) — ChatGPT second-round review rewrites
FIXES = [
 ("实现广播级画质与零外部常驻后台进程，彻底免疫 USB 总线丢包与驱动崩溃。",
  "通过减少中间层依赖，降低 USB 采集过程中的丢帧风险。系统不需要额外后台服务，采集和处理流程保持在单一应用内。",
  "Broadcast-grade output with zero external background daemons, immune to USB bus packet corruption.",
  "Fewer middleware layers mean fewer dropped frames during USB capture. No extra background services — capture and processing stay inside a single app."),
 ("显存占用与推理速度极致平衡；VAD 语音活动检测精准裁切首尾静音，避免尾音重复幻觉；Unix Domain Socket 进程间通信隔离监听与推理。",
  "在模型部署时，我重点优化显存占用和响应速度之间的平衡。通过 VAD 判断有效语音区间，减少无意义音频输入，同时将监听和推理拆分为独立进程，避免任务互相影响。",
  None, None),
 ("纯原生 Python 3 (sqlite3, json, qdbus6) 结合 KWin 内部脚本，零外部 pip 依赖。三级渐进式窗口识别算法（用户自定义映射 → XDG .desktop 应用程序元数据 → 进程兜底匹配）。",
  "项目尽量保持轻量化，没有引入额外 Python 第三方依赖。窗口识别采用三级匹配策略：1. 用户自定义规则优先；2. 使用系统应用元数据辅助判断；3. 最后根据进程信息进行兜底。",
  None, None),
 ("实现零心智负担沉淀", "让信息记录变成低干扰的后台流程", None, None),
 ("牺牲了远距离视距渲染以换取极致低带宽，适合局域或固定小圈子联机场景。",
  "为降低网络带宽需求，项目限制了远距离场景的数据同步范围，更适合局域网或固定玩家群体使用。",
  None, None),
 ("目前系统已打通‘个人目标追踪 - 日志复盘 - 决策反思’的内生闭环。核心痛点在于：LifeOS 涉及现实生活的多元领域（金融市场、行为习惯、情绪心理等），当前缺乏统一且具备深度感知预测能力的‘世界模型 (World Model)’，且缺乏跨领域的严谨 Agent Harness 评测工程进行多维校准与安全约束。",
  "当前版本已经实现了目标记录、行为日志分析和阶段性复盘之间的数据连接。下一阶段主要挑战是如何让系统理解更加复杂的人类行为场景。例如，不同领域的数据（工作、财务、习惯、情绪）之间存在关联，但目前仍缺少一个可靠的方法进行统一建模和长期预测。",
  None, None),
 ("严谨的医疗级 Agent Harness 评估工程", "严谨的医疗级评估工程", None, None),
 ("严格的量化 Financial Harness 评测工程", "严格的量化评测工程", None, None),
 ("全面���进升级", "全面升级", None, None),
 ("内生闭环", "流程", None, None),
]

def fix(text, lang):
    for zh_old, zh_new, en_old, en_new in FIXES:
        if lang == 'zh' and zh_old in text:
            text = text.replace(zh_old, zh_new)
        if lang == 'en' and en_old and en_old in text:
            text = text.replace(en_old, en_new)
    return text

# ---------------------------------------------------------------- per-project flows & trees
# key: match substring in title_zh -> (steps[(zh,en)...], tree[(node, zh, en)...])
FLOWS = {
 "银行从业": ([("清洗题库","Clean bank"),("校准监管口径","Calibrate rules"),("仿真机考","Simulate exam"),("错题进 Anki","Wrong → Anki")],
   [("exam.html","ATA 机考界面","ATA exam UI"),("tvm-calc.js","TVM 金融计算器","TVM calculator"),("questions-710.json","真题库","question bank"),("anki-export.js","FSRS 卡包导出","FSRS deck export")]),
 "Whisper": ([("按下快捷键","Hotkey"),("捕获音频","Capture audio"),("VAD 裁切","VAD trim"),("本地推理","Local inference"),("注入文本","Inject text")],
   [("daemon.py","常驻监听","resident listener"),("vad.py","语音端点检测","voice activity detection"),("infer.py","CTranslate2 推理","inference"),("wayland-inject.py","文本注入","text injection")]),
 "TimeTracker": ([("监听窗口","Listen"),("三级识别","3-level identify"),("本地存储","Local store"),("夜间日报","Nightly report")],
   [("kwin-script.js","窗口监听","window listener"),("identify.py","三级识别","3-level identify"),("store.db","SQLite 本地存储","local storage"),("report.py","日报生成","report generator")]),
 "LifeOS": ([("记录日志","Log"),("检索事实","Retrieve"),("LLM 复盘","AI review"),("决策建议","Advise")],
   [("api/","FastAPI 模块化单体","modular monolith"),("web/","Next.js 前端","frontend"),("postgres/","规范事实库","fact store"),("qdrant/","语义向量检索","vector search")]),
 "Opportunity Intelligence": ([("抓取多渠道","Fetch feeds"),("加权打分","Weighted score"),("推送高分","Push top")],
   [("fetch_feeds.py","多源抓取引擎","feed fetcher"),("score.py","加权打分","scoring"),("server.py","轻量 HTTP 服务","micro server"),("radar.svg","机会雷达图","opportunity radar")]),
 "Hermes": ([("定时调度","Schedule"),("执行任务","Execute"),("异常报警","Alert")],
   [("cron/","18+ 定时管线","scheduled pipelines"),("tunnel/","安全传输通道","secure tunnel"),("watchdog.sh","健康巡检","health checks"),("webhook","Telegram 报警","alert hook")]),
 "Finance-Intel": ([("聚合行情","Aggregate"),("检测异动","Detect anomaly"),("早报推送","Morning brief")],
   [("fetch.py","多源行情聚合","data aggregation"),("anomaly.py","异动检测","anomaly detection"),("brief.py","早报生成推送","brief + push")]),
 "知识库同步桥": ([("本地编辑","Edit locally"),("混合写入","Hybrid write"),("云端同步","Sync to cloud")],
   [("obsidian-api","编辑器热写入","hot write"),("fallback-fs","文件直写降级","fs fallback"),("notion-sync","云端看板同步","board sync")]),
 "OBS": ([("YUYV 直采","Raw capture"),("绕过软解","Bypass decode"),("叠加信息","Overlay"),("推流","Stream")],
   [("yuyv-capture","原始像素直采","raw capture"),("udev.rules","禁用 USB 休眠","no autosuspend"),("overlay.lua","时间/待办叠加","overlays")]),
 "WTF": ([("拉取 API","Fetch APIs"),("渲染组件","Render widgets"),("终端展示","Terminal view")],
   [("pai.go","目标进度组件","goal widget"),("poi.go","机会榜单组件","opportunity widget")]),
 "被动式 AI 笔记": ([("发送消息","Send message"),("意图分类","Classify intent"),("分流存储","Route & store")],
   [("bot.py","Telegram 接收","receiver"),("classify.py","Gemini 意图分类","intent sort"),("to-notion.py","任务分流","task route"),("to-obsidian.py","日记分流","journal route")]),
 "Vitals": ([("OCR 提取","OCR extract"),("归一化","Normalize"),("异常标红","Flag anomaly")],
   [("ocr.py","报告提取","report OCR"),("normalize.py","指标归一化","normalization"),("flag.py","异常标红","anomaly flags")]),
 "mc118": ([("安全硬化","Harden"),("压缩带宽","Slim bandwidth"),("反向备份","Reverse backup")],
   [("paper-1.18.1","服务端","game server"),("bbr+ufw","网络与防火墙","net + firewall"),("backup.sh","反向备份","reverse backup")]),
 "课程录音": ([("切分音频","Split audio"),("转写","Transcribe"),("归档","Archive")],
   [("split.sh","按课程切分","split by course"),("whisper.py","faster-whisper 转写","transcription"),("archive.py","讲义归档","note archive")]),
 "Linux 工作站": ([("装机调优","Tune system"),("网络配置","Configure net"),("证书自动化","Auto TLS")],
   [("arch/","Zen 内核调优","tuned kernel"),("debian-vps/","云服务器","cloud VPS"),("tls-auto/","证书自动化","cert automation")]),
 "反指纹": ([("封堵泄漏","Block leaks"),("扰动指纹","Perturb prints"),("保持体验","Keep UX")],
   [("webrtc-block","泄漏封堵","leak blocking"),("canvas-noise","指纹扰动","print noise"),("tz-spoof","时区模拟","timezone spoof")]),
 "WriteMap": ([("提交作文","Submit essay"),("多维打分","Rubric score"),("结构反馈","Structural feedback")],
   [("editor/","编辑器+结构树","editor + tree"),("score.ts","多维打分","scoring"),("prisma.db","作品存储","essay storage")]),
 "Gaokao": ([("抓取接口","Scrape API"),("清洗数据","Clean data"),("对比决策","Compare")],
   [("scrape.py","接口抓取","API scrape"),("clean.py","Pandas 清洗","cleaning"),("compare.csv","对比表格","comparison table")]),
 "演示文稿": ([("理解需求","Read brief"),("网格排版","Grid layout"),("交付","Deliver")],
   [("grid/","网格排版系统","grid system"),("type/","思源黑体规范","typography spec")]),
 "Minecraft 联机社区": ([("拨号组网","Dial-up net"),("论坛招募","Recruit"),("运营活动","Operate")],
   [("pppoe","拨号公网 IP","dial-up public IP"),("nat-map","端口映射","port mapping"),("forum","社区运营","community ops")]),
}

DOMAINS = [
 ("all", "全部", "All"),
 ("ai", "AI / Agent", "AI / Agent"),
 ("linux", "Linux 系统", "Linux"),
 ("quant", "量化金融", "Quant Finance"),
 ("web", "Web 应用", "Web Apps"),
 ("net", "网络基建", "Network & Infra"),
 ("tool", "小工具", "Tools"),
]
DOMAIN_OF_TAG = {"ai":"ai","agent":"ai","linux":"linux","quant":"quant","web":"web","net":"net","tool":"tool"}

def esc(s):
    return htmllib.escape(s, quote=True)

def find_flow(title):
    for k, v in FLOWS.items():
        if k in title:
            return v
    return ([("输入","Input"),("处理","Process"),("输出","Output")],
            [("src/","源码","source")])

# ---------------------------------------------------------------- rendering

def extract_links():
    html = open('index.html', encoding='utf-8').read()
    items = re.findall(r'<li class="project-item[^"]*"[^>]*>.*?</li>', html, re.S)
    out = {}
    for it in items:
        t = re.search(r'class="project-title-text"[^>]*\sdata-zh="([^"]*)"', it)
        if not t:
            continue
        links = []
        for m in re.finditer(r'<a [^>]*href="([^"]+)"[^>]*>', it):
            tag = m.group(0)
            if 'demo-badge-link' in tag:
                links.append(('demo', m.group(1)))
            elif 'repo-badge-link' in tag:
                links.append(('repo', m.group(1)))
        out[t.group(1)] = links
    return out

LINKS = extract_links()

def get_row(p, *labels):
    for r in p['detail_rows']:
        if r['label'] in labels:
            return r
    return None

def trim_zh(s, n=170):
    s = s.strip()
    parts = re.split(r'(?<=[。！？])', s)
    out = ''
    for part in parts:
        if out and len(out) + len(part) > n:
            break
        out += part
    return out or s[:n]

def trim_en(s, n=260):
    s = s.strip()
    parts = re.split(r'(?<=\.) ', s)
    out = ''
    for part in parts:
        if out and len(out) + len(part) > n:
            break
        out += part if out.endswith('.') or not out else ' ' + part
    return (out or s[:n]).strip()

def bielem(zh, en, tag='span', cls=''):
    zh, en = esc(fix(zh, 'zh')), esc(fix(en, 'en'))
    c = f' class="{cls}"' if cls else ''
    return f'<{tag}{c} data-zh="{zh}" data-en="{en}">{zh}</{tag}>'

def card(p, idx):
    num = f'PROJECT_{idx:02d}'
    if '已归档' in p['desc_zh'] or 'Archived' in p['desc_en']:
        st_en, st_zh, st_cls = 'ARCHIVED', '已归档', 'archived'
    elif 'featured' in p['data_tags']:
        st_en, st_zh, st_cls = 'FEATURED', '精选', 'featured'
    else:
        st_en, st_zh, st_cls = 'ACTIVE', '进行中', 'active'
    domains = sorted({DOMAIN_OF_TAG[t] for t in p['data_tags'] if t in DOMAIN_OF_TAG})
    steps, tree = find_flow(p['title_zh'])

    problem = get_row(p, '核心痛点与问题')
    method = get_row(p, '方法策略与工程实现', 'AI 目标、规划与提示词设定')
    tradeoff = get_row(p, '局限权衡与后续演进')

    prob_zh = fix(problem['zh'], 'zh') if problem else p['desc_zh']
    prob_en = fix(problem['en'], 'en') if problem else p['desc_en']
    res_zh = trim_zh(tradeoff['zh']) if tradeoff else p['desc_zh']
    res_en = trim_en(tradeoff['en']) if tradeoff else p['desc_en']

    # flow steps
    flow_html = ''
    for i, (szh, sen) in enumerate(steps):
        if i:
            flow_html += '<span class="farrow">→</span>'
        flow_html += f'<span class="step">{bielem(szh, sen)}</span>'
    method_note = ''
    if method:
        mz = trim_zh(fix(method['zh'], 'zh'), 220)
        me = trim_en(fix(method['en'], 'en'), 340)
        if mz:
            method_note = f'<p class="sec-body eng-note">{bielem(mz, me)}</p>'

    # tree
    tree_lines = [f'<span class="tdir">{esc(p["title_en"][:24] if p["title_en"] else "proj")}/</span>']
    for i, (node, nzh, nen) in enumerate(tree):
        branch = '└──' if i == len(tree) - 1 else '├──'
        tree_lines.append(bielem(f'{branch} {node} ── {nzh}', f'{branch} {node} ── {nen}'))
    tree_html = '<pre class="tree">' + '\n'.join(tree_lines) + '</pre>'

    # engineering note (fixed arch text, trimmed)
    arch = next((r for r in p['detail_rows'] if r['label'].startswith('架构设计')), None)
    eng_note = ''
    if arch:
        nz = trim_zh(fix(arch['zh'], 'zh'), 220)
        ne = trim_en(fix(arch['en'], 'en'), 340)
        if nz and nz not in prob_zh:
            eng_note = f'<p class="sec-body eng-note">{bielem(nz, ne)}</p>'

    # links
    link_html = ''
    for typ, url in LINKS.get(p['title_zh'], []):
        if typ == 'demo':
            link_html += f'<a class="hlink" href="{esc(url)}" target="_blank" rel="noopener">{bielem("演示 ↗", "Demo ↗")}</a>'
        else:
            link_html += f'<a class="hlink" href="{esc(url)}" target="_blank" rel="noopener">GitHub ↗</a>'

    tags = [t for t in p['tag_labels'] if '精选' not in t and 'Featured' not in t]
    tag_html = ''.join(f'<span class="tag">{esc(t)}</span>' for t in tags)

    return f'''
<article class="card" id="p{idx:02d}" data-domains="{' '.join(domains)}">
  <div class="card-top mono">
    <span class="proj-num">{num}</span>
    <span class="status {st_cls}">{bielem(st_zh, st_en)}</span>
    <span class="card-links">{link_html}</span>
  </div>
  <h2 class="card-title">{bielem(p['title_zh'], p['title_en'])}</h2>
  <p class="oneline">{bielem(p['desc_zh'], p['desc_en'])}</p>
  <section class="sec">
    <div class="seclab mono"><span class="dot"></span>{bielem('问题', 'PROBLEM')}</div>
    <p class="sec-body">{bielem(prob_zh, prob_en)}</p>
  </section>
  <section class="sec">
    <div class="seclab mono"><span class="dot"></span>{bielem('方法', 'APPROACH')}</div>
    <div class="flow">{flow_html}</div>
    {method_note}
  </section>
  <section class="sec">
    <div class="seclab mono"><span class="dot"></span>{bielem('工程', 'ENGINEERING')}</div>
    {tree_html}
    {eng_note}
  </section>
  <section class="sec">
    <div class="seclab mono"><span class="dot"></span>{bielem('结果 / 状态', 'RESULT')}</div>
    <p class="sec-body">{bielem(res_zh, res_en)}</p>
  </section>
  <div class="tagrow">{tag_html}</div>
</article>'''

# ---------------------------------------------------------------- page template

CSS = '''
:root{--bg:#0d1117;--panel:#161b22;--line:#30363d;--text:#e6edf3;--muted:#8b949e;
--accent:#58a6ff;--green:#3fb950;--yellow:#d29922;--star:#e3b341;--purple:#bc8cff}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--text);margin:0;
font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC","PingFang SC","Microsoft YaHei",sans-serif;
line-height:1.7}
.mono{font-family:ui-monospace,SFMono-Regular,"JetBrains Mono",Menlo,Consolas,monospace}
.wrap{max-width:880px;margin:0 auto;padding:24px 18px 80px}
.topbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:28px;flex-wrap:wrap;gap:12px}
.backlink{color:var(--muted);text-decoration:none;font-size:13px}
.backlink:hover{color:var(--accent)}
.langbtn{background:transparent;border:1px solid var(--line);color:var(--text);border-radius:6px;
padding:6px 14px;cursor:pointer;font-size:13px}
.langbtn:hover{border-color:var(--accent);color:var(--accent)}
.hero{border:1px solid var(--line);border-radius:12px;padding:32px 28px;margin-bottom:24px;
background:linear-gradient(180deg,#161b22,#0d1117)}
.hero .kicker{font-size:12px;letter-spacing:3px;color:var(--accent)}
.hero h1{font-size:34px;margin:10px 0 6px;letter-spacing:1px}
.hero .sub{color:var(--muted);font-size:14px;margin:0 0 20px}
.stats{display:flex;gap:28px;flex-wrap:wrap}
.stat .n{font-size:26px;color:var(--text)}
.stat .l{font-size:11px;color:var(--muted);letter-spacing:2px}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px}
.chip{background:transparent;border:1px solid var(--line);color:var(--muted);border-radius:20px;
padding:5px 14px;font-size:13px;cursor:pointer}
.chip:hover{border-color:var(--accent);color:var(--text)}
.chip.on{background:var(--accent);border-color:var(--accent);color:#0d1117;font-weight:600}
.countline{color:var(--muted);font-size:12px;margin:10px 0 0}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:22px;margin:20px 0}
.card.hide{display:none}
.card-top{display:flex;align-items:center;gap:10px;margin-bottom:8px;flex-wrap:wrap}
.proj-num{font-size:12px;color:var(--muted);letter-spacing:1px}
.status{font-size:11px;padding:2px 10px;border-radius:20px;border:1px solid}
.status.active{color:var(--green);border-color:var(--green)}
.status.archived{color:var(--muted);border-color:var(--muted)}
.status.featured{color:var(--star);border-color:var(--star)}
.card-links{margin-left:auto;display:flex;gap:10px}
.hlink{color:var(--muted);text-decoration:none;font-size:12px;border:1px solid var(--line);
border-radius:4px;padding:2px 8px}
.hlink:hover{color:var(--accent);border-color:var(--accent)}
.card-title{font-size:20px;margin:6px 0 4px}
.oneline{color:var(--text);font-size:14.5px;margin:0 0 6px}
.sec{margin-top:16px;border-top:1px dashed var(--line);padding-top:12px}
.seclab{font-size:11px;letter-spacing:3px;color:var(--accent);margin-bottom:8px;display:flex;align-items:center;gap:8px}
.seclab .dot{width:7px;height:7px;border-radius:50%;background:var(--accent);display:inline-block}
.sec-body{font-size:14px;color:var(--text);margin:0}
.flow{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.step{background:#0d1117;border:1px solid var(--accent);border-radius:6px;padding:5px 12px;font-size:13px}
.farrow{color:var(--accent);font-weight:700}
.tree{background:#0d1117;border:1px solid var(--line);border-radius:6px;padding:12px 14px;
font-size:12.5px;overflow-x:auto;margin:0;line-height:1.8;color:var(--text)}
.tree .tdir{color:var(--purple)}
.eng-note{margin-top:10px;font-size:13.5px;color:var(--muted)}
.eng-note:hover{color:var(--text)}
.tagrow{margin-top:14px;display:flex;gap:6px;flex-wrap:wrap}
.tag{font-size:11.5px;color:var(--muted);border:1px solid var(--line);border-radius:4px;padding:1px 8px}
footer{margin-top:48px;color:var(--muted);font-size:12px;text-align:center}
footer a{color:var(--muted)}
@media(max-width:640px){.hero h1{font-size:26px}.hero{padding:22px 18px}.card{padding:16px}}
'''

JS = '''
let lang='zh';
function setLang(l){
  lang=l;
  document.querySelectorAll('[data-zh]').forEach(el=>{
    el.textContent=el.getAttribute('data-'+l);
  });
  document.getElementById('langBtn').textContent = l==='zh' ? 'EN / 英文' : '中文 / ZH';
  document.documentElement.lang = l==='zh'?'zh-CN':'en';
  applyFilter();
}
document.getElementById('langBtn').addEventListener('click',()=>setLang(lang==='zh'?'en':'zh'));
applyFilter();

const chips=document.querySelectorAll('.chip');
const cards=document.querySelectorAll('.card');
const countEl=document.getElementById('countLine');
function applyFilter(){
  const on=document.querySelector('.chip.on');
  const d=on?on.dataset.domain:'all';
  let n=0;
  cards.forEach(c=>{
    const show = d==='all' || c.dataset.domains.split(' ').includes(d);
    c.classList.toggle('hide',!show);
    if(show)n++;
  });
  const total=cards.length;
  countEl.textContent = lang==='zh' ? `显示 ${n} / ${total} 个项目` : `Showing ${n} / ${total} projects`;
}
chips.forEach(ch=>ch.addEventListener('click',()=>{
  chips.forEach(c=>c.classList.remove('on'));
  ch.classList.add('on');
  applyFilter();
}));
'''

def main():
    cards_html = '\n'.join(card(p, i + 1) for i, p in enumerate(P))
    chips_html = '\n'.join(
        f'<button class="chip mono{" on" if d=="all" else ""}" data-domain="{d}">{bielem(zh, en)}</button>'
        for d, zh, en in DOMAINS)
    n_feat = sum(1 for p in P if 'featured' in p['data_tags'])
    n_arch = sum(1 for p in P if '已归档' in p['desc_zh'])

    page = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Project Atlas — LYF Archive (neo)</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <div class="topbar">
    <a class="backlink mono" href="../">← lyf266.github.io</a>
    <button class="langbtn mono" id="langBtn">EN / 英文</button>
  </div>
  <header class="hero">
    <div class="kicker mono">NEO · EXPERIMENTAL REDESIGN</div>
    <h1 class="mono">LYF PROJECT ATLAS</h1>
    <p class="sub">{bielem('20 个项目的技术档案库 —— 每个项目：问题 → 方法 → 工程 → 结果。不再是 README 墙。',
'Technical archive of 20 projects — each one: problem → approach → engineering → result. Not a README wall.')}</p>
    <div class="stats mono">
      <div class="stat"><div class="n">{len(P)}</div><div class="l">{bielem("项目","PROJECTS")}</div></div>
      <div class="stat"><div class="n">06</div><div class="l">{bielem("技术领域","DOMAINS")}</div></div>
      <div class="stat"><div class="n">{n_feat:02d}</div><div class="l">{bielem("精选","FEATURED")}</div></div>
      <div class="stat"><div class="n">02</div><div class="l">{bielem("语言","LANGUAGES")}</div></div>
    </div>
  </header>
  <div class="filters">{chips_html}</div>
  <p class="countline mono" id="countLine"></p>
  <main>{cards_html}</main>
  <footer class="mono">
    {bielem('实验性改版 · 由主站内容生成 · neo 分支',
           'Experimental redesign · generated from main site content · neo branch')}<br>
    <a href="../">← {bielem("返回主站","back to main site")}</a>
  </footer>
</div>
<script>{JS}</script>
</body>
</html>'''
    open('neo/index.html', 'w', encoding='utf-8').write(page)
    print(f'wrote neo/index.html ({len(page)} chars, {len(P)} cards)')

main()
