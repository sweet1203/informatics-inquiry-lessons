/**
 * 정보 과제 연구 — 제출 + 조회
 *
 * 시트 구조
 * - 명단: A 학번 / B 이름 / C 개별비번
 * - 01차시, 02차시, … : 그 차시 제출. 차시 번호는 탭 이름에서 읽습니다.
 *
 * 설치: 이 파일로 기존 코드를 교체한 뒤
 * 배포 → 배포 관리 → 기존 웹 앱 연필 → 버전 「새 버전」 → 배포
 */

const ROSTER_NAMES = ["명단", "명단시트", "명렬"];
const TASK_SHEETS = { "1": "수행1", "2": "수행2" };
const FAIL_LIMIT = 8;
const FAIL_MINUTES = 10;

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    const p = (e && e.parameter) || {};
    if (p.task) {
      return ContentService.createTextOutput(taskPost_(p));
    }
    const n = Number(p.n);
    const sheet = lessonSheet_(n, true);
    const item = canonItem_(p.item, p.kind);
    const lastCol = Math.max(sheet.getLastColumn(), 6);
    const header = sheet.getLastRow() >= 1
      ? sheet.getRange(1, 1, 1, lastCol).getValues()[0]
      : [];
    const map = colMap_(header);
    const wide = itemCols_(header);

    if (wide.length && map.sid != null) {
      upsertWide_(sheet, header, map, wide, {
        sid: p.sid || "",
        name: p.name || "",
        item: item,
        body: p.body || "",
        when: new Date()
      });
    } else {
      appendLog_(sheet, header, map, {
        when: new Date(),
        n: n || "",
        sid: p.sid || "",
        name: p.name || "",
        kind: p.kind || "",
        item: item,
        body: p.body || ""
      });
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

  if (p.task) {
    const t = taskLoad_(p.task, matched.sid);
    return {
      ok: true,
      sid: matched.sid,
      name: matched.name,
      task: String(p.task),
      fields: t.fields,
      status: t.status,
      when: t.when
    };
  }

  return {
    ok: true,
    sid: matched.sid,
    name: matched.name,
    sheets: existingLessonNums_(),
    submissions: collectSubmissions_(matched.sid)
  };
}

function existingLessonNums_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const seen = {};
  const nums = [];
  ss.getSheets().forEach(function (sh) {
    const n = lessonNumFromName_(sh.getName());
    if (n == null || seen[n]) return;
    seen[n] = true;
    nums.push(n);
  });
  nums.sort(function (a, b) { return a - b; });
  return nums;
}

function collectSubmissions_(sid) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const out = [];
  ss.getSheets().forEach(function (sh) {
    const sheetName = sh.getName();
    if (skipInLessonScan_(sheetName)) return;
    const values = sh.getDataRange().getValues();
    if (!values.length) return;
    const lessonN = lessonNumFromName_(sheetName);
    const header = values[0];
    const map = colMap_(header);
    const wide = itemCols_(header);
    const start = map.header ? 1 : 0;

    if (wide.length && map.sid != null) {
      for (let r = start; r < values.length; r++) {
        const row = values[r];
        if (normSid_(row[map.sid]) !== sid) continue;
        const when = formatWhen_(row[map.when]);
        wide.forEach(function (col) {
          const body = cellText_(row[col.i]);
          if (!body) return;
          out.push({
            n: lessonN != null ? lessonN : "",
            item: col.item,
            kind: col.kind,
            body: body,
            when: when
          });
        });
      }
      return;
    }

    for (let r = start; r < values.length; r++) {
      const row = values[r];
      const rowSid = sidFromRow_(row, map);
      if (!rowSid || rowSid !== sid) continue;
      const body = cellText_(row[map.body]);
      const item = canonItem_(row[map.item], row[map.kind]);
      if (!body && !item) continue;
      const nRaw = map.n != null ? row[map.n] : "";
      const n = looksLikeLesson_(nRaw) ? Number(nRaw) : lessonN;
      out.push({
        n: n == null ? "" : n,
        item: item,
        kind: cellText_(row[map.kind]),
        body: body,
        when: formatWhen_(row[map.when])
      });
    }
  });
  return out;
}

