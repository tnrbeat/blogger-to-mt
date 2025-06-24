import xml.etree.ElementTree as ET
from html import unescape

def convert_blogger_to_mt(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()
    ns = {'atom': 'http://www.w3.org/2005/Atom'}

    with open(output_file, 'w', encoding='utf-8') as out:
        for entry in root.findall('atom:entry', ns):
            kind = entry.find('atom:category', ns)
            if not kind or 'kind#post' not in kind.attrib.get('term', ''):
                continue

            title = entry.find('atom:title', ns)
            content = entry.find('atom:content', ns)
            published = entry.find('atom:published', ns)

            out.write('TITLE: {}\n'.format(title.text.strip() if title is not None else 'Untitled'))
            out.write('DATE: {}\n'.format(published.text.strip() if published is not None else ''))
            out.write('-----\n')
            if content is not None:
                html = unescape(content.text or '')
                out.write(html.strip() + '\n')
            out.write('--------\n\n')

if __name__ == '__main__':
    convert_blogger_to_mt('blogger.xml', 'export.txt')
