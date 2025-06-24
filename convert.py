import xml.etree.ElementTree as ET

def convert_blogger_to_mt(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    ns = {'atom': 'http://www.w3.org/2005/Atom'}

    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in root.findall('atom:entry', ns):
            kind = entry.find("atom:category[@scheme='http://schemas.google.com/g/2005#kind']", ns)
            if kind is not None and kind.attrib.get('term') == 'http://schemas.google.com/blogger/2008/kind#post':
                title = entry.find('atom:title', ns).text or ''
                content = entry.find('atom:content', ns).text or ''
                published = entry.find('atom:published', ns).text or ''

                f.write(f"TITLE: {title}\n")
                f.write(f"DATE: {published}\n")
                f.write("-----\n")
                f.write(content + "\n\n")

if __name__ == '__main__':
    convert_blogger_to_mt('blogger.xml', 'output.txt')