function lessonNumFromName_(name) {
  const m = String(name).match(/(\d+)\s*차시/);
  if (m) return Number(m[1]);
  if (/^\d{1,2}$/.test(String(name).trim())) return Number(name);
  return null;
}

function lessonSheetName_(n) {
  const num = Number(n);
  if (!num) return "";
  return (num < 10 ? "0" + num : String(num)) + "차시";
}

function lessonSheet_(n, createIfMissing) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const padded = lessonSheetName_(n);
  const plain = Number(n) ? String(Number(n)) + "차시" : "";
  let sh = padded && ss.getSheetByName(padded);
  if (!sh && plain) sh = ss.getSheetByName(plain);
  if (!sh && createIfMissing && padded) {
    sh = ss.insertSheet(padded);
    sh.appendRow(["시각", "학번", "이름", "구분", "항목", "내용"]);
  }
  return sh;
}

function looksLikeLesson_(v) {
  const n = Number(v);
  return n >= 1 && n <= 80;
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

/* 차시 제출 집계에서 건너뛸 시트.
 * 명단 · 수행평가 시트 · 이력 시트는 차시 시트가 아니므로 제외한다.
 * 빠뜨리면 collectSubmissions_ 가 이 시트들을 차시 제출로 오인해
 * 「내 제출 확인」에 엉뚱한 줄이 뜬다. */
function skipInLessonScan_(name) {
  const nm = String(name);
  if (isRoster_(nm)) return true;
  if (/_이력$/.test(nm)) return true;
  for (const k in TASK_SHEETS) {
    if (TASK_SHEETS[k] === nm) return true;
  }
  return false;
}

function colMap_(headerRow) {
  const idx = { when: 0, n: 1, sid: 2, name: 3, kind: 4, item: 5, body: 6, header: false };
  const aliases = {
    when: ["시각", "시간", "타임스탬프", "timestamp", "when", "일시", "제출시각"],
    n: ["차시", "차시번호", "n", "lesson"],
    sid: ["학번", "sid"],
    name: ["이름", "성명", "name"],
    kind: ["구분", "kind", "종류"],
    item: ["항목", "item", "과제"],
    body: ["내용", "본문", "body", "답", "제출내용", "응답"]
  };
  const found = {};
  (headerRow || []).forEach(function (cell, i) {
    const k = String(cell == null ? "" : cell).trim().toLowerCase();
    if (!k) return;
    Object.keys(aliases).forEach(function (field) {
      if (aliases[field].indexOf(k) !== -1) found[field] = i;
    });
  });
  if (found.sid != null) {
    idx.header = true;
    Object.keys(found).forEach(function (k) { idx[k] = found[k]; });
  }
  return idx;
}

function itemCols_(headerRow) {
  const cols = [];
  (headerRow || []).forEach(function (cell, i) {
    const item = canonItem_(cell, "");
    if (item === "생각나누기" || item === "프로젝트") {
      cols.push({
        i: i,
        item: item,
        kind: item === "생각나누기" ? "생기부" : "프로젝트"
      });
    }
  });
  return cols;
}

function canonItem_(item, kind) {
  const a = String(item == null ? "" : item).trim();
  const b = String(kind == null ? "" : kind).trim();
  const s = a + " " + b;
  if (/생각나누기|생기부/.test(s)) return "생각나누기";
  if (/프로젝트|내 연구/.test(s)) return "프로젝트";
  if (a === "생각나누기" || a === "프로젝트") return a;
  return a;
}

function sidFromRow_(row, map) {
  if (map.header && map.sid != null) return normSid_(row[map.sid]);
  for (let i = 0; i < Math.min(row.length, 4); i++) {
    const s = normSid_(row[i]);
    if (s && /^\d{4,6}$/.test(s)) return s;
  }
  return "";
}

function upsertWide_(sheet, header, map, wide, rec) {
  const last = sheet.getLastRow();
  const width = Math.max(sheet.getLastColumn(), header.length);
  const values = last >= 2
    ? sheet.getRange(2, 1, last - 1, width).getValues()
    : [];
  let rowIndex = -1;
  for (let i = 0; i < values.length; i++) {
    if (normSid_(values[i][map.sid]) === normSid_(rec.sid)) {
      rowIndex = i + 2;
      break;
    }
  }
  const col = wide.filter(function (c) { return c.item === rec.item; })[0];
  if (rowIndex === -1) {
    const row = [];
    for (let i = 0; i < width; i++) row[i] = "";
    row[map.sid] = rec.sid;
    if (map.name != null) row[map.name] = rec.name;
    if (map.when != null) row[map.when] = rec.when;
    if (col) row[col.i] = rec.body;
    sheet.appendRow(row);
    return;
  }
  if (col) sheet.getRange(rowIndex, col.i + 1).setValue(rec.body);
  if (map.when != null) sheet.getRange(rowIndex, map.when + 1).setValue(rec.when);
}

function appendLog_(sheet, header, map, rec) {
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(["시각", "학번", "이름", "구분", "항목", "내용"]);
    map = colMap_(["시각", "학번", "이름", "구분", "항목", "내용"]);
  }
  if (map.header) {
    const width = Math.max(sheet.getLastColumn(), 6);
    const row = [];
    for (let i = 0; i < width; i++) row[i] = "";
    if (map.when != null) row[map.when] = rec.when;
    if (map.n != null) row[map.n] = rec.n;
    if (map.sid != null) row[map.sid] = rec.sid;
    if (map.name != null) row[map.name] = rec.name;
    if (map.kind != null) row[map.kind] = rec.kind;
    if (map.item != null) row[map.item] = rec.item;
    if (map.body != null) row[map.body] = rec.body;
    sheet.appendRow(row);
  } else {
    sheet.appendRow([rec.when, rec.sid, rec.name, rec.kind, rec.item, rec.body]);
  }
}

