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
   ["", "DBpia", "RISS", "KCI", "국회전자도서관", "구글 학술검색", "기관 연구보고서", "그 밖"]),
  ("1-연구1질문", "연구 1 — ① 무엇이 궁금했는가", "area", "그 연구의 연구 질문", None),
  ("1-연구1방법", "연구 1 — ② 무엇으로 어떻게 알아냈는가", "area",
   "어떤 자료를 어떻게 다뤘는지. 도구 이름만 쓰면 방법으로 보지 않습니다", None),
  ("1-연구1결론", "연구 1 — ③ 결론은 무엇인가", "area", "숫자나 방향이 드러나게", None),
  ("1-연구2제목", "연구 2 — 제목", "text", None, None),
  ("1-연구2출처", "연구 2 — 어디서 찾았나", "select", None,
   ["", "DBpia", "RISS", "KCI", "국회전자도서관", "구글 학술검색", "기관 연구보고서", "그 밖"]),
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
<div class="box">💾 <b>학번 · 이름 · 개별 비밀번호를 먼저 넣으세요.</b> 저장·제출·불러오기에 모두 필요합니다.<br>
<b>「임시저장」</b>을 누르면 지금까지 쓴 내용이 시트에 저장됩니다.
다음 시간에 <b>「불러오기」</b>를 누르면 이어서 쓸 수 있습니다. 다른 컴퓨터에서도 됩니다.<br>
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
const LSBASE = "정연-수행" + TASK;
let 차단 = 0;
let 제출됨 = false;
let 저장함 = true;   /* 마지막으로 고친 뒤에 저장(또는 제출)했는가 */

const $ = function (id) { return document.getElementById(id); };
const el = function (k) { return $("f_" + k); };

function note(t) { $("who-msg").textContent = t; }
function who() {
  return { sid: $("sid").value.trim(), name: $("nm").value.trim(), pw: $("pw").value.trim() };
}
function collect() {
  const d = {};
  KEYS.forEach(function (k) { const e = el(k); if (e) d[k] = e.value; });
  return d;
}
function fill(d) {
  KEYS.forEach(function (k) {
    const e = el(k);
    if (e && d[k] != null) e.value = d[k];
    const c = $("c_" + k);
    if (c && e) c.textContent = e.value.length + "자";
  });
}
function 변경됨() { 저장함 = false; }

/* ── 붙여넣기 차단 · 글자 수 ── */
KEYS.forEach(function (k) {
  const e = el(k);
  if (!e) return;
  if (PASTE_OK.indexOf(k) === -1) {
    e.addEventListener("paste", function (ev) { ev.preventDefault(); 차단++; note("붙여넣기는 막혀 있습니다 (" + 차단 + "회)"); });
    e.addEventListener("drop", function (ev) { ev.preventDefault(); });
  }
  e.addEventListener("input", 변경됨);
  e.addEventListener("change", 변경됨);
  if (e.tagName === "TEXTAREA") {
    e.addEventListener("input", function () {
      const c = $("c_" + k);
      if (c) c.textContent = e.value.length + "자";
    });
  }
});

/* ── 서버에 본인 확인 (JSONP) — 불러오기와 저장 전 확인에 함께 씁니다 ── */
function 서버에묻기(done) {
  const w = who();
  const cb = "cb" + Date.now() + Math.floor(Math.random() * 1000);
  let 끝 = false;
  const 마무리 = function (r) {
    if (끝) return;
    끝 = true;
    try { delete window[cb]; } catch (e) {}
    done(r);
  };
  window[cb] = 마무리;
  const s = document.createElement("script");
  s.src = ENDPOINT + "?task=" + TASK + "&sid=" + encodeURIComponent(w.sid)
        + "&name=" + encodeURIComponent(w.name) + "&pw=" + encodeURIComponent(w.pw)
        + "&callback=" + cb;
  s.onerror = function () { 마무리(null); };
  document.body.appendChild(s);
  setTimeout(function () { s.remove(); 마무리(null); }, 20000);
}

function 확인실패문구(r) {
  if (!r) return "연결에 실패했습니다. 잠시 뒤 다시 눌러 주세요";
  if (r.reason === "lockout") return "시도가 많아 잠겼습니다. 선생님께 말하세요";
  return "학번 · 이름 · 개별 비밀번호를 다시 확인해 주세요";
}

