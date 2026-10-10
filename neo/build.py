#!/usr/bin/env python3
"""Rebuild neo/index.html from the UI reference prototype + real project data.

- Template: workspace/user/files/portfolio-ui-reference.html (visual/interaction)
- Data: neo/projects.json (extracted from main index.html)
- Applies fact-check fixes: no fabricated numbers, honest question-bank labeling.
"""
import json, re, html as htmllib

REF = '/home/hatch/workspace/user/files/portfolio-ui-reference.html'
P = json.load(open('neo/projects.json', encoding='utf-8'))
html = open(REF, encoding='utf-8').read()

def esc(s):
    return htmllib.escape(s, quote=True)

# ---------------------------------------------------------------- links
def extract_links():
    src = open('/home/hatch/workspace/portfolio-site/index.html', encoding='utf-8').read()
    items = re.findall(r'<li class="project-item[^"]*"[^>]*>.*?</li>', src, re.S)
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

# ---------------------------------------------------------------- fact-checked archive data
# key: substring of title_zh -> (category, type_label, desc_zh, desc_en)
ARCHIVE = [
 ("Personal Opportunity Intelligence", "ai", "AI / AUTOMATION",
  "每天自动从几十个信息源里筛出值得看的内容和机会，推送到手机上。",
  "Filters dozens of feeds daily and pushes worthwhile reads and opportunities to your phone."),
 ("LifeOS", "ai", "AI / KNOWLEDGE",
  "帮你管目标、记日志的个人系统，还能定时自动生成复盘报告。",
  "A personal system for goals and journaling that auto-generates periodic review reports."),
 ("Hermes", "ai", "LINUX / OPS",
  "一台 24 小时在线的云服务器，替我跑定时任务：抓晨报、盯持仓、巡检服务器。",
  "A 24/7 cloud server running scheduled jobs: morning digests, portfolio watch, health checks."),
 ("Linux 工作站", "linux", "LINUX / INFRA",
  "自己动手搭的开发环境：主力机 Arch Linux + Debian 云服务器，配好域名解析、CDN 和证书自动化。",
  "Hand-built dev environment: Arch Linux workstation plus Debian VPS, with DNS, CDN and auto TLS."),
 ("银行从业", "web", "WEB / LEARNING",
  "银行从业刷题网站：710 道题（2 套真题 + 回忆版/改编/自编题），错题自动生成 Anki 记忆卡片。",
  "Banking exam practice site: 710 questions (2 real sets plus recalled, adapted and self-written items); wrong answers become Anki cards."),
 ("Whisper", "ai", "LINUX / AI",
  "Linux 上好用的全局语音输入法很少，所以自己做了一个：按快捷键说话就变成文字，模型常驻本地，无需联网。",
  "A rare thing on Linux — a system-wide voice input: hotkey, speak, text appears; model stays resident locally."),
 ("OBS", "linux", "LINUX / VIDEO",
  "调好了 Linux 下的推流：针对特定设备的解码与坐标问题做了配置规避，画面上可实时显示时间和待办。",
  "Tuned Linux streaming: config workarounds for device-specific decode and coordinate issues, with live overlays."),
 ("知识库同步桥", "ai", "AI / AUTOMATION",
  "让本地笔记软件和云端看板自动同步，两边改的内容都不丢。",
  "Keeps the local note app and cloud dashboard in sync — edits on either side are never lost."),
 ("TimeTracker", "linux", "LINUX / PYTHON",
  "自动记录每天在每个窗口上花了多少时间，生成日报，帮你看清时间去哪了。",
  "Tracks time per window automatically and generates a daily report of where your time goes."),
 ("Finance-Intel", "data", "DATA / FINANCE",
  "每天开盘前自动生成一份市场早报，行情异动就发提醒。",
  "Auto-generates a market morning brief before each trading day, with alerts on unusual moves."),
 ("WriteMap", "web", "WEB / EDUCATION",
  "写英语作文没人改？这个应用从词汇、语法、连贯性三个维度打分，告诉你弱在哪。",
  "No one to grade your English essays? This app scores vocabulary, grammar and coherence."),
 ("Gaokao", "data", "DATA / PYTHON",
  "抓了各大学历年的录取分数，做成干净表格，填志愿时一眼对比。",
  "Scraped historical university admission scores into clean tables for college-choice comparison."),
 ("被动式 AI 笔记", "archived", "ARCHIVED",
  "想到什么就给 Telegram 机器人发句话，它自动分类成任务或日记，同步到笔记软件。（已归档）",
  "Message the Telegram bot whatever is on your mind; it sorts messages into tasks or journal entries. (Archived)"),
 ("课程录音", "archived", "ARCHIVED",
  "上课录音丢进去，自动切分转成文字讲义归档。（已归档）",
  "Drop in lecture recordings; get them split, transcribed and archived as notes. (Archived)"),
 ("mc118", "linux", "OPS / NETWORK",
  "开了个百人 Minecraft 服务器，针对低带宽环境做了网络优化。",
  "Ran a 100-player Minecraft server, tuned for low-bandwidth environments."),
 ("WTF", "linux", "LINUX / TERMINAL",
  "在终端里一眼看到今天的目标进度，不用打开一堆软件。",
  "See today's goal progress at a glance inside the terminal."),
 ("Vitals", "web", "DATA / HEALTH",
  "把家人纸质体检报告变成电子档案，标出异常指标，方便对比历年变化。只做数据整理，不做医疗判断。",
  "Digitizes family paper checkup reports and flags abnormal indicators for comparison. Data organization only."),
 ("反指纹", "data", "PRIVACY / BROWSER",
  "浏览器隐私加固配置：屏蔽 WebRTC 泄漏、隔离 Canvas 指纹，减少网站跨站追踪。",
  "Browser privacy hardening: blocks WebRTC leaks, isolates canvas fingerprints, reduces cross-site tracking."),
 ("演示文稿", "web", "DESIGN",
  "承接商业 PPT 外包设计；兼职做过校园即时跑腿。",
  "Freelance commercial slide-deck design; part-time campus errand courier."),
 ("Minecraft 联机社区", "data", "NETWORK / COMMUNITY",
  "10 岁时从零运营起一个 100+ 人活跃的 Minecraft 玩家社区；自学宽带拨号和路由器端口映射解决联机问题。",
  "At age 10, grew and ran a 100+ player Minecraft community from scratch; self-taught networking to get everyone online."),
]

