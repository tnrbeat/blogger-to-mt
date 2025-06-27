import os
import csv

# マッピング読み込み
def load_url_mapping(file_path):
    mapping = {}
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for old_url, new_url in reader:
            mapping[old_url.strip()] = new_url.strip()
    return mapping

# ファイル処理
def replace_links_in_articles(input_dir, output_dir, mapping):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.endswith('.html') or filename.endswith('.txt'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()

            for old_url, new_url in mapping.items():
                content = content.replace(old_url, new_url)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    mapping = load_url_mapping('url_mapping.csv')
    replace_links_in_articles('articles', 'updated', mapping)
    print("✅ 全記事リンク置換が完了しました！")
