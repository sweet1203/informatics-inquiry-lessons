# -*- coding: utf-8 -*-
"""수행평가 안내 3부작 — 허브 / 수행1 / 수행2"""
import io, os, re

CSS = re.search(r'<style>(.*?)</style>',
                io.open('_생성기.py', encoding='utf-8').read(), re.S).group(1).replace('{{','{').replace('}}','}')

EXTRA = """
.cmp{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:14px 0}
@media(max-width:640px){.cmp{grid-template-columns:1fr}}
.cmp>div{border:1px solid var(--line);border-radius:11px;overflow:hidden}
.cmp h5{margin:0;padding:9px 13px;font-size:.92rem}
.good h5{background:var(--ok);color:var(--ink2)}
.bad h5{background:#b91c1c;color:#fff}
.cmp .bd{padding:13px;font-size:.93rem}
.split{background:var(--quiz);border:1px solid var(--quizline);border-radius:10px;padding:12px 15px;margin:10px 0 22px;font-size:.92rem}
.split b{color:var(--warn)}
.gr{display:inline-block;background:var(--accent);color:var(--ink2);font-weight:800;
padding:2px 11px;border-radius:99px;font-size:.82rem;margin-left:6px}
.bad .gr{background:#b91c1c}
.qbox{border-left:3px solid var(--accent);background:var(--soft);padding:12px 15px;border-radius:0 9px 9px 0;margin:16px 0}
.talk{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;margin:10px 0;font-size:.94rem}
.talk .who{font-weight:800;color:var(--accent)}
nav.go{display:grid;grid-template-columns:1fr 1fr;gap:11px;margin:22px 0 6px}
@media(max-width:560px){nav.go{grid-template-columns:1fr}}
nav.go a{display:block;padding:15px 17px;border:1px solid var(--line);border-radius:12px;
background:var(--soft);color:inherit;text-decoration:none;transition:border-color .15s}
nav.go a:hover{border-color:var(--accent)}
nav.go .k{display:block;font-size:.8rem;color:var(--muted);font-weight:700}
nav.go .v{display:block;font-size:1.02rem;font-weight:800;margin-top:3px;letter-spacing:-.01em}
.eg{font-size:.82rem;color:var(--muted);font-weight:600}
.blank{background:repeating-linear-gradient(45deg,transparent,transparent 7px,var(--soft) 7px,var(--soft) 14px);color:var(--muted);font-style:italic;text-align:center}
"""

def page(title, chip, h1, sub, body, nav):
    return ('<!doctype html>\n<html lang="ko"><head><meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{title}</title>\n<style>' + CSS + EXTRA + '</style>\n</head><body>\n'
            '<div class="wrap">\n<header>\n'
            f'  <span class="chip">{chip}</span>\n  <h1>{h1}</h1>\n  <p class="sub">{sub}</p>\n</header>\n'
            + nav + body + nav + '\n</div>\n</body></html>\n')

L_HUB  = '<a href="answer-guide.html"><span class="k">← 돌아가기</span><span class="v">수행평가 안내</span></a>'
L_T1   = '<a href="answer-task1.html"><span class="k">수행평가 1 · 30%</span><span class="v">선행 연구 분석 · 내 주제 설정</span></a>'
L_T2   = '<a href="answer-task2.html"><span class="k">수행평가 2 · 40%</span><span class="v">연구 계획서 · 구술 발표</span></a>'
NAV_HUB = f'<nav class="go">{L_T1}{L_T2}</nav>\n'
NAV_T1  = f'<nav class="go">{L_HUB}{L_T2}</nav>\n'
NAV_T2  = f'<nav class="go">{L_HUB}{L_T1}</nav>\n'

등급표 = """<h3>채점 등급</h3>
<table><tr><th>등급</th><th>뜻</th></tr>
<tr><td><b>A</b></td><td>요구한 것을 모두 갖추고 서로 맞물리게 썼다</td></tr>
<tr><td><b>B</b></td><td>요구한 것을 모두 갖췄다</td></tr>
<tr><td><b>C</b></td><td>대부분 갖췄으나 일부가 빠지거나 연결이 약하다</td></tr>
<tr><td><b>D</b></td><td>기본 항목만 갖췄다</td></tr>
<tr><td><b>E</b></td><td>일부만 작성했다</td></tr></table>
<p><b>등급마다 붙는 점수는 교과협의회에서 정합니다.</b> 다섯 단계의 <b>간격은 같습니다.</b></p>"""