def find_proj(key):
    for p in P:
        if key in p['title_zh'] or key in p['title_en']:
            return p
    raise ValueError('no project for ' + key)

# ---------------------------------------------------------------- archive list
items_html = []
for i, (key, cat, typ, dzh, den) in enumerate(ARCHIVE, start=5):
    p = find_proj(key)
    links = LINKS.get(p['title_zh'], [])
    if links:
        typ0, url = links[0]
        label = '在线演示' if typ0 == 'demo' else 'GitHub'
        link = (f'<a class="archive-link" href="{esc(url)}" target="_blank" rel="noreferrer">'
                f'{esc(label)} <svg class="icon"><use href="#i-arrow-up-right"/></svg></a>')
    else:
        link = ('<span class="archive-link"><span data-zh="项目档案" data-en="Archive">项目档案</span> '
                '<svg class="icon"><use href="#i-arrow-up-right"/></svg></span>')
    items_html.append(
        f'''<article class="archive-item" data-category="{cat}"><span class="archive-index">{i:02d}</span>'''
        f'''<div><div class="archive-title">{esc(p['title_zh'])}</div>'''
        f'''<div class="archive-desc" data-zh="{esc(dzh)}" data-en="{esc(den)}">{esc(dzh)}</div></div>'''
        f'''<span class="archive-type">{esc(typ)}</span>{link}</article>''')

start = html.index('<div class="archive-list" id="archiveList">')
end = html.index('</div>\n  </section>', start) + len('</div>')
html = (html[:start] + '<div class="archive-list" id="archiveList">\n      '
        + '\n      '.join(items_html) + '\n    </div>' + html[end:])
