import os, requests

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["DATABASE_ID"]
headers = {"Authorization": f"Bearer {NOTION_TOKEN}", "Content-Type": "application/json", "Notion-Version": "2022-06-28"}

def get_notion_data():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    res = requests.post(url, headers=headers)
    data = res.json()
    
    if "results" not in data:
        print(f"API Error: {data}")
        return {}

    results = data.get("results", [])
    
    # 1. 모든 데이터에서 '학기' 목록을 추출하여 가장 최신 학기 찾기
    all_semesters = []
    for row in results:
        try:
            sem = row["properties"]["학기"]["select"]["name"]
            all_semesters.append(sem)
        except: continue
    
    if not all_semesters:
        print("학기 데이터를 찾을 수 없습니다.")
        return {}

    # 문자열 정렬을 통해 가장 큰 값(최신 학기)을 결정합니다.
    latest_semester = max(all_semesters)
    print(f"Detected Latest Semester: {latest_semester}")

    # 2. 최신 학기에 해당하는 수업만 필터링하여 테이블 생성
    table = {p: {d: "" for d in ["월", "화", "수", "목", "금"]} for p in range(1, 9)}
    
    for row in results:
        props = row["properties"]
        try:
            # 학기 체크
            if props["학기"]["select"]["name"] != latest_semester:
                continue
                
            name = props["이름"]["title"][0]["plain_text"]
            days = [d["name"] for d in props["요일"]["multi_select"]]
            start = int(props["시작 교시"]["number"])
            end = int(props["종료 교시"]["number"])
            
            # 이수 구분 처리 (다중 선택)
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
rows_html = "".join([f"<tr><td class='time-label'>{p}교시</td>" + "".join([f"<td>{table_data[p][d]}</td>" for d in ["월", "화", "수", "목", "금"]]) + "</tr>" for p in range(1, 9)])
with open("index_template.html", "r", encoding="utf-8") as f: template = f.read()
with open("index.html", "w", encoding="utf-8") as f: f.write(template.replace("{{CONTENT}}", rows_html))
table_data = get_notion_data()
rows_html = "".join([f"<tr><td class='time-label'>{p}교시</td>" + "".join([f"<td>{table_data[p][d]}</td>" for d in ["월", "화", "수", "목", "금"]]) + "</tr>" for p in range(1, 9)])
with open("index_template.html", "r", encoding="utf-8") as f: template = f.read()
with open("index.html", "w", encoding="utf-8") as f: f.write(template.replace("{{CONTENT}}", rows_html))
