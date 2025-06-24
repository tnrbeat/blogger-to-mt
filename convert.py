import xml.etree.ElementTree as ET

INPUT_FILE = "blogger.xml"
OUTPUT_FILE = "output.txt"

NS = {'atom': 'http://www.w3.org/2005/Atom'}
tree = ET.parse(INPUT_FILE)
root = tree.getroot()

mt_posts = []
for entry in root.findall('atom:entry', NS):
    title_elem = entry.find('atom:title', NS)
    content_elem = entry.find('atom:content', NS)
    published_elem = entry.find('atom:published', NS)

    if title_elem is not None and content_elem is not None and published_elem is not None:
        title = title_elem.text or "No title"
        content = content_elem.text or ""
        published = published_elem.text or ""
        date = published.replace('T', ' ').split('.')[0]

        mt_post = f"""AUTHOR: あなたの名前
TITLE: {title}
STATUS: Publish
ALLOW COMMENTS: 1
CONVERT BREAKS: 0
DATE: {date}
-----
BODY:
{content}
--------
"""
        mt_posts.append(mt_post)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(mt_posts))

print(f"✅ {OUTPUT_FILE} にMT形式で出力完了！")
