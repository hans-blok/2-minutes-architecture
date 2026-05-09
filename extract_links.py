import re
with open(r'temp\Squarespace-Wordpress-Export-05-08-2026.xml', 'r', encoding='utf-8') as f:
    xml = f.read()
urls = set(re.findall(r'href=[\x22\x27](https?://.*?)[\x22\x27]', xml))
for u in sorted(list(urls)):
    print(u)
