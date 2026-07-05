import os
from dotenv import load_dotenv
from anthropic import Anthropic
import requests
from hn import fetch_top_stories
import trafilatura 
load_dotenv()                             # 读 .env，把 KEY 灌进本进程的环境变量
api_key = os.getenv("ANTHROPIC_API_KEY")  # 从环境里读出来（就是 hn.py 学过的 os.getenv）

client = Anthropic(api_key=api_key)

def fetch_article_text(url: str, max_chars: int = 2000) -> str | None:
    """抓一个网页、抠出正文;抓不动就返回 None(不让脚本崩)。"""
    try:                                                    # 【新】try/except
        headers = {"User-Agent": "Mozilla/5.0"}            # 【新】伪装浏览器
        r = requests.get(url, headers=headers, timeout=10) # 【新】timeout=10 秒
        if r.status_code != 200:
            return None
        text = trafilatura.extract(r.text)                 # 【新】HTML → 干净正文
        if text is None:                                   # 有些页面抽不出正文
            return None
        return text[:max_chars]                            # 截断控 token(你的老朋友切片)
    except Exception as e:                                 # 【新】兜住一切抓取错误
        print(f"⚠️ 抓取失败 {url}: {e}")
        return None

def format_stories(stories: list[dict]) -> str:
    """把 10 条 story 揉成一段带编号的文本。"""
    blocks = []
    for i, s in enumerate(stories, start=1):          #【学】enumerate 带序号
        title = s.get("title")
        score = s.get("score")
        content = s.get("content")

        block = f"[{i}] {title}（{score} 分）"
        if content:
            block += f"\n{content}"                    #【学】+= 接字符串
        blocks.append(block)

    return "\n\n".join(blocks)


def format_links(stories: list[dict]) -> str:
    """把 10 条整理成带编号的 markdown 链接清单,给人点。"""
    lines = []
    for i, s in enumerate(stories, start=1):
        title = s.get("title")
        url = s.get("url")
        if url:
            lines.append(f"{i}. [{title}]({url})")   #【学】markdown 链接语法
        else:
            lines.append(f"{i}. {title}（无外链）")    # Ask HN 没 url,不硬凑链接
    return "\n".join(lines)



# ---- 主流程 ----
stories = fetch_top_stories()
for s in stories:
    url = s.get("url")
    s["content"] = fetch_article_text(url) if url else None  #【学】三元表达式

data_text = format_stories(stories)
prompt = f"""你是我的科技资讯助手。下面是 Hacker News 今天的热帖,每条有标题、分数、正文(有的没抓到正文)。

请**基于正文内容**(不要只看标题)写一份中文摘要:
1. 先用 3-4 句话概括今天科技圈在聊什么。
2. 再挑最值得读的 3 条,每条一句话说清讲了什么、为什么值得看。

热帖如下:

{data_text}""" 


message = client.messages.create(                       # ← 用 client 发请求
    model="claude-haiku-4-5-20251001",
    max_tokens=1000,
    messages=[{"role": "user", "content": prompt}],
)


summary = message.content[0].text        # Claude 写的摘要
links = format_links(stories)            # 你代码生成的链接清单

output = f"""# HN 今日摘要

{summary}

---

## 原文链接

{links}
"""                                       #【学】用 markdown 把两块组装成一份文档
print(output)
with open("hn_summary.md", "w", encoding="utf-8") as f:
    f.write(output)