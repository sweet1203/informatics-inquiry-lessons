/**
 * 정보 과제 연구 — 제출 + 조회 (이 파일 하나로 교체해도 됩니다)
 *
 * 설치
 * 1. 제출이 쌓이는 스프레드시트 → 확장 프로그램 → Apps Script
 * 2. 기존 코드를 전부 지우고 이 파일을 붙여 넣는다.
 * 3. 저장 후: 배포 → 배포 관리 → 기존 웹 앱의 연필 → 버전 「새 버전」 → 배포
 *    ※ 「새 배포」를 누르면 URL 이 바뀌어 차시 제출이 끊깁니다. 반드시 기존 배포를 수정하세요.
 *
 * 이 스크립트가 하는 일
 * - doPost: 차시 HTML 에서 학생이 낸 답을 제출 탭에 한 줄 추가 (기존과 같은 역할)
 * - doGet:  학번·이름·개별비번이 맞으면 그 학생 제출만 돌려줌
 *
 * 하지 않는 일
 * - 이미 쌓인 제출 행을 지우거나 고치지 않음
 * - 명단 탭(A 학번 / B 이름 / C 개별비번)은 읽기만 함
 * - 차시 HTML · Vercel 사이트는 건드리지 않음
 *
 * 명단 탭 이름: 명단 (또는 명단시트 / 명렬)
 * 제출 탭: 명단이 아닌 탭. 「제출」 탭이 있으면 거기로 넣고,
 *          없으면 명단을 제외한 탭 중 데이터가 가장 많은 곳으로 넣습니다.
 */

const ROSTER_NAMES = ["명단", "명단시트", "명렬"];
const SUBMIT_NAMES = ["제출", "응답", "기록"];
const FAIL_LIMIT = 8;
const FAIL_MINUTES = 10;

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    const p = (e && e.parameter) || {};
    const sheet = submitSheet_();
    const values = [
      new Date(),
      p.n || "",
      p.sid || "",
      p.name || "",
      p.kind || "",
      p.item || "",
      p.body || ""
    ];
    const lastCol = Math.max(sheet.getLastColumn(), 7);
    const header = sheet.getLastRow() >= 1
      ? sheet.getRange(1, 1, 1, lastCol).getValues()[0]
      : [];
    const map = colMap_(header);
    if (map.header) {
      const row = [];
      for (let i = 0; i < lastCol; i++) row[i] = "";
      row[map.when] = values[0];
      row[map.n] = values[1];
      row[map.sid] = values[2];
      row[map.name] = values[3];
      row[map.kind] = values[4];
      row[map.item] = values[5];
      row[map.body] = values[6];
      sheet.appendRow(row);
    } else {
      if (sheet.getLastRow() === 0) {
        sheet.appendRow(["시각", "차시", "학번", "이름", "구분", "항목", "내용"]);
      }
      sheet.appendRow(values);
    }
    return ContentService.createTextOutput("ok");
  } finally {
    lock.releaseLock();
  }
}

function doGet(e) {
  const p = (e && e.parameter) || {};
  const cb = safeCallback_(p.callback);
  let out;
  try {
    out = lookup_(p);
  } catch (err) {
    out = { ok: false, reason: "error" };
  }
  return ContentService
    .createTextOutput(cb + "(" + JSON.stringify(out) + ")")
    .setMimeType(ContentService.MimeType.JAVASCRIPT);
}

function lookup_(p) {
  const sid = normSid_(p.sid);
  const name = normName_(p.name);
  const pw = String(p.pw == null ? "" : p.pw).trim();
  if (!sid || !name || !pw) return { ok: false, reason: "auth" };
  if (tooManyFails_(sid)) return { ok: false, reason: "lockout" };

  const roster = rosterSheet_();
  if (!roster) return { ok: false, reason: "no-roster" };

  const last = roster.getLastRow();
  if (last < 2) return { ok: false, reason: "auth" };
  const rows = roster.getRange(2, 1, last - 1, 3).getValues();

  let matched = null;
  for (let i = 0; i < rows.length; i++) {
    const rSid = normSid_(rows[i][0]);
    const rName = normName_(rows[i][1]);
    const rPw = String(rows[i][2] == null ? "" : rows[i][2]).trim();
    if (rSid && rSid === sid && rName === name && rPw === pw) {
      matched = { sid: rSid, name: String(rows[i][1]).trim() };
      break;
    }
  }
  if (!matched) {
    recordFail_(sid);
    return { ok: false, reason: "auth" };
  }

  return {
    ok: true,
    sid: matched.sid,
    name: matched.name,
    submissions: collectSubmissions_(matched.sid)
  };
}

function rosterSheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  for (let i = 0; i < ROSTER_NAMES.length; i++) {
    const sh = ss.getSheetByName(ROSTER_NAMES[i]);
    if (sh) return sh;
  }
  return null;
}

function isRoster_(name) {
  return ROSTER_NAMES.indexOf(name) !== -1;
}

function submitSheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  for (let i = 0; i < SUBMIT_NAMES.length; i++) {
    const sh = ss.getSheetByName(SUBMIT_NAMES[i]);
    if (sh) return sh;
  }
  const others = ss.getSheets().filter(function (sh) {
    return !isRoster_(sh.getName());
  });
  if (!others.length) return ss.insertSheet("제출");
  others.sort(function (a, b) {
    return b.getLastRow() - a.getLastRow();
  });
  return others[0];
}

function collectSubmissions_(sid) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const out = [];
  ss.getSheets().forEach(function (sh) {
    if (isRoster_(sh.getName())) return;
    const values = sh.getDataRange().getValues();
    if (!values.length) return;
    const map = colMap_(values[0]);
    const start = map.header ? 1 : 0;
    for (let r = start; r < values.length; r++) {
      const row = values[r];
      const rowSid = normSid_(row[map.sid]);
      if (!rowSid || rowSid !== sid) continue;
      const whenRaw = row[map.when];
      let when = "";
      if (whenRaw instanceof Date) {
        when = Utilities.formatDate(whenRaw, "Asia/Seoul", "yyyy-MM-dd HH:mm");
      } else if (whenRaw) {
        when = String(whenRaw);
      }
      out.push({
        n: Number(row[map.n]) || String(row[map.n] || "").trim(),
        item: String(row[map.item] || "").trim(),
        kind: String(row[map.kind] || "").trim(),
        body: String(row[map.body] || ""),
        when: when
      });
    }
  });
  return out;
}

function colMap_(headerRow) {
  const idx = { when: 0, n: 1, sid: 2, name: 3, kind: 4, item: 5, body: 6, header: false };
  const aliases = {
    when: ["시각", "시간", "타임스탬프", "timestamp", "when", "일시"],
    n: ["차시", "차시번호", "n", "lesson"],
    sid: ["학번", "sid", "id"],
    name: ["이름", "성명", "name"],
    kind: ["구분", "kind", "종류"],
    item: ["항목", "item", "과제"],
    body: ["내용", "본문", "body", "답", "제출내용"]
  };
  const found = {};
  (headerRow || []).forEach(function (cell, i) {
    const k = String(cell == null ? "" : cell).trim().toLowerCase();
    if (!k) return;
    Object.keys(aliases).forEach(function (field) {
      if (aliases[field].indexOf(k) !== -1) found[field] = i;
    });
  });
  if (found.sid != null && (found.n != null || found.item != null || found.body != null)) {
    idx.header = true;
    Object.keys(found).forEach(function (k) { idx[k] = found[k]; });
  }
  return idx;
}

function normSid_(v) {
  if (v == null || v === "") return "";
  if (typeof v === "number") return String(Math.round(v));
  return String(v).trim().replace(/\.0$/, "");
}

function normName_(v) {
  if (v == null) return "";
  return String(v).trim().normalize("NFC").replace(/\s+/g, "");
}

function failKey_(sid) {
  return "fail_" + sid;
}

function tooManyFails_(sid) {
  const n = Number(CacheService.getScriptCache().get(failKey_(sid)) || "0");
  return n >= FAIL_LIMIT;
}

function recordFail_(sid) {
  const cache = CacheService.getScriptCache();
  const key = failKey_(sid);
  const n = Number(cache.get(key) || "0") + 1;
  cache.put(key, String(n), FAIL_MINUTES * 60);
}

function safeCallback_(raw) {
  const s = String(raw || "callback");
  return /^[A-Za-z_][A-Za-z0-9_]*$/.test(s) ? s : "callback";
}
