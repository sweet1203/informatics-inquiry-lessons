# -*- coding: utf-8 -*-
"""수행평가 제출 폼 생성 — task1-submit.html · task2-submit.html
스타일은 _생성기.py 의 것을 그대로 가져다 쓴다."""
import io, os, re, json

src = io.open('_생성기.py', encoding='utf-8').read()
CSS = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
CSS = CSS.replace('{{', '{').replace('}}', '}')

# 차시 페이지가 쓰는 것과 같은 Apps Script 주소
ENDPOINT = re.search(r'const ENDPOINT = "([^"]*)"', io.open('lesson09.html', encoding='utf-8').read()).group(1)

EXTRA = """
.fld{margin:16px 0}
.fld>label{display:block;font-weight:700;margin-bottom:5px;font-size:.97rem}
.fld .hint{font-size:.86rem;color:var(--muted);margin:0 0 6px}
.fld input[type=text],.fld textarea,.fld select{width:100%;box-sizing:border-box;
padding:9px 11px;border:1px solid var(--line);border-radius:8px;font:inherit;background:var(--card);color:var(--ink)}
.fld textarea{min-height:96px;resize:vertical;line-height:1.6}
#f_AI활용{min-height:200px}
.fld input:focus,.fld textarea:focus,.fld select:focus{outline:2px solid var(--accent);outline-offset:1px}
.grp{border:1px solid var(--line);border-radius:12px;padding:2px 15px 15px;margin:18px 0}
.grp>h4{margin:0 -15px 4px;padding:10px 15px;background:var(--accent);color:var(--ink2);
font-size:.96rem;border-radius:11px 11px 0 0}
.who{display:flex;gap:9px;flex-wrap:wrap;align-items:flex-end}
.who .fld{flex:1 1 130px;margin:0}
.bar{position:sticky;bottom:0;background:var(--bg);border-top:1px solid var(--line);
padding:11px 0;display:flex;gap:9px;align-items:center;flex-wrap:wrap;z-index:5}
.state{font-size:.88rem;color:var(--muted);margin-left:auto}
.state b{color:var(--ok)}
.lock{opacity:.55;pointer-events:none}
.cnt{font-size:.82rem;color:var(--muted);text-align:right;margin:3px 0 0}
.cnt.over{color:var(--warn)}
"""

# ── 필드 정의 ─────────────────────────────────────────────────
# (열이름, 라벨, 종류, 힌트, 선택지)
T1 = [
 ("문항 1 · 선행 연구 분석 <span style='font-weight:400'>40점</span>", [
  ("1-연구1제목", "연구 1 — 제목", "text", "찾은 논문·연구 보고서의 제목을 그대로", None),
  ("1-연구1출처", "연구 1 — 어디서 찾았나", "select", None,
   ["", "DBpia", "RISS", "국회전자도서관", "구글 학술검색", "기관 연구보고서", "그 밖"]),
  ("1-연구1질문", "연구 1 — ① 무엇이 궁금했는가", "area", "그 연구의 연구 질문", None),
  ("1-연구1방법", "연구 1 — ② 무엇으로 어떻게 알아냈는가", "area",
   "어떤 자료를 어떻게 다뤘는지. 도구 이름만 쓰면 방법으로 보지 않습니다", None),
  ("1-연구1결론", "연구 1 — ③ 결론은 무엇인가", "area", "숫자나 방향이 드러나게", None),
  ("1-연구2제목", "연구 2 — 제목", "text", None, None),
  ("1-연구2출처", "연구 2 — 어디서 찾았나", "select", None,
   ["", "DBpia", "RISS", "국회전자도서관", "구글 학술검색", "기관 연구보고서", "그 밖"]),
  ("1-연구2질문", "연구 2 — ① 무엇이 궁금했는가", "area", None, None),
  ("1-연구2방법", "연구 2 — ② 무엇으로 어떻게 알아냈는가", "area", None, None),
  ("1-연구2결론", "연구 2 — ③ 결론은 무엇인가", "area", None, None),
  ("1-비교대상", "④ 어느 연구로 쓸 건가요", "select", None, ["", "연구 1", "연구 2"]),
  ("1-차이서술", "④ 같은 주제를 사회·과학 과제 연구로 다룬다면 무엇이 달라지나", "area",
   "방법의 차이를 짚으면 됩니다. 학문 분류를 정확히 쓸 필요는 없습니다", None),
 ]),
 ("문항 2 · 읽은 연구의 과정 분석 <span style='font-weight:400'>30점</span>", [
  ("2-고른연구", "어느 연구를 고를 건가요", "select", None, ["", "연구 1", "연구 2"]),
  ("2-설계", "① 설계 — 그 연구자가 무엇을 했나", "area",
   "무엇을 셀 수 있는 값으로 바꿨는지, 무엇과 무엇을 견주기로 했는지", None),
  ("2-수행", "② 수행 — 그 연구자가 무엇을 했나", "area", None, None),
  ("2-결론도출", "③ 결론 도출 — 그 연구자가 무엇을 했나", "area", None, None),
  ("2-발표", "④ 발표 — 그 연구자가 무엇을 했나", "area", "논문 작성·보고서 작성으로 써도 됩니다", None),
 ]),
 ("문항 3 · 내 연구 주제와 방법 설정 <span style='font-weight:400'>30점</span>", [
  ("3-연구질문", "내 연구 질문 — 한 문장으로", "text", "무엇과 무엇을 견줄지 드러나게", None),
  ("3-왜골랐나", "① 왜 이 주제를 골랐나 — 읽은 연구와 연결지어", "area",
   "「따라 하겠다」도, 「저렇게는 안 하겠다」도 됩니다", None),
  ("3-무엇으로", "② 무엇으로 답을 낼 것인가", "area", "데이터 / 장치 / 프로그램", None),
  ("3-어떻게", "③ 어떻게 답을 낼 것인가", "area", "방법", None),
  ("3-걱정되는점", "④ 미리 걱정되는 점", "area", "그때 무엇을 하겠다는 대비까지", None),
 ]),
]

