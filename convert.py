from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup

def convert_blogger_to_mt(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()
    ns = {'atom': 'http://www.w3.org/2005/Atom'}

    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in root.findall('atom:entry', ns):
            content_elem = entry.find('atom:content', ns)
            if content_elem is None:
                continue

            title = entry.find('atom:title', ns).text or ''
            published = entry.find('atom:published', ns).text or ''
            raw_content = content_elem.text or ''

            # HTMLパースして本文だけ抽出
            soup = BeautifulSoup(raw_content, 'html.parser')

            # 本文だけテキスト化（HTMLタグはそのまま残したい場合は .prettify() や .decode_contents()）
            # はてなブログはHTMLもOKなのでタグ付きで中身だけ抽出例：
            content_html = ''.join(str(x) for x in soup.body.contents) if soup.body else raw_content

            # Movable Type形式で出力
            f.write(f'''TITLE: {title}
DATE: {published}
-----
{content_html}
-----
\n''')

if __name__ == "__main__":
    convert_blogger_to_mt("blogger.xml", "export.txt")
