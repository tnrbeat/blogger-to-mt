import re
import csv

filename = 'hatena_export.txt'
pattern_title = re.compile(r'<title>(.*?)</title>')
pattern_link = re.compile(r'<link>(.*?)</link>')

titles = []
links = []

with open(filename, encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '<item>' in line:
        # 次の数行でタイトルとリンクを探す
        for j in range(i, i+10):
            if j >= len(lines):
                break
            title_match = pattern_title.search(lines[j])
            link_match = pattern_link.search(lines[j])
            if title_match:
                title = title_match.group(1)
            if link_match:
                link = link_match.group(1)
                titles.append(title)
                links.append(link)
                break

# CSVに書き出す
with open('hatena_urls.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['title', 'new_url'])
    for t, l in zip(titles, links):
        writer.writerow([t, l])

print('hatena_urls.csv を作成しました')
