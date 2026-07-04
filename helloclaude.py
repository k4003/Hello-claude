import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()                             # 读 .env，把 KEY 灌进本进程的环境变量
api_key = os.getenv("ANTHROPIC_API_KEY")  # 从环境里读出来（就是 hn.py 学过的 os.getenv）

client = Anthropic(api_key=api_key)       # 拿 key 建一个客户端对象

message = client.messages.create(
    model="claude-haiku-4-5-20251001",    # 最便宜的模型，测试够用
    max_tokens=100,                       # 输出上限，必填
    messages=[
        {"role": "user", "content": "Hello, Claude! 用一句话证明你在。"}
    ],
)

print(message.content[0].text)