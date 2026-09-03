import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

# DeepSeek 的 OpenAI 兼容接口：SDK 底下其实就是 POST 到这个 URL
API_URL = "https://api.deepseek.com/chat/completions"

def chat_raw(messages: list[dict], temperature: float = 0.1) -> dict:
    """
    【Day5 核心】用 requests 裸调 HTTP，不用 SDK。
    SDK 的一行 client.chat.completions.create(...)
    底层 = 一次带 JSON 请求体的 HTTP POST，返回一个 JSON 响应。
    这里返回【未拆包】的完整响应字典。
    """
    headers = {
        # 认证：固定格式 "Bearer<空格>API Key"
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
        "Content-Type": "application/json",  # 告诉服务器：请求体是 JSON
    }
    payload = {
        # 请求体：和 SDK 时传的参数一样，只是自己拼字典
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": temperature,
    }
    # json=payload 会自动把字典序列化成 JSON 字符串
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    if not resp.ok:
        print("API 错误响应体:", resp.text)   # 看清 DeepSeek 到底说了啥
        resp.raise_for_status()
    return resp.json()       # JSON 字符串 -> Python 字典

def chat_with_messages(messages: list[dict], temperature: float = 0.1):
    """
    和 llm_client.chat_with_messages 相同的对外接口（返回 answer, usage）。
    区别：取值全用字典语法，usage 是字典不是对象。
    """
    data = chat_raw(messages, temperature=temperature)
    answer = data["choices"][0]["message"]["content"]
    usage = data["usage"]  # 字典：usage["prompt_tokens"] / usage["completion_tokens"]
    return answer, usage

def ask_llm(prompt: str, system: str = "", temperature: float = 0.1):
    """
    【Day6】单轮提问的便捷封装。
    和 Day3 llm_client.get_llm_response 接口一致，但底层走裸调 HTTP。
    返回 (answer, usage_dict)。
    """
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
    return chat_with_messages(messages, temperature=temperature)

if __name__ == "__main__":
        # ============================================================
    # 【Day6 实验】同一问题，三个温度对比 + token 观察
    # ============================================================
    PROMPT = "用一句话介绍 Python 的列表推导式"
    SYSTEM = "你是一个简洁的 Python 老师"

    print("=" * 60)
    print("【Day6】温度对比实验")
    print("=" * 60)

    for t in (0.1, 0.7, 1.5):  # 低 / 中 / 高
        ans, usage = ask_llm(PROMPT, system=SYSTEM, temperature=t)
        print(f"\n--- temperature = {t} ---")
        print(f"回答: {ans}")
        print(f"token: 输入 {usage['prompt_tokens']} / "
              f"输出 {usage['completion_tokens']} / "
              f"合计 {usage['total_tokens']}")
    # ============================================================
    # 第 1 部分：单次调用，打印完整响应 JSON
    # ============================================================
    msgs = [{"role": "user", "content": "什么是HTTP？一句话回答"}]

    data = chat_raw(msgs)

    print("=" * 60)
    print("【1】完整响应 JSON")
    print("=" * 60)
    # ensure_ascii=False 中文正常显示；indent=2 缩进排版
    print(json.dumps(data, ensure_ascii=False, indent=2))

    # ============================================================
    # 第 2 部分：层层拆包，对照上面的 JSON 看取值路径
    # ============================================================
    print("=" * 60)
    print("【2】一层层取值")
    print("=" * 60)
    print(f"data                    类型: {type(data).__name__}")                 # dict
    print(f"data['choices']         类型: {type(data['choices']).__name__}")     # list
    print(f"data['choices'][0]      类型: {type(data['choices'][0]).__name__}")  # dict
    print(f"data['choices'][0]['message'] 内容: {data['choices'][0]['message']}")

    # 沿着结构一路取到底：字典 -> 列表 -> 字典 -> 字典
    content = data["choices"][0]["message"]["content"]
    print(f"\n最终答案: {content}")

    # usage 也是字典（SDK 里是对象 res.usage.prompt_tokens）
    print(f"输入 token: {data['usage']['prompt_tokens']}")
    print(f"输出 token: {data['usage']['completion_tokens']}")

    # 对照记忆（本质是同一份数据，SDK 只是把 resp.json() 的字典包装成了对象）：
    # SDK : res.choices[0].message.content          （点号取属性）
    # 裸调: data["choices"][0]["message"]["content"] （方括号取键 / 下标）

    # ============================================================
    # 第 3 部分：多轮对话（复刻 main.py，换用裸调客户端）
    # ============================================================
    print("=" * 60)
    print("【3】多轮对话（输入 exit 退出）")
    print("=" * 60)

    messages = [{"role": "system", "content": "你是一个简洁、耐心的 Python 学习助手，回答尽量简短。"}]

    while True:
        user_input = input("\n你：").strip()
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "q"):
            break

        messages.append({"role": "user", "content": user_input})
        try:
            answer, usage = chat_with_messages(messages)
        except Exception as e:
            print(f"❌ 调用失败：{e}")
            messages.pop()  # 回滚没得到回复的提问
            continue

        messages.append({"role": "assistant", "content": answer})
        print(f"\n助手：{answer}")
        print(f"[输入 {usage['prompt_tokens']} tok / 输出 {usage['completion_tokens']} tok]")

    print("\n👋 对话结束，再见！")