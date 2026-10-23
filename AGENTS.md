# AGENTS.md — 李耀飞 (F1are) 个人作品集与项目归档系统

> 本文件为本仓库（`lyf266.github.io`）在 Orca ADE 及各类智能体（Antigravity、Claude Code、Codex 等）环境下的**全局工程与内容规范（Constitution）**。
> 所有接手本项目的 Agent 必须严格遵守本规范中的架构约定、排版准则、事实核验红线与提交流程。

---

## 1. 项目定位与双轨架构 (Architecture & Structure)

本仓库是李耀飞（F1are）的官方个人站点与技术作品集归档，直接通过 GitHub Pages（`https://lyf266.github.io`）部署。采用**纯原生静态技术栈**（Zero-Framework: 纯 HTML5 / 现代 CSS / 原生 Vanilla JS），杜绝庞大的前端框架与黑盒打包器，保证极端轻量、秒开与高可维护性。

站点采用**双轨共存**模式：
1. **主站极简目录轨（Root Minimalist Directory）**：`index.html`
   - 定位：Web 1.0 目录美学与工程师终端纯粹质感，全屏收录全部个人软硬件/系统/AI 项目。
   - 核心功能：双语无缝切换、深浅色模式切换、标签即时多维筛选、抽屉式折叠卡片（含交互式架构流程图、核心痛点、工程方案、验证结果）、A4 两页打印版式优化。
2. **Neo 杂志编辑轨（Editorial Showcase）**：`neo/index.html`
   - 定位：现代深度案例杂志版（Editorial Layout），精选 4 个核心项目深度长图文案例（POI 智能感知、Personal LifeOS、Hermes 云端智能体矩阵、Linux 开发工作站与 VPS 基建）+ 可筛选的完整历史项目档案抽屉。
   - 数据基座：`neo/projects.json`（结构化项目数据库）与 `neo/build.py`（自动化构建与模板注入脚本）。
3. **独立 PDF 向量简历**：`portfolio.pdf`（中文 A4 简版）、`portfolio_en.pdf`（英文 A4 简版），可直接打印或下载。

---

## 2. 事实核验与表达红线 (Fact-Checking & Content Honesty)

所有面向公众与招聘官呈现的文案必须遵循**客观、严谨、可验证**原则，严禁 AI 生成式浮夸辞藻与虚构数据：

1. **绝对禁止虚构性能数据**：
   - 严禁编造未实测的压测结果、吞吐量或“提升 300%”等无依据数字；
   - 凡未做系统性基准测试的数据，必须明确标注“待验证”或“未系统测量”，杜绝以假乱真。
2. **银行从业考试模拟系统真题口径**：
   - 题库规模：**全量 710 题**。
   - **严格事实口径**：必须准确表述为“**2 套全国统考真题 + 历年考场回忆版 / 改编题 / 知识点自编题**”；
   - **红线**：严禁对外宣称为“全部 710 道均为泄露/真实统考原卷”。
3. **语音输入法硬件实测数据**：
   - 模型采用 CTranslate2 与 CUDA 上下文常驻显存，端到端快捷键呼出至文字上屏实测延迟约为 **~300ms**，完全离线无云端隐私泄露风险。
4. **窗口时间追踪器（Desktop TimeTracker）**：
   - 基于 Wayland KWin 脚本与 D-Bus 监听，后台守护进程常驻内存实测开销约为 **~13MB**。
5. **个人核心主攻方向文案锁定**：
   - 中文：`主攻: 发现问题并设计框架与约束，让 AI 解决问题`
   - 英文：`Focus: Problem Framing & Constraint Design · Directing AI Solutions`

---

## 3. 排版、字体与双语交互规范 (Typography & UI Guidelines)

1. **字体栈全局硬约束 (Typography Invariant)**：
   - **中文字体（EastAsian）**：必须优先采用思源黑体（`"Source Han Sans SC", "Noto Sans CJK SC", "Noto Sans SC"`），搭配系统备用字体；
   - **代码与等宽字体（Monospace）**：统一采用 `"JetBrains Mono", Consolas, Menlo, monospace`；
   - **字距与行距**：正文行高设定在 `1.25` 至 `1.6` 之间，中英文混排必须保持半角空格及严谨标点避头尾法则。
