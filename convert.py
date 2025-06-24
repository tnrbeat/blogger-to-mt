from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup, Comment
import re

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

            soup = BeautifulSoup(raw_content, 'html.parser')

            # Blogger独自タグ除去
            for b_tag in soup.find_all(re.compile(r"^b:")):
                b_tag.decompose()
            for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
                comment.extract()

            # ここで本文のHTML部分だけを抽出
            content_div = soup.find('div', class_='content')
            if content_div:
                content_html = ''.join(str(x) for x in content_div.contents).strip()
            else:
                # fallbackで全文出力
                content_html = str(soup).strip()

            f.write(f'''TITLE: {title}
DATE: {published}
-----
{content_html}
-----
\n''')

if __name__ == "__main__":
    convert_blogger_to_mt("blogger.xml", "export.txt")