/* ── 불러오기 ── */
function load() {
  const w = who();
  if (!w.sid || !w.name || !w.pw) { note("학번 · 이름 · 개별 비밀번호를 모두 넣어 주세요"); return; }
  note("불러오는 중…");
  서버에묻기(function (r) {
    if (!r || !r.ok) { note(확인실패문구(r)); return; }
    fill(r.fields || {});
    저장함 = true;
    제출됨 = (r.status === "제출");
    $("nm").value = r.name || w.name;
    note(r.when ? ("불러왔습니다 — 마지막 저장 " + r.when + (r.status ? " (" + r.status + ")" : ""))
                : "저장해 둔 내용이 없습니다. 새로 쓰면 됩니다");
    if (제출됨) $("state").innerHTML = "<b>제출 완료</b> — 다시 저장하면 덮어씁니다";
  });
}

/* ── 저장 · 제출 ── */
function save(final) {
  const w = who();
  if (!w.sid || !w.name || !w.pw) { note("학번 · 이름 · 개별 비밀번호를 모두 넣어 주세요"); return; }
  const data = collect();

  if (final) {
    const 빈칸 = KEYS.filter(function (k) { return !String(data[k] || "").trim(); });
    if (빈칸.length && !confirm("아직 안 쓴 칸이 " + 빈칸.length + "개 있습니다.\\n그래도 제출할까요?")) return;
  }

  /* 보내기 전에 본인 확인을 합니다. 비밀번호가 틀리면 서버가 받지 않으므로,
     「저장했습니다」라고 안내해 놓고 실제로는 안 들어가는 일을 막습니다. */
  note("확인하는 중…");
  서버에묻기(function (r) {
    if (!r || !r.ok) { note(확인실패문구(r)); return; }
    if (r.status === "제출" && !제출됨 &&
        !confirm("이미 「제출」로 기록된 내용이 있습니다.\\n다시 저장하면 바뀝니다. 계속할까요?")) { note(""); return; }
    보내기(w, data, final);
  });
}

function 보내기(w, data, final) {
  try { localStorage.setItem(LSBASE + "-" + w.sid, JSON.stringify(data)); } catch (e) {}

  const f = document.createElement("form");
  f.action = ENDPOINT; f.method = "POST"; f.target = "sink";
  const put = function (n, v) {
    const i = document.createElement("input");
    i.type = "hidden"; i.name = n; i.value = v; f.appendChild(i);
  };
  put("task", TASK); put("sid", w.sid); put("name", w.name); put("pw", w.pw);
  put("status", final ? "제출" : "임시저장");
  put("paste", String(차단));
  put("data", JSON.stringify(data));
  document.body.appendChild(f); f.submit(); document.body.removeChild(f);

  const t = new Date().toLocaleString("ko-KR", { month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" });
  if (final) 제출됨 = true;
  저장함 = true;
  차단 = 0;        /* 서버에 누적되므로 보낸 뒤 초기화 */
  note("");
  $("state").innerHTML = final ? ("<b>제출했습니다</b> — " + t) : ("임시저장했습니다 — " + t);
}

/* ── 이 기기에 남은 것 되살리기 ──
   학번마다 따로 둡니다. 컴퓨터실처럼 여럿이 쓰는 PC에서
   앞 학생이 쓴 내용이 다음 학생 화면에 뜨는 것을 막습니다. */
try { localStorage.removeItem(LSBASE); } catch (e) {}   /* 학번 없이 저장하던 옛 자리 정리 */
let 되살핀학번 = "";
function 기기복원() {
  const s = $("sid").value.trim();
  if (!s || s === 되살핀학번) return;
  되살핀학번 = s;
  let a = null;
  try { a = localStorage.getItem(LSBASE + "-" + s); } catch (e) { return; }
  if (!a) return;
  const 쓴것 = KEYS.some(function (k) { const e = el(k); return e && e.value.trim(); });
  if (쓴것) { note("이 기기에 " + s + " 학번으로 저장해 둔 것이 있습니다. 「불러오기」를 누르면 서버 것을 가져옵니다"); return; }
  try { fill(JSON.parse(a)); } catch (e) { return; }
  저장함 = false;
  note("이 기기에 남아 있던 내용입니다. 서버 것과 맞추려면 「불러오기」를 누르세요");
}
$("sid").addEventListener("change", 기기복원);

window.addEventListener("beforeunload", function (ev) {
  const 쓴것 = KEYS.some(function (k) { const e = el(k); return e && e.value.trim(); });
  if (쓴것 && !저장함) { ev.preventDefault(); ev.returnValue = ""; }
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
