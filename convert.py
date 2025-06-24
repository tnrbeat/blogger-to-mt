from xml.etree import ElementTree as ET

def convert_blogger_to_mt(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()
    ns = {'atom': 'http://www.w3.org/2005/Atom'}

    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in root.findall('atom:entry', ns):
            if entry.find('atom:content', ns) is None:
                continue  # スキップ（例：コメントなど）
            title = entry.find('atom:title', ns).text or ''
            content = entry.find('atom:content', ns).text or ''
            published = entry.find('atom:published', ns).text or ''
            f.write(f'''TITLE: {title}
DATE: {published}
-----
{content}
-----
\n''')

if __name__ == "__main__":
    convert_blogger_to_mt("blogger.xml", "export.txt")
