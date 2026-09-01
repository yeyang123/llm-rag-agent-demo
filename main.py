from llm_client import chat_with_messages


def chat_loop(system: str = "你是一个简洁、耐心的 Python 学习助手，回答尽量简短。"):
    """
    Day 4 多轮对话主函数。
    语法学习点：列表、字典、列表.append()、while True、break、continue、input()
    """

    # ========= 【字典 & 列表】初始化消息列表 =========
    # messages 是一个「列表」：[] 包裹，按顺序存每一条对话
    # 列表里的每一项是一个「字典」：{} 包裹，有两个固定 key：role（角色）、content（内容）
    # role 只能是三种：system(系统提示) / user(用户说) / assistant(模型答)
    messages = []

    if system:
        # 【列表追加】：list.append(一个元素)，把字典扔进列表里
        # 这里追加的是一条 system 消息（字典）
        messages.append({"role": "system", "content": system})

    print("=" * 60)
    print("🤖 多轮对话已开启（输入 exit 退出，输入 clear 清空上下文）")
    print("=" * 60)

    # ========= 【while 循环】一直聊，直到用户说退出 =========
    # while True 就是“无限循环”的经典写法，永远为真，直到遇到 break 才跳出
    while True:
        # 【input()】：让用户在终端打字，回车后得到字符串
        user_input = input("\n你：").strip()  # .strip() 去掉两端空格/换行

        # 1) 空输入，跳过（避免用户按回车误触发 API 调用）
        # continue 意思是：跳过本轮循环剩余代码，回到 while True 开头继续下一轮
        if not user_input:
            continue

        # 2) 用户说 exit / quit：结束对话
        # break 意思是：立刻跳出 while 循环（往下走第 97 行的告别语）
        if user_input.lower() in ("exit", "quit", "q"):
            break

        # 3) 用户说 clear：清空上下文（相当于开了一个全新会话）
        if user_input.lower() == "clear":
            # 【列表重置】重新赋值为只有 system 的新列表
            messages = [{"role": "system", "content": system}] if system else []
            print("(已清空上下文，对话从头开始)")
            continue

        # ========= 把用户说的话加入 messages =========
        # 再 append 一个 user 字典
        messages.append({"role": "user", "content": user_input})

        try:
            # 把整个 messages（列表套字典）一起发给模型
            # 模型每次都能看到完整的历史，所以才“记得”之前的对话
            answer, usage = chat_with_messages(messages)
        except Exception as e:
            print(f"❌ 调用失败：{e}")
            # 出错了就把刚才那条 user 消息回滚掉，别让它留在历史里
            # 否则下次再问时 messages 里多了一个没得到回复的提问
            messages.pop()  # 【列表删除最后一项】
            continue

        # ========= 把模型回答也加入 messages =========
        # 下一轮用户再问时，模型就能“看到”自己这次说了什么
        messages.append({"role": "assistant", "content": answer})

        # 打印结果
        print(f"\n助手：{answer}")
        print(
            f"[轮次 {len([m for m in messages if m['role'] != 'system'])} | "
            f"输入 {usage.prompt_tokens} tok / 输出 {usage.completion_tokens} tok]"
        )

    print("\n👋 对话结束，再见！")


if __name__ == "__main__":
    chat_loop()
