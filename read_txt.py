def read_text(path):
    """读取 txt 文件内容"""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_text(path, text):
    """把文本写入 txt（覆盖式）"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

if __name__ == "__main__":
    # 1. 写一个新问题进 txt（演示写入）
    write_text("questions.txt", "什么是 RAG？请用一句话解释")

    # 2. 读出来
    content = read_text("questions.txt")
    print("=== 读到的提问 ===")
    print(content)

    # 3. 发给 DeepSeek
    from llm_client import get_llm_response
    answer, usage = get_llm_response(content)
    print("=== 模型回答 ===")
    print(answer)
    print(f"消耗 token: {usage}")