T2 = [
 ("연구 계획서 여덟 칸 <span style='font-weight:400'>80점</span>", [
  ("트랙", "트랙", "select", None,
   ["", "A 데이터 분석", "B 피지컬 컴퓨팅", "C 프로그램 제작"]),
  ("①제목", "① 연구 제목", "text", "제목만 읽고 무엇을 어떻게 하는지 알 수 있게", None),
  ("②동기", "② 연구 동기", "area", "「지금은 ○○인데, △△가 되면 좋겠다」 두 문장", None),
  ("③연구질문", "③ 연구 질문", "text", "답할 수 있는 한 문장", None),
  ("④데이터장치", "④ 사용할 데이터 또는 장치·프로그램", "area", "실제로 구할 수 있는 것만", None),
  ("⑤방법도구", "⑤ 분석·구현 방법과 도구", "area", "어떤 도구로 어떻게 다룰지", None),
  ("⑥절차", "⑥ 연구 절차", "area", "언제 무엇을 할지", None),
  ("⑦예상결과", "⑦ 예상 결과", "area", "견줄 수 있게 숫자나 방향으로. 틀려도 됩니다", None),
  ("⑧어려움", "⑧ 예상되는 어려움", "area", "어려움마다 대비 방법을 함께", None),
 ]),
]

AI_FIELD = ("AI활용", "생성형 AI를 썼다면 — 무엇을 물었고, 무엇을 쓰고 무엇을 버렸나", "area",
            "이 칸은 붙여넣기가 됩니다. 주고받은 대화를 그대로 붙여 넣어도 됩니다. "
            "쓰지 않았으면 「사용 안 함」이라고 적으세요", None)

# 붙여넣기를 막지 않는 칸
PASTE_OK = ["AI활용"]


def field_html(key, label, kind, hint, opts):
    h = '<div class="fld">\n<label for="f_%s">%s</label>\n' % (key, label)
    if hint:
        h += '<p class="hint">%s</p>\n' % hint
    if kind == "select":
        h += '<select id="f_%s" data-k="%s">' % (key, key)
        for o in opts:
            h += '<option value="%s">%s</option>' % (o, o or "— 고르세요 —")
        h += '</select>\n'
    elif kind == "text":
        h += '<input type="text" id="f_%s" data-k="%s">\n' % (key, key)
    else:
        h += '<textarea id="f_%s" data-k="%s"></textarea>\n<p class="cnt" id="c_%s">0자</p>\n' % (key, key, key)
    return h + '</div>\n'


