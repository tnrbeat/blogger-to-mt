import xml.etree.ElementTree as ET
import csv

xml_file = 'blogger.xml'
tree = ET.parse(xml_file)
root = tree.getroot()

ns = {'atom': 'http://www.w3.org/2005/Atom'}
with open('blogger_urls.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['title', 'old_url'])  # ヘッダー
    for entry in root.findall('atom:entry', ns):
        title_elem = entry.find('atom:title', ns)
        link_elem = entry.find('atom:link[@rel="alternate"]', ns)
        if title_elem is not None and link_elem is not None:
            title = title_elem.text
            old_url = link_elem.attrib['href']
            writer.writerow([title, old_url])

print('✅ blogger_urls.csv を生成しました')
