def convert_blogger_to_mt(input_file, output_file):
    import xml.etree.ElementTree as ET

    tree = ET.parse(input_file)
    root = tree.getroot()
    ns = {'atom': 'http://www.w3.org/2005/Atom'}

    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in root.findall('atom:entry', ns):
            kind = entry.find("atom:category[@scheme='http://schemas.google.com/g/2005#kind']", ns)
            if kind is None or kind.attrib['term'] != 'http://schemas.google.com/blogger/2008/kind#post':
                continue  # 投稿記事のみ処理

            title = entry.find('atom:title', ns).text or 'No Title'
            published = entry.find('atom:published', ns).text or ''
            content = entry.find('atom:content', ns).text or ''

            # 必須のSourceを固定または動的に入れる（ここはブログURLなどに変更してください）
            source_url = 'https://flashsoudannavi.blogspot.com/'

            f.write(f"Title: {title}\n")
            f.write(f"Date: {published}\n")
            f.write(f"Source: {source_url}\n")  # ここが重要！
            f.write("-----\n")
            f.write(content + "\n\n")
