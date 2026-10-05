/* =============================================================================
 * TinUI 面板设计器
 * 纯 HTML + CSS + JavaScript 实现，语法对齐 TinUIXml.py 的“面板模式”
 * （<tinui layout='panel' root='...'> / <child ...> / <panel> / <control>）。
 *
 * 功能：
 *   · 左侧：面板与控件面板（点击或拖拽加入）
 *   · 中间：模拟窗口，按 TinUIPanel 的布局算法实时排布
 *   · 右侧：结构树（可选中被控件覆盖的面板）+ 属性（尺寸 size / 最小尺寸 min_size / 权重 weight / 序号 index / anchor 等）
 *   · 导出：生成可直接被 TinUIXml.loadxml() 解析的 XML
 * ========================================================================== */
(function () {
  "use strict";

  /* =========================================================================
   * 1. 元数据（与 TinUIXml.py / TinUIPanel.py 对齐）
   * ======================================================================= */
  const ROOT_TYPES = {
    expand: "expandpanel",
    vertical: "verticalpanel",
    horizon: "horizonpanel",
    card: "cardpanel",
  };
  const ROOT_LABELS = {
    expand: "扩展 expand",
    vertical: "纵向 vertical",
    horizon: "横向 horizon",
    card: "卡片 card",
  };

  // 与 TinUIXml.panel_attrs 保持一致（顺序即导出顺序）
  const PANEL_ATTR_ORDER = {
    expandpanel: ["padding", "min_width", "min_height", "bg", "bd", "line", "linew"],
    verticalpanel: ["padding", "spacing", "min_width", "min_height", "bg", "bd", "line", "linew"],
    horizonpanel: ["padding", "spacing", "min_width", "min_height", "bg", "bd", "line", "linew"],
    cardpanel: ["card_width", "card_height", "padding", "h_spacing", "v_spacing", "min_width", "bg", "bd", "line", "linew"],
    sash: ["bg", "bd", "line", "linew", "draggable"],
  };

  const PANELS = {
    // bg 一律留空：TinUIPanel 中 bg='' 即透明背景，
// 且 BasePanel 仅在 bg 非空时才绘制（fix_bg 直接 return），故不预设任何底色。
    expandpanel: {
      label: "扩展面板", desc: "单子项铺满",
      attrs: { padding: "0,0,0,0", min_width: "0", min_height: "0", bg: "", bd: "9", line: "", linew: "0" },
    },
    verticalpanel: {
      label: "纵向面板", desc: "子项上下排列",
      attrs: { padding: "0,0,0,0", spacing: "0", min_width: "0", min_height: "0", bg: "", bd: "9", line: "", linew: "0" },
    },
    horizonpanel: {
      label: "横向面板", desc: "子项左右排列",
      attrs: { padding: "0,0,0,0", spacing: "0", min_width: "0", min_height: "0", bg: "", bd: "9", line: "", linew: "0" },
    },
    cardpanel: {
      label: "卡片面板", desc: "网格排列",
      attrs: { card_width: "120", card_height: "80", padding: "0,0,0,0", h_spacing: "5", v_spacing: "5", min_width: "0", bg: "", bd: "9", line: "", linew: "0" },
    },
    sash: {
      label: "拉伸条", desc: "拖动分割",
      attrs: { bg: "", bd: "0", line: "", linew: "0", draggable: "true" },
    },
  };

  /* 控件分组：左侧控件面板按此顺序展示（对应 TinUI.add_* 中带 layout 的全部控件） */
  const CONTROL_GROUPS = [
    { title: "文本 Text", tags: ["title", "paragraph", "label", "link"] },
    { title: "按钮 Button", tags: ["button", "button2", "togglebutton", "menubutton", "segmentbutton", "barbutton", "checkbutton", "radiobutton", "radiobox", "pivot", "navigation", "breadcrumb"] },
    { title: "输入 Input", tags: ["entry", "passwordbox", "textbox", "combobox", "spinbox", "picker", "scalebar", "labels"] },
    { title: "显示 Display", tags: ["progressbar", "waitbar1", "waitbar3", "waitframe", "ratingbar", "onoff", "separate", "image", "table", "listbox", "listview", "treeview", "ui", "pipspager", "notebook", "expander"] },
  ];

  /* 全部控件。attrs 为默认导出的参数；其余参数可在右侧属性面板中自行添加。
     mock: true 表示该控件外观难以用 HTML 还原，画布中以「矩形 + 中心文本」代替。 */
  const CONTROLS = {
    /* 文本 */
    title: { label: "标题", desc: "大号强调文字", attrs: { text: "标题", anchor: "nw" } },
    paragraph: { label: "段落", desc: "自动换行的说明文字", attrs: { text: "段落文本", width: "200", anchor: "nw" } },
    label: { label: "标签", desc: "带底色的文字标签", attrs: { text: "标签", anchor: "nw" } },
    link: { label: "超链接", desc: "可点击的文本链接", attrs: { text: "链接", url: "", anchor: "nw" } },
    /* 按钮 */
    button: { label: "普通按钮", desc: "矩形按钮", attrs: { text: "Button", anchor: "nw" } },
    button2: { label: "圆角按钮", desc: "圆角 / 带图标按钮", attrs: { text: "Button", anchor: "nw" } },
    togglebutton: { label: "状态按钮", desc: "可切换按下状态", attrs: { text: "Toggle", anchor: "nw" } },
    menubutton: { label: "菜单按钮", desc: "点击弹出菜单", attrs: { text: "菜单", anchor: "nw" } },
    segmentbutton: { label: "分段按钮", desc: "一组互斥选项", attrs: { content: "('A', 'B', 'C')", anchor: "nw" } },
    barbutton: { label: "工具栏按钮", desc: "图标工具栏", attrs: { content: "(('返回', '\ue74e', None), ('设置', '\ue713', None))", anchor: "nw" } },
    checkbutton: { label: "复选框", desc: "可勾选的选项", attrs: { text: "复选项", anchor: "nw" } },
    radiobutton: { label: "单选框", desc: "纵向排列的单选组", attrs: { width: "160", choices: "('选项一', '选项二')", anchor: "nw" } },
    radiobox: { label: "单选框组", desc: "可横向换行的单选组", attrs: { content: "('选项一', '', '选项二')", anchor: "nw" } },
    pivot: { label: "枢轴导航", desc: "横向标题导航", attrs: { content: "(('标题一', 'tag1'), ('标题二', 'tag2'))", anchor: "nw" } },
    navigation: { label: "导航栏", desc: "汉堡式导航菜单", attrs: { content: "(('\ue790', 'Color'), ('\ue743', 'Geometry'))", anchor: "nw" } },
    breadcrumb: { label: "面包屑", desc: "层级路径导航", attrs: { root: "HOME", anchor: "nw" } },
    /* 输入 */
    entry: { label: "输入框", desc: "单行文本输入", attrs: { width: "160", anchor: "nw" } },
    passwordbox: { label: "密码框", desc: "掩码输入", attrs: { width: "160", anchor: "nw" } },
    textbox: { label: "文本框", desc: "多行文本输入", attrs: { width: "200", height: "100", text: "", anchor: "nw" } },
    combobox: { label: "下拉框", desc: "可输入的下拉选择", attrs: { width: "160", content: "('选项一', '选项二')", anchor: "nw" } },
    spinbox: { label: "选值框", desc: "上下箭头选值", attrs: { width: "120", data: "('1', '2', '3')", anchor: "nw" } },
    picker: { label: "滚动选择器", desc: "多列滚动选择", attrs: { data: "(('2022', '2023', '2024'), ('春', '夏', '秋', '冬'))", anchor: "nw" } },
    scalebar: { label: "调节条", desc: "连续数值调节", attrs: { width: "200", data: "(1, 2, 3, 4, 5)", start: "1", anchor: "nw" } },
    labels: { label: "标签集合", desc: "动态标签组", mock: true, attrs: { anchor: "nw" } },
    /* 显示 */
    progressbar: { label: "进度条", desc: "百分比进度", attrs: { width: "200", anchor: "nw" } },
    waitbar1: { label: "等待环", desc: "环形等待指示", attrs: { r: "20", anchor: "nw" } },
    waitbar3: { label: "等待条", desc: "条形等待指示", attrs: { width: "200", anchor: "nw" } },
    waitframe: { label: "等待框", desc: "占位等待区域", mock: true, attrs: { width: "300", height: "300", anchor: "nw" } },
    ratingbar: { label: "评分", desc: "星级评分", attrs: { num: "5", anchor: "nw" } },
    onoff: { label: "开关", desc: "布尔开关", attrs: { anchor: "nw" } },
    separate: { label: "分割线", desc: "横向 / 纵向分割", attrs: { width: "200", direction: "x", anchor: "center" } },
    image: { label: "图片", desc: "静态图片", mock: true, attrs: { width: "120", height: "90", anchor: "nw" } },
    table: { label: "表格", desc: "首行为表头的数据表", attrs: { data: "(('1', '2', '3'), ('a', 'b', 'c'))", minwidth: "100", anchor: "nw" } },
    listbox: { label: "列表框", desc: "可滚动文本列表", attrs: { width: "200", height: "120", data: "('a', 'b', 'c')", anchor: "nw" } },
    listview: { label: "图片列表", desc: "纵向图片列表", mock: true, attrs: { width: "300", height: "240", anchor: "nw" } },
    treeview: { label: "树状图", desc: "可展开的多级树", attrs: { width: "200", height: "300", content: "(('one', ('1', '2', '3')), 'two', ('three', ('a', ('b', ('b1', 'b2', 'b3')), 'c')), 'four')", anchor: "nw" } },
    ui: { label: "子画布", desc: "可滚动的子 BasicTinUI", mock: true, attrs: { width: "200", height: "160", anchor: "nw" } },
    pipspager: { label: "画布翻页器", desc: "子画布翻页浏览", mock: true, attrs: { width: "200", height: "160", anchor: "nw" } },
    notebook: { label: "标签容器", desc: "多标签页容器", attrs: { width: "360", height: "240", anchor: "nw" } },
    expander: { label: "折叠面板", desc: "可展开 / 折叠的内容块", attrs: { width: "200", height: "120", title: "展开内容", anchor: "nw" } },
  };

  const ANCHORS = ["nw", "n", "ne", "e", "se", "s", "sw", "w", "center"];
  // pivot 画布字号，需与 styles.css 中 .c-piv 的 font-size 保持一致
  const PIVOT_FONT = 11;
  // expandpanel 的子控件会被拉伸填满（对齐 TinUI 中 layout(..., expand=True) 的行为）
  const STRETCHABLE = new Set([
    "button", "button2", "label", "entry", "passwordbox", "separate", "scalebar",
    "progressbar", "textbox", "listbox", "listview", "ui", "pipspager", "notebook",
    "waitbar3", "waitframe", "labels",
  ]);
  const NUMBER_ATTRS = new Set(["bd", "linew", "spacing", "min_width", "min_height", "card_width", "card_height", "h_spacing", "v_spacing"]);

  const ATTR_LABELS = {
    padding: "内边距 padding", spacing: "间距 spacing", min_width: "最小宽 min_width",
    min_height: "最小高 min_height", card_width: "卡片宽 card_width",
    card_height: "卡片高 card_height", h_spacing: "横向间距 h_spacing",
    v_spacing: "纵向间距 v_spacing", bg: "背景 bg", bd: "圆角 bd", line: "线色 line",
    linew: "线宽 linew", draggable: "可拖动 draggable", margin: "外边距 margin",
  };

  /* =========================================================================
   * 2. 运行时状态
   * ======================================================================= */
  let state = { root: null, selectedId: null, canvasW: 840, canvasH: 560 };
  let idSeq = 1;
  const collapsed = new Set();
  let drag = null;
  let toastTimer = null;
  const els = {};

  /* =========================================================================
   * 3. 工具函数
   * ======================================================================= */
  function num(v, d) {
    const n = parseFloat(v);
    if (isNaN(n)) return d == null ? 0 : d;
    return n;
  }
  function trimNum(n) {
    if (typeof n !== "number") return String(n);
    if (Number.isInteger(n)) return String(n);
    return String(Math.round(n * 1000) / 1000);
  }
  /* 估算文本像素宽度：中日韩等全角字符按字号计，半角字符按 0.55 字号计 */
  function textWidth(s, size) {
    let w = 0;
    const str = String(s == null ? "" : s);
    for (let i = 0; i < str.length; i++) {
      w += str.charCodeAt(i) > 0x2e80 ? size : size * 0.55;
    }
    return w;
  }
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
  function xmlEscape(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function attrVal(v) {
    const s = xmlEscape(v);
    if (s.indexOf("'") >= 0 && s.indexOf('"') < 0) return '"' + s + '"';
    if (s.indexOf("'") >= 0) return '"' + s.replace(/'/g, "&apos;") + '"';
    return "'" + s + "'";
  }
  function attrStr(name, v) {
    return " " + name + "=" + attrVal(v);
  }
  function deepCopy(o) {
    return JSON.parse(JSON.stringify(o));
  }
  function newId() {
    return "n" + (idSeq++);
  }
  function newNode(kind, tag, attrs) {
    return {
      id: newId(), kind: kind, tag: tag, name: "",
      attrs: Object.assign({}, attrs || {}),
      _size: null, _minSize: 0, _weight: 0, _index: null,
      _rect: null, _cell: null, _depth: 0,
      children: [],
    };
  }
  function parsePadding(v) {
    const p = String(v == null ? "" : v).split(/[,\s]+/).filter(function (s) { return s !== ""; }).map(Number);
    if (p.length === 0) return [0, 0, 0, 0];
    if (p.length === 1) return [p[0], p[0], p[0], p[0]];
    if (p.length === 2) return [p[0], p[1], p[0], p[1]];
    if (p.length === 3) return [p[0], p[1], p[2], p[1]];
    return [p[0] || 0, p[1] || 0, p[2] || 0, p[3] || 0];
  }
  function normalizePadding(v) {
    // TinUIPanel 要求 padding 恰好 4 个值（top,right,bottom,left）
    const p = String(v == null ? "" : v).split(/[,\s]+/).filter(function (s) { return s !== ""; }).map(function (s) { return trimNum(Math.round(num(s, 0))); });
    let a;
    if (p.length === 0) a = ["0", "0", "0", "0"];
    else if (p.length === 1) a = [p[0], p[0], p[0], p[0]];
    else if (p.length === 2) a = [p[0], p[1], p[0], p[1]];
    else if (p.length === 3) a = [p[0], p[1], p[2], p[1]];
    else a = [p[0], p[1], p[2], p[3]];
    return a.join(",");
  }
  function parseTuple(v) {
    if (v == null || v === "") return [];
    if (Array.isArray(v)) return v;
    try {
      const r = Function('"use strict";return(' + pyToJs(v) + ");")();
      if (r == null) return [];
      if (typeof r === "number" || typeof r === "boolean") return [r];
      if (typeof r === "string") return r.split(",");
      return Array.prototype.slice.call(r);
    } catch (e) {
      return String(v).replace(/[()'"]/g, "").split(",").map(function (s) { return s.trim(); }).filter(Boolean);
    }
  }
  /* Python 字面量转 JS：None/True/False 替换、元组 (…) 转列表 […]，
     引号内的内容原样保留（XML 中 content/data 等参数按 Python 字面量书写） */
  function pyToJs(v) {
    const s = String(v);
    let out = "";
    let quote = "";
    let i = 0;
    while (i < s.length) {
      const c = s[i];
      if (quote) {
        out += c;
        if (c === "\\") { out += s[i + 1] || ""; i += 2; continue; }
        if (c === quote) quote = "";
        i += 1;
        continue;
      }
      if (c === "'" || c === '"') { quote = c; out += c; i += 1; continue; }
      if (c === "(") { out += "["; i += 1; continue; }
      if (c === ")") { out += "]"; i += 1; continue; }
      const tail = s.slice(i);
      if (/^None\b/.test(tail)) { out += "null"; i += 4; continue; }
      if (/^True\b/.test(tail)) { out += "true"; i += 4; continue; }
      if (/^False\b/.test(tail)) { out += "false"; i += 5; continue; }
      out += c;
      i += 1;
    }
    return out;
  }
  function panelType(node) {
    if (!node) return "";
    return node.kind === "root" ? (ROOT_TYPES[node.attrs.root] || "expandpanel") : node.tag;
  }
  /* 把 content / data 一类的元组转成字符串列表；index 指定取二元组的第几项 */
  function tupleTexts(v, index) {
    return parseTuple(v).map(function (item) {
      if (Array.isArray(item)) {
        const it = index == null ? item[0] : item[index];
        return String(it == null ? "" : it);
      }
      return String(item == null ? "" : item);
    });
  }
  /* content 中的空串表示换行 → 二维字符串列表（radiobox / pivot 共用） */
  function tupleRows(v) {
    const rows = [];
    let cur = [];
    tupleTexts(v).forEach(function (c) {
      if (c === "") {
        if (cur.length) { rows.push(cur); cur = []; }
        return;
      }
      cur.push(c);
    });
    if (cur.length) rows.push(cur);
    return rows;
  }
  /* 表格数据：二维列表 */
  function tableRows(v) {
    const d = parseTuple(v);
    if (!Array.isArray(d) || d.length === 0) return [["1", "2", "3"], ["a", "b", "c"]];
    return d.map(function (row) { return Array.isArray(row) ? row : [row]; });
  }
  /* 树状图数据：(标题, (子项...)) 可嵌套，纯字符串为叶子 */
  function treeRows(v) {
    const list = parseTuple(v);
    if (!list.length) return [{ label: "(树状图)", children: [], open: false }];
    return list.map(function (item) {
      if (Array.isArray(item)) {
        return {
          label: String(item[0] == null ? "" : item[0]),
          children: treeRows(item.slice(1)),
          open: true,
        };
      }
      return { label: String(item == null ? "" : item), children: [], open: false };
    });
  }
  /* 树状图递归渲染：带展开箭头与缩进竖线；仅顶层首项标为选中 */
  function treeHtml(rows, top) {
    return rows.map(function (row, i) {
      const sign = row.children.length
        ? '<span class="c-tree-sign' + (row.open ? " open" : "") + '">' + (row.open ? "▾" : "▸") + "</span>"
        : '<span class="c-tree-sign"></span>';
      const kids = row.children.length
        ? '<span class="c-tree-kids">' + treeHtml(row.children, false) + "</span>"
        : "";
      const on = top && i === 0 ? " on" : "";
      return '<span class="c-tree-row' + on + '">' + sign + esc(row.label) + kids + "</span>";
    }).join("");
  }
  /* 树状图展平后的行数与最大层级，用于估算固有尺寸 */
  function treeMetrics(rows, depth) {
    depth = depth || 0;
    let count = 0, maxDepth = 0;
    rows.forEach(function (r) {
      count += 1;
      maxDepth = Math.max(maxDepth, depth);
      const m = treeMetrics(r.children, depth + 1);
      count += m.count;
      maxDepth = Math.max(maxDepth, m.maxDepth);
    });
    return { count: count, maxDepth: maxDepth };
  }
  function findNode(id, node) {
    node = node || state.root;
    if (!node) return null;
    if (node.id === id) return node;
    for (let i = 0; i < node.children.length; i++) {
      const r = findNode(id, node.children[i]);
      if (r) return r;
    }
    return null;
  }
  function findParent(id) {
    let result = null;
    (function walk(node) {
      for (let i = 0; i < node.children.length; i++) {
        if (node.children[i].id === id) { result = node; return; }
        walk(node.children[i]);
        if (result) return;
      }
    })(state.root);
    return result;
  }
  function pathTo(id) {
    const out = [];
    (function walk(node, stack) {
      stack.push(node);
      if (node.id === id) { out.push.apply(out, stack); return true; }
      for (let i = 0; i < node.children.length; i++) {
        if (walk(node.children[i], stack)) return true;
      }
      stack.pop();
      return false;
    })(state.root, []);
    return out;
  }
  function displayName(node) {
    if (!node) return "";
    if (node.kind === "root") return "tinui";
    if (node.kind === "panel") return (PANELS[node.tag] && PANELS[node.tag].label) || node.tag;
    return node.name || node.tag;
  }

  /* =========================================================================
   * 4. 布局引擎（对齐 TinUIPanel.update_layout 的行为）
   * ======================================================================= */
  function layoutAll() {
    const W = state.canvasW;
    const H = state.canvasH;
    const margin = Math.max(0, num(state.root.attrs.margin, 5));
    layoutPanel(state.root, { x: margin, y: margin, w: Math.max(0, W - margin * 2), h: Math.max(0, H - margin * 2) }, 0);
  }

  function inset(rect, pad) {
    return {
      x: rect.x + pad[3],
      y: rect.y + pad[0],
      w: Math.max(0, rect.w - pad[1] - pad[3]),
      h: Math.max(0, rect.h - pad[0] - pad[2]),
    };
  }

  function layoutPanel(node, rect, depth) {
    node._depth = depth;
    const type = panelType(node);

    if (type === "cardpanel") { layoutCard(node, rect, depth); return; }

    node._rect = rect;
    if (type === "sash") return;

    const pad = parsePadding(node.attrs.padding);
    const minW = num(node.attrs.min_width, 0);
    const minH = num(node.attrs.min_height, 0);
    const content = inset(rect, pad);
    content.w = Math.max(content.w, minW);
    content.h = Math.max(content.h, minH);

    if (type === "expandpanel") {
      const child = node.children[0];
      if (child) layoutChild(child, content, true, depth + 1);
      return;
    }

    const vertical = type === "verticalpanel";
    const spacing = num(node.attrs.spacing, 0);
    const kids = node.children;
    const last = kids.length - 1;

    let totalWeight = 0;
    let fixed = 0;
    const items = kids.map(function (child, i) {
      const sp = i < last ? spacing : 0;
      let size = child._size;
      if (size == null || size <= 0) size = naturalMain(child, vertical);
      const minS = child._minSize || 0;
      const weight = child._weight || 0;
      if (weight > 0) totalWeight += weight;
      else fixed += Math.max(size, minS) + sp;
      return { child: child, size: size, minS: minS, weight: weight, sp: sp };
    });

    const avail = vertical ? content.h : content.w;
    const remaining = Math.max(0, avail - fixed);
    let cur = vertical ? content.y : content.x;
    const end = vertical ? content.y + content.h : content.x + content.w;

    for (let i = 0; i < items.length; i++) {
      const it = items[i];
      let actual;
      if (it.weight > 0 && totalWeight > 0) actual = Math.max(remaining * it.weight / totalWeight, it.minS);
      else actual = Math.max(it.size, it.minS);
      // 与 TinUIPanel 一致：子项矩形超出内容区时截断，但位置仍按真实尺寸推进
      const stop = Math.min(cur + actual, end);
      const cell = vertical
        ? { x: content.x, y: cur, w: content.w, h: Math.max(0, stop - cur) }
        : { x: cur, y: content.y, w: Math.max(0, stop - cur), h: content.h };
      layoutChild(it.child, cell, false, depth + 1);
      cur += actual + it.sp;
      if (cur >= end) break;
    }
  }

  function layoutCard(node, rect, depth) {
    node._depth = depth;
    const pad = parsePadding(node.attrs.padding);
    const cw = Math.max(1, num(node.attrs.card_width, 100));
    const ch = Math.max(1, num(node.attrs.card_height, 100));
    const hs = num(node.attrs.h_spacing, 5);
    const vs = num(node.attrs.v_spacing, 5);
    const contentX = rect.x + pad[3];
    const contentY = rect.y + pad[0];
    const contentW = Math.max(0, rect.w - pad[1] - pad[3]);
    const cols = Math.max(1, Math.floor((contentW + hs) / (cw + hs)));
    const n = node.children.length;
    const rows = n > 0 ? Math.ceil(n / cols) : 1;
    const totalH = rows * ch + Math.max(0, rows - 1) * vs;
    node._rect = { x: rect.x, y: rect.y, w: rect.w, h: totalH + pad[0] + pad[2] };
    for (let i = 0; i < n; i++) {
      const col = i % cols;
      const row = Math.floor(i / cols);
      const cell = {
        x: contentX + col * (cw + hs),
        y: contentY + row * (ch + vs),
        w: cw, h: ch,
      };
      layoutChild(node.children[i], cell, false, depth + 1);
    }
  }

  function layoutChild(child, cell, expand, depth) {
    child._depth = depth;
    child._cell = cell;
    if (child.kind !== "control") {
      layoutPanel(child, cell, depth);
      return;
    }
    const nat = naturalSize(child);
    let w = nat[0], h = nat[1];
    const stretch = expand && STRETCHABLE.has(child.tag);
    if (stretch) { w = cell.w; h = cell.h; }
    const anchor = stretch ? "nw" : (expand ? "center" : (child.attrs.anchor || "nw"));
    child._rect = placeWithin(cell, w, h, anchor);
  }

  function placeWithin(cell, w, h, anchor) {
    let x = cell.x, y = cell.y;
    switch (anchor) {
      case "nw": x = cell.x; y = cell.y; break;
      case "n": x = cell.x + (cell.w - w) / 2; y = cell.y; break;
      case "ne": x = cell.x + cell.w - w; y = cell.y; break;
      case "e": x = cell.x + cell.w - w; y = cell.y + (cell.h - h) / 2; break;
      case "se": x = cell.x + cell.w - w; y = cell.y + cell.h - h; break;
      case "s": x = cell.x + (cell.w - w) / 2; y = cell.y + cell.h - h; break;
      case "sw": x = cell.x; y = cell.y + cell.h - h; break;
      case "w": x = cell.x; y = cell.y + (cell.h - h) / 2; break;
      case "center": x = cell.x + (cell.w - w) / 2; y = cell.y + (cell.h - h) / 2; break;
      default: break;
    }
    return { x: x, y: y, w: Math.max(0, w), h: Math.max(0, h) };
  }

  function naturalSize(node, depth) {
    if (node.kind !== "control") return naturalPanelSize(node, depth);
    const a = node.attrs || {};
    const tag = node.tag;
    const text = String(a.text == null ? "" : a.text);
    const len = text.length;
    let w = 80, h = 26;
    switch (tag) {
      case "title": w = Math.max(40, len * 18 + 8); h = 30; break;
      case "paragraph": {
        w = Math.max(20, num(a.width, 200));
        const lines = Math.max(1, Math.ceil((len * 13 + 4) / Math.max(20, w)));
        h = lines * 22 + 4;
        break;
      }
      case "label": w = Math.max(30, len * 13 + 12); h = 24; break;
      case "link": w = Math.max(30, len * 13 + 6); h = 22; break;
      case "button": case "button2": case "togglebutton":
        w = Math.max(60, len * 14 + 30); h = 32; break;
      case "entry": case "passwordbox": w = Math.max(40, num(a.width, 160)); h = 32; break;
      case "checkbutton": w = Math.max(50, len * 13 + 34); h = 24; break;
      case "radiobutton": {
        const list = parseTuple(a.choices);
        const n = Math.max(1, list.length);
        w = Math.max(60, num(a.width, 160));
        h = n * 24 + 4;
        break;
      }
      case "onoff": w = 52; h = 26; break;
      case "progressbar": w = Math.max(40, num(a.width, 200)); h = 16; break;
      case "separate": {
        if (String(a.direction || "x") === "y") { w = 3; h = 120; }
        else { w = Math.max(20, num(a.width, 200)); h = 3; }
        break;
      }
      case "ratingbar": w = num(a.num, 5) * 24 + 6; h = 26; break;
      case "spinbox": w = Math.max(50, num(a.width, 120)); h = 32; break;
      case "scalebar": w = Math.max(60, num(a.width, 200)); h = 26; break;
      case "textbox": w = Math.max(60, num(a.width, 200)); h = Math.max(40, num(a.height, 100)); break;
      case "combobox": w = Math.max(60, num(a.width, 160)); h = 32; break;
      case "menubutton": w = Math.max(70, len * 14 + 76); h = 32; break;
      case "segmentbutton": {
        const list = tupleTexts(a.content);
        let mw = 20;
        for (let i = 0; i < list.length; i++) mw = Math.max(mw, list[i].length * 13 + 10);
        w = Math.max(40, (mw + 10) * Math.max(1, list.length) - 10);
        h = 30;
        break;
      }
      case "barbutton": {
        const n = Math.max(1, parseTuple(a.content).length);
        w = n * 34 + 8;
        h = 28;
        break;
      }
      case "breadcrumb": {
        w = Math.max(80, String(a.root == null ? "" : a.root).length * 9 + 76);
        h = 28;
        break;
      }
      case "navigation": {
        // 顶栏一个图标（font_height），下方每栏 font_height + scale(15) 间距，
        // 栏宽受 maxwidth 约束，故控件是竖长条而非横向累加
        const n = Math.max(1, parseTuple(a.content).length);
        const mx = num(a.maxwidth, 150);
        w = Math.max(60, mx);
        h = 20 + 15 + n * (20 + 15);
        break;
      }
      case "radiobox": {
        const list = tupleTexts(a.content);
        const padx = num(a.padx, 15);
        const pady = num(a.pady, 10);
        let rows = 1, cur = 0, widest = 0;
        list.forEach(function (s) {
          if (s === "") { rows += 1; cur = 0; return; }
          cur += 28 + padx;
          widest = Math.max(widest, cur);
        });
        w = Math.max(60, widest + 22);
        h = Math.max(24, rows * 24 + pady * 2 + 8);
        break;
      }
      case "pivot": {
        // 横向排列：每一项占 width + padx 横向推进，content 中的空串换行
        // （nowy = t_bbox[3] + pady，故行间距为 pady）
        const padx = num(a.padx, 10);
        const pady = num(a.pady, 10);
        const rows = tupleRows(a.content);
        let widest = 0;
        rows.forEach(function (row) {
          let rw = 0;
          row.forEach(function (s, i) {
            // 每项 = 文本宽 + 左右内边距 4 + 2px 提示线，取整到像素避免文字被裁切
            rw += Math.max(20, Math.ceil(textWidth(s, PIVOT_FONT)) + 6) + (i ? padx : 0);
          });
          widest = Math.max(widest, rw);
        });
        w = Math.max(40, widest + 2);
        // 每行 = 字号 11 * 1.2 + 上下内边距 5 + 2px 提示线
        h = Math.max(24, Math.max(1, rows.length) * 20 + Math.max(0, rows.length - 1) * pady);
        break;
      }
      case "picker": {
        // 控件本体只是一条按钮：宽度仅由 text 的 (标题, 宽度) 决定（与弹出的
        // 滚轮窗口同宽），高度即单行标题高度，均与 data 的行数无关
        const cols = Math.max(1, Math.min(2, parseTuple(a.data).length));
        const textw = [60, 100]; // add_picker 默认 text=(("year", 60), ("season", 100))
        w = 9; // TINUI_RADIUS_SMALL
        for (let i = 0; i < cols; i++) w += textw[i] + 3;
        h = 18;
        break;
      }
      case "waitbar1": { const r = num(a.r, 20); w = r * 2; h = r * 2; break; }
      case "waitbar3": w = Math.max(40, num(a.width, 200)); h = 8; break;
      case "waitframe": w = Math.max(60, num(a.width, 300)); h = Math.max(60, num(a.height, 300)); break;
      case "labels": w = 160; h = 80; break;
      case "image": w = Math.max(20, num(a.width, 120)); h = Math.max(20, num(a.height, 90)); break;
      case "listbox": w = Math.max(60, num(a.width, 200)); h = Math.max(40, num(a.height, 120)); break;
      case "listview": w = Math.max(60, num(a.width, 300)); h = Math.max(60, num(a.height, 240)); break;
      case "treeview": {
        const m = treeMetrics(treeRows(a.content));
        w = Math.max(80, num(a.width, 200));
        h = Math.max(60, num(a.height, m.count * 24 + 8));
        break;
      }
      case "ui": w = Math.max(60, num(a.width, 200)); h = Math.max(60, num(a.height, 160)); break;
      case "pipspager": w = Math.max(60, num(a.width, 200)); h = Math.max(60, num(a.height, 160)); break;
      case "notebook": w = Math.max(80, num(a.width, 360)); h = Math.max(60, num(a.height, 240)); break;
      case "expander": w = Math.max(60, num(a.width, 200)); h = Math.max(46, num(a.height, 120)); break;
      case "table": {
        const rows = tableRows(a.data);
        const minw = num(a.minwidth, 100);
        const cols = rows.reduce(function (m, r) { return Math.max(m, r.length); }, 1);
        let total = 0;
        for (let c = 0; c < cols; c++) {
          let cw = minw;
          rows.forEach(function (row) {
            if (row[c] != null) cw = Math.max(cw, String(row[c]).length * 13 + 10);
          });
          total += cw;
        }
        w = total + Math.max(0, cols - 1) * 2;
        h = Math.max(24, rows.length * 24 + 4);
        break;
      }
      default: break;
    }
    if (a.width != null && a.width !== "" &&
      tag !== "paragraph" && tag !== "radiobutton" && tag !== "separate") w = num(a.width, w);
    // picker 的 height 是弹出滚轮窗口的高度，与按钮本体无关，故不参与覆盖
    if (a.height != null && a.height !== "" && tag !== "combobox" && tag !== "picker") {
      h = num(a.height, h);
    }
    return [Math.max(1, w), Math.max(1, h)];
  }

  /* 面板的固有尺寸：由子项尺寸推出（对齐 TinUIPanel 中 _child_height / get_max_size 的思路） */
  function naturalPanelSize(node, depth) {
    depth = depth || 0;
    const pt = panelType(node);
    if (pt === "sash") {
      const s = Math.max(1, node._size || 0) || 100;
      return [s, s];
    }
    if (depth > 12) return [100, 100];
    const pad = parsePadding(node.attrs.padding);
    let cw = 0, ch = 0;
    if (pt === "cardpanel") {
      const cardW = Math.max(1, num(node.attrs.card_width, 100));
      const cardH = Math.max(1, num(node.attrs.card_height, 100));
      const n = Math.max(1, node.children.length);
      const cols = Math.max(1, Math.min(n, 4));
      const rows = Math.ceil(n / cols);
      cw = cols * cardW + (cols - 1) * num(node.attrs.h_spacing, 5);
      ch = rows * cardH + (rows - 1) * num(node.attrs.v_spacing, 5);
    } else if (pt === "expandpanel") {
      if (node.children[0]) {
        const s = naturalSize(node.children[0], depth + 1);
        cw = s[0];
        ch = s[1];
      }
    } else {
      const vertical = pt === "verticalpanel";
      const spacing = num(node.attrs.spacing, 0);
      const last = node.children.length - 1;
      let main = 0, cross = 0;
      node.children.forEach(function (c, i) {
        const s = naturalSize(c, depth + 1);
        main += Math.max(vertical ? s[1] : s[0], c._minSize || 0) + (i < last ? spacing : 0);
        cross = Math.max(cross, vertical ? s[0] : s[1]);
      });
      cw = vertical ? cross : main;
      ch = vertical ? main : cross;
    }
    const w = Math.max(cw + pad[1] + pad[3], num(node.attrs.min_width, 0));
    const h = Math.max(ch + pad[0] + pad[2], num(node.attrs.min_height, 0));
    return [Math.max(1, w), Math.max(1, h)];
  }

  function naturalMain(node, vertical) {
    const s = naturalSize(node);
    return vertical ? s[1] : s[0];
  }

  /* =========================================================================
   * 5. 渲染
   * ======================================================================= */
  function rerender(opts) {
    opts = opts || {};
    layoutAll();
    paintCanvas();
    paintOverlays();
    paintOutline();
    paintBreadcrumb();
    if (opts.props !== false) paintProps();
  }

  function select(id) {
    state.selectedId = id;
    rerender();
  }

  function paintCanvas() {
    els.canvas.innerHTML = "";
    const frag = document.createDocumentFragment();
    (function walk(node, depth) {
      frag.appendChild(buildNodeEl(node));
      for (let i = 0; i < node.children.length; i++) walk(node.children[i], depth + 1);
    })(state.root, 0);
    els.canvas.appendChild(frag);
  }

  function buildNodeEl(node) {
    const d = document.createElement("div");
    d.className = "pd-node " + (node.kind === "control" ? "pd-control" : "pd-panel");
    d.dataset.id = node.id;
    const r = node._rect || { x: 0, y: 0, w: 0, h: 0 };
    d.style.left = r.x + "px";
    d.style.top = r.y + "px";
    d.style.width = Math.max(0, r.w) + "px";
    d.style.height = Math.max(0, r.h) + "px";
    // 层级上限 900，确保始终低于导出弹窗（.modal z-index:2000）
    d.style.zIndex = String(Math.min(900, 10 + (node._depth || 0) * 4));
    if (node.kind === "control") {
      d.classList.add("pd-t-" + node.tag);
      d.innerHTML = controlInner(node);
    } else {
      applyPanelStyle(node, d);
    }
    if (node.id === state.selectedId) d.classList.add("pd-on");
    return d;
  }

  function applyPanelStyle(node, d) {
    const a = node.attrs;
    const bg = a.bg == null ? "" : String(a.bg);
    // bg 为空即透明，与 TinUIPanel 一致（BasePanel.fix_bg 在 bg 为空时不绘制任何图元）
    if (bg) d.style.background = bg;
    else d.classList.add("pd-nobg");
    // bd 是圆角大小（对应 BasePanel 的 create_polygon(width=bd)），不是边框宽度
    const bd = num(a.bd, 0);
    if (bd > 0) d.style.borderRadius = bd + "px";
    // line 是边框颜色、linew 是边框宽度
    const line = a.line == null ? "" : String(a.line);
    const linew = num(a.linew, 0);
    if (line && linew > 0) d.style.border = linew + "px solid " + line;
    // 拉伸条无背景时给一条可见的示意色，仅用于画布预览，不影响导出的 bg
    if (node.tag === "sash" && !bg) d.style.background = "#b9c3d4";
  }

  function controlInner(node) {
    const a = node.attrs;
    const tag = node.tag;
    const meta = CONTROLS[tag] || {};
    if (meta.mock) return '<span class="c-mock">' + esc(tag) + "</span>";
    const text = a.text == null ? "" : String(a.text);
    switch (tag) {
      case "title": return '<span>' + esc(text) + "</span>";
      case "paragraph": return '<span>' + esc(text) + "</span>";
      case "label": return '<span>' + esc(text) + "</span>";
      case "link": return '<span class="c-link">' + esc(text) + "</span>";
      case "button": case "button2": case "togglebutton":
        return "<span>" + esc(text) + "</span>";
      case "menubutton": return "<span>" + esc(text) + '</span><span class="c-caret">▾</span>';
      case "segmentbutton": {
        const list = tupleTexts(a.content);
        if (!list.length) return '<span class="c-mock">' + esc(tag) + "</span>";
        return list.map(function (c, i) {
          return '<span class="c-seg' + (i === 0 ? " on" : "") + '">' + esc(c) + "</span>";
        }).join("");
      }
      case "barbutton": {
        const list = tupleTexts(a.content);
        if (!list.length) return '<span class="c-mock">' + esc(tag) + "</span>";
        return list.map(function (c) {
          return '<span class="c-bbtn">' + esc(c || "•") + "</span>";
        }).join("");
      }
      case "breadcrumb": {
        const root = a.root == null ? "" : String(a.root);
        return '<span class="c-crumb">' + esc(root) + '</span>' +
          '<span class="c-crumb-sep">›</span><span class="c-crumb">子项</span>';
      }
      case "navigation": {
        // 固定示意三个栏目：顶栏汉堡图标 + 三行标题
        return '<span class="c-nav">' +
          '<span class="c-nav-bar"></span>' +
          '<span class="c-nav-item">Color</span>' +
          '<span class="c-nav-item">Geometry</span>' +
          '<span class="c-nav-item">Iconography</span>' +
          "</span>";
      }
      case "radiobox": {
        const rows = tupleRows(a.content);
        if (!rows.length) return '<span class="c-mock">' + esc(tag) + "</span>";
        return rows.map(function (row) {
          return '<span class="c-rb-row">' + row.map(function (c) {
            return '<span class="c-rb-cell">' + esc(c) + "</span>";
          }).join("") + "</span>";
        }).join("");
      }
      case "pivot": {
        // 横向排列，content 中的空串换行；首项默认选中（对应 sel_it(0, ...)）
        const rows = tupleRows(a.content);
        if (!rows.length) return '<span class="c-mock">' + esc(tag) + "</span>";
        return rows.map(function (row, ri) {
          return '<span class="c-piv-row">' + row.map(function (c, ci) {
            return '<span class="c-piv' + (ri === 0 && ci === 0 ? " on" : "") + '">' + esc(c) + "</span>";
          }).join("") + "</span>";
        }).join("");
      }
      case "picker": {
        // 只画按钮本体：每列显示当前选值（set_it 会把 texts 改写为所选值）
        const cols = parseTuple(a.data).map(function (col) { return Array.isArray(col) ? col : [col]; });
        const n = Math.max(1, Math.min(2, cols.length)); // 最多两列，与默认 text 对应
        const cells = [];
        for (let i = 0; i < n; i++) {
          const v = cols[i] && cols[i].length ? cols[i][0] : "";
          cells.push('<span class="c-pk-col">' + esc(String(v)) + "</span>");
        }
        return '<span class="c-picker">' + cells.join("") + "</span>";
      }
      case "entry": return '<span class="c-placeholder">请输入…</span>';
      case "passwordbox": return '<span class="c-placeholder">••••••</span>';
      case "checkbutton": return '<input type="checkbox" class="c-check"><span>' + esc(text) + "</span>";
      case "radiobutton": {
        let list = parseTuple(a.choices);
        if (!list.length) list = ["选项一", "选项二"];
        return list.map(function (c, i) {
          return '<span class="c-radio-row"><span class="c-radio' + (i === 0 ? " on" : "") + '"></span>' + esc(String(c)) + "</span>";
        }).join("");
      }
      case "onoff": return '<span class="c-switch"><span class="c-knob"></span></span>';
      case "progressbar": return '<span class="c-progress"><span class="c-progress-fill"></span></span>';
      case "waitbar1": return '<span class="c-ring"></span>';
      case "waitbar3": return '<span class="c-progress"><span class="c-progress-slide"></span></span>';
      case "separate": {
        return String(a.direction || "x") === "y"
          ? '<span class="c-separate c-separate-v"></span>'
          : '<span class="c-separate"></span>';
      }
      case "expander": {
        const t = a.title == null ? "展开内容" : String(a.title);
        return '<span class="c-exp-head">' + esc(t) + '<span class="c-caret">▾</span></span>' +
          '<span class="c-exp-body">内容区域</span>';
      }
      case "notebook": {
        return '<span class="c-nb-tabs"><span class="on">标签一</span><span>标签二</span></span>' +
          '<span class="c-nb-body"></span>';
      }
      case "table": {
        const rows = tableRows(a.data);
        let html = '<span class="c-table">';
        rows.forEach(function (row, ri) {
          html += '<span class="c-trow' + (ri === 0 ? " head" : "") + '">';
          row.forEach(function (cell) {
            html += '<span class="c-tcell">' + esc(String(cell == null ? "" : cell)) + "</span>";
          });
          html += "</span>";
        });
        return html + "</span>";
      }
      case "listbox": {
        const list = tupleTexts(a.data);
        const rows = list.length ? list : ["a", "b", "c"];
        return '<span class="c-list">' + rows.map(function (c, i) {
          return '<span class="c-list-row' + (i === 0 ? " on" : "") + '">' + esc(c) + "</span>";
        }).join("") + "</span>";
      }
      case "treeview": {
        return '<span class="c-tree">' + treeHtml(treeRows(a.content), true) + "</span>";
      }
      case "ratingbar": {
        const n = Math.max(1, Math.round(num(a.num, 5)));
        let s = "";
        for (let i = 0; i < n; i++) s += "★";
        return s;
      }
      case "spinbox": {
        const data = parseTuple(a.data);
        return "<span>" + esc(String(data[0] != null ? data[0] : "")) + '</span><span class="c-spin-btns">▲▼</span>';
      }
      case "scalebar": return '<span class="c-scale"><span class="c-scale-thumb"></span></span>';
      case "textbox": return '<span class="c-placeholder">文本内容…</span>';
      case "combobox": {
        const content = parseTuple(a.content);
        return '<span>' + esc(String(content[0] != null ? content[0] : "请选择")) + '</span><span class="c-caret">▾</span>';
      }
      default: return esc(text);
    }
  }

  function setBox(el, r) {
    el.style.left = r.x + "px";
    el.style.top = r.y + "px";
    el.style.width = Math.max(0, r.w) + "px";
    el.style.height = Math.max(0, r.h) + "px";
  }

  function paintOverlays() {
    const node = state.selectedId ? findNode(state.selectedId) : null;
    if (!node) { els.overlay.style.display = "none"; return; }
    els.overlay.style.display = "block";
    const r = node._rect || { x: 0, y: 0, w: 0, h: 0 };
    setBox(els.ovSel, r);

    const cell = node._cell;
    const showCell = cell && node.kind !== "root" && (
      Math.abs(cell.x - r.x) > 0.5 || Math.abs(cell.y - r.y) > 0.5 ||
      Math.abs(cell.w - r.w) > 0.5 || Math.abs(cell.h - r.h) > 0.5
    );
    if (showCell) { els.ovCell.style.display = "block"; setBox(els.ovCell, cell); }
    else els.ovCell.style.display = "none";

    const parent = findParent(node.id);
    let dir = null;
    if (parent) {
      const pt = panelType(parent);
      if (pt === "verticalpanel") dir = "v";
      else if (pt === "horizonpanel") dir = "h";
    }
    if (dir === "v" && cell) {
      els.ovHandleV.style.display = "block";
      els.ovHandleV.style.left = (cell.x + cell.w / 2 - 6) + "px";
      els.ovHandleV.style.top = (cell.y + cell.h - 6) + "px";
      els.ovHandleH.style.display = "none";
    } else if (dir === "h" && cell) {
      els.ovHandleH.style.display = "block";
      els.ovHandleH.style.left = (cell.x + cell.w - 6) + "px";
      els.ovHandleH.style.top = (cell.y + cell.h / 2 - 6) + "px";
      els.ovHandleV.style.display = "none";
    } else {
      els.ovHandleV.style.display = "none";
      els.ovHandleH.style.display = "none";
    }
  }

  function paintOutline() {
    els.outline.innerHTML = "";
    const tree = document.createElement("div");
    (function build(node, depth) {
      const row = document.createElement("div");
      row.className = "tree-row" + (node.id === state.selectedId ? " on" : "");
      row.style.paddingLeft = (5 + depth * 14) + "px";
      const isCollapsed = collapsed.has(node.id);
      const caret = node.children.length
        ? '<button class="tree-caret">' + (isCollapsed ? "▸" : "▾") + "</button>"
        : '<span class="tree-caret-space"></span>';
      const tagText = node.kind === "root" ? ("root=" + node.attrs.root) : node.tag;
      row.innerHTML = caret +
        '<span class="tree-name">' + esc(displayName(node)) + "</span>" +
        '<span class="tree-tag">' + esc(tagText) + "</span>";
      const caretEl = row.querySelector(".tree-caret");
      if (caretEl) {
        caretEl.addEventListener("click", function (e) {
          e.stopPropagation();
          if (collapsed.has(node.id)) collapsed.delete(node.id);
          else collapsed.add(node.id);
          paintOutline();
        });
      }
      row.addEventListener("click", function (e) {
        if (e.target.closest(".tree-caret")) return;
        select(node.id);
      });
      tree.appendChild(row);
      if (!isCollapsed) {
        for (let i = 0; i < node.children.length; i++) build(node.children[i], depth + 1);
      }
    })(state.root, 0);
    els.outline.appendChild(tree);
  }

  function paintBreadcrumb() {
    els.breadcrumb.innerHTML = "";
    if (!state.selectedId) {
      els.breadcrumb.innerHTML = '<span class="crumb-muted">未选中节点</span>';
      return;
    }
    const path = pathTo(state.selectedId);
    path.forEach(function (n, i) {
      if (i) {
        const sep = document.createElement("span");
        sep.className = "crumb-sep";
        sep.textContent = "›";
        els.breadcrumb.appendChild(sep);
      }
      const b = document.createElement("button");
      b.className = "crumb" + (n.id === state.selectedId ? " on" : "");
      b.textContent = displayName(n);
      b.addEventListener("click", function () { select(n.id); });
      els.breadcrumb.appendChild(b);
    });
  }

  /* ---------------- 属性面板 ---------------- */
  function section(title) {
    const s = document.createElement("div");
    s.className = "prop-section";
    if (title) {
      const h = document.createElement("h4");
      h.textContent = title;
      s.appendChild(h);
    }
    return s;
  }
  function note(text) {
    const d = document.createElement("div");
    d.className = "note";
    d.textContent = text;
    return d;
  }
  function numField(label, value, setter, opts) {
    opts = opts || {};
    const row = document.createElement("label");
    row.className = "row";
    const s = document.createElement("span");
    s.className = "row-label";
    s.textContent = label;
    const inp = document.createElement("input");
    inp.type = "number";
    inp.className = "row-input";
    inp.value = value == null ? "" : value;
    if (opts.min != null) inp.min = opts.min;
    if (opts.step != null) inp.step = opts.step;
    inp.addEventListener("input", function () { setter(inp.value); });
    row.appendChild(s); row.appendChild(inp);
    return row;
  }
  function textField(label, value, setter, opts) {
    opts = opts || {};
    const row = document.createElement("label");
    row.className = "row";
    const s = document.createElement("span");
    s.className = "row-label";
    s.textContent = label;
    const inp = document.createElement("input");
    inp.type = "text";
    inp.className = "row-input";
    inp.value = value == null ? "" : value;
    if (opts.placeholder) inp.placeholder = opts.placeholder;
    inp.addEventListener("input", function () { setter(inp.value); });
    row.appendChild(s); row.appendChild(inp);
    return row;
  }
  function selectField(label, value, options, setter, labels) {
    const row = document.createElement("label");
    row.className = "row";
    const s = document.createElement("span");
    s.className = "row-label";
    s.textContent = label;
    const sel = document.createElement("select");
    sel.className = "row-input";
    options.forEach(function (o) {
      const op = document.createElement("option");
      op.value = o;
      op.textContent = labels && labels[o] ? labels[o] : o;
      sel.appendChild(op);
    });
    sel.value = value;
    sel.addEventListener("change", function () { setter(sel.value); });
    row.appendChild(s); row.appendChild(sel);
    return row;
  }
  function colorField(label, value, setter) {
    const row = document.createElement("label");
    row.className = "row";
    const s = document.createElement("span");
    s.className = "row-label";
    s.textContent = label;
    const wrap = document.createElement("span");
    wrap.className = "color-wrap";
    const c = document.createElement("input");
    c.type = "color";
    c.className = "color-input";
    c.value = /^#[0-9a-fA-F]{6}$/.test(value || "") ? value : "#ffffff";
    const t = document.createElement("input");
    t.type = "text";
    t.className = "row-input";
    t.value = value == null ? "" : value;
    t.placeholder = "留空为透明";
    c.addEventListener("input", function () { t.value = c.value; setter(c.value); });
    t.addEventListener("input", function () {
      if (/^#[0-9a-fA-F]{6}$/.test(t.value)) c.value = t.value;
      setter(t.value);
    });
    wrap.appendChild(c); wrap.appendChild(t);
    row.appendChild(s); row.appendChild(wrap);
    return row;
  }
  function btn(text, fn, disabled, danger) {
    const b = document.createElement("button");
    b.className = "btn small" + (danger ? " danger" : "");
    b.textContent = text;
    b.disabled = !!disabled;
    b.addEventListener("click", fn);
    return b;
  }

  function paintProps() {
    els.props.innerHTML = "";
    if (!state.selectedId) {
      const e = document.createElement("div");
      e.className = "empty";
      e.innerHTML = "未选中任何节点<br><small>在画布或右侧结构树中选择</small>";
      els.props.appendChild(e);
      return;
    }
    const node = findNode(state.selectedId);
    if (!node) { state.selectedId = null; paintProps(); return; }

    const head = document.createElement("div");
    head.className = "prop-head";
    head.innerHTML = "<strong>" + esc(displayName(node)) + '</strong><span class="badge">' +
      esc(node.kind === "root" ? ("root=" + node.attrs.root) : node.tag) + "</span>";
    els.props.appendChild(head);

    if (node.kind === "root") els.props.appendChild(rootSection(node));

    const cons = constraintsSection(node);
    if (cons) els.props.appendChild(cons);

    if (node.kind !== "control") els.props.appendChild(panelAttrsSection(node));
    if (node.kind === "control") els.props.appendChild(controlSection(node));

    els.props.appendChild(actionsSection(node));
  }

  function constraintsSection(node) {
    const parent = findParent(node.id);
    if (!parent) return null;
    const pt = panelType(parent);
    const sec = section("布局约束（相对父面板）");
    if (pt === "verticalpanel" || pt === "horizonpanel") {
      sec.appendChild(numField("尺寸 size", node._size, function (v) {
        node._size = v === "" ? null : num(v, 0);
        rerender({ props: false });
      }, { min: 0, step: 1 }));
      sec.appendChild(numField("最小尺寸 min_size", node._minSize || "", function (v) {
        node._minSize = v === "" ? 0 : num(v, 0);
        rerender({ props: false });
      }, { min: 0, step: 1 }));
      sec.appendChild(numField("权重 weight", node._weight || "", function (v) {
        node._weight = v === "" ? 0 : num(v, 0);
        rerender({ props: false });
      }, { min: 0, step: 0.1 }));
      if (node._weight > 0) sec.appendChild(note("weight 大于 0 时按剩余空间分配，size 不生效；拖动选中框调整尺寸会自动将 weight 置 0。"));
    } else if (pt === "cardpanel") {
      sec.appendChild(note("卡片面板按网格自动排列，子项尺寸由 card_width / card_height 决定；用「上移 / 下移」调整顺序。"));
    } else if (pt === "expandpanel") {
      sec.appendChild(note("扩展面板的子项会自动铺满，无需设置尺寸。"));
    }
    return sec;
  }

  function panelAttrsSection(node) {
    const pt = panelType(node);
    const meta = PANELS[pt] || { attrs: {} };
    const order = PANEL_ATTR_ORDER[pt] || [];
    order.forEach(function (k) {
      if (!(k in node.attrs)) node.attrs[k] = meta.attrs[k] != null ? meta.attrs[k] : "";
    });
    const sec = section(node.kind === "root" ? "根面板属性" : "面板属性");
    order.forEach(function (k) {
      const label = ATTR_LABELS[k] || k;
      if (k === "draggable") {
        sec.appendChild(selectField(label, node.attrs[k], ["true", "false"], function (v) {
          node.attrs[k] = v;
          rerender({ props: false });
        }, { true: "可拖动 true", false: "不可拖动 false" }));
      } else if (k === "bg" || k === "line") {
        sec.appendChild(colorField(label, node.attrs[k], function (v) {
          node.attrs[k] = v;
          rerender({ props: false });
        }));
      } else if (k === "padding") {
        sec.appendChild(textField(label, node.attrs[k], function (v) {
          node.attrs[k] = v;
          rerender({ props: false });
        }, { placeholder: "上,右,下,左" }));
      } else if (NUMBER_ATTRS.has(k)) {
        sec.appendChild(numField(label, node.attrs[k], function (v) {
          node.attrs[k] = v === "" ? "0" : v;
          rerender({ props: false });
        }, { min: 0, step: 1 }));
      } else {
        sec.appendChild(textField(label, node.attrs[k], function (v) {
          node.attrs[k] = v;
          rerender({ props: false });
        }));
      }
    });
    return sec;
  }

  /* 控件属性：只保留设计器自身的排布项，不暴露控件构造参数 */
  function controlSection(node) {
    const sec = section("控件");
    sec.appendChild(textField("标签名 name", node.name, function (v) {
      node.name = v;
      paintOutline();
    }, { placeholder: "可选，对应 self.tags[...]" }));
    sec.appendChild(selectField("对齐 anchor", node.attrs.anchor || "nw", ANCHORS, function (v) {
      node.attrs.anchor = v;
      rerender({ props: false });
    }));
    sec.appendChild(note("控件构造参数固定为 " + node.tag + " 的默认值，如需调整请在导出后修改 XML。"));
    return sec;
  }

  function rootSection(node) {
    const sec = section("根设置");
    sec.appendChild(selectField("root 类型", node.attrs.root, Object.keys(ROOT_TYPES), function (v) {
      node.attrs.root = v;
      const pt = ROOT_TYPES[v];
      PANEL_ATTR_ORDER[pt].forEach(function (k) {
        if (!(k in node.attrs)) node.attrs[k] = PANELS[pt].attrs[k] != null ? PANELS[pt].attrs[k] : "";
      });
      if (v === "expand" && node.children.length > 1) {
        node.children = node.children.slice(0, 1);
        toast("expand 根只能保留一个子项");
      }
      rerender();
    }, ROOT_LABELS));
    sec.appendChild(numField("外边距 margin", node.attrs.margin, function (v) {
      node.attrs.margin = v === "" ? "0" : v;
      rerender({ props: false });
    }, { min: 0, step: 1 }));
    return sec;
  }

  function actionsSection(node) {
    const sec = section("");
    const parent = findParent(node.id);
    if (!parent) {
      sec.appendChild(note("根面板不可移动或删除。可在此调整 root 类型与画布外边距。"));
      return sec;
    }
    const row = document.createElement("div");
    row.className = "actions";
    const idx = parent.children.indexOf(node);
    row.appendChild(btn("上移", function () { moveNode(node, -1); }, idx === 0));
    row.appendChild(btn("下移", function () { moveNode(node, 1); }, idx === parent.children.length - 1));
    row.appendChild(btn("复制", function () { duplicateNode(node); }));
    row.appendChild(btn("删除", function () { deleteNode(node); }, false, true));
    sec.appendChild(row);
    return sec;
  }

  /* =========================================================================
   * 6. 编辑操作
   * ======================================================================= */
  function resolveContainerFrom(node) {
    if (!node) return { node: state.root };
    if (node.kind === "root" || node.kind === "panel") {
      if (node.tag === "sash") {
        const p = findParent(node.id);
        return p ? resolveContainerFrom(p) : { node: state.root };
      }
      let n = node;
      while (panelType(n) === "expandpanel") {
        if (n.children.length === 0) return { node: n };
        const c = n.children[0];
        if (c.kind === "control") return { error: "扩展面板只能包含一个子项（当前子项是控件）" };
        n = c;
      }
      return { node: n };
    }
    const p = findParent(node.id);
    return resolveContainerFrom(p);
  }

  function addNew(kind, tag, targetNode) {
    const res = resolveContainerFrom(targetNode);
    if (res.error) { toast(res.error); return; }
    const container = res.node;
    const pt = panelType(container);
    if (tag === "sash" && pt !== "verticalpanel" && pt !== "horizonpanel") {
      toast("拉伸条只能放入纵向 / 横向面板");
      return;
    }
    if (pt === "expandpanel" && container.children.length >= 1) {
      toast("扩展面板只能包含一个子项");
      return;
    }
    const meta = kind === "panel" ? PANELS[tag] : CONTROLS[tag];
    const node = newNode(kind, tag, deepCopy(meta.attrs));
    if (tag === "sash") node._size = 6;
    container.children.push(node);
    state.selectedId = node.id;
    rerender();
    toast("已添加：" + meta.label);
  }

  function deleteNode(node) {
    const p = findParent(node.id);
    if (!p) return;
    p.children.splice(p.children.indexOf(node), 1);
    state.selectedId = p.id;
    rerender();
  }

  function moveNode(node, dir) {
    const p = findParent(node.id);
    if (!p) return;
    const i = p.children.indexOf(node);
    const j = i + dir;
    if (j < 0 || j >= p.children.length) return;
    p.children.splice(i, 1);
    p.children.splice(j, 0, node);
    rerender();
  }

  function cloneNode(node) {
    const c = newNode(node.kind, node.tag, deepCopy(node.attrs));
    c.name = node.name;
    c._size = node._size;
    c._minSize = node._minSize;
    c._weight = node._weight;
    c._index = node._index;
    c.children = node.children.map(cloneNode);
    return c;
  }

  function duplicateNode(node) {
    const p = findParent(node.id);
    if (!p) return;
    const clone = cloneNode(node);
    p.children.splice(p.children.indexOf(node) + 1, 0, clone);
    state.selectedId = clone.id;
    rerender();
  }

  /* =========================================================================
   * 7. 导出 XML
   * ======================================================================= */
  function childAttrs(node) {
    let s = "";
    if (node._size != null && node._size > 0) s += attrStr("size", trimNum(node._size));
    if (node._minSize > 0) s += attrStr("min_size", trimNum(node._minSize));
    if (node._weight > 0) s += attrStr("weight", trimNum(node._weight));
    if (node._index != null) s += attrStr("index", trimNum(node._index));
    return s;
  }

  function panelAttrsXML(node) {
    const pt = panelType(node);
    const order = PANEL_ATTR_ORDER[pt] || [];
    let s = "";
    order.forEach(function (k) {
      if (!(k in node.attrs)) return;
      const v = k === "padding" ? normalizePadding(node.attrs[k]) : node.attrs[k];
      s += attrStr(k, v);
    });
    return s;
  }

  /* 控件参数固定为 CONTROLS 中声明的默认值，按声明顺序导出，空值省略 */
  function orderedControlAttrs(node) {
    const declared = (CONTROLS[node.tag] && CONTROLS[node.tag].attrs) || {};
    return Object.keys(declared).map(function (k) {
      const v = node.attrs[k];
      if (v === undefined || v === null) return "";
      if (String(v).trim() === "") return ""; // 空值等同 TinUI 默认，不导出
      return attrStr(k, v);
    }).join("");
  }

  function buildRootXML(node) {
    let s = "<tinui layout='panel'" + attrStr("root", node.attrs.root) + panelAttrsXML(node);
    // 暂不导出 animate / duration：当前 TinUIPanel 在根面板首次布局时
    // animate_layout 会先调用 get_rect()，此时背景多边形坐标不足而报错。
    if (node.attrs.margin != null && node.attrs.margin !== "") s += attrStr("margin", node.attrs.margin);
    if (node.children.length === 0) return s + "/>";
    s += ">\n";
    node.children.forEach(function (c) { s += buildChild(c, 1) + "\n"; });
    s += "</tinui>";
    return s;
  }

  function buildChild(node, indent) {
    const pad = "  ".repeat(indent);
    let s = pad + "<child" + childAttrs(node) + ">\n";
    s += buildNodeXML(node, indent + 1) + "\n";
    s += pad + "</child>";
    return s;
  }

  function buildNodeXML(node, indent) {
    const pad = "  ".repeat(indent);
    if (node.kind === "control") {
      const open = pad + "<" + node.tag + orderedControlAttrs(node);
      const name = (node.name || "").trim();
      if (!name) return open + "/>";
      return open + ">" + xmlEscape(name) + "</" + node.tag + ">";
    }
    const attrs = panelAttrsXML(node);
    if (node.children.length === 0) return pad + "<" + node.tag + attrs + "/>";
    let s = pad + "<" + node.tag + attrs + ">\n";
    node.children.forEach(function (c) { s += buildChild(c, indent + 1) + "\n"; });
    s += pad + "</" + node.tag + ">";
    return s;
  }

  function exportWarnings() {
    const warns = [];
    (function walk(node) {
      const pt = panelType(node);
      if (pt === "expandpanel" && node.children.length !== 1) {
        warns.push((node.kind === "root" ? "根面板 " : "") + "expandpanel 必须且只能包含一个子项（当前 " + node.children.length + " 个）");
      }
      if (node.tag === "sash") {
        const p = findParent(node.id);
        if (p) {
          const pt2 = panelType(p);
          if (pt2 !== "verticalpanel" && pt2 !== "horizonpanel") {
            warns.push("拉伸条 sash 必须位于纵向 / 横向面板内部");
          }
        }
      }
      if (node.kind === "control" && node.tag === "image" && !String(node.attrs.imgfile || "").trim()) {
        warns.push("图片 image 需要 imgfile 参数（本地图片路径），可在「添加参数」中填入");
      }
      node.children.forEach(walk);
    })(state.root);
    return warns;
  }

  function openExport() {
    const xml = buildRootXML(state.root);
    const warns = exportWarnings();
    els.exportWarn.innerHTML = warns.length
      ? "<strong>导出提示：</strong><br>" + warns.map(function (w) { return "· " + esc(w); }).join("<br>")
      : "";
    els.exportText.value = xml;
    els.modal.classList.add("show");
    els.modalClose.focus();
  }
  function closeExport() { els.modal.classList.remove("show"); }
  function downloadXML() {
    const blob = new Blob([els.exportText.value], { type: "application/xml" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "tinui-panel.xml";
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
  }
  function copyXML() {
    const text = els.exportText.value;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { toast("已复制到剪贴板"); }, function () { fallbackCopy(); });
    } else fallbackCopy();
    function fallbackCopy() {
      els.exportText.select();
      try { document.execCommand("copy"); toast("已复制到剪贴板"); } catch (e) { toast("复制失败，请手动选择"); }
    }
  }

  /* =========================================================================
   * 8. 初始化与事件
   * ======================================================================= */
  function $(id) { return document.getElementById(id); }
  function cacheEls() {
    els.canvasWrap = $("canvasWrap");
    els.canvas = $("canvas");
    els.overlay = $("overlay");
    els.ovSel = $("ovSel");
    els.ovCell = $("ovCell");
    els.ovHandleV = $("ovHandleV");
    els.ovHandleH = $("ovHandleH");
    els.outline = $("outline");
    els.outlineBlock = $("outlineBlock");
    els.outlineSplitter = $("outlineSplitter");
    els.breadcrumb = $("breadcrumb");
    els.props = $("props");
    els.palettePanels = $("palettePanels");
    els.paletteControls = $("paletteControls");
    els.canvasW = $("canvasW");
    els.canvasH = $("canvasH");
    els.modal = $("modal");
    els.modalClose = $("modalClose");
    els.exportWarn = $("exportWarn");
    els.exportText = $("exportText");
    els.toast = $("toast");
  }

  function paletteItem(kind, tag) {
    const meta = kind === "panel" ? PANELS[tag] : CONTROLS[tag];
    const sub = kind === "panel" ? (meta.desc || tag) : tag;
    const b = document.createElement("button");
    b.type = "button";
    b.className = "palette-item";
    b.draggable = true;
    b.dataset.kind = kind;
    b.dataset.tag = tag;
    b.title = (meta.desc ? meta.desc + " · " : "") + tag;
    b.innerHTML = '<span class="pi-text"><b>' + esc(meta.label) + "</b><small>" + esc(sub) + "</small></span>";
    b.addEventListener("click", function () {
      addNew(kind, tag, state.selectedId ? findNode(state.selectedId) : state.root);
    });
    b.addEventListener("dragstart", function (e) {
      e.dataTransfer.setData("text/plain", JSON.stringify({ kind: kind, tag: tag }));
      e.dataTransfer.effectAllowed = "copy";
    });
    return b;
  }

  function buildPalette() {
    els.palettePanels.innerHTML = "";
    Object.keys(PANELS).forEach(function (tag) { els.palettePanels.appendChild(paletteItem("panel", tag)); });
    els.paletteControls.innerHTML = "";
    CONTROL_GROUPS.forEach(function (g) {
      const h = document.createElement("div");
      h.className = "palette-group";
      h.textContent = g.title;
      els.paletteControls.appendChild(h);
      const box = document.createElement("div");
      box.className = "palette grid-2";
      g.tags.forEach(function (tag) {
        if (CONTROLS[tag]) box.appendChild(paletteItem("control", tag));
      });
      els.paletteControls.appendChild(box);
    });
  }

  

  function applyCanvasSize() {
    const w = state.canvasW + "px", h = state.canvasH + "px";
    els.canvasWrap.style.width = w;
    els.canvasWrap.style.height = h;
    els.canvas.style.width = w;
    els.canvas.style.height = h;
    els.overlay.style.width = w;
    els.overlay.style.height = h;
  }

  function toast(msg) {
    els.toast.textContent = msg;
    els.toast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { els.toast.classList.remove("show"); }, 1800);
  }

  function elementsNodesAt(x, y) {
    const list = document.elementsFromPoint
      ? document.elementsFromPoint(x, y)
      : [document.elementFromPoint(x, y)];
    return list.filter(function (el) {
      return el && el.classList && el.classList.contains("pd-node");
    });
  }

  function startDrag(e) {
    e.preventDefault();
    e.stopPropagation();
    const node = findNode(state.selectedId);
    if (!node || !node._cell) return;
    const vertical = e.currentTarget.dataset.dir === "v";
    if (node._weight > 0) {
      node._weight = 0;
      toast("已将 weight 置 0，改用固定 size");
    }
    drag = {
      node: node,
      vertical: vertical,
      start: vertical ? e.clientY : e.clientX,
      base: vertical ? node._cell.h : node._cell.w,
    };
    document.body.classList.add("dragging");
  }

  function bindEvents() {
    // 画布选择
    els.canvas.addEventListener("mousedown", function (e) {
      if (e.button !== 0) return;
      if (e.target.closest(".ov-handle")) return;
      const stack = elementsNodesAt(e.clientX, e.clientY);
      if (e.altKey) {
        const panels = stack.filter(function (el) { return !el.classList.contains("pd-control"); });
        if (panels.length) {
          const cur = state.selectedId;
          let idx = -1;
          for (let i = 0; i < panels.length; i++) { if (panels[i].dataset.id === cur) { idx = i; break; } }
          const next = idx >= 0 ? panels[(idx + 1) % panels.length] : panels[0];
          select(next.dataset.id);
          return;
        }
        if (stack.length) { select(stack[0].dataset.id); return; }
      }
      const nodeEl = e.target.closest(".pd-node");
      if (nodeEl) select(nodeEl.dataset.id);
      else select(null);
    });

    // 拖拽加入
    els.canvas.addEventListener("dragover", function (e) { e.preventDefault(); e.dataTransfer.dropEffect = "copy"; });
    els.canvas.addEventListener("drop", function (e) {
      e.preventDefault();
      let data;
      try { data = JSON.parse(e.dataTransfer.getData("text/plain")); } catch (err) { return; }
      if (!data || !data.tag) return;
      const el = document.elementFromPoint(e.clientX, e.clientY);
      const nodeEl = el && el.closest ? el.closest(".pd-node") : null;
      const target = nodeEl ? findNode(nodeEl.dataset.id) : state.root;
      addNew(data.kind, data.tag, target);
    });

    // 尺寸拖拽
    els.ovHandleV.addEventListener("mousedown", startDrag);
    els.ovHandleH.addEventListener("mousedown", startDrag);

    // 结构树高度分割线
    let splitDrag = null;
    els.outlineSplitter.addEventListener("mousedown", function (e) {
      e.preventDefault();
      splitDrag = { start: e.clientY, base: els.outlineBlock.offsetHeight };
      document.body.classList.add("dragging");
      els.outlineSplitter.classList.add("on");
    });
    document.addEventListener("mousemove", function (e) {
      if (!splitDrag) return;
      const max = els.outlineBlock.parentElement.clientHeight - 120;
      // 结构树在分割线下方：向上拖增大高度，向下拖减小高度
      const h = Math.max(90, Math.min(max, Math.round(splitDrag.base + (splitDrag.start - e.clientY))));
      els.outlineBlock.style.height = h + "px";
    });
    document.addEventListener("mouseup", function () {
      if (!splitDrag) return;
      splitDrag = null;
      document.body.classList.remove("dragging");
      els.outlineSplitter.classList.remove("on");
    });

    document.addEventListener("mousemove", function (e) {
      if (!drag) return;
      const cur = drag.vertical ? e.clientY : e.clientX;
      const val = Math.max(1, Math.round(drag.base + (cur - drag.start)));
      drag.node._size = val;
      layoutAll();
      paintCanvas();
      paintOverlays();
      paintOutline();
    });
    document.addEventListener("mouseup", function () {
      if (drag) { drag = null; document.body.classList.remove("dragging"); paintProps(); }
    });

    // 键盘
    document.addEventListener("keydown", function (e) {
      const t = e.target;
      if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.tagName === "SELECT")) return;
      if (e.key === "Escape") { select(null); closeExport(); return; }
      if (!state.selectedId) return;
      const node = findNode(state.selectedId);
      if (!node) return;
      if (e.key === "Delete" || e.key === "Backspace") {
        if (findParent(node.id)) { e.preventDefault(); deleteNode(node); }
      } else if (e.ctrlKey && (e.key === "d" || e.key === "D")) {
        if (findParent(node.id)) { e.preventDefault(); duplicateNode(node); }
      } else if (e.altKey && e.key === "ArrowUp") {
        e.preventDefault(); moveNode(node, -1);
      } else if (e.altKey && e.key === "ArrowDown") {
        e.preventDefault(); moveNode(node, 1);
      }
    });

    // 工具栏
    document.getElementById("btnExample").addEventListener("click", function () {
      idSeq = 1;
      state.root = defaultModel();
      state.selectedId = null;
      rerender();
      toast("已载入示例");
    });
    document.getElementById("btnClear").addEventListener("click", function () {
      state.root.children = [];
      state.selectedId = state.root.id;
      rerender();
      toast("已清空子项");
    });
    document.getElementById("btnExport").addEventListener("click", openExport);

    // 画布尺寸
    els.canvasW.addEventListener("input", function () {
      const v = parseInt(els.canvasW.value, 10);
      if (!isNaN(v) && v >= 120) { state.canvasW = v; applyCanvasSize(); rerender({ props: false }); }
    });
    els.canvasH.addEventListener("input", function () {
      const v = parseInt(els.canvasH.value, 10);
      if (!isNaN(v) && v >= 120) { state.canvasH = v; applyCanvasSize(); rerender({ props: false }); }
    });

    // 导出弹窗
    els.modalClose.addEventListener("click", closeExport);
    els.modal.addEventListener("mousedown", function (e) { if (e.target === els.modal) closeExport(); });
    document.getElementById("btnCopy").addEventListener("click", copyXML);
    document.getElementById("btnDownload").addEventListener("click", downloadXML);
  }

  function defaultModel() {
    const root = newNode("root", "tinui", {
      root: "horizon", padding: "5,5,5,5", spacing: "5",
      min_width: "0", min_height: "0", bg: "", bd: "9", line: "", linew: "0",
      margin: "5",
    });

    const left = newNode("panel", "verticalpanel", deepCopy(PANELS.verticalpanel.attrs));
    left.attrs.padding = "5,5,5,5";
    left.attrs.spacing = "5";
    left._size = 160;
    left.children.push(newNode("control", "paragraph", { text: "面板设计器", width: "130", anchor: "nw" }));
    left.children.push(newNode("control", "button2", { text: "打开", anchor: "nw" }));
    left.children.push(newNode("control", "checkbutton", { text: "启用选项", anchor: "nw" }));
    left.children.push(newNode("control", "progressbar", { width: "140", anchor: "nw" }));

    const card = newNode("panel", "cardpanel", deepCopy(PANELS.cardpanel.attrs));
    card.attrs.padding = "5,5,5,5";
    card.attrs.h_spacing = "8";
    card.attrs.v_spacing = "8";
    card._weight = 1;
    card.children.push(newNode("control", "label", { text: "卡片 A", anchor: "center" }));
    card.children.push(newNode("control", "label", { text: "卡片 B", anchor: "center" }));
    card.children.push(newNode("control", "button2", { text: "确认", anchor: "center" }));
    card.children.push(newNode("control", "onoff", { anchor: "center" }));

    root.children.push(left, card);
    return root;
  }

  function init() {
    cacheEls();
    idSeq = 1;
    state.root = defaultModel();
    state.selectedId = null;
    state.canvasW = 840;
    state.canvasH = 560;
    els.canvasW.value = state.canvasW;
    els.canvasH.value = state.canvasH;
    buildPalette();
    applyCanvasSize();
    bindEvents();
    rerender();
  }

  /* 供 Node 端验证导出（不依赖 DOM） */
  function exportExampleXML() {
    idSeq = 1;
    return buildRootXML(defaultModel());
  }

  if (typeof document !== "undefined") {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
    else init();
  }
  if (typeof module !== "undefined" && module.exports) {
    module.exports = { exportExampleXML: exportExampleXML, buildRootXML: buildRootXML, defaultModel: defaultModel };
  }
})();
