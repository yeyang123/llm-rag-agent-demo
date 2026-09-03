# llm-rag-agent-demo

基于 **DeepSeek API** 的 LLM / RAG / Agent 学习演示项目，从最基础的 LLM 调用开始，逐步构建 RAG 与 Agent 能力。

## 项目结构

```
llm-rag-agent-demo/
├─ main.py            # Day4 入口：while + input() 多轮对话，维护 messages 列表
├─ llm_client.py      # 封装：get_llm_response() 单轮 / chat_with_messages() 多轮
├─ read_txt.py        # Day3 演示：txt 文件读写 + 发起提问
├─ questions.txt      # Day3 演示用的问题文件
├─ http_client.py     # Day5：requests 裸调 HTTP，对照 JSON 理解 SDK 底层
├─ requirements.txt   # 依赖清单
├─ .env               # 存放 API Key（已被 .gitignore 排除，不会上传）
├─ .gitignore         # git 忽略配置
└─ .venv/             # Python 虚拟环境（本地生成，不入库）

```

## 环境要求

- Python 3.10+（推荐 3.13）
- 一个 [DeepSeek](https://platform.deepseek.com/) API Key

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/yeyang123/llm-rag-agent-demo.git
cd llm-rag-agent-demo
```

### 2. 创建并激活虚拟环境

```bash
# 创建
python -m venv .venv

# Windows PowerShell 激活
.venv\Scripts\Activate.ps1

# macOS / Linux 激活
source .venv/bin/activate
```

> Windows 下如果激活脚本报"禁止运行脚本"，先以管理员执行：
> `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置 API Key

在项目根目录创建 `.env` 文件（**切勿提交到 GitHub**）：

```dotenv
DEEPSEEK_API_KEY=sk-你的key
```

### 5. 运行

```bash
# 方式一：多轮对话（Day4）
python main.py

# 方式二：测试封装的客户端（单轮 + 多轮演示）
python llm_client.py
```

多轮对话中支持的特殊命令：

- `exit` / `quit` / `q`：退出对话
- `clear`：清空上下文，相当于开新会话

运行成功会输出模型回答和本次消耗的 token 统计。

## 代码说明

### main.py

Day4 多轮对话入口：`while True` + `input()` 循环读取用户输入，用「列表套字典」维护 `messages` 对话历史，每次把完整历史发给模型，模型因此能记住上下文。核心语法点：列表 `append()` / `pop()`、字典、`while True`、`break` / `continue`、`input()`。

### llm_client.py

把对话逻辑封装成函数，供后续 RAG / Agent 代码复用：

```python
from llm_client import get_llm_response

answer, usage = get_llm_response("什么是RAG？一句话")
```
### http_client.py
SDK 的 client.chat.completions.create(...) 底层其实就是一次 HTTP POST，自己用 requests 复刻一遍，对照完整响应 JSON，搞清 choices[0].message.content 的取值路径

## Roadmap

- [x] LLM 基础调用（DeepSeek）
- [x] 文件读写 + 复用客户端提问
- [x] 多轮对话（messages 列表套字典）
- [x] requests 裸调 HTTP（看懂 SDK 底层）
- [x] requests 裸调 HTTP + temperature 对比 + token 观察
- [ ] Prompt 模板
- [ ] RAG：文档切分 + 向量检索 + 上下文注入
- [ ] Agent：工具调用（Function Calling）
- [ ] 简单 Web UI

## 注意事项

- `.env` 存有 API Key，已被 `.gitignore` 排除，**任何时候都不要手动提交或截图泄露**
- `temperature=0.1` 让输出更稳定，适合学习调试
