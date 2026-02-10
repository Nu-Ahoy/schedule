import os, requests

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["DATABASE_ID"]
headers = {"Authorization": f"Bearer {NOTION_TOKEN}", "Content-Type": "application/json", "Notion-Version": "2022-06-28"}

def get_notion_data():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    res = requests.post(url, headers=headers)
    data = res.json()
    
    if "results" not in data:
        print(f"❌ API 응답 오류: {data}")
        return {}

    results = data.get("results", [])
    print(f"✅ 총 {len(results)}개의 데이터를 가져왔습니다.")

    # 1. 학기 필터링 로직
    all_semesters = []
    for row in results:
        try:
            sem = row["properties"]["학기"]["select"]["name"]
            all_semesters.append(sem)
        except Exception: continue
    
    if not all_semesters:
        print("❌ 오류: '학기' 속성이 비어있거나 이름을 찾을 수 없습니다. 노션의 '학기' 속성을 확인하세요!")
        return {}

    latest_semester = max(all_semesters)
    print(f"⭐ 탐지된 최신 학기: {latest_semester}")

    table = {p: {d: "" for d in ["월", "화", "수", "목", "금"]} for p in range(1, 9)}
    
    for row in results:
        props = row["properties"]
        try:
            # 학기 일치 여부 확인
            curr_sem = props["학기"]["select"]["name"]
            if curr_sem != latest_semester: continue
                
            name = props["이름"]["title"][0]["plain_text"]
            days = [d["name"] for d in props["요일"]["multi_select"]]
            start = int(props["시작 교시"]["number"])
            end = int(props["종료 교시"]["number"])
            
            # 이수 구분 처리 (다중 선택 대응)
            m_types = [d["name"] for d in props["이수 구분"]["multi_select"]]
            m_type = m_types[0] if m_types else "교양"
            
            color = "aqua" if m_type == "이중전공" else "pink" if m_type == "본전공" else "purple"
            box = f'<div class="class-box {color}">{name}</div>'
            
            print(f"📝 추가 중: {name} ({day} {start}-{end}교시)")
            
            for day in days:
                for p in range(start, end + 1):
                    if p in table: table[p][day] = box
        except KeyError as e:
            print(f"❌ 속성 이름 불일치: 노션에 '{e}'라는 이름의 속성이 정확히 있나요?")
        except Exception as e:
            print(f"❌ 데이터 처리 오류: {e}")
            continue
            
    return table

table_data = get_notion_data()
if not table_data:
    raise Exception("데이터가 비어있어 HTML을 생성할 수 없습니다.")

rows_html = "".join([f"<tr><td class='time-label'>{p}교시</td>" + "".join([f"<td>{table_data[p][d]}</td>" for d in ["월", "화", "수", "목", "금"]]) + "</tr>" for p in range(1, 9)])
with open("index_template.html", "r", encoding="utf-8") as f: template = f.read()
with open("index.html", "w", encoding="utf-8") as f: f.write(template.replace("{{CONTENT}}", rows_html))
