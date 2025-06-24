from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
import re

def convert_blogger_to_mt(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()
    ns = {'atom': 'http://www.w3.org/2005/Atom'}

    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in root.findall('atom:entry', ns):
            # 投稿タイプが「記事（post）」以外はスキップ（テンプレや設定除外）
            category = entry.find("atom:category", ns)
            if category is None or "kind#post" not in category.attrib.get("term", ""):
                continue

            title = entry.find('atom:title', ns).text or ''
            published = entry.find('atom:published', ns).text or ''
            content_elem = entry.find('atom:content', ns)
            content = content_elem.text if content_elem is not None else ''

            # 本文HTMLを整形（不要タグ除去）
            soup = BeautifulSoup(content, 'html.parser')
            for tag in soup.find_all(re.compile(r"^b:")):
                tag.decompose()

            content_html = str(soup).strip()

            # 書き出し（Movable Type形式）
            f.write(f'''TITLE: {title}
DATE: {published}
-----
{content_html}
-----
\n''')

if __name__ == "__main__":
    convert_blogger_to_mt("blogger.xml", "export.txt")
