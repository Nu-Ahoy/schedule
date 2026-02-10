import os, requests
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["DATABASE_ID"]
headers = {"Authorization": f"Bearer {NOTION_TOKEN}", "Content-Type": "application/json", "Notion-Version": "2022-06-28"}

def get_notion_data():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    res = requests.post(url, headers=headers)
    data = res.json()
    table = {p: {d: "" for d in ["월", "화", "수", "목", "금"]} for p in range(1, 9)}
    for row in data.get("results", []):
        props = row["properties"]
        try:
            name = props["이름"]["title"][0]["plain_text"]
            days = [d["name"] for d in props["요일"]["multi_select"]]
            start, end = int(props["시작 교시"]["number"]), int(props["종료 교시"]["number"])
            m_type = props["전공 구분"]["select"]["name"]
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
