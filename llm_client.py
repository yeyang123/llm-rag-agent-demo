from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# 为了避免每次调用都重新创建 client，提升多轮对话效率
_client = None


def _get_client():
    """单例获取 client（一个会话只用一个连接对象）"""
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com",
        )
    return _client


def chat_with_messages(messages: list[dict], temperature: float = 0.1):
    """
    支持完整多轮消息的调用。
    messages: OpenAI 标准消息格式，例如：
        [
            {"role": "system", "content": "你是一个助手"},
            {"role": "user",   "content": "你好"},
            {"role": "assistant", "content": "你好呀！"},
            {"role": "user",   "content": "你叫什么？"},
        ]
    """
    client = _get_client()
    res = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=temperature,
    )
    return res.choices[0].message.content, res.usage


def get_llm_response(prompt: str, system: str = "", temperature: float = 0.1):
    """
    兼容旧代码：只传一个 prompt（单轮），内部自动拼成 messages。
    新增参数 system：可选的系统提示词（例如"你是一个简洁的 Python 老师"）。
    """
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    return chat_with_messages(messages, temperature=temperature)


if __name__ == "__main__":
    # 演示 1：单轮调用（向后兼容，原有行为不变）
    ans, usage = get_llm_response("什么是Agent？一句话")
    print("[单轮] " + ans)

    # 演示 2：多轮 messages 调用（Day 4 要学的形式）
    msgs = [
        {"role": "user", "content": "我叫小明"},      # 第一轮：告诉模型名字
        {"role": "assistant", "content": "你好小明！很高兴认识你。"},  # 模拟模型回答
        {"role": "user", "content": "我叫什么名字？"},  # 第二轮：考验模型是否记得
    ]
    ans2, usage2 = chat_with_messages(msgs)
    print("[多轮] " + ans2)
