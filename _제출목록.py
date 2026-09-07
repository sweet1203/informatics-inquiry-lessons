# -*- coding: utf-8 -*-
"""assignments.json 생성 — check.html(내 제출 확인)이 읽는 차시·항목 목록.

차시정의.py 의 LESSONS 를 그대로 따라가므로, 차시를 보관하거나 문항을 고치면
이 스크립트를 다시 돌리기만 하면 조회 화면이 따라옵니다.

⚠️ 이걸 안 돌리면 보관한 차시가 조회 화면에 「미제출」로 남습니다.
"""
import io, json, os, re
import 차시정의 as C


def strip(html):
    """문항 텍스트에서 태그를 걷어낸다. check.html 은 평문으로 보여 준다."""
    t = re.sub(r'<[^>]+>', '', str(html))
    return re.sub(r'\s+', ' ', t).strip()


lessons = []
for l in sorted(C.LESSONS, key=lambda x: x['n']):
    items = []
    if l.get('open'):
        items.append({
            "id": "생각나누기",
            "label": "생각나누기",
            "questions": [strip(q['q']) for q in l['open']],
        })
    if l.get('proj'):
        items.append({
            "id": "프로젝트",
            "label": "내 연구로 가져오기",
            "questions": [strip(q['q']) for q in l['proj']],
        })
    if not items:
        continue
    lessons.append({
        "n": l['n'],
        "href": "lesson%02d.html" % l['n'],
        "title": l['title'],
        "note": l.get('subtitle', ''),
        "items": items,
    })

data = {"lessons": lessons}
with io.open('assignments.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
    f.write('\n')

칸 = sum(len(x['items']) for x in lessons)
print('  ✅ assignments.json  (차시 %d개 · 칸 %d개 · %s bytes)'
      % (len(lessons), 칸, format(os.path.getsize('assignments.json'), ',')))