AI지침 = """<h3>🤖 AI 사용 지침</h3>
<p>생성형 AI(챗지피티·클로드·제미나이 등)를 <b>연구 전 과정에서 써도 됩니다.</b> 다만 아래를 지켜야 합니다.</p>

<table><tr><th></th><th>써도 되는 것</th></tr>
<tr><td>1</td><td>연구 주제와 관련된 <b>자료 찾기</b> · 검색어 다듬기</td></tr>
<tr><td>2</td><td><b>아이디어 넓히기</b> — "이 주제로 어떤 데이터가 필요할까?"</td></tr>
<tr><td>3</td><td><b>도구 사용법</b> 묻기 · 오류 해결</td></tr>
<tr><td>4</td><td>내가 쓴 글을 <b>다듬기</b></td></tr></table>

<table><tr><th></th><th>하면 안 되는 것</th><th>어떻게 되나</th></tr>
<tr><td>1</td><td><b>AI가 만든 글·이미지·코드를 그대로 자기 것으로 제출</b></td><td><b>부정행위</b>로 처리</td></tr>
<tr><td>2</td><td>AI를 쓰고도 <b>기록하지 않음</b></td><td>해당 내용 <b>채점 제외</b></td></tr>
<tr><td>3</td><td>AI가 알려준 자료를 <b>확인하지 않고</b> 인용</td><td>그 자료는 <b>없는 것으로</b> 처리</td></tr>
<tr><td>4</td><td>AI 입력창에 <b>이름·학번·생년월일·주소·연락처</b> 입력</td><td>개인정보 보호 위반</td></tr></table>

<h4>📝 AI를 썼으면 이렇게 적습니다</h4>
<div class="box"><b>[AI 활용 기록]</b><br>
▪ <b>사용한 AI</b> — 챗지피티<br>
▪ <b>물어본 것</b> — "버스 승하차 데이터로 정류장을 비교하려면 어떤 값을 쓰면 좋을까?"<br>
▪ <b>반영한 방식</b> — 「시간대별 평균」을 쓰라는 제안을 <b>채택</b>. 「표준편차도 보라」는 제안은 아직 안 배워서 <b>안 씀</b><br>
▪ <b>출처</b> — AI가 알려준 논문 2편은 <b>DBpia에서 직접 찾아 초록을 확인</b>함</div>

<div class="box">⚠️ <b>AI는 없는 자료를 진짜처럼 만들어 냅니다.</b><br>
제목도 그럴듯하고 저자와 연도까지 붙어 있는데 찾아보면 존재하지 않아요. 이걸 <b>할루시네이션</b>이라고 합니다.<br>
<b>규칙은 하나입니다 — AI가 알려준 자료는 원 출처를 직접 열어 확인한다.</b> 못 찾으면 쓰지 않습니다.</div>

<div class="box">🎤 <b>구술 발표가 확인 지점입니다.</b><br>
AI의 도움을 받아 계획서를 썼더라도, <b>자기 연구를 자기 말로 설명하고 질문에 답할 수 있어야</b> 합니다.
답하지 못하면 그 내용은 채점에서 빠질 수 있어요.</div>

<div class="box">💡 <b>연구 질문 · 결과 해석 · 한계와 개선 방향</b> 이 셋은 <b>반드시 본인 판단</b>으로 쓰세요.
AI 글로 채우면 해당 항목이 채점에서 제외됩니다.</div>"""

