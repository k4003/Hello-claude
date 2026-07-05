import requests

def fetch_top_stories(n: int = 10) -> list[dict]:
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    r = requests.get(url)
    if r.status_code != 200:
            print(f"请求失败,状态码 {r.status_code}")
    else:
            index = r.json()

    
    

    # 第一步:拿 topstories → 切前 n 个 id  ← 你已有,搬过来
    ids = index[:n]                     # r.json()[:n],别忘那个 [:n]

    stories = []                      # 空 list,准备往里攒
    for story_id in ids:
        # 第二步:item/{story_id} 抓这条的 dict  ← 你已有
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        item = requests.get(item_url).json()

        # 从 item 里挑要喂 Claude 的字段,组成一个小 dict,塞进 stories
        stories.append({
            "title": item.get("title"),  # ← 你那个 KeyError,用 .get() 兜
            "score": item.get("score"),
            "url": item.get("url"),   # ← Ask HN 没外链,用 .get() 兜(你 6/16 那个 KeyError)
        })

    return stories                    # ← 交给下一站,不是 print
print(fetch_top_stories())