print(f'archive: {len(items_html)} items injected')

# ---------------------------------------------------------------- case studies (bilingual, honest)
CASES = {
 "poi": {
  "zh": {"category": "AI / 工作流 / 01", "title": "Personal Opportunity Intelligence",
   "intro": "将分散在多个信息源中的机会整理成可筛选、可追踪的清单。重点是减少手动收集和重复浏览，而不是增加 AI 输出。",
   "problem": "奖学金、开源资助、竞赛与岗位信息分散在不同网站，需要反复搜索、核对资格并记录截止时间，信噪比很低。",
   "approach": "用 RSS / Atom 采集信息源，解析并去重条目，再按一组明确的规则维度加权评分；达到阈值的机会推送到 Telegram 和 Notion。",
   "steps": ["多源采集", "解析去重", "规则评分", "推送追踪"],
   "evidence": "待验证：信息源可用率、去重准确率、推送中被实际点开的比例。在系统性测量之前，不展示命中率。",
   "limits": "规则评分只是初筛，不代表对机会质量的判断；信息以官方原始页面为准；需要处理失效链接、过期机会和来源格式变化。",
   "tech": "Python · RSS / Atom · Telegram Bot · Notion API"},
  "en": {"category": "AI WORKFLOW / 01", "title": "Personal Opportunity Intelligence",
   "intro": "Collect scattered opportunities into a filterable, trackable list. The point is less manual searching, not more AI output.",
   "problem": "Scholarships, open-source grants, competitions and job posts live on different sites; checking eligibility and deadlines by hand is noisy and repetitive.",
   "approach": "Collect feeds via RSS/Atom, parse and dedupe entries, score them against explicit weighted rules; items above threshold go to Telegram and Notion.",
   "steps": ["Collect feeds", "Parse & dedupe", "Rule scoring", "Push & track"],
   "evidence": "To verify: feed availability, dedupe accuracy, share of pushed items actually opened. No hit-rate claims before systematic measurement.",
   "limits": "Rule scoring is a first pass, not a quality judgment; always check the official source page; handle dead links, expired items and feed format changes.",
   "tech": "Python · RSS / Atom · Telegram Bot · Notion API"}},
 "lifeos": {
  "zh": {"category": "AI / 知识库 / 02", "title": "Personal LifeOS (Project PAI)",
   "intro": "让 AI 记住长期目标与日志的个人系统：事实存数据库、语义走向量，定时生成复盘，而不是每次对话都从零开始。",
   "problem": "对话式 AI 随会话结束而遗忘，长期使用出现上下文漂移、多会话割裂；个人目标缺乏持续跟踪，复盘靠自觉。",
   "approach": "FastAPI 后端 + PostgreSQL 存规范事实 + Qdrant 存语义向量；检索优先于推理，定时任务触发复盘生成。",
   "steps": ["记录日志", "事实/向量检索", "生成复盘", "决策参考"],
   "evidence": "待验证：长期记忆对目标达成的实际帮助、检索准确率、复盘建议被采纳的比例。目前是个人使用的探索版本。",
   "limits": "涉及生活多领域数据，统一建模与长期预测仍是开放问题；这是个人工作流实验，不是通用方案。",
   "tech": "Python · FastAPI · PostgreSQL · Qdrant · LLM"},
  "en": {"category": "AI / KNOWLEDGE BASE / 02", "title": "Personal LifeOS (Project PAI)",
   "intro": "A personal system that gives AI long-term memory: facts in a database, semantics in vectors, scheduled reviews — no more starting from zero each chat.",
   "problem": "Conversational AI forgets when the session ends; long-term use drifts across sessions; personal goals get no continuous tracking.",
   "approach": "FastAPI backend, PostgreSQL for canonical facts, Qdrant for semantic vectors; retrieval before reasoning, scheduled review generation.",
   "steps": ["Log", "Fact/vector retrieval", "Generate review", "Decision reference"],
   "evidence": "To verify: whether long-term memory actually helps goal completion, retrieval accuracy, share of review suggestions adopted. Currently a personal exploratory build.",
   "limits": "Life data spans many domains; unified modeling and long-term prediction remain open problems. A personal workflow experiment, not a general solution.",
   "tech": "Python · FastAPI · PostgreSQL · Qdrant · LLM"}},
 "hermes": {
  "zh": {"category": "LINUX / 运维 / 03", "title": "Hermes 定时任务管家",
   "intro": "跑在云服务器上的定时任务管家：抓晨报、盯持仓、巡检服务器，异常时推送到手机。",
   "problem": "定时任务散落在各处，单脚本缺乏容错，出问题时没人知道；需要一台 24 小时在线的执行环境。",
   "approach": "Debian VPS 上用 Cron / Systemd 调度 18+ 个任务管线，Telegram Webhook 做异常报警；按战略、运维、实验、情报四个角色组织任务。",
   "steps": ["定时调度", "执行任务", "状态检查", "异常报警"],
   "evidence": "待验证：任务成功率统计、报警准确率（误报/漏报）。“18+ 个任务”是当前配置数量，不是性能指标。",
   "limits": "节点间靠文件系统与消息钩子交互，缺少统一事件总线；是个人运维方案，不是生产级调度平台。",
   "tech": "Debian · Cron / Systemd · Telegram Bot"},
  "en": {"category": "LINUX / OPS / 03", "title": "Hermes Job Butler",
   "intro": "A scheduled-job butler on a cloud server: morning digests, portfolio watch, health checks — alerts pushed to your phone.",
   "problem": "Cron jobs scattered everywhere with no fault tolerance; nobody notices when one breaks; needs a 24/7 execution environment.",
   "approach": "Debian VPS with Cron/Systemd scheduling 18+ pipelines, Telegram webhooks for anomaly alerts; jobs organized into strategy, ops, experiment and intel roles.",
   "steps": ["Schedule", "Execute", "Health check", "Alert"],
   "evidence": "To verify: job success-rate stats, alert accuracy (false/missed). “18+ jobs” is the current config count, not a performance claim.",
   "limits": "Nodes communicate via filesystem and message hooks; no unified event bus. A personal ops setup, not a production scheduler.",
   "tech": "Debian · Cron / Systemd · Telegram Bot"}},
 "infra": {
  "zh": {"category": "LINUX / 基建 / 04", "title": "Linux 工作站与 VPS",
   "intro": "自己动手搭建的日常开发环境：主力机 Arch Linux + Debian 云服务器，网络、域名、证书全套打通。",
   "problem": "希望脱离 Windows 生态，有一套自己完全掌控、安全可用的日常开发与云端工作环境。",
   "approach": "Arch Linux 做主力系统（Zen 内核调优），Debian VPS 跑云端服务；Cloudflare 管域名解析与 CDN；Let's Encrypt 证书自动化。",
   "steps": ["系统调优", "网络配置", "域名/CDN", "证书自动化"],
   "evidence": "这是环境搭建类工作，验证方式是“日常可用”：主力开发、云端任务、HTTPS 访问都跑在这套环境上。没有做过性能对比测试。",
   "limits": "早期靠人工逐行配置，现在用 AI 协助生成配置与排错；是个人工程积累，不是可复制的发行版方案。",
   "tech": "Arch Linux · Debian · Cloudflare · Let's Encrypt"},
  "en": {"category": "LINUX / INFRA / 04", "title": "Linux Workstation & VPS",
   "intro": "A hand-built daily dev environment: Arch Linux workstation plus Debian cloud server — network, DNS and certificates all wired up.",
   "problem": "Wanted out of the Windows ecosystem: a fully self-controlled, secure daily dev and cloud working environment.",
   "approach": "Arch Linux as daily driver (tuned Zen kernel), Debian VPS for cloud services; Cloudflare for DNS and CDN; automated Let's Encrypt certificates.",
   "steps": ["Tune system", "Configure network", "DNS/CDN", "Auto certificates"],
   "evidence": "This is environment work; verification is “daily usable”: dev work, cloud jobs and HTTPS all run on it. No comparative performance tests done.",
   "limits": "Early setup was manual line-by-line config, now AI-assisted; personal engineering accumulation, not a reproducible distro.",
   "tech": "Arch Linux · Debian · Cloudflare · Let's Encrypt"}},
}