def build(task, title, sub, groups, lead):
    keys = []
    body = ""
    for gname, flds in groups:
        body += '<div class="grp"><h4>%s</h4>\n' % gname
        for f in flds:
            body += field_html(*f)
            keys.append(f[0])
        body += '</div>\n'
    body += '<div class="grp"><h4>AI 활용 기록</h4>\n' + field_html(*AI_FIELD) + '</div>\n'
    keys.append(AI_FIELD[0])

    page = """<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ · 정보과제연구</title>
<style>__CSS____EXTRA__</style>
</head><body>
<div class="wrap">
<header>
  <span class="chip">제출</span>
  <h1>__TITLE__</h1>
  <p class="sub">__SUB__</p>
</header>

<section class="learn">
__LEAD__
<div class="box">💾 <b>「임시저장」을 누르면 지금까지 쓴 내용이 시트에 저장됩니다.</b><br>
다음 시간에 학번·이름·개별 비밀번호를 넣고 <b>「불러오기」</b>를 누르면 이어서 쓸 수 있습니다. 다른 컴퓨터에서도 됩니다.<br>
<b>빈 칸은 저장해도 앞서 쓴 내용을 지우지 않습니다.</b> 정말 지우려면 그 칸에 <b>－</b> 한 글자만 넣으세요.</div>
<div class="box">⚠️ <b>답안 칸은 붙여넣기가 막혀 있습니다.</b> 시도한 횟수가 함께 기록됩니다.<br>
<b>맨 아래 「AI 활용 기록」 칸만 붙여넣기가 됩니다.</b> 주고받은 대화를 그대로 넣으세요.</div>

<div class="who">
  <div class="fld"><label for="sid">학번</label><input type="text" id="sid" inputmode="numeric"></div>
  <div class="fld"><label for="nm">이름</label><input type="text" id="nm"></div>
  <div class="fld"><label for="pw">개별 비밀번호</label><input type="password" id="pw"></div>
  <div><button class="ghost" onclick="load()">불러오기</button></div>
</div>
<div id="who-msg" class="cnt"></div>
</section>

<section class="learn" id="form">
__BODY__
</section>

<div class="bar">
  <button class="ghost" onclick="save(false)">💾 임시저장</button>
  <button onclick="save(true)">📮 제출하기</button>
  <span class="state" id="state">아직 저장하지 않았습니다</span>
</div>

</div>
<iframe name="sink" style="display:none"></iframe>
<script>
const ENDPOINT = "__ENDPOINT__";
const TASK = "__TASK__";
const KEYS = __KEYS__;
const PASTE_OK = __PASTEOK__;
const LS = "정연-수행" + TASK;
let 차단 = 0;
let 불러옴 = false;   /* 이번에 서버에서 기존 내용을 확인했는가 */
let 제출됨 = false;

const $ = function (id) { return document.getElementById(id); };
const el = function (k) { return $("f_" + k); };

/* ── 붙여넣기 차단 ── */
KEYS.forEach(function (k) {
  const e = el(k);
  if (!e) return;
  if (PASTE_OK.indexOf(k) === -1) {
    e.addEventListener("paste", function (ev) { ev.preventDefault(); 차단++; note("붙여넣기는 막혀 있습니다 (" + 차단 + "회)"); });
    e.addEventListener("drop", function (ev) { ev.preventDefault(); });
  }
  if (e.tagName === "TEXTAREA") {
    e.addEventListener("input", function () {
      const c = $("c_" + k);
      if (c) c.textContent = e.value.length + "자";
    });
  }
});

function note(t) { const m = $("who-msg"); m.textContent = t; }
function who() {
  return { sid: $("sid").value.trim(), name: $("nm").value.trim(), pw: $("pw").value.trim() };
}
function collect() {
  const d = {};
  KEYS.forEach(function (k) { const e = el(k); if (e) d[k] = e.value; });
  return d;
}
function fill(d) {
  KEYS.forEach(function (k) { const e = el(k); if (e && d[k] != null) e.value = d[k];
    const c = $("c_" + k); if (c && e) c.textContent = e.value.length + "자"; });
}

/* ── 불러오기 (JSONP) ── */
function load() {
  const w = who();
  if (!w.sid || !w.name || !w.pw) { note("학번 · 이름 · 개별 비밀번호를 모두 넣어 주세요"); return; }
  note("불러오는 중…");
  const cb = "cb" + Date.now();
  window[cb] = function (r) {
    delete window[cb];
    if (!r || !r.ok) {
      note(r && r.reason === "lockout" ? "시도가 많아 잠겼습니다. 선생님께 말하세요"
        : "학번 · 이름 · 비밀번호를 다시 확인해 주세요");
      return;
    }
    fill(r.fields || {});
    불러옴 = true;
    제출됨 = (r.status === "제출");
    $("nm").value = r.name || w.name;
    note(r.when ? ("불러왔습니다 — 마지막 저장 " + r.when + (r.status ? " (" + r.status + ")" : ""))
                : "저장해 둔 내용이 없습니다. 새로 쓰면 됩니다");
    if (r.status === "제출") $("state").innerHTML = "<b>제출 완료</b> — 다시 저장하면 덮어씁니다";
  };
  const s = document.createElement("script");
  s.src = ENDPOINT + "?task=" + TASK + "&sid=" + encodeURIComponent(w.sid)
        + "&name=" + encodeURIComponent(w.name) + "&pw=" + encodeURIComponent(w.pw)
        + "&callback=" + cb;
  s.onerror = function () { delete window[cb]; note("연결에 실패했습니다. 잠시 뒤 다시 눌러 주세요"); };
  document.body.appendChild(s);
  setTimeout(function () { s.remove(); }, 20000);
}

/* ── 저장 · 제출 ── */
function save(final) {
  const w = who();
  if (!w.sid || !w.name) { note("학번과 이름을 넣어 주세요"); return; }
  const data = collect();

  /* 불러오기를 안 했다면 먼저 확인시킵니다. 서버가 빈 칸을 보호하긴 하지만,
     학생이 「내가 쓴 게 사라졌다」고 느끼지 않게 하는 편이 낫습니다. */
  if (!불러옴 && w.pw) {
    note("먼저 「불러오기」를 눌러 앞서 쓴 내용을 확인해 주세요");
    if (!confirm("아직 「불러오기」를 하지 않았습니다.\\n\\n앞서 저장해 둔 내용이 있다면 화면에 안 보일 수 있습니다.\\n(빈 칸은 지워지지 않으니 안심하세요)\\n\\n그래도 저장할까요?")) return;
  }
  if (제출됨 && !confirm("이미 제출한 상태입니다.\\n다시 저장하면 내용이 바뀝니다. 계속할까요?")) return;

  if (final) {
    const 빈칸 = KEYS.filter(function (k) { return !String(data[k] || "").trim(); });
    if (빈칸.length) {
      if (!confirm("아직 안 쓴 칸이 " + 빈칸.length + "개 있습니다.\\n그래도 제출할까요?")) return;
    }
  }
  try { localStorage.setItem(LS, JSON.stringify(data)); } catch (e) {}

  if (!ENDPOINT) { $("state").textContent = "전송 설정 전입니다. 이 기기에만 저장했습니다"; return; }
  const f = document.createElement("form");
  f.action = ENDPOINT; f.method = "POST"; f.target = "sink";
  const put = function (n, v) {
    const i = document.createElement("input");
    i.type = "hidden"; i.name = n; i.value = v; f.appendChild(i);
  };
  put("task", TASK); put("sid", w.sid); put("name", w.name);
  put("status", final ? "제출" : "임시저장");
  put("paste", String(차단));
  put("data", JSON.stringify(data));
  document.body.appendChild(f); f.submit(); document.body.removeChild(f);

  const t = new Date().toLocaleString("ko-KR", { month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" });
  if (final) 제출됨 = true;
  불러옴 = true;   /* 방금 내가 쓴 것이 서버의 최신본이 됩니다 */
  차단 = 0;        /* 서버에 누적되므로 보낸 뒤 초기화 */
  $("state").innerHTML = final ? ("<b>제출했습니다</b> — " + t) : ("임시저장했습니다 — " + t);
}

/* 이 기기에 남은 것이 있으면 되살립니다 */
try { const a = localStorage.getItem(LS); if (a) fill(JSON.parse(a)); } catch (e) {}
window.addEventListener("beforeunload", function (ev) {
  const 쓴것 = KEYS.some(function (k) { const e = el(k); return e && e.value.trim(); });
  if (쓴것 && $("state").textContent.indexOf("저장") === -1) { ev.preventDefault(); ev.returnValue = ""; }
});
</script>
</body></html>
"""
    page = (page.replace("__CSS__", CSS).replace("__EXTRA__", EXTRA)
                .replace("__TITLE__", title).replace("__SUB__", sub)
                .replace("__LEAD__", lead).replace("__BODY__", body)
                .replace("__ENDPOINT__", ENDPOINT).replace("__TASK__", task)
                .replace("__PASTEOK__", json.dumps(PASTE_OK, ensure_ascii=False))
                .replace("__KEYS__", json.dumps(keys, ensure_ascii=False)))
    fn = "task%s-submit.html" % task
    with io.open(fn, "w", encoding="utf-8") as f:
        f.write(page)
    print("  ✅ %s  (%s bytes)" % (fn, format(os.path.getsize(fn), ",")))


build("1", "수행평가 1 제출",
      "선행 연구 사례 분석 및 연구 주제 설정하기",
      T1,
      '<div class="box">📄 <b><a href="answer-task1.html" target="_blank" rel="noopener">수행평가 1 안내</a></b></div>')

build("2", "수행평가 2 제출",
      "연구 계획서 작성",
      T2,
      '<div class="box">📄 <b><a href="sample-plan.html" target="_blank" rel="noopener">계획서 예시</a></b> · '
      '<b><a href="answer-task2.html" target="_blank" rel="noopener">수행평가 2 안내</a></b></div>'
      '<div class="box">🎯 <b>③ 연구 질문 · ④ 데이터·장치 · ⑤ 분석 방법은 서로 맞물려야 합니다.</b><br>'
      '④로 ③에 답할 수 있고, ⑤로 ④를 다룰 수 있어야 합니다.</div>')
