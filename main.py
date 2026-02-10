import os, requests

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["DATABASE_ID"]
headers = {"Authorization": f"Bearer {NOTION_TOKEN}", "Content-Type": "application/json", "Notion-Version": "2022-06-28"}

# 유나님의 학교 시간표 매핑
TIME_MAP = {
    1: "09:00~10:15", 2: "10:30~11:45", 3: "12:00~13:15",
    4: "13:30~14:45", 5: "15:00~16:15", 6: "16:30~17:45",
    7: "18:00~18:50", 8: "19:00~19:50", 9: "20:00~20:50", 10: "21:00~21:50"
}

def get_notion_data():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    res = requests.post(url, headers=headers)
    data = res.json()
    if "results" not in data: return {}
    results = data.get("results", [])

    all_semesters = []
    for row in results:
        try:
            sem = row["properties"]["학기"]["select"]["name"]
            all_semesters.append(sem)
        except: continue
    if not all_semesters: return {}
    latest_semester = max(all_semesters)

    # 10교시까지 범위를 확장했습니다
    table = {p: {d: "" for d in ["월", "화", "수", "목", "금"]} for p in range(1, 11)}
    
    for row in results:
        props = row["properties"]
        try:
            if props["학기"]["select"]["name"] != latest_semester: continue
            name = props["이름"]["title"][0]["plain_text"]
            days = [d["name"] for d in props["요일"]["multi_select"]]
            start, end = int(props["시작 교시"]["number"]), int(props["종료 교시"]["number"])
            m_types = [d["name"] for d in props["이수 구분"]["multi_select"]]
            m_type = m_types[0] if m_types else "교양"
            color = "aqua" if m_type == "이중전공" else "pink" if m_type == "본전공" else "purple"
            box = f'<div class="class-box {color}">{name}</div>'
            for day in days:
                for p in range(start, end + 1):
                    if p in table: table[p][day] = box
        except: continue
    return table

table_data = get_notion_data()
rows_html = ""
for p in range(1, 11): # 10교시까지 표시
    time_str = TIME_MAP.get(p, "")
    rows_html += f"<tr><td class='time-label'>{p}교시<span class='time-sub'>{time_str}</span></td>"
    for day in ["월", "화", "수", "목", "금"]:
        rows_html += f"<td>{table_data[p][day]}</td>"
    rows_html += "</tr>"

with open("index_template.html", "r", encoding="utf-8") as f: template = f.read()
with open("index.html", "w", encoding="utf-8") as f: f.write(template.replace("{{CONTENT}}", rows_html))
