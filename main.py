from llm_client import get_llm_response

if __name__ == "__main__":
    print("===== 测试DeepSeek调用 =====")
    prompt = "什么是Agent？一句话"
    answer, usage = get_llm_response(prompt)

    print("大模型输出：")
    print(answer)
    print("\ntoken消耗统计：")
    print(usage)