# ══════════════════════════════ 허브 ══════════════════════════════
HUB = """
<section class="learn">
<h2>평가는 세 번입니다</h2>
<table>
<tr><th>구분</th><th>언제</th><th>무엇</th><th>반영</th></tr>
<tr><td><b>수행평가 1</b></td><td>9월 3주<br><i>17차시 제출</i></td><td>선행 연구 분석 · 내 주제 설정 <i>(서술형)</i></td><td><b>30%</b></td></tr>
<tr><td><b>수행평가 2</b></td><td>9월 5주<br><i>23차시 · 24~25차시</i></td><td>연구 계획서 + 구술 발표</td><td><b>40%</b></td></tr>
<tr><td>1차 정기시험</td><td>10월 12~15일</td><td>객관식 <i>(서술형 없음)</i></td><td><b>30%</b></td></tr>
</table>

<div class="box">📌 성취도는 <b>A · B · C 3단계</b>이고 <b>석차등급은 나오지 않습니다.</b><br>
원점수 80점 이상 A · 60점 이상 B · 60점 미만 C</div>

""" + 등급표 + """

<h3>「평가 주간」이란</h3>
<div class="box">🗓️ 수행평가를 <b>완성해서 내는 주</b>를 말합니다.<br>
<b>그날 한 번에 쓰는 시험이 아닙니다.</b> 주간 안 여러 차시에 걸쳐 <b>수업 시간에</b> 나누어 씁니다.<br>
주간 안에 결석하면 <b>같은 주간의 다른 차시</b>에 이어서 쓰면 됩니다.</div>

<h3>못 냈을 때</h3>
<p>사유와 관계없이 <b>추가로 낼 기회를 계속 줍니다.</b> 문항과 요소를 따로 채점하므로 하나를 놓쳐도 전체가 0점이 되지 않습니다.</p>
<div class="box">⚠️ <b>구술만 예외입니다.</b> 계획서는 나중에 낼 수 있지만 구술은 그럴 수 없어요.
결석했으면 <b>따로 시간을 잡아</b> 봅니다.</div>

</section>

<section class="learn">
""" + AI지침 + """
</section>
"""