2. **双语完全对齐 (Bilingual Parity)**：
   - 页面中所有文本元素（主标题、副标题、项目名、标签、按钮、折叠卡片正文、弹窗详情等）必须完整具备 `data-zh` 和 `data-en` 属性，或在 JS 多语言字典对象中有完整键值对；
   - 切换语言时，严禁出现“部分中文未变”或“英文变成 undefined/空白”的断裂现象。
3. **深浅色主题无障碍对比度 (Theme Contrast & A11y)**：
   - 亮色模式：背景 `#FFFFFF`，主字 `#1A1A1A`，边框 `#E5E5E5`；
   - 暗色模式：背景 `#121212`，主字 `#E5E5E5`，次级字 `#C5C5C5`，边框 `#2A2A2A`；
   - 确保文本与背景在 WCAG AA 标准下对比度不低于 4.5:1，严禁暗色模式下出现不可读的“黑底灰字”或“白底白字”。
4. **响应式与移动端体验**：
   - 页面在 `375px`（手机）到 `1920px`（桌面宽屏）均需完美自适应；
   - 严禁出现意外水平横向滚动条（强制设置容器边界）；
   - 触控目标（按钮、标签、链接）尺寸在移动端不得小于 `44×44px`。
5. **外链安全性**：
   - 所有外部超链接（GitHub 源码、Demo 演示、外部参考等）必须带有 `target="_blank" rel="noopener noreferrer"`。

---

## 4. 本地开发、测试与验证工作流 (Dev & Verification Workflow)

### 常用命令

```bash
# 1. 启动本地静态服务器（推荐根目录预览）
python3 -m http.server 8000
# 或使用 bun / npx
# bunx serve .

# 2. 访问主站与 neo 子站
# 主站极简目录：http://localhost:8000/
# Neo 编辑部版：http://localhost:8000/neo/

# 3. 注意：neo/index.html 是当前线上经过完整编辑与调试的正式版本（~2900行），
# 包含丰富的深度案例卡片与双语模态框。若执行 neo/build.py，请先做好 git 备份，避免覆盖已精修的内容。
# python3 neo/build.py
```

### 交付前六重门禁自检 (Quality Gate Checklist)
在提交任何代码或合并分支前，必须逐一验证以下六项：
1. **多语言验证**：点击右上角 `[EN]` / `[中]` 切换，检查标题、标签、项目描述、展开详情抽屉是否全部无遗漏翻译；
2. **主题切换验证**：点击 `[☼]` / `[☽]` 切换，检查抽屉展开状态、架构图、卡片边框色彩对比度是否正常；
3. **交互折叠验证**：测试 `[详情 +]` / `[折叠 -]` 抽屉，检查展开动画、流程步骤图、指标栏是否布局对齐；
4. **标签筛选验证**：点击不同技术标签（`Python`, `linux`, `agent`, `Wayland` 等），确认过滤计数与高亮样式正确；
5. **打印与 PDF 预览**：按下 `Ctrl + P` 检查浏览器打印预览，确认 `@media print` 规则生效，无多余大面积背景色浪费墨水，两页排版整洁紧凑；
6. **无报错与无死链**：打开浏览器开发者工具 Console，确认无 JavaScript 异常，所有链接有效。

---

## 5. Orca ADE 与 Git 协作规范 (Orca Worktree & Branch Governance)

1. **主干保护与工作区隔离**：
   - `main` 分支是与线上 GitHub Pages 直连的生产分支，默认受保护；
   - 在 Orca ADE 中开展新功能探索、视觉改版或重构时，优先通过 `orca worktree create --name <feature-name>` 派生并行 Git Worktree；
   - 重大改动必须经过本地 `http.server` 浏览器实测并自检通过后，方可快进（Fast-Forward）或 PR 合并入 `main`。
2. **原子化 Commit 消息**：
   - 遵循清晰的动词前缀，如：
     - `feat: 新增 XXX 项目架构流程图与双语描述`
     - `fix: 修正银行从业真题口径与测算延迟数据`
     - `style: 优化暗色模式下抽屉卡片对比度`
     - `docs: 更新 AGENTS.md 规范`