function cellText_(v) {
  if (v == null || v === "") return "";
  if (v instanceof Date) return formatWhen_(v);
  return String(v).trim();
}

function formatWhen_(v) {
  if (v instanceof Date) {
    return Utilities.formatDate(v, "Asia/Seoul", "yyyy-MM-dd HH:mm");
  }
  return v ? String(v) : "";
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

function tooManyFails_(sid) {
  const n = Number(CacheService.getScriptCache().get("fail_" + sid) || "0");
  return n >= FAIL_LIMIT;
}

function recordFail_(sid) {
  const cache = CacheService.getScriptCache();
  const key = "fail_" + sid;
  const n = Number(cache.get(key) || "0") + 1;
  cache.put(key, String(n), FAIL_MINUTES * 60);
}

function safeCallback_(raw) {
  const s = String(raw || "callback");
  return /^[A-Za-z_][A-Za-z0-9_]*$/.test(s) ? s : "callback";
}


/* ═══════════════════════════════════════════════════════════
 * 수행평가 제출 — 수행1 · 수행2
 * 시트 한 행 = 학생 한 명. 「임시저장」을 누를 때마다 같은 행을 덮어씁니다.
 * 열은 보내온 필드 이름으로 자동 생성되므로 폼을 고치면 시트도 따라옵니다.
 * ═══════════════════════════════════════════════════════════ */

const TASK_FIXED = ["학번", "이름", "상태", "최근저장", "최종제출"];

function taskSheet_(task, createIfMissing) {
  const nm = TASK_SHEETS[String(task)];
  if (!nm) return null;
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(nm);
  if (!sh && createIfMissing) {
    sh = ss.insertSheet(nm);
    sh.appendRow(TASK_FIXED);
    sh.setFrozenRows(1);
    sh.setFrozenColumns(2);
  }
  return sh;
}

function taskPost_(p) {
  const sh = taskSheet_(p.task, true);
  if (!sh) return "no-task";
  const sid = normSid_(p.sid);
  if (!sid) return "no-sid";

  let data = {};
  try { data = JSON.parse(p.data || "{}"); } catch (err) { data = {}; }

  const lastCol = Math.max(sh.getLastColumn(), TASK_FIXED.length);
  const header = sh.getRange(1, 1, 1, lastCol).getValues()[0]
    .map(function (v) { return String(v == null ? "" : v).trim(); });

  TASK_FIXED.forEach(function (k) { if (header.indexOf(k) === -1) header.push(k); });
  Object.keys(data).forEach(function (k) { if (header.indexOf(k) === -1) header.push(k); });
  if (header.indexOf("붙여넣기차단") === -1) header.push("붙여넣기차단");
  sh.getRange(1, 1, 1, header.length).setValues([header]);

  const sidCol = header.indexOf("학번");
  const last = sh.getLastRow();
  let target = 0;
  if (last >= 2) {
    const sids = sh.getRange(2, sidCol + 1, last - 1, 1).getValues();
    for (let i = 0; i < sids.length; i++) {
      if (normSid_(sids[i][0]) === sid) { target = i + 2; break; }
    }
  }
  if (!target) target = last + 1;

  let row;
  if (target <= last) {
    row = sh.getRange(target, 1, 1, header.length).getValues()[0];
  } else {
    row = [];
    for (let i = 0; i < header.length; i++) row.push("");
  }

  const put = function (col, val) {
    const i = header.indexOf(col);
    if (i !== -1) row[i] = val;
  };
  const get = function (col) {
    const i = header.indexOf(col);
    return i === -1 ? "" : row[i];
  };
  const now = new Date();
  const submitting = String(p.status || "") === "제출";
  const already = String(get("상태") || "").trim() === "제출";

  put("학번", sid);
  if (String(p.name || "").trim()) put("이름", String(p.name).trim());
  put("상태", (submitting || already) ? "제출" : "임시저장");
  put("최근저장", now);
  if (submitting) put("최종제출", now);
  put("붙여넣기차단", Number(get("붙여넣기차단") || 0) + Number(p.paste || 0));

  /* ⚠️ 빈 값으로는 덮어쓰지 않습니다.
   * 「불러오기」를 하지 않고 저장했을 때 앞서 쓴 내용이 지워지는 것을 막습니다.
   * 학생이 실제로 지우려면 폼에서 「－」 한 글자를 넣게 안내합니다. */
  let 보호 = 0;
  Object.keys(data).forEach(function (k) {
    const v = String(data[k] == null ? "" : data[k]);
    if (!v.trim()) {
      if (String(get(k) || "").trim()) 보호++;
      return;
    }
    put(k, v === "－" ? "" : v);
  });

  sh.getRange(target, 1, 1, header.length).setValues([row]);
  taskLog_(p.task, {
    when: now, sid: sid, name: String(p.name || "").trim(),
    status: submitting ? "제출" : "임시저장",
    paste: Number(p.paste || 0),
    kept: 보호,
    data: data
  });
  return 보호 ? ("ok-kept-" + 보호) : "ok";
}

/* 저장할 때마다 한 줄씩 쌓이는 이력. 되돌릴 일이 생기면 여기서 찾습니다. */
function taskLog_(task, rec) {
  const nm = (TASK_SHEETS[String(task)] || "수행") + "_이력";
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(nm);
  if (!sh) {
    sh = ss.insertSheet(nm);
    sh.appendRow(["시각", "학번", "이름", "상태", "붙여넣기차단", "빈칸보호", "내용(JSON)"]);
    sh.setFrozenRows(1);
  }
  sh.appendRow([rec.when, rec.sid, rec.name, rec.status, rec.paste, rec.kept,
                JSON.stringify(rec.data)]);
}

function taskLoad_(task, sid) {
  const empty = { fields: {}, status: "", when: "" };
  const sh = taskSheet_(task, false);
  if (!sh) return empty;
  const last = sh.getLastRow();
  if (last < 2) return empty;

  const header = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0]
    .map(function (v) { return String(v == null ? "" : v).trim(); });
  const sidCol = header.indexOf("학번");
  if (sidCol === -1) return empty;

  const values = sh.getRange(2, 1, last - 1, header.length).getValues();
  for (let i = 0; i < values.length; i++) {
    if (normSid_(values[i][sidCol]) !== sid) continue;
    const fields = {};
    header.forEach(function (h, j) {
      if (!h || TASK_FIXED.indexOf(h) !== -1 || h === "붙여넣기차단") return;
      fields[h] = cellText_(values[i][j]);
    });
    const stCol = header.indexOf("상태");
    const whCol = header.indexOf("최근저장");
    return {
      fields: fields,
      status: stCol === -1 ? "" : cellText_(values[i][stCol]),
      when: whCol === -1 ? "" : formatWhen_(values[i][whCol])
    };
  }
  return empty;
}
