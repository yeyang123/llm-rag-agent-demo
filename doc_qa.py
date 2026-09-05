"""
Day 7：读文档提问（RAG 雏形）
- Day 3 的零件：read_text() 读 TXT 全文
- Day 6 的零件：ask_llm() 裸调 HTTP
拼起来：文档全文 + 用户问题 -> 塞进 prompt -> 模型只根据文档回答
"""
from read_txt import read_text
from http_client import ask_llm

SYSTEM_PROMPT = "你是一个严谨的客服助手。只能根据【参考文档】里的内容回答问题；文档里没有的信息，就明确说'文档中没有提到'，不许编造。"

def ask_about_doc(doc_text: str, question: str, temperature: float = 0.1):
    """
    把文档全文和问题拼成一个 prompt（这就是最朴素的 RAG：全文注入 stuffing）。
    返回 (answer, usage)。
    """
    prompt = f"""【参考文档】
{doc_text}

【用户问题】
{question}

请根据上面的参考文档回答。"""
    return ask_llm(prompt, system=SYSTEM_PROMPT, temperature=temperature)

if __name__ == "__main__":
    # 1. 读文档（Day 3 的函数）
    doc = read_text("knowledge.txt")
    print(f"已读取文档，共 {len(doc)} 个字符\n")

    # 2. 两个对比问题：一个文档里有，一个文档里没有
    questions = [
        "喵喵翻译机 Pro 卖多少钱？保修多久？",   # 文档里有
        "喵喵翻译机支持韩语吗？",                 # 文档里明确说"不支持"
        "喵喵翻译机有多重？能防水吗？",            # 文档里完全没提 -> 应拒答
    ]

    for q in questions:
        answer, usage = ask_about_doc(doc, q)
        print("=" * 60)
        print(f"问：{q}")
        print(f"答：{answer}")
        print(f"[token: 输入 {usage['prompt_tokens']} / 输出 {usage['completion_tokens']}]")
        print()