# ══════════════════════════════ 수행평가 1 ══════════════════════════════
T1 = """
<section class="learn">
<h2>문항 ① 선행 연구 분석</h2>
<div class="qbox"><b>[문항]</b> 완성된 연구 <b>2편</b>을 찾아 읽고, 각각 ① 무엇이 궁금했는가 ② 무엇으로 어떻게 알아냈는가 ③ 결론이 무엇인가를 정리하시오.
<b>학술 데이터베이스에서 찾은 논문·연구 보고서로 한다.</b> <i>(초록을 읽고 정리한다.)</i><br>
두 편 중 한 편을 골라, <b>같은 주제를 사회나 과학 과제 연구로 다룬다면 무엇이 달라지는지</b> 서술하시오.</div>

<div class="cmp">
<div class="good"><h5>⭕ 이렇게 <span class="gr">A</span></h5><div class="bd">
<b>연구 1</b> — 「○○ 지역 인구 감소 요인의 데이터 분석」 <i>(DBpia · 초록)</i><br>
① 어떤 지역이 인구 소멸 위험이 큰가, 무엇이 그 차이를 만드는가<br>
② 통계청 인구 자료로 <b>소멸위험지수(20~39세 여성 ÷ 65세 이상)</b>를 지역마다 계산해 비교<br>
③ 지수 0.5 미만 지역이 여럿이었고, 그 지역들은 <b>청년 순유출이 함께</b> 나타남<br><br>
<b>연구 2</b> — 「대중교통 이용 데이터를 활용한 정류장별 혼잡 특성 분석」 <i>(RISS · 초록)</i><br>
① 같은 노선인데 정류장마다 이용객 수가 크게 다른 이유는 무엇인가<br>
② 교통카드 승하차 기록을 <b>정류장별·시간대별로 집계</b>하고 주변 시설과 견주어 비교<br>
③ 출근 시간대는 <b>주거지 인근</b>, 하교 시간대는 <b>학교 인근</b>이 뚜렷하게 높았음<br><br>
<b>④ 사회 과제 연구와의 차이</b> — 연구 1을 사회 과제 연구로 한다면 「왜 젊은 사람이 떠나는가」를 <b>설문이나 면담</b>으로 알아볼 것이다. 정보 과제 연구는 <b>이미 공개된 데이터를 골라 계산식 하나로 답을 냈다.</b>
</div></div>
<div class="bad"><h5>❌ 이러면 <span class="gr">D</span></h5><div class="bd">
<b>연구 1</b> — 인구 감소에 관한 논문<br>
① 인구가 줄어드는 문제를 다뤘다<br>
② <b>통계를 썼다</b><br>
③ <b>인구가 줄고 있다는 결과가 나왔다</b><br><br>
<b>연구 2</b> — 버스 이용에 관한 논문<br>
① 버스 이용에 대해 조사했다<br><br>
<i>(②③ 없음, ④ 없음)</i>
</div></div>
</div>

<div class="split">🔍 <b>무엇이 갈랐나</b><br>
▪ <b>②가 「통계를 썼다」</b> — 도구 이름만 적으면 <b>방법 서술로 보지 않습니다.</b> 「무엇을 어떻게 계산했는지」가 있어야 해요<br>
▪ <b>③이 「인구가 줄고 있다」</b> — <b>숫자나 방향이 없으면</b> 결론으로 보지 않습니다<br>
▪ <b>두 번째 연구가 ①만</b> — 2편 모두 ①②③이 다 있어야 합니다<br>
▪ <b>④가 빠짐</b> — 이것만 없어도 등급이 두 단계 내려갑니다</div>

<h3>등급 기준</h3>
<table><tr><th>등급</th><th>이 정도면</th></tr>
<tr><td><b>A</b></td><td>2편의 ①②③을 각각 정리 + 한 편에 대해 사회·과학 과제 연구와의 차이를 <b>근거를 들어</b> 서술</td></tr>
<tr><td><b>B</b></td><td>2편의 ①②③ 정리 + 차이를 제시</td></tr>
<tr><td><b>C</b></td><td>2편의 ①②③을 정리</td></tr>
<tr><td><b>D</b></td><td>1편의 ①②③을 정리</td></tr>
<tr><td><b>E</b></td><td>연구 자료를 찾아 제목과 내용을 제시</td></tr></table>

<div class="box">📚 <b>어디서 찾나</b> — <b>DBpia</b>(우리 학교 구독) · RISS · KCI · 구글 학술검색<br>
😌 <b>초록을 읽고 정리합니다.</b> 논문 초록에 <b>목적·방법·결과</b>가 다 들어 있고, 그게 바로 ①②③이에요.<br>
⚠️ 기사·블로그·백과사전 항목은 <b>0점</b>입니다. 논문이나 연구 보고서여야 합니다.</div>
</section>

<section class="learn">
<h2>문항 ② 연구 과정 분석</h2>
<div class="qbox"><b>[문항]</b> 문항 ①에서 읽은 연구 중 <b>한 편</b>을 골라, <b>설계 → 수행 → 결론 도출 → 발표</b> 네 단계로 나누고 각 단계에서 <b>그 연구자가 무엇을 했는지</b> 서술하시오.</div>

<div class="cmp">
<div class="good"><h5>⭕ 이렇게 <span class="gr">A</span></h5><div class="bd">
「정류장별 혼잡 특성 분석」을 네 단계로 나누면 이렇다.<br><br>
<b>① 설계</b> — '혼잡하다'는 그대로 잴 수 없으므로 <b>「정류장별·시간대별 승하차 인원」</b>이라는 셀 수 있는 값으로 바꾸고, 비교할 정류장과 시간대 구간을 미리 나눴다.<br>
<b>② 수행</b> — 교통카드 승하차 기록을 정류장별·시간대별로 집계했다.<br>
<b>③ 결론 도출</b> — 집계값을 주변 시설(학교·상가)과 견주어 비교하고, 「출근 시간대는 주거지 인근, 하교 시간대는 학교 인근이 높다」로 정리했다.<br>
<b>④ 발표</b> — 표와 그래프에 단위를 붙여 논문으로 정리했다.
</div></div>
<div class="bad"><h5>❌ 이러면 <span class="gr">C</span></h5><div class="bd">
<b>① 설계</b> — 연구 계획을 세웠다.<br>
<b>② 수행</b> — 데이터를 모았다.<br>
<b>③ 결론 도출</b> — 결과를 정리했다.<br>
<b>④ 발표</b> — <b>발표했다.</b>
</div></div>
</div>

<div class="split">🔍 <b>무엇이 갈랐나</b><br>
▪ 아쉬운 답안은 <b>단계 이름을 되풀이</b>했을 뿐입니다. <b>「무엇을 어떻게」</b>가 없어요<br>
▪ 한 단계의 서술이 <b>한 낱말뿐이면</b> 그 단계는 없는 것으로 봅니다<br>
▪ ⚠️ <b>내 연구 계획을 나누면 안 됩니다.</b> <b>읽은 연구</b>를 나누는 문항이에요</div>

<h3>등급 기준</h3>
<table><tr><th>등급</th><th>이 정도면</th></tr>
<tr><td><b>A</b></td><td>네 단계로 나누고 각 단계에서 한 일을 <b>구체적으로</b>(무엇을·어떻게) 서술</td></tr>
<tr><td><b>B</b></td><td>네 단계로 나누고 각 단계에서 한 일을 서술</td></tr>
<tr><td><b>C</b></td><td>세 단계 이상으로 나누고 각 단계에서 한 일을 서술</td></tr>
<tr><td><b>D</b></td><td>두 단계 이상으로 나누어 서술</td></tr>
<tr><td><b>E</b></td><td>연구 과정에 단계가 있음을 서술</td></tr></table>

<div class="box">💡 단계 이름이 교과서와 달라도 됩니다. <b>준비–실행–정리–공유</b>처럼 써도 네 단계의 기능이 구분되면 인정해요.
「발표」를 「논문 작성」·「보고서 작성」으로 바꿔 써도 됩니다.</div>
</section>

<section class="learn">
<h2>문항 ③ 내 주제와 방법 설정</h2>
<div class="qbox"><b>[문항]</b> 읽은 연구에서 배운 점을 바탕으로 <b>자신의 연구 질문</b>을 한 문장으로 정하고, ① 왜 이 주제를 골랐는지(<b>읽은 연구와 연결지어</b>) ② <b>무엇으로</b> ③ <b>어떻게</b> 답을 낼 것인지 ④ 미리 걱정되는 점은 무엇인지 서술하시오.</div>

<div class="cmp">
<div class="good"><h5>⭕ 이렇게 <span class="gr">A</span></h5><div class="bd">
<b>내 연구 질문</b> — 우리 동네 버스 정류장 세 곳의 <b>시간대별 이용객 수는 얼마나 다른가?</b><br><br>
<b>① 왜 골랐나</b> — 등굣길에 어떤 정류장은 사람이 넘치고 다음 정류장은 비어 있는 게 궁금했다. 읽은 연구 2가 <b>'혼잡'을 '시간대별 승하차 인원'으로 바꿔 잰 것</b>을 보고, 나도 '붐빈다'를 셀 수 있는 값으로 바꿔 정했다.<br>
<b>② 무엇으로</b> — 공공데이터포털 「정류장별 시간대별 승하차 인원」 지난달 자료<br>
<b>③ 어떻게</b> — 정류장 3곳의 시간대별 평균을 스프레드시트로 내고 막대그래프로 비교한다. 차이가 가장 큰 시간대를 찾아 답한다.<br>
<b>④ 미리 걱정되는 점</b> — 같은 정류장이 데이터에 여러 이름으로 나뉘어 있을 수 있다. <b>그러면 이름을 합쳐 세는 작업이 먼저 필요하다.</b>
</div></div>
<div class="bad"><h5>❌ 이러면 <span class="gr">E</span></h5><div class="bd">
<b>내 연구 질문</b> — <b>버스 정류장에 대하여</b><br><br>
<b>① 왜 골랐나</b> — 평소에 관심이 있었다.<br>
<b>② 무엇으로</b> — 인터넷 자료<br>
<b>③ 어떻게</b> — 조사해서 정리한다.<br>
<b>④</b> — <i>(없음)</i>
</div></div>
</div>

<div class="split">🔍 <b>무엇이 갈랐나</b><br>
▪ <b>「~에 대하여」는 질문이 아닙니다.</b> 무엇과 무엇을 견주는지 드러나야 합니다<br>
▪ <b>①에 읽은 연구와의 연결이 없음</b> — 「평소에 관심이 있었다」로는 안 됩니다<br>
▪ <b>②가 「인터넷 자료」</b> — 어느 사이트의 무슨 자료인지 있어야 합니다<br>
▪ <b>④가 빠짐</b> — 미리 걱정되는 점과 대비가 있어야 합니다</div>

<h3>등급 기준</h3>
<table><tr><th>등급</th><th>이 정도면</th></tr>
<tr><td><b>A</b></td><td>연구 질문을 <b>답할 수 있는 한 문장</b>으로 쓰고, <b>읽은 연구를 근거로</b> 선정 이유를 밝히고, 무엇으로·어떻게와 <b>걱정되는 점</b>까지 서술</td></tr>
<tr><td><b>B</b></td><td>연구 질문 한 문장 + 무엇으로 어떻게 + 읽은 연구와 연결</td></tr>
<tr><td><b>C</b></td><td>연구 질문 한 문장 + 무엇으로 어떻게</td></tr>
<tr><td><b>D</b></td><td>연구 질문과 사용할 데이터 또는 장치를 서술</td></tr>
<tr><td><b>E</b></td><td>관심 있는 주제를 제시</td></tr></table>

<div class="box">💡 <b>①의 연결은 「저렇게는 안 하겠다」도 인정</b>됩니다. 따라 하든 반대로 가든, <b>읽은 것이 내 결정에 영향을 줬다</b>는 게 보이면 돼요.<br>
⚠️ <b>검색 한 번으로 답이 나오는 질문</b>(「미세먼지는 왜 나쁜가?」)은 <b>최저점</b>입니다.</div>
</section>
"""

