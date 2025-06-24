from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup, Comment
import re

def convert_blogger_to_mt(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()
    ns = {'atom': 'http://www.w3.org/2005/Atom'}

    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text or ''
            published = entry.find('atom:published', ns).text or ''

            summary_elem = entry.find('atom:summary', ns)
            content_elem = entry.find('atom:content', ns)

            if summary_elem is not None and summary_elem.text:
                raw_content = summary_elem.text
            elif content_elem is not None and content_elem.text:
                raw_content = content_elem.text
            else:
                raw_content = ''

            soup = BeautifulSoup(raw_content, 'html.parser')

            # Bloggerタグ除去
            for b_tag in soup.find_all(re.compile(r"^b:")):
                b_tag.decompose()
            for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
                comment.extract()

            # できれば本文部分だけ抽出（要調整）
            content_div = soup.find('div', class_='post-body') or soup.find('div', class_='content')
            if content_div:
                content_html = ''.join(str(x) for x in content_div.contents).strip()
            else:
                content_html = str(soup).strip()

            f.write(f'''TITLE: {title}
DATE: {published}
-----
{content_html}
-----
\n''')

if __name__ == "__main__":
    convert_blogger_to_mt("blogger.xml", "export.txt")
