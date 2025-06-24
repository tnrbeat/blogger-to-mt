import xml.etree.ElementTree as ET
from datetime import datetime

# BloggerバックアップXMLファイル
INPUT_FILE = "blogger_backup.xml"
OUTPUT_FILE = "output_mt.txt"

# 名前空間
NS = {'atom': 'http://www.w3.org/2005/Atom'}

tree = ET.parse(INPUT_FILE)
root = tree.getroot()

mt_posts = []

# entry 要素を取得
for entry in root.findall('atom:entry', NS):
    # 投稿記事のみ取得（postKindが空でなくtitleがあるもの）
    title_elem = entry.find('atom:title', NS)
    content_elem = entry.find('atom:content', NS)
    published_elem = entry.find('atom:published', NS)

    if title_elem is not None and content_elem is not None and published_elem is not None:
        title = title_elem.text or "No title"
        content = content_elem.text or ""
        published = published_elem.text or ""

        # 日付整形
        date = published.replace('T', ' ').split('.')[0]

        mt_post = f"""AUTHOR: あなたの名前
TITLE: {title}
DATE: {date}
-----
BODY:
{content}
--------
"""
        mt_posts.append(mt_post)

# MTファイル出力
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(mt_posts))

print(f"✅ {OUTPUT_FILE} にMT形式で出力完了！")
