#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
건대입구 게스트하우스 4개 유닛 운영 대시보드 생성기.
오늘 날짜 기준 4주(28일) 로테이션 윈도우(이번 주 일요일 시작)로
1) 예약 캘린더(체크인 인원 + 확인된 얼리체크인/레이트체크아웃),
2) 주차여부/바베큐여부 캘린더
를 만든다. 확인되지 않은 정보는 추측하지 않고 "확인 필요"로 명시한다.
"""
import datetime
import html as htmlmod

TODAY = datetime.date(2026, 8, 20)
WEEKDAY_KR = ['일', '월', '화', '수', '목', '금', '토']

def week_sunday(dt):
    # 주 경계는 "월요일에 넘어갈 때" 바뀐다: 이번 주가 월~일이라고 볼 때
    # 창의 시작일은 그 주의 월요일 하루 전(=직전 일요일)이다. 즉 일요일 당일에는
    # 아직 창이 넘어가지 않고, 그 다음날 월요일이 되어야 다음 4주 창으로 넘어간다.
    monday_of_week = dt - datetime.timedelta(days=dt.weekday())  # Monday=0 ... Sunday=6
    return monday_of_week - datetime.timedelta(days=1)

WIN_START = week_sunday(TODAY)
WIN_END = WIN_START + datetime.timedelta(days=27)  # 28 days inclusive
ALL_DAYS = [WIN_START + datetime.timedelta(days=i) for i in range(28)]

# 사용자 지정 색상: 501=브라운, 502=블랙, 401=노란색, 402=하늘색 (문 색상과 일치)
UNITS = {
    "501": {"name": "더테라스 하우스 501호", "sub": "브라운문", "color": "#8A5A3B"},
    "502": {"name": "더블랑 하우스 502호", "sub": "검정문", "color": "#262626"},
    "401": {"name": "우드블랑 하우스 401호", "sub": "골드문", "color": "#C98500"},
    "402": {"name": "우드블랑 하우스 402호", "sub": "그레이문", "color": "#1E88B8"},
}
UNIT_ORDER = ["501", "502", "401", "402"]

def d(y, m, day):
    return datetime.date(y, m, day)

# status: confirmed | hosting | checkout_done | change_request
# early: 확인된 얼리체크인 메모 (없으면 None) / late: 확인된 레이트체크아웃 메모 (없으면 None)
# note: 기타 확인 필요 메모
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
    dict(unit="401", guest="Glenda Galvez", ci=d(2026,8,20), co=d(2026,8,22), adults=5, children=0, status="change_request", note="예약 변경요청 처리중 - 확인 필요"),
    dict(unit="401", guest="승준 이", ci=d(2026,8,22), co=d(2026,8,24), adults=1, children=0, status="confirmed"),
    dict(unit="401", guest="신욱 곽", ci=d(2026,8,30), co=d(2026,9,1), adults=4, children=0, status="confirmed"),
    # 402호 우드블랑 그레이문
    dict(unit="402", guest="지원 이", ci=d(2026,8,19), co=d(2026,8,20), adults=3, children=1, status="checkout_done"),
    dict(unit="402", guest="유나 이", ci=d(2026,8,20), co=d(2026,8,21), adults=4, children=0, status="hosting"),
    dict(unit="402", guest="경미 이", ci=d(2026,8,21), co=d(2026,8,22), adults=4, children=0, status="confirmed"),
    dict(unit="402", guest="지웅 이", ci=d(2026,8,22), co=d(2026,8,23), adults=8, children=0, status="confirmed"),
    dict(unit="402", guest="李致姗 李", ci=d(2026,8,23), co=d(2026,8,27), adults=4, children=0, status="confirmed", note="얼리체크인 문의 있었음 - 확인 필요"),
]

def esc(s):
    return htmlmod.escape(str(s), quote=True)

def guests_label(r):
    g = f"성인 {r['adults']}명"
    if r["children"]:
        g += f", 어린이 {r['children']}명"
    return g

def fmt_range(a, b):
    return f"{a.month}/{a.day} - {b.month}/{b.day}"

# 연박인 경우 체크인일부터 체크아웃 전날까지 매일 표시한다 (숙박 중인 모든 날짜에 나타남).
stay_by_day = {dt: [] for dt in ALL_DAYS}
for r in RESERVATIONS:
    if r["status"] == "checkout_done":
        continue  # 이미 퇴실한 예약은 캘린더에 표시하지 않음
    night = r["ci"]
    while night < r["co"]:
        if night in stay_by_day:
            stay_by_day[night].append(r)
        night += datetime.timedelta(days=1)

def day_active_checkins(dt):
    return stay_by_day[dt]

def day_cell(dt, body_html):
    today_cls = " today" if dt == TODAY else ""
    wd = WEEKDAY_KR[(dt.weekday()+1) % 7]
    wd_cls = " sat" if wd == "토" else (" sun" if wd == "일" else "")
    return f'''<div class="cal-day{today_cls}">
  <div class="num">{dt.month}/{dt.day}<span class="wd{wd_cls}">{wd}</span></div>
  {body_html}
</div>'''

def build_calendar_grid(day_body_fn):
    weeks = [ALL_DAYS[i:i+7] for i in range(0, 28, 7)]
    out = ['<div class="cal-wd-row">']
    for wd in WEEKDAY_KR:
        cls = " sat" if wd == "토" else (" sun" if wd == "일" else "")
        out.append(f'<div class="cal-wd{cls}">{wd}</div>')
    out.append('</div>')
    for week in weeks:
        out.append('<div class="cal-grid">')
        for dt in week:
            out.append(day_cell(dt, day_body_fn(dt)))
        out.append('</div>')
    return "\n".join(out)

# ----- Calendar 1: 예약 캘린더 (체크인~체크아웃 전날까지 연속 표시, 확인된 얼리/레이트 표시) -----
def reservation_day_body(dt):
    lines = []
    for r in sorted(day_active_checkins(dt), key=lambda r: UNIT_ORDER.index(r["unit"])):
        c = UNITS[r["unit"]]["color"]
        is_checkin_day = (dt == r["ci"])
        tags = []
        if is_checkin_day:
            if r.get("early"):
                tags.append(f"얼리체크인 {r['early']}")
            if r.get("note"):
                tags.append(r["note"])
        else:
            tags.append("연박")
        if r.get("late") and dt == r["co"] - datetime.timedelta(days=1):
            tags.append(f"레이트체크아웃 {r['late']}")
        tag_html = f' <span class="tag">· {esc(", ".join(tags))}</span>' if tags else ""
        lines.append(f'<div class="evt" style="background:{c}1a;color:{c};border-left:3px solid {c};">'
                      f'{esc(r["unit"])} {esc(r["guest"])} ({esc(guests_label(r))}){tag_html}</div>')
    if not lines:
        return '<div class="empty-hint">-</div>'
    return '<div class="evt-list">' + "".join(lines) + '</div>'

# ----- Calendar 2: 주차여부 / 바베큐여부 캘린더 -----
# 확인된 내용이 있을 때만 표시한다. parking/bbq 필드가 없으면(=파악된 내용 없음)
# 그 게스트 자체를 이 캘린더에 표시하지 않는다 ("확인 필요" 같은 플레이스홀더를 굳이 채우지 않음).
def parking_bbq_day_body(dt):
    lines = []
    for r in sorted(day_active_checkins(dt), key=lambda r: UNIT_ORDER.index(r["unit"])):
        park = r.get("parking")
        bbq = r.get("bbq")
        if not park and not bbq:
            continue
        c = UNITS[r["unit"]]["color"]
        parts = []
        if park:
            parts.append(f"주차: {esc(park)}")
        if bbq:
            parts.append(f"바베큐: {esc(bbq)}")
        lines.append(f'<div class="evt" style="background:{c}1a;color:{c};border-left:3px solid {c};">'
                      f'{esc(r["unit"])} {esc(r["guest"])}<br>{" · ".join(parts)}</div>')
    if not lines:
        return '<div class="empty-hint">-</div>'
    return '<div class="evt-list">' + "".join(lines) + '</div>'

def build_legend():
    items = []
    for k in UNIT_ORDER:
        u = UNITS[k]
        items.append(f'<div class="item"><span class="chip" style="background:{u["color"]}"></span>{esc(u["name"])}<span class="legend-sub">{esc(u["sub"])}</span></div>')
    return "\n".join(items)

CAL1 = build_calendar_grid(reservation_day_body)
CAL2 = build_calendar_grid(parking_bbq_day_body)
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
)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(out)

print(f"Window: {WIN_START} ~ {WIN_END}")
print(f"Reservations: {len(RESERVATIONS)}")
print(f"Wrote {OUTPUT_PATH} ({len(out)} bytes)")
