# -*- coding: utf-8 -*-
"""계획서 예시 페이지 생성 — 스타일은 _생성기.py 의 것을 그대로 가져다 쓴다."""
import io, os, re

src = io.open('_생성기.py', encoding='utf-8').read()
CSS = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
CSS = CSS.replace('{{', '{').replace('}}', '}')          # .format 용 이중 중괄호 되돌리기

EXTRA = """
.rep{border:1px solid var(--line);border-radius:12px;padding:0;margin:18px 0;overflow:hidden}
.rep>h4{margin:0;padding:11px 15px;background:var(--accent);color:var(--ink2);font-size:.98rem}
.rep>div{padding:15px}
.see{background:var(--quiz);border:1px solid var(--quizline);border-radius:0 0 11px 11px;
padding:11px 15px;font-size:.89rem;margin:0}
.see b{color:var(--warn)}
.no{color:#b91c1c}.yes{color:var(--ok)}
@media print{body{background:#fff}section{break-inside:avoid}}
"""

BODY = r"""
<div class="wrap">
<header>
  <span class="chip">참고 자료</span>
  <h1>계획서 예시 — 여덟 칸을 채우면</h1>
  <p class="sub">교과서 계획서 양식(①~⑧)을 실제로 채운 것</p>
</header>

<section class="learn">
<h2>읽는 법</h2>
<p class="lead">각 칸 아래 주황색 상자는 <b>계획서에 들어가는 내용이 아닙니다.</b> 그 칸에서 무엇을 보라는 설명입니다.</p>

<div class="box">이 예시는 트랙 B(피지컬 컴퓨팅)이지만 <b>여덟 칸의 틀은 A·C 트랙도 같습니다.</b><br>
<b><a href="sample-report.html" target="_blank" rel="noopener">참고 보고서</a></b>는 이 계획서로 실제 연구를 끝낸 결과입니다.</div>

<h3>이 계획서 한눈에</h3>
<table>
<tr><th>트랙</th><td>B. 피지컬 컴퓨팅 — 사운드 센서</td></tr>
<tr><th>연구 질문</th><td>교실 소음은 수업 활동의 종류에 따라 얼마나 달라지는가</td></tr>
<tr><th>장치</th><td>아두이노 우노 + 사운드 센서 + RTC 모듈</td></tr>
<tr><th>기간</th><td>사흘 · 1분 간격</td></tr>
</table>
</section>

<section class="learn">
<h2>계획서 전문</h2>

<div style="background:var(--soft);border:1px solid var(--line);border-radius:9px;padding:12px;font-size:.92rem;margin-bottom:6px">
학번 <b>30000</b> &nbsp; 이름 <b>구예시</b> &nbsp; 트랙 <b>B 피지컬</b>
</div>

<div class="rep"><h4>① 연구 제목</h4><div>
수업 활동 유형에 따른 교실 소음 변화 측정 — 아두이노 사운드 센서를 이용하여
</div></div>
<p class="see">👀 <b>제목만 읽고 무엇을 어떻게 하는지 알 수 있어야 합니다.</b><br>
「교실 소음 연구」는 무엇을 하는지 알 수 없습니다.</p>

<div class="rep"><h4>② 연구 동기</h4><div>
지금은 교실이 시끄럽다고 느껴도 <b>어느 활동에서 얼마나 시끄러운지 아는 사람이 없다.</b><br>
활동 유형별 소음 크기를 숫자로 알면 <b>수업 활동을 배치할 때 근거로 쓸 수 있겠다.</b>
</div></div>
<p class="see">👀 <b>「지금은 ○○인데, △△가 되면 좋겠다」 두 문장.</b><br>
앞 문장이 현재 상태, 뒤 문장이 바라는 상태입니다. 그 차이가 연구할 문제입니다.</p>

<div class="rep"><h4>③ 연구 질문</h4><div>
우리 반 교실의 소음은 <b>수업 활동의 종류(강의 · 개별 활동 · 모둠 토의)에 따라 얼마나 달라지는가?</b>
</div></div>
<p class="see">👀 <b>답할 수 있는 한 문장.</b><br>
「얼마나 달라지는가」는 숫자로 답이 나옵니다. 「교실이 왜 시끄러운가」는 답이 안 나옵니다.</p>

<div class="rep"><h4>④ 사용할 데이터 또는 장치·프로그램</h4><div>
<b>아두이노 우노 + 사운드 센서(아날로그) + RTC 모듈(DS1302)</b><br>
교실 뒤편 게시판 아래에 고정 설치하고 <b>1분 간격</b>으로 측정값과 시각을 기록한다.<br>
같은 시각의 <b>수업 활동 유형</b>은 손으로 기록한다. <i>(강의 / 개별 활동 / 모둠 토의)</i>
</div></div>
<p class="see">👀 <b>실제로 가진 것만 씁니다.</b> 사운드 센서와 RTC는 학교 보유 키트에 있습니다.<br>
SD카드 모듈이 없어 <b>상시 로깅은 안 됩니다.</b> 그래서 수업 시간에 PC를 붙여 두고 기록하는 방식으로 정했습니다.</p>

<div class="rep"><h4>⑤ 분석·구현 방법과 도구</h4><div>
<b>구글 스프레드시트</b>로 측정값을 활동 유형별로 나눈 뒤
<b>평균 · 최댓값 · 최솟값</b>을 계산하고 <b>막대그래프</b>로 비교한다.<br>
교시별 변화는 <b>꺾은선그래프</b>로 그린다.
</div></div>
<p class="see">👀 <b>③④⑤가 맞물리는지 여기서 확인합니다.</b><br>
③이 「활동에 따라 얼마나 다른가」(비교) → ④가 활동 유형이 붙은 소음값 → ⑤가 유형별 평균 비교.<br>
세 칸이 같은 방향을 봅니다. 여기가 어긋나면 실행 단계에서 막힙니다.</p>

<div class="rep"><h4>⑥ 연구 절차</h4><div>
<table><tr><th>순서</th><th>할 일</th></tr>
<tr><td>1</td><td>배선 후 시리얼 모니터로 값 확인 · 설치 위치 고정</td></tr>
<tr><td>2</td><td>사흘간 측정 · 같은 시간에 활동 유형 기록</td></tr>
<tr><td>3</td><td>스프레드시트로 옮겨 활동 유형별로 분류</td></tr>
<tr><td>4</td><td>평균·최댓값 계산 후 그래프 작성</td></tr>
<tr><td>5</td><td>결과 해석 및 보고서 작성</td></tr></table>
</div></div>
<p class="see">👀 <b>언제 무엇을 하는지</b>만 있으면 됩니다.</p>

<div class="rep"><h4>⑦ 예상 결과</h4><div>
<b>모둠 토의 때가 가장 높을 것</b>으로 예상한다.
개별 활동보다 <b>1.5배 이상</b> 차이가 날 것 같다.
</div></div>
<p class="see">👀 <b>「잘 나올 것 같다」는 안 됩니다.</b><br>
「1.5배 이상」처럼 써야 결과가 나왔을 때 <b>맞았는지 틀렸는지 견줄 수 있습니다.</b><br>
틀려도 됩니다. 틀린 이유를 쓰면 그게 결과 해석이 됩니다.</p>

<div class="rep"><h4>⑧ 예상되는 어려움</h4><div>
<table><tr><th>어려움</th><th>대비</th></tr>
<tr><td>복도 소리가 섞여 들어올 수 있다</td><td>센서를 복도 반대편에 설치하고, 이동 시간대 값은 따로 표시해 둔다</td></tr>
<tr><td>청소 시간에 센서 위치가 바뀔 수 있다</td><td>고정 테이프로 붙이고 위치를 사진으로 남긴다</td></tr>
<tr><td>사흘로는 자료가 부족할 수 있다</td><td>부족하면 측정 범위를 「사흘간」으로 좁혀서 그 안에서 비교한다</td></tr></table>
</div></div>
<p class="see">👀 <b>어려움만 쓰면 부족합니다.</b> 각각에 <b>대비 방법</b>을 붙입니다.</p>
</section>

<section class="learn">
<h2>제출 전 점검</h2>
<table>
<tr><th>#</th><th>확인할 것</th></tr>
<tr><td>1</td><td>여덟 칸을 <b>모두</b> 채웠는가</td></tr>
<tr><td>2</td><td>③ 연구 질문이 <b>답할 수 있는 한 문장</b>인가</td></tr>
<tr><td>3</td><td>④의 데이터·장치를 <b>실제로 구했는가</b></td></tr>
<tr><td>4</td><td><b>④로 ③에 답할 수 있는가</b></td></tr>
<tr><td>5</td><td><b>⑤로 ④를 다룰 수 있는가</b></td></tr>
<tr><td>6</td><td>⑦ 예상 결과에 <b>숫자나 방향</b>이 있는가</td></tr>
<tr><td>7</td><td>⑧ 어려움마다 <b>대비 방법</b>이 붙었는가</td></tr>
<tr><td>8</td><td>맨 위 <b>학번 · 이름 · 트랙</b>을 적었는가</td></tr>
</table>
</section>

</div>
"""

PAGE = ("<!doctype html>\n<html lang=\"ko\"><head><meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "<title>계획서 예시 · 정보과제연구</title>\n"
        "<style>" + CSS + EXTRA + "</style>\n</head><body>\n" + BODY + "\n</body></html>\n")

with io.open('sample-plan.html', 'w', encoding='utf-8') as f:
    f.write(PAGE)
print(f'  ✅ sample-plan.html  ({os.path.getsize("sample-plan.html"):,} bytes)')
