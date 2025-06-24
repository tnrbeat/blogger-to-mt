import xml.etree.ElementTree as ET

def convert_blogger_to_mt(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    with open(output_file, "w", encoding="utf-8") as f:
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            # 投稿のみ抽出
            kind = entry.find("{http://schemas.google.com/g/2005}category")
            if kind is None:
                continue
            term = kind.attrib.get("term", "")
            if "kind#post" not in term:
                continue

            title = entry.find("{http://www.w3.org/2005/Atom}title").text or ""
            content = entry.find("{http://www.w3.org/2005/Atom}content").text or ""

            # MT形式の1記事出力（例）
            f.write("--------\n")
            f.write(f"TITLE: {title}\n")
            f.write("-----\n")
            f.write(content)
            f.write("\n\n")

if __name__ == "__main__":
    convert_blogger_to_mt("blogger.xml", "export.txt")
