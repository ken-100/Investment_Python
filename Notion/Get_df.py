from notion_client import Client
import pandas as pd

# Integration Secret
TOKEN = "ntn_D78560023007D4hsbljH2zVk65wnowkNdCV7nKUAqfC6DX"

# Database ID
DATABASE_ID = "2601d44114fc80998207d751c6c328db"

# Notionクライアント
notion = Client(auth=TOKEN)

# データベースのスキーマ情報を取得
db_info = notion.databases.retrieve(DATABASE_ID)

# プロパティ一覧を表示
fields = list(db_info["properties"].keys())
print("Fields:", fields)




resp = notion.databases.query(database_id=DATABASE_ID)

rows = []
for row in resp["results"]:
    props = row["properties"]
    data = {}
    for field in fields:
        ftype = props[field]["type"]

        if ftype == "title":
            val = props[field]["title"]
            val = val[0]["text"]["content"] if val else ""
        elif ftype == "rich_text":
            val = props[field]["rich_text"]
            val = val[0]["text"]["content"] if val else ""
        elif ftype == "number":
            val = props[field].get("number")
        elif ftype == "date":
            val = props[field]["date"]["start"] if props[field]["date"] else None
        else:
            val = None  # その他の型はとりあえずNone
        data[field] = val
    rows.append(data)

df = pd.DataFrame(rows)
df