CASE_JS = "const caseData=" + json.dumps(CASES, ensure_ascii=False) + ";"

old_case = re.search(r'const caseData=\{.*?\n\};\n', html, re.S)
assert old_case, 'caseData block not found'
html = html[:old_case.start()] + CASE_JS + '\n' + html[old_case.end():]
print('caseData replaced')

# ---------------------------------------------------------------- modal logic: bilingual render + re-render on toggle
old_modal = re.search(
    r'const modal=document\.getElementById\(\'caseModal\'\);.*?document\.getElementById\(\'langToggle\'\)\.addEventListener',
    html, re.S)
assert old_modal, 'modal JS block not found'

MODAL_JS = '''const modal=document.getElementById('caseModal'); const modalTitle=document.getElementById('modalTitle'); const modalEyebrow=document.getElementById('modalEyebrow'); const modalContent=document.getElementById('modalContent'); let previousFocus=null; let currentCase=null;
function renderCase(){const d=caseData[currentCase];if(!d)return;const t=d[lang]||d.zh;modalEyebrow.textContent=t.category;modalTitle.textContent=t.title;const L=lang==='zh'?['问题场景','实现方式','工作流程','值得补充的验证','限制与取舍','技术栈','这份案例基于现有项目介绍整理。“待验证”标注的是尚未系统测量的项目，不代表已完成的测试结果。','查看项目案例']:['Problem','Approach','Workflow','To verify','Limits & trade-offs','Stack','Case studies are compiled from existing project notes. Items marked “to verify” have not been systematically measured.','View case study'];modalContent.innerHTML=`<p class="modal-intro">${t.intro}</p><div class="case-grid"><section class="case-box"><h3><svg class="icon"><use href="#i-target"/></svg>${L[0]}</h3><p>${t.problem}</p></section><section class="case-box"><h3><svg class="icon"><use href="#i-wrench"/></svg>${L[1]}</h3><p>${t.approach}</p></section><section class="case-box full"><h3><svg class="icon"><use href="#i-git"/></svg>${L[2]}</h3><div class="case-flow">${t.steps.map((s,i)=>`${i?'<svg class="icon"><use href="#i-arrow-right"/></svg>':''}<span>${s}</span>`).join('')}</div></section><section class="case-box"><h3><svg class="icon"><use href="#i-chart"/></svg>${L[3]}</h3><p>${t.evidence}</p></section><section class="case-box"><h3><svg class="icon"><use href="#i-check"/></svg>${L[4]}</h3><p>${t.limits}</p></section><section class="case-box full"><h3><svg class="icon"><use href="#i-code"/></svg>${L[5]}</h3><p>${t.tech}</p></section></div><div class="honesty-note">${L[6]}</div>`;}
function openCase(key){if(!caseData[key])return;previousFocus=document.activeElement;currentCase=key;renderCase();modal.classList.add('open');document.body.style.overflow='hidden';document.getElementById('modalClose').focus()}
function closeCase(){modal.classList.remove('open');document.body.style.overflow='';currentCase=null;if(previousFocus)previousFocus.focus()}
document.querySelectorAll('.case-open').forEach(b=>b.addEventListener('click',()=>openCase(b.dataset.case)));document.getElementById('modalClose').addEventListener('click',closeCase);modal.addEventListener('click',e=>{if(e.target===modal)closeCase()});document.addEventListener('keydown',e=>{if(e.key==='Escape'&&modal.classList.contains('open'))closeCase()});
document.querySelectorAll('.filter').forEach(btn=>btn.addEventListener('click',()=>{document.querySelectorAll('.filter').forEach(b=>b.classList.toggle('active',b===btn));const f=btn.dataset.filter;document.querySelectorAll('.archive-item').forEach(item=>{item.hidden=f!=='all'&&!item.dataset.category.split(' ').includes(f)})}));
document.getElementById('themeToggle').addEventListener('click',()=>{document.body.classList.toggle('dark');const dark=document.body.classList.contains('dark');document.querySelector('#themeToggle use').setAttribute('href',dark?'#i-sun':'#i-moon');document.getElementById('themeToggle').setAttribute('aria-label',dark?'切换浅色模式':'切换深色模式')});
let lang='zh'; document.getElementById('langToggle').addEventListener'''
html = html[:old_modal.start()] + MODAL_JS + html[old_modal.end():]
print('modal JS replaced')

