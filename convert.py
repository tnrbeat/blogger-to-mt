import xml.etree.ElementTree as ET
from html import unescape

def convert_blogger_to_mt(input_file, output_file):
    ns = {
        'atom': 'http://www.w3.org/2005/Atom',
        'blogger': 'http://schemas.google.com/blogger/2008'
    }

    tree = ET.parse(input_file)
    root = tree.getroot()

    with open(output_file, 'w', encoding='utf-8') as out:
        for entry in root.findall('atom:entry', ns):
            category = entry.find('atom:category', ns)
            if category is None or category.attrib.get('term') != 'http://schemas.google.com/blogger/2008/kind#post':
                continue

            title_elem = entry.find('atom:title', ns)
            content_elem = entry.find('atom:content', ns)
            published_elem = entry.find('atom:published', ns)

            title = title_elem.text if title_elem is not None else '無題'
            content = unescape(content_elem.text if content_elem is not None else '')
            date = published_elem.text if published_elem is not None else '2000-01-01T00:00:00Z'

            out.write(f'TITLE: {title}\n')
            out.write(f'DATE: {date}\n')
            out.write('-----\n')
            out.write(f'{content}\n')
            out.write('--------\n\n')

if __name__ == '__main__':
    convert_blogger_to_mt('blogger.xml', 'export.txt')