# ══════════════════════════════ 수행평가 2 ══════════════════════════════
T2 = """
<section class="learn">
<h2>요소 ① 연구 계획서</h2>
<p class="lead">양식 <b>8개 항목</b>을 채웁니다. 등급을 가르는 건 <b>③④⑤가 서로 맞물리는가</b>예요.</p>

<h3>📋 연구 계획서 양식 — 여덟 칸</h3>
<p><b>③④⑤는 예시를 채워 두었습니다.</b> 서로 어떻게 맞물리는지 보세요. <b>⑦⑧은 비워 두었습니다 — 직접 쓰는 칸입니다.</b></p>

<table>
<tr><th>#</th><th>항목</th><th>예시</th></tr>
<tr><td>①</td><td><b>연구 제목</b></td><td>버스 정류장별 시간대 이용객 수 비교</td></tr>
<tr><td>②</td><td><b>연구 동기</b></td><td>등굣길에 어떤 정류장은 사람이 넘치는데 다음 정류장은 비어 있어서 궁금했다.</td></tr>
<tr><td><b>③</b></td><td><b>연구 질문</b></td><td>우리 동네 버스 정류장 세 곳의 <b>시간대별 이용객 수는 얼마나 다른가?</b></td></tr>
<tr><td><b>④</b></td><td><b>사용할 데이터<br>또는 장치·프로그램</b></td><td>공공데이터포털 「정류장별 시간대별 승하차 인원」 지난달 자료<br><i>(정류장 3곳 · 평일만)</i></td></tr>
<tr><td><b>⑤</b></td><td><b>분석·구현 방법과 도구</b></td><td>구글 스프레드시트로 정류장별·시간대별 <b>평균</b>을 내고 <b>막대그래프</b>로 비교한다. 차이가 가장 큰 시간대를 찾는다.</td></tr>
<tr><td>⑥</td><td><b>연구 절차</b></td><td>1주 자료 내려받기 → 2주 정류장 이름 정리 → 3주 평균 계산 → 4주 그래프와 정리</td></tr>
<tr><td><b>⑦</b></td><td><b>예상 결과</b></td><td class="blank">직접 쓰는 칸입니다</td></tr>
<tr><td><b>⑧</b></td><td><b>예상되는 어려움</b></td><td class="blank">직접 쓰는 칸입니다</td></tr>
</table>

<div class="split">🔍 <b>③④⑤를 이어서 읽어 보세요</b><br>
③ <b>「얼마나 다른가」</b>를 묻습니다 → ④ 승하차 <b>인원 수</b>가 있으면 셀 수 있습니다 → ⑤ <b>평균을 비교</b>하면 「얼마나」에 답이 나옵니다.<br>
세 칸이 <b>하나의 줄기</b>로 이어집니다. 이게 맞물린다는 뜻이에요.</div>

<h3>⭐ 「③④⑤가 맞물린다」는 이런 뜻입니다</h3>
<div class="cmp">
<div class="good"><h5>⭕ 맞물림</h5><div class="bd">
<b>③ 연구 질문</b><br>정류장 세 곳의 이용객은 <b>얼마나 다른가</b><br><br>
<b>④ 데이터</b><br>공공데이터 승하차 인원<br><br>
<b>⑤ 방법</b><br>정류장별 평균을 내어 막대그래프로 비교<br><br>
<i>→ ④로 ③에 답할 수 있고, ⑤로 ④를 다룰 수 있다</i>
</div></div>
<div class="bad"><h5>❌ 안 맞물림</h5><div class="bd">
<b>③ 연구 질문</b><br>사람들은 <b>왜</b> 이 정류장을 많이 쓰는가<br><br>
<b>④ 데이터</b><br>승하차 인원 데이터<br><br>
<b>⑤ 방법</b><br>평균 비교<br><br>
<i>→ <b>「왜」는 이 데이터로 답할 수 없다.</b> 설문이 필요하다</i>
</div></div>
</div>

<div class="split">🔍 <b>세 물음에 모두 「예」여야 맞물린 겁니다</b><br>
1. ④의 데이터·장치로 ③의 질문에 <b>답할 수 있는가</b><br>
2. ⑤의 방법으로 ④의 데이터를 <b>다룰 수 있는가</b><br>
3. ⑤의 결과가 ③의 질문 형태와 <b>맞는가</b> <i>(비교 질문 → 비교 방법)</i></div>

<h3>등급 기준</h3>
<table><tr><th>등급</th><th>이 정도면</th></tr>
<tr><td><b>A</b></td><td>8개 항목을 다 쓰고 <b>③④⑤가 맞물리며</b>, ⑦ 예상 결과가 ③에 답하는 형태이고, ⑧ 어려움에 <b>대비 방법까지</b> 적었다</td></tr>
<tr><td><b>B</b></td><td>8개 항목을 다 쓰고 ③④⑤가 맞물린다</td></tr>
<tr><td><b>C</b></td><td>8개 항목을 다 썼다</td></tr>
<tr><td><b>D</b></td><td>6개 항목 이상</td></tr>
<tr><td><b>E</b></td><td>4개 항목 이상</td></tr></table>

<h3>⑦·⑧에서 자주 깎입니다</h3>
<div class="cmp">
<div class="good"><h5>⭕ 이렇게</h5><div class="bd">
<b>⑦ 예상 결과</b><br>등교 시간대(7~8시)에 학교 앞 정류장이 다른 두 곳보다 <b>1.5배 이상</b> 많을 것이다<br><br>
<b>⑧ 예상되는 어려움</b><br>같은 정류장이 여러 이름으로 나뉘어 있을 수 있다.<br><b>→ 이름 목록을 먼저 뽑아 합치는 작업을 한다</b>
</div></div>
<div class="bad"><h5>❌ 이러면 깎임</h5><div class="bd">
<b>⑦ 예상 결과</b><br><b>잘 나올 것 같다</b><br><i>(숫자도 방향도 없음)</i><br><br>
<b>⑧ 예상되는 어려움</b><br><b>시간이 부족할 것 같다</b><br><i>(대비 방법 없음 · 연구의 어려움도 아님)</i>
</div></div>
</div>
</section>

<section class="learn">
<h2>요소 ② 구술 발표</h2>
<p class="lead"><b>교실 앞에서 발표</b>합니다. 1인 <b>3분</b>, 이어서 선생님 질문 2개. 설명할 것은 <b>셋뿐</b>입니다.</p>

<h3>이런 모습입니다</h3>
<div class="talk">
<span class="who">학생</span> 제 연구 질문은 <b>「우리 동네 버스 정류장 세 곳의 시간대별 이용객 수가 얼마나 다른가」</b>입니다.
등굣길에 어떤 정류장은 사람이 넘치는데 다음 정류장은 비어 있어서 궁금했어요. <i>(20초)</i><br><br>
공공데이터포털에 <b>정류장별·시간대별 승하차 인원</b>이 공개돼 있어서 지난달 자료를 받았습니다.
정류장 세 곳을 골라 <b>시간대별 평균</b>을 스프레드시트로 내고 <b>막대그래프</b>로 비교할 계획입니다.
차이가 가장 큰 시간대를 찾으면 질문에 답이 됩니다. <i>(80초)</i><br><br>
예상으로는 <b>등교 시간대에 학교 앞 정류장이 1.5배쯤 많을 것</b> 같습니다.
읽은 논문에서도 하교 시간대에 학교 인근이 높게 나왔거든요. <i>(40초)</i>
</div>
<div class="talk">
<span class="who">선생님</span> 그 데이터로 그 질문에 정말 답이 나옵니까?<br>
<span class="who">학생</span> 네. 질문이 <b>「얼마나 다른가」</b>라서 <b>평균을 비교하면 답이 나옵니다.</b>
만약 <b>「왜 다른가」</b>였다면 이 데이터만으로는 안 되고 설문이 필요했을 거예요.
</div>
<div class="talk">
<span class="who">선생님</span> 데이터를 못 구하면 어떻게 할 겁니까?<br>
<span class="who">학생</span> 자료는 이미 받아 뒀는데, 열어 보니 <b>같은 정류장이 여러 이름으로</b> 나뉘어 있었습니다.
그래서 <b>이름을 합치는 작업을 먼저</b> 하려고 합니다. 그래도 안 되면 정류장 수를 두 곳으로 줄이겠습니다.
</div>

<div class="split">🔍 <b>이 발표가 A등급인 이유</b><br>
▪ 셋(질문 · 무엇으로 어떻게 · 예상 결과)을 <b>다 말했습니다</b><br>
▪ <b>계획서를 읽은 게 아니라 자기 말</b>입니다 — "궁금했어요", "받아 뒀는데" 같은 표현<br>
▪ 발문에 <b>자기 계획을 근거로</b> 답했습니다 — 「질문이 '얼마나'라서 평균 비교면 된다」</div>

<h3>선생님이 물을 질문 5개</h3>
<table><tr><th>#</th><th>질문</th></tr>
<tr><td>1</td><td>그 데이터(장치)로 그 질문에 정말 답이 나옵니까?</td></tr>
<tr><td>2</td><td>데이터를 못 구하거나 장치가 안 되면 어떻게 할 겁니까?</td></tr>
<tr><td>3</td><td>예상 결과가 그렇게 나올 거라고 보는 근거는 무엇입니까?</td></tr>
<tr><td>4</td><td>이 연구에서 가장 어려울 것 같은 지점은 어디입니까?</td></tr>
<tr><td>5</td><td>읽은 논문에서 무엇을 가져왔습니까?</td></tr></table>
<p>이 중 <b>여러분 계획에 맞는 2개</b>를 묻습니다. 다섯 개 답을 <b>한 줄씩</b> 적어 두면 충분해요.</p>

<div class="box">✅ <b>걱정 안 해도 되는 것</b><br>
▪ <b>계획서를 손에 들고 봐도 됩니다.</b> 다만 문장을 그대로 읽으면 A등급은 안 나와요<br>
▪ <b>말이 유창한지, 목소리가 큰지는 채점하지 않습니다</b><br>
▪ 3분을 못 채워도 <b>셋을 다 설명했으면 감점 없습니다</b></div>

<h3>등급 기준</h3>
<table><tr><th>등급</th><th>이 정도면</th></tr>
<tr><td><b>A</b></td><td>셋을 <b>계획서를 읽지 않고 자기 말로</b> 설명 + 발문 2개에 <b>내 계획을 근거로</b> 답변</td></tr>
<tr><td><b>B</b></td><td>셋을 자기 말로 설명 + 발문 2개에 답변</td></tr>
<tr><td><b>C</b></td><td>셋을 설명 + 발문 1개에 답변</td></tr>
<tr><td><b>D</b></td><td>셋 중 둘 이상을 설명</td></tr>
<tr><td><b>E</b></td><td>자신의 연구 주제를 말함</td></tr></table>
</section>
"""

io.open('answer-guide.html','w',encoding='utf-8').write(
    page('수행평가 안내 · 정보과제연구', '수행평가 안내', '수행평가 안내',
         '무엇을 · 언제 · 어떻게 평가하는지', HUB, NAV_HUB))
io.open('answer-task1.html','w',encoding='utf-8').write(
    page('수행평가 1 · 정보과제연구', '수행평가 1 · 30%', '선행 연구 분석 · 내 주제 설정',
         '문항별 답안 예시와 등급 기준', T1, NAV_T1))
io.open('answer-task2.html','w',encoding='utf-8').write(
    page('수행평가 2 · 정보과제연구', '수행평가 2 · 40%', '연구 계획서 · 구술 발표',
         '요소별 답안 예시와 등급 기준', T2, NAV_T2))
for f in ('answer-guide.html','answer-task1.html','answer-task2.html'):
    print('  ✅ %-22s (%s bytes)' % (f, format(os.path.getsize(f), ',')))
