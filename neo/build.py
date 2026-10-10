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
 ("银行从业", "web", "WEB / LEARNING",
  "银行从业刷题网站：710 道练习题（基于教材考点与典型题型整理，含改编与自编题），错题自动生成 Anki 记忆卡片。",
  "Banking exam practice site: 710 practice questions compiled from textbook key points; wrong answers become Anki cards."),
 ("Whisper", "ai", "LINUX / AI",
  "Linux 上好用的全局语音输入法很少，所以自己做了一个：按快捷键说话就变成文字，模型常驻本地，无需联网。",
  "A rare thing on Linux — a system-wide voice input: hotkey, speak, text appears; model stays resident locally."),
 ("OBS", "linux", "LINUX / VIDEO",
  "调好了 Linux 下的推流：针对特定设备的解码与坐标问题做了配置规避，画面上可实时显示时间和待办。",
  "Tuned Linux streaming: config workarounds for device-specific decode and coordinate issues, with live overlays."),
 ("LifeOS", "ai", "AI / KNOWLEDGE",
  "帮你管目标、记日志的个人系统，还能定时自动生成复盘报告。",
  "A personal system for goals and journaling that auto-generates periodic review reports."),
 ("知识库同步桥", "ai", "AI / AUTOMATION",
  "让本地笔记软件和云端看板自动同步，两边改的内容都不丢。",
  "Keeps the local note app and cloud dashboard in sync — edits on either side are never lost."),
 ("TimeTracker", "linux", "LINUX / PYTHON",
  "自动记录每天在每个窗口上花了多少时间，生成日报，帮你看清时间去哪了。",
  "Tracks time per window automatically and generates a daily report of where your time goes."),
 ("Finance-Intel", "data", "DATA / FINANCE",
  "每天开盘前自动生成一份市场早报，行情异动就发提醒。",
  "Auto-generates a market morning brief before each trading day, with alerts on unusual moves."),
 ("Hermes", "ai", "LINUX / OPS",
  "一台 24 小时在线的云服务器，替我跑定时任务：抓晨报、盯持仓、巡检服务器。",
  "A 24/7 cloud server running scheduled jobs: morning digests, portfolio watch, health checks."),
 ("WriteMap", "web", "WEB / EDUCATION",
  "写英语作文没人改？这个应用从词汇、语法、连贯性三个维度打分，告诉你弱在哪。",
  "No one to grade your English essays? This app scores vocabulary, grammar and coherence."),
 ("Gaokao", "data", "DATA / PYTHON",
  "抓了各大学历年的录取分数，做成干净表格，填志愿时一眼对比。",
  "Scraped historical university admission scores into clean tables for college-choice comparison."),
 ("Linux 工作站", "linux", "LINUX / INFRA",
  "自己动手搭的开发环境：主力机 Arch Linux + Debian 云服务器，配好域名解析、CDN 和证书自动化。",
  "Hand-built dev environment: Arch Linux workstation plus Debian VPS, with DNS, CDN and auto TLS."),
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
 "exam": {
  "zh": {"category": "WEB / 学习工具 / 02", "title": "银行考试模拟系统",
   "intro": "为个人备考场景构建的浏览器端练习工具，把模拟答题、自动判分、金融计算器和错题复习放在一个流程里。",
   "problem": "市面刷题软件广告较多，部分题库的监管条文口径可能过时（如旧银保监会口径），且界面与 ATA 机考的倒计时、题号导航、专用计算器交互有差异。",
   "approach": "实现计时答题、题号导航、自动判分与 TVM 金融计算器；错题可导出为 Anki FSRS 复习卡。",
   "steps": ["模拟答题", "自动判分", "定位错题", "复习巩固"],
   "evidence": "待验证：题目与解析的人工抽检正确率、移动端交互测试、计时与判分边界测试。仅在实际统计后展示数量与正确率。",
   "limits": "题库共 710 道练习题，基于教材核心考点与典型题型整理，包含改编题与自编模拟题；官方考试不公开历年真题，这里不宣称为“历年真题”。",
   "tech": "Vanilla JavaScript · HTML / CSS · Anki / FSRS"},
  "en": {"category": "WEB / LEARNING TOOL / 02", "title": "Bank Exam Simulator",
   "intro": "A browser-based practice tool for personal exam prep: timed mock exams, auto-grading, financial calculators and wrong-answer review in one flow.",
   "problem": "Commercial practice apps carry ads, some question banks use outdated regulatory wording, and their UI differs from the ATA exam countdown, question navigator and calculator interactions.",
   "approach": "Timed practice, question navigation, auto-grading and TVM financial calculators; wrong answers export as Anki FSRS cards.",
   "steps": ["Mock exam", "Auto-grading", "Locate mistakes", "Review"],
   "evidence": "To verify: sampled question/answer accuracy, mobile interaction tests, timer and grading edge cases. Show counts and accuracy only after real measurement.",
   "limits": "710 practice questions compiled from textbook key points and typical patterns, including adapted and self-written mocks; the official exam does not release past papers, so these are not presented as such.",
   "tech": "Vanilla JavaScript · HTML / CSS · Anki / FSRS"}},
 "whisper": {
  "zh": {"category": "LINUX / 本地 AI / 03", "title": "Linux Whisper Input",
   "intro": "通过全局快捷键触发本地语音识别，把结果输入当前应用，减少切换窗口和重复加载模型的等待。",
   "problem": "在线转写依赖网络且有隐私顾虑；本地模型每次冷启动都要加载数 GB 权重，等待数秒会打断连续输入。",
   "approach": "模型常驻显存的后台服务；用 PipeWire 采集音频，VAD 裁切有效语音段；快捷键触发，Wayland 注入文本。",
   "steps": ["快捷键触发", "音频采集", "本地转写", "插入文本"],
   "evidence": "待验证：端到端延迟需要先定义测量口径（按键到文本出现）、记录设备型号与模型配置，再做多次实测；不把单次观察值当作稳定性能。",
   "limits": "依赖 NVIDIA GPU；长语音的分段策略、不同应用的输入兼容性仍需单独验证。",
   "tech": "Python · CTranslate2 · PipeWire · Wayland"},
  "en": {"category": "LINUX / LOCAL AI / 03", "title": "Linux Whisper Input",
   "intro": "Trigger local speech recognition with a global hotkey and insert the result into the current app — less window switching, no repeated model loads.",
   "problem": "Cloud transcription needs network and raises privacy concerns; loading multi-GB local models on every trigger stalls input for seconds.",
   "approach": "A resident service keeps the model in VRAM; audio via PipeWire, VAD trims speech segments; hotkey triggers, text injected through Wayland.",
   "steps": ["Hotkey trigger", "Audio capture", "Local transcription", "Insert text"],
   "evidence": "To verify: define end-to-end latency (hotkey to text appearing), record device and model config, then measure repeatedly; single observations are not stable performance.",
   "limits": "Requires NVIDIA GPU; long-speech segmentation and per-app input compatibility still need separate verification.",
   "tech": "Python · CTranslate2 · PipeWire · Wayland"}},
 "obs": {
  "zh": {"category": "LINUX / 故障排查 / 04", "title": "OBS 摄像头与画面叠加修复",
   "intro": "排查 Linux 推流环境中特定设备的摄像头解码、透明视频渲染与场景坐标问题，并做回归测试。",
   "problem": "特定设备上，MJPEG 采集遇到坏包曾触发 FFmpeg 解码异常；透明 WebM 的解码设置影响 alpha 通道；场景切换后叠加元素坐标可能偏移。",
   "approach": "改用 YUYV 4:2:2 原始像素采集，绕开原先出问题的 MJPEG 解码路径；调整透明视频解码方式；校正绝对/相对坐标；udev 禁用 USB 自动休眠；Lua 显示时间与待办。",
   "steps": ["摄像头采集", "调整解码配置", "校准叠加坐标", "回归测试"],
   "evidence": "待补充：摄像头型号、分辨率/帧率、连续推流测试时长与复现记录。没有测试记录前，不宣称“广播级画质”或“彻底免疫故障”。",
   "limits": "针对当前设备与已观察问题的配置规避，不保证消除所有 USB 传输、硬件或驱动故障；跨设备使用前需重新验证。",
   "tech": "OBS Studio · V4L2 · Lua · udev"},
  "en": {"category": "LINUX / TROUBLESHOOTING / 04", "title": "OBS Camera & Overlay Fixes",
   "intro": "Diagnose camera decoding, transparent-video rendering and scene-coordinate issues in a Linux streaming setup on specific hardware, then regression-test.",
   "problem": "On specific hardware, MJPEG capture hit decoder crashes on corrupt packets; transparent WebM decode settings affected the alpha channel; overlay coordinates could drift after scene switches.",
   "approach": "Switched to YUYV 4:2:2 raw capture to bypass the problematic MJPEG path; adjusted transparent-video decoding; corrected absolute/relative coordinates; disabled USB autosuspend via udev; Lua overlays for time and todos.",
   "steps": ["Capture", "Tune decode config", "Calibrate overlays", "Regression test"],
   "evidence": "To add: camera model, resolution/fps, soak-test duration and reproduction notes. No “broadcast-grade” or “immune to failures” claims without test records.",
   "limits": "Workarounds for observed issues on current hardware; does not guarantee against all USB, hardware or driver failures; re-verify on other devices.",
   "tech": "OBS Studio · V4L2 · Lua · udev"}},
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

# ---------------------------------------------------------------- featured card links
CARD_LINKS = {"poi": "Personal Opportunity Intelligence", "exam": "银行从业",
              "whisper": "Whisper", "obs": "OBS"}
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
