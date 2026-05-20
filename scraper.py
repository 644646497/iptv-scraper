import requests
import time
from datetime import datetime

# 直播源列表
SOURCES = [
    "https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/ipv6.m3u",
    "https://raw.githubusercontent.com/youshandefeiyang/IPTV/main/IPTV.m3u",
]

def fetch(url):
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            print(f"✅ 成功: {url}")
            return r.text
        else:
            print(f"❌ 失败: {url} - {r.status_code}")
            return None
    except Exception as e:
        print(f"❌ 错误: {url} - {e}")
        return None

def merge(files):
    lines = []
    for f in files:
        if f:
            lines.extend(f.split('\n'))
    # 去重
    unique = []
    seen = set()
    for line in lines:
        if line not in seen:
            seen.add(line)
            unique.append(line)
    header = f"#EXTM3U\n# 更新时间: {datetime.now()}\n"
    return header + '\n'.join(unique)

def main():
    print("抓取直播源...")
    contents = []
    for url in SOURCES:
        c = fetch(url)
        if c:
            contents.append(c)
        time.sleep(1)
    merged = merge(contents)
    with open('live.m3u', 'w') as f:
        f.write(merged)
    
    # 统计频道数
    count = 0
    for line in merged.split('\n'):
        if line.startswith('http'):
            count += 1
    print(f"完成！共 {count} 个频道")

if __name__ == "__main__":
    main()