# ---------------------------------------------------------------- featured cards swap
# exam/whisper/obs -> lifeos/hermes/infra (keep poi)
def _card(idx, vlabel, vcode, flows, cat, status_zh, status_en, title, dzh, den, techs, case):
    units = []
    for icon, fzh, fen in flows:
        units.append(f'<div class="flow-unit"><svg class="icon"><use href="#{icon}"/></svg>'
                     f'<span data-zh="{fzh}" data-en="{fen}">{fzh}</span></div>')
    flow = ('<svg class="icon flow-arrow"><use href="#i-arrow-right"/></svg>').join(units)
    tech = ''.join(f'<span class="tech">{t}</span>' for t in techs)
    return (f'<article class="project-card"><div class="project-visual">'
            f'<div class="visual-label"><span>{vlabel}</span><span>{idx} / {vcode}</span></div>'
            f'<div class="visual-flow">{flow}</div><div class="visual-index">{idx}</div></div>'
            f'<div class="card-body"><div class="card-meta"><span class="category">{cat}</span>'
            f'<span class="status" data-zh="{status_zh}" data-en="{status_en}">{status_zh}</span></div>'
            f'<h3>{title}</h3><p data-zh="{dzh}" data-en="{den}">{dzh}</p>'
            f'<div class="techs">{tech}</div>'
            f'<button class="text-link case-open" data-case="{case}">'
            f'<span data-zh="查看项目案例" data-en="View case study">查看项目案例</span>'
            f'<svg class="icon"><use href="#i-arrow-right"/></svg></button></div></article>')

