#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
건대입구 게스트하우스 4개 유닛 + 마포 아현동 취향집 운영 대시보드 생성기.
오늘 날짜 기준 4주(28일) 로테이션 윈도우로 예약/주차/게스트노트 캘린더와
청소 일정, 주차 배정 안내를 만든다. 확인되지 않은 정보는 추측하지 않고
"확인 필요"로 명시한다.
"""
import datetime
import html as htmlmod

TODAY = datetime.date(2026, 8, 20)
WEEKDAY_KR = ['일', '월', '화', '수', '목', '금', '토']

def week_sunday(dt):
    offset = (dt.weekday() + 1) % 7  # days since Sunday
    return dt - datetime.timedelta(days=offset)

WIN_START = week_sunday(TODAY)
WIN_END = WIN_START + datetime.timedelta(days=27)  # 28 days inclusive
ALL_DAYS = [WIN_START + datetime.timedelta(days=i) for i in range(28)]

UNITS = {
    "501": {"name": "더테라스 하우스 501호", "sub": "브라운문", "color": "#2a78d6"},
    "502": {"name": "더블랑 하우스 502호", "sub": "검정문", "color": "#eb6834"},
    "401": {"name": "우드블랑 하우스 401호", "sub": "골드문", "color": "#1baf7a"},
    "402": {"name": "우드블랑 하우스 402호", "sub": "그레이문", "color": "#eda100"},
    "MAPO": {"name": "취향집", "sub": "마포구 아현동", "color": "#e87ba4"},
}
UNIT_ORDER = ["501", "502", "401", "402", "MAPO"]
BUILDING_UNITS = ["501", "502", "401", "402"]  # 주차 규칙이 적용되는 건대입구 4개 유닛

def d(y, m, day):
    return datetime.date(y, m, day)

RESERVATIONS = [
    # 501호 더테라스 하우스
    dict(unit="501", guest="세아 마", ci=d(2026,8,19), co=d(2026,8,20), adults=4, children=0, status="checkout_done"),
    dict(unit="501", guest="병준 전", ci=d(2026,8,20), co=d(2026,8,21), adults=4, children=0, status="hosting"),
    dict(unit="501", guest="현수 양", ci=d(2026,8,21), co=d(2026,8,22), adults=4, children=0, status="confirmed"),
    dict(unit="501", guest="병준 이", ci=d(2026,8,22), co=d(2026,8,23), adults=4, children=0, status="confirmed"),
    dict(unit="501", guest="승주 임", ci=d(2026,8,23), co=d(2026,8,24), adults=5, children=0, status="confirmed"),
    dict(unit="501", guest="서현 김", ci=d(2026,8,25), co=d(2026,8,26), adults=6, children=0, status="confirmed"),
    dict(unit="501", guest="은미 이", ci=d(2026,8,26), co=d(2026,8,27), adults=4, children=0, status="confirmed"),
    dict(unit="501", guest="진우 이", ci=d(2026,8,30), co=d(2026,8,31), adults=4, children=2, status="confirmed"),
    # 502호 더블랑 하우스
    dict(unit="502", guest="원재 장", ci=d(2026,8,19), co=d(2026,8,20), adults=5, children=0, status="checkout_done"),
    dict(unit="502", guest="Kevin 이", ci=d(2026,8,20), co=d(2026,8,21), adults=4, children=0, status="hosting"),
    dict(unit="502", guest="김 진영", ci=d(2026,8,21), co=d(2026,8,22), adults=9, children=0, status="confirmed"),
    dict(unit="502", guest="혜란 강", ci=d(2026,8,22), co=d(2026,8,23), adults=4, children=2, status="confirmed"),
    dict(unit="502", guest="민정 조", ci=d(2026,8,23), co=d(2026,8,24), adults=7, children=0, status="confirmed"),
    dict(unit="502", guest="Dukhwa Kang", ci=d(2026,8,27), co=d(2026,8,28), adults=7, children=0, status="confirmed"),
    dict(unit="502", guest="지혜 강", ci=d(2026,8,29), co=d(2026,8,30), adults=8, children=0, status="confirmed"),
    dict(unit="502", guest="병구 김", ci=d(2026,8,30), co=d(2026,8,31), adults=6, children=4, status="confirmed"),
    dict(unit="502", guest="Jiny Choi", ci=d(2026,9,5), co=d(2026,9,6), adults=8, children=0, status="confirmed"),
    dict(unit="502", guest="인애 나", ci=d(2026,9,12), co=d(2026,9,13), adults=10, children=0, status="confirmed"),
    # 401호 우드블랑 골드문
    dict(unit="401", guest="현수 김", ci=d(2026,8,19), co=d(2026,8,20), adults=3, children=0, status="checkout_done"),
    dict(unit="401", guest="Glenda Galvez", ci=d(2026,8,20), co=d(2026,8,22), adults=5, children=0, status="change_request"),
    dict(unit="401", guest="승준 이", ci=d(2026,8,22), co=d(2026,8,24), adults=1, children=0, status="confirmed"),
    dict(unit="401", guest="신욱 곽", ci=d(2026,8,30), co=d(2026,9,1), adults=4, children=0, status="confirmed"),
    # 402호 우드블랑 그레이문
    dict(unit="402", guest="지원 이", ci=d(2026,8,19), co=d(2026,8,20), adults=3, children=1, status="checkout_done"),
    dict(unit="402", guest="유나 이", ci=d(2026,8,20), co=d(2026,8,21), adults=4, children=0, status="hosting"),
    dict(unit="402", guest="경미 이", ci=d(2026,8,21), co=d(2026,8,22), adults=4, children=0, status="confirmed"),
    dict(unit="402", guest="지웅 이", ci=d(2026,8,22), co=d(2026,8,23), adults=8, children=0, status="confirmed"),
    dict(unit="402", guest="李致姗 李", ci=d(2026,8,23), co=d(2026,8,27), adults=4, children=0, status="confirmed_note", note="얼리체크인 문의 있었음 - 확인 필요"),
    # 마포 취향집
    dict(unit="MAPO", guest="기강 윤", ci=d(2026,8,20), co=d(2026,8,21), adults=6, children=0, status="hosting"),
    dict(unit="MAPO", guest="晓诗 陈 외", ci=d(2026,8,21), co=d(2026,8,22), adults=6, children=0, status="confirmed"),
    dict(unit="MAPO", guest="Yan Ren", ci=d(2026,8,22), co=d(2026,8,27), adults=4, children=2, status="confirmed"),
    dict(unit="MAPO", guest="馨 夏", ci=d(2026,8,28), co=d(2026,8,29), adults=4, children=0, status="confirmed"),
    dict(unit="MAPO", guest="유나 조", ci=d(2026,8,29), co=d(2026,8,30), adults=3, children=0, status="confirmed"),
    dict(unit="MAPO", guest="Yuci Wu", ci=d(2026,9,12), co=d(2026,9,14), adults=6, children=0, status="confirmed"),
]

STATUS_LABEL = {
    "checkout_done": "체크아웃 완료",
    "hosting": "현재 호스팅 중",
    "confirmed": "확정",
    "confirmed_note": "확정",
    "change_request": "예약 변경요청 처리중 - 확인 필요",
}

def esc(s):
    return htmlmod.escape(str(s), quote=True)

def fmt_range(a, b):
    return f"{a.month}/{a.day} - {b.month}/{b.day}"

def guests_label(r):
    g = f"성인 {r['adults']}명"
    if r["children"]:
        g += f", 어린이 {r['children']}명"
    return g

# ---------- index reservations by date ----------
checkins_by_day = {dt: [] for dt in ALL_DAYS}
checkouts_by_day = {dt: [] for dt in ALL_DAYS}
for r in RESERVATIONS:
    if r["ci"] in checkins_by_day:
        checkins_by_day[r["ci"]].append(r)
    if r["co"] in checkouts_by_day:
        checkouts_by_day[r["co"]].append(r)

# same-day turnover detection (checkout + new checkin same unit same day)
same_day_turnover = set()
for dt in ALL_DAYS:
    co_units = {r["unit"] for r in checkouts_by_day[dt]}
    ci_units = {r["unit"] for r in checkins_by_day[dt]}
    same_day_turnover |= (co_units & ci_units) and {dt} or set()

# ---------- build calendar grid HTML (generic) ----------
def day_cell(dt, body_html, extra_class=""):
    in_win = WIN_START <= dt <= WIN_END
    today_cls = " today" if dt == TODAY else ""
    wd = WEEKDAY_KR[(dt.weekday()+1) % 7]
    wd_cls = " sat" if wd == "토" else (" sun" if wd == "일" else "")
    return f'''<div class="cal-day{today_cls} {extra_class}">
  <div class="num">{dt.month}/{dt.day}<span class="wd{wd_cls}">{wd}</span></div>
  {body_html}
</div>'''

def build_calendar_grid(day_body_fn):
    weeks = [ALL_DAYS[i:i+7] for i in range(0, 28, 7)]
    out = ['<div class="cal-wd-row">']
    for i, wd in enumerate(WEEKDAY_KR):
        cls = " sat" if wd == "토" else (" sun" if wd == "일" else "")
        out.append(f'<div class="cal-wd{cls}">{wd}</div>')
    out.append('</div>')
    for week in weeks:
        out.append('<div class="cal-grid">')
        for dt in week:
            out.append(day_cell(dt, day_body_fn(dt)))
        out.append('</div>')
    return "\n".join(out)

# ----- Calendar 1: reservation calendar (check-in / check-out) -----
def reservation_day_body(dt):
    lines = []
    for r in sorted(checkins_by_day[dt], key=lambda r: UNIT_ORDER.index(r["unit"])):
        c = UNITS[r["unit"]]["color"]
        lines.append(f'<div class="evt in" style="background:{c}1a;color:{c};border-left:3px solid {c};">'
                      f'IN {esc(r["unit"] if r["unit"]!="MAPO" else "마포")} · {esc(r["guest"])} ({guests_label(r)})</div>')
    for r in sorted(checkouts_by_day[dt], key=lambda r: UNIT_ORDER.index(r["unit"])):
        c = UNITS[r["unit"]]["color"]
        lines.append(f'<div class="evt out" style="background:{c}0d;color:{c};border-left:3px solid {c}66;">'
                      f'OUT {esc(r["unit"] if r["unit"]!="MAPO" else "마포")} · {esc(r["guest"])}</div>')
    if not lines:
        return '<div class="empty-hint">-</div>'
    return '<div class="evt-list">' + "".join(lines) + '</div>'

# ----- Calendar 2: parking calendar (건대입구 4개 유닛만 해당) -----
def parking_day_body(dt):
    lines = []
    for r in sorted(checkins_by_day[dt], key=lambda r: UNIT_ORDER.index(r["unit"])):
        if r["unit"] not in BUILDING_UNITS:
            continue
        if r["status"] == "checkout_done":
            continue
        c = UNITS[r["unit"]]["color"]
        lines.append(f'<div class="pk unknown" style="border-left:3px solid {c};">'
                      f'{esc(r["unit"])} {esc(r["guest"])} · 주차 확인 필요</div>')
    if not lines:
        return '<div class="empty-hint">-</div>'
    return '<div class="evt-list">' + "".join(lines) + '</div>'

# ----- Calendar 3: guest note calendar (얼리체크인/레이트체크아웃/바베큐/대가족 등) -----
def guestnote_day_body(dt):
    lines = []
    for r in sorted(checkins_by_day[dt], key=lambda r: UNIT_ORDER.index(r["unit"])):
        tags = []
        total = r["adults"] + r["children"]
        if r["children"] > 0:
            tags.append("어린이 동반")
        if total >= 8:
            tags.append(f"대인원 {total}명")
        if r.get("note"):
            tags.append(r["note"])
        if r["status"] == "change_request":
            tags.append(STATUS_LABEL["change_request"])
        if not tags:
            continue
        c = UNITS[r["unit"]]["color"]
        label = r["unit"] if r["unit"] != "MAPO" else "마포"
        lines.append(f'<div class="evt note-tag" style="background:{c}1a;color:{c};border-left:3px solid {c};">'
                      f'{esc(label)} {esc(r["guest"])} · {esc(", ".join(tags))}</div>')
    if not lines:
        return '<div class="empty-hint">-</div>'
    return '<div class="evt-list">' + "".join(lines) + '</div>'

# ---------- cleaning schedule list (checkout-driven, chronological) ----------
def build_cleaning_list():
    items = []
    for dt in ALL_DAYS:
        if dt < TODAY:
            continue
        for r in sorted(checkouts_by_day[dt], key=lambda r: UNIT_ORDER.index(r["unit"])):
            same_unit_checkin_today = any(x["unit"] == r["unit"] and x["ci"] == dt for x in RESERVATIONS)
            items.append((dt, r, same_unit_checkin_today))
    out = []
    for dt, r, urgent in items:
        c = UNITS[r["unit"]]["color"]
        label = UNITS[r["unit"]]["name"]
        urgent_cls = " urgent" if urgent else ""
        badge = '<span class="badge urgent">당일 재입실</span>' if urgent else '<span class="badge normal">여유 있음</span>'
        wd = WEEKDAY_KR[(dt.weekday()+1) % 7]
        out.append(f'''<div class="clean-item{urgent_cls}">
  <div class="when">{dt.month}/{dt.day}<span class="time">({wd}) 체크아웃</span></div>
  <div class="body">
    <div class="unit"><span class="dot" style="background:{c}"></span>{esc(label)}</div>
    <div class="flow">{esc(r["guest"])} 퇴실 → {"같은 유닛 당일 재입실 있음, 빠른 청소 필요" if urgent else "익일까지 여유"}</div>
  </div>
  {badge}
</div>''')
    return "\n".join(out) if out else '<p class="empty-hint">이번 4주 동안 예정된 체크아웃이 없습니다.</p>'

# ---------- parking assignment detail table ----------
def build_parking_table():
    rows = []
    for dt in ALL_DAYS:
        if dt < TODAY:
            continue
        for r in sorted(checkins_by_day[dt], key=lambda r: UNIT_ORDER.index(r["unit"])):
            if r["unit"] not in BUILDING_UNITS or r["status"] == "checkout_done":
                continue
            c = UNITS[r["unit"]]["color"]
            rows.append(f'''<tr>
  <td>{dt.month}/{dt.day}</td>
  <td><span class="dot" style="background:{c}"></span>{esc(UNITS[r["unit"]]["name"])}</td>
  <td>{esc(r["guest"])}</td>
  <td>{esc(guests_label(r))}</td>
  <td class="muted">확인 필요 (세단 초과 시 케이타워B오피스텔 1만원 / SUV·승합차는 송정공영주차장, 호스트 최대 1만원 지원)</td>
</tr>''')
    return "\n".join(rows)

# ---------- legend ----------
def build_legend():
    items = []
    for k in UNIT_ORDER:
        u = UNITS[k]
        items.append(f'<div class="item"><span class="chip" style="background:{u["color"]}"></span>{esc(u["name"])}<span class="legend-sub">{esc(u["sub"])}</span></div>')
    return "\n".join(items)

CAL1 = build_calendar_grid(reservation_day_body)
CAL2 = build_calendar_grid(parking_day_body)
CAL3 = build_calendar_grid(guestnote_day_body)
CLEAN_LIST = build_cleaning_list()
PARK_TABLE = build_parking_table()
LEGEND = build_legend()
WIN_LABEL = fmt_range(WIN_START, WIN_END)
UPDATED_LABEL = f"{TODAY.year}. {TODAY.month}. {TODAY.day}."

TEMPLATE_PATH = "template.html"
OUTPUT_PATH = "index.html"

with open(TEMPLATE_PATH, encoding="utf-8") as f:
    tpl = f.read()

out = (tpl
    .replace("{{WIN_LABEL}}", WIN_LABEL)
    .replace("{{UPDATED_LABEL}}", UPDATED_LABEL)
    .replace("{{LEGEND}}", LEGEND)
    .replace("{{CAL1}}", CAL1)
    .replace("{{CAL2}}", CAL2)
    .replace("{{CAL3}}", CAL3)
    .replace("{{CLEAN_LIST}}", CLEAN_LIST)
    .replace("{{PARK_TABLE}}", PARK_TABLE)
)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(out)

print(f"Window: {WIN_START} ~ {WIN_END}")
print(f"Reservations: {len(RESERVATIONS)}")
print(f"Wrote {OUTPUT_PATH} ({len(out)} bytes)")
