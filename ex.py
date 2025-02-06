import os
import json
import hashlib
import requests
import webbrowser
import time
import argparse
import random
from bs4 import BeautifulSoup

# -----------------------------
# 解析命令行参数
# -----------------------------
parser = argparse.ArgumentParser(description="Exhentai 更新检测脚本")
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "--random", type=int, help="随机打开指定数量的作者网页（不会更新fingerprint）"
)
group.add_argument(
    "--force", action="store_true", help="强制打开所有作者网页，并更新fingerprint"
)
args = parser.parse_args()

# -----------------------------
# 定义作者列表
# -----------------------------
authors = [
    "derauea",
    "tsukino jyogi",
    "ishigaki",
    "kojima saya",
    "ringoya",
    "fukuyama naoto",
    "tonnosuke",
    "Yoshiura Kazuya",
    "udonya",
    "ishimura",
    "Ikumura",
    "okayusan",
    "puyocha",
    "ahegao chinese",
    "anal chinese",
    "gessyu",
    "Hyouuma",
    "sian",
    "jitaku vacation",
    "kyockcho",
    "kemokomoya",
    "karasu",
    "cior",
    "Bonske",
    "Nasi-pasuya",
    "NoriPachi",
    "Miyamoto Issa",
    "mon-petit",
    "Karube Guri",
    "Shuuen no Ma",
    "Sanuki",
    "Eggutarto",
    "chinchintei",
]

# -----------------------------
# 指纹数据保存文件
# -----------------------------
fp_file = "fingerprints.json"
if os.path.exists(fp_file):
    with open(fp_file, "r", encoding="utf-8") as f:
        fingerprints = json.load(f)
else:
    fingerprints = {}

# -----------------------------
# 读取cookie.txt文件中的cookies
# 假定导出格式为JSON数组，每个元素包含"name"和"value"
# -----------------------------
cookie_file = "cookie.txt"
if os.path.exists(cookie_file):
    with open(cookie_file, "r", encoding="utf-8") as f:
        try:
            cookie_list = json.load(f)
            cookies = {cookie["name"]: cookie["value"] for cookie in cookie_list}
        except Exception as e:
            print(f"读取cookie.txt时出错: {e}")
            cookies = {}
else:
    print("未找到cookie.txt文件，使用空cookies")
    cookies = {}

# -----------------------------
# 请求头设置
# -----------------------------
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


# -----------------------------
# 定义处理单个作者的函数
# 参数说明：
#   update_fingerprint: 是否更新指纹数据（默认True）
#   force: 如果为True，则无条件打开网页
# -----------------------------
def process_author(author, update_fingerprint=True, force=False):
    time.sleep(0.1)
    url = f"https://exhentai.org/?f_search={author}"
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        if response.status_code != 200:
            print(f"访问 {url} 失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"访问 {url} 时出现异常: {e}")
        return None

    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    # 提取所有 class 为 "gl4t glname glink" 的 <div> 元素
    title_divs = soup.select("div.gl4t.glname.glink")
    if len(title_divs) < 2:
        print(f"对于作者 {author}，未能找到至少两个标题元素。")
        return None

    first_title = title_divs[0].get_text(strip=True)
    second_title = title_divs[1].get_text(strip=True)
    combined_str = first_title + second_title
    new_fingerprint = hashlib.md5(combined_str.encode("utf-8")).hexdigest()

    # 强制模式下，无论fingerprint如何都打开网页
    if force:
        print(f"[Force] 打开 {author} 的网页。")
        webbrowser.open(url)
    else:
        # 默认模式：检测是否首次访问或fingerprint有变化
        if author not in fingerprints:
            print(f"首次访问 {author}，打开网页并保存指纹。")
            webbrowser.open(url)
        elif fingerprints[author]["fingerprint"] != new_fingerprint:
            print(f"检测到 {author} 网页内容更新，打开网页。")
            webbrowser.open(url)
        else:
            print(f"{author} 网页内容无变化。")

    # 只有在默认或force模式下更新fingerprint，不在随机模式中更新
    if update_fingerprint:
        fingerprints[author] = {
            "fingerprint": new_fingerprint,
            "first_title": first_title,
        }
    return new_fingerprint


# -----------------------------
# 根据命令行参数选择处理模式
# -----------------------------
if args.force:
    # 强制模式：处理所有作者，force=True，更新fingerprint
    for author in authors:
        process_author(author, update_fingerprint=True, force=True)
    # 保存更新后的fingerprint数据
    with open(fp_file, "w", encoding="utf-8") as f:
        json.dump(fingerprints, f, indent=2)
elif args.random is not None:
    # 随机模式：从作者列表中随机选择指定数量，不更新fingerprint数据
    n = args.random
    if n < 0:
        n = 0
    if n > len(authors):
        n = len(authors)
    selected_authors = random.sample(authors, n)
    for author in selected_authors:
        process_author(author, update_fingerprint=False)
    # 随机模式下，不写回fingerprint文件
else:
    # 默认模式：处理所有作者
    for author in authors:
        process_author(author, update_fingerprint=True)
    with open(fp_file, "w", encoding="utf-8") as f:
        json.dump(fingerprints, f, indent=2)