NEW_CARDS = {
 "exam": _card("02", "AI KNOWLEDGE", "LIFEOS",
    [("i-target", "记录目标", "Log goals"), ("i-database", "检索记忆", "Retrieve"), ("i-brain", "生成复盘", "Review")],
    "AI / KNOWLEDGE", "进行中", "Active", "Personal LifeOS (Project PAI)",
    "让 AI 记住长期目标与日志的个人系统：事实存数据库、语义走向量，定时生成复盘。",
    "A personal system that gives AI long-term memory: facts in a database, semantics in vectors, scheduled reviews.",
    ["Python", "FastAPI", "PostgreSQL", "Qdrant"], "lifeos"),
 "whisper": _card("03", "LINUX OPS", "HERMES",
    [("i-sliders", "定时调度", "Schedule"), ("i-check", "执行检查", "Run & check"), ("i-send", "异常报警", "Alert")],
    "LINUX / OPS", "运行中", "Running", "Hermes 定时任务管家",
    "云服务器上的定时任务管家：抓晨报、盯持仓、巡检服务器，异常推送到手机。",
    "A scheduled-job butler on a cloud server: morning digests, portfolio watch, health checks, alerts to your phone.",
    ["Debian", "Cron / Systemd", "Telegram Bot"], "hermes"),
 "obs": _card("04", "LINUX INFRA", "WORKSTATION",
    [("i-monitor", "主力机", "Workstation"), ("i-globe", "域名网络", "DNS & net"), ("i-check", "证书自动化", "Auto TLS")],
    "LINUX / INFRA", "持续维护", "Maintained", "Linux 工作站与 VPS",
    "自己动手搭的开发环境：Arch Linux 主力机 + Debian 云服务器，域名、CDN、证书全套打通。",
    "Hand-built dev environment: Arch Linux workstation plus Debian VPS \u2014 DNS, CDN and certificates all wired up.",
    ["Arch Linux", "Debian", "Cloudflare", "Let\u2019s Encrypt"], "infra"),
}
for oldkey, newcard in NEW_CARDS.items():
    pat = re.compile(r'<article class="project-card">(?:(?!</article>).)*?data-case="' + oldkey + r'".*?</article>', re.S)
    html, n = pat.subn(newcard, html, count=1)
    assert n == 1, f'card swap failed for {oldkey}'
    print(f'card swapped: {oldkey}')

# ---------------------------------------------------------------- featured card links
CARD_LINKS = {"poi": "Personal Opportunity Intelligence", "lifeos": "LifeOS",
              "hermes": "Hermes", "infra": "Linux 工作站"}
for key, titlekey in CARD_LINKS.items():
    p = find_proj(titlekey)
    links = LINKS.get(p['title_zh'], [])
    if not links:
        continue
    add = ''
    for typ, url in links:
        if typ == 'demo':
            add += (f'<a class="text-link" href="{esc(url)}" target="_blank" rel="noreferrer">'
                    '<span data-zh="在线演示" data-en="Live demo">在线演示</span>'
                    ' <svg class="icon"><use href="#i-arrow-up-right"/></svg></a> ')
        else:
            add += (f'<a class="text-link" href="{esc(url)}" target="_blank" rel="noreferrer">'
                    'GitHub <svg class="icon"><use href="#i-arrow-up-right"/></svg></a> ')
    pat = re.compile(r'(<button class="text-link case-open" data-case="' + key + r'">.*?</button>)', re.S)
    html, n = pat.subn(r'\1 ' + add.strip(), html, count=1)
    print(f'card {key}: links added ({n})')

# ---------------------------------------------------------------- footer PDF links
old_footer = '<footer class="wrap"><span>© 2026 F1are / Portfolio concept</span>'
assert old_footer in html
html = html.replace(old_footer,
    '<footer class="wrap"><span>© 2026 F1are / Portfolio</span>'
    '<span><a href="../portfolio.pdf" data-zh="PDF 简版" data-en="PDF (ZH)">PDF 简版</a>'
    ' · <a href="../portfolio_en.pdf" data-zh="PDF 英文版" data-en="PDF (EN)">PDF 英文版</a></span>')
print('footer PDF links added')

# ---------------------------------------------------------------- title + remove handoff notes
# ---------------------------------------------------------------- section note: drop "prototype" wording
html = html.replace(
  'data-zh="用图示先说明项目如何工作，再展开阅读问题、实现方式与验证结果。以下是视觉结构示例，实际数据应以项目测试为准。"',
  'data-zh="用图示先说明项目如何工作，再展开阅读问题、实现方式与验证结果；标注“待验证”的数据尚未系统测量。"')
html = html.replace(
  'data-en="Show how each project works at a glance, then explore the problem, implementation and evidence. This is a layout concept; real results should come from project tests."',
  'data-en="See how each project works at a glance, then explore the problem, implementation and evidence. Items marked \\u201cto verify\\u201d have not been systematically measured."')
print('section-note patched')

html = html.replace('<title>Portfolio UI Reference — F1are</title>',
                    '<title>李耀飞 (F1are) — 作品集 / Portfolio</title>')
html, n = re.subn(r'<details class="wrap handoff" id="handoffNotes">.*?</details>\s*', '', html, flags=re.S)
print(f'handoff removed ({n})')

# ---------------------------------------------------------------- lang toggle: re-render open modal
old_toggle = "document.getElementById('langToggle').setAttribute('aria-label',lang==='zh'?'Switch language':'切换语言')});"
assert old_toggle in html, 'lang toggle handler not found'
html = html.replace(old_toggle,
    "document.getElementById('langToggle').setAttribute('aria-label',lang==='zh'?'Switch language':'切换语言');if(currentCase)renderCase()});")
print('lang toggle patched for modal re-render')

# ---------------------------------------------------------------- write
open('neo/index.html', 'w', encoding='utf-8').write(html)
print(f'wrote neo/index.html ({len(html)} chars)')
