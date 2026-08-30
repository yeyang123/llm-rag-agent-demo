# llm-rag-agent-demo

基于 **DeepSeek API** 的 LLM / RAG / Agent 学习演示项目，从最基础的 LLM 调用开始，逐步构建 RAG 与 Agent 能力。

## 项目结构

```
llm-rag-agent-demo/
├─ main.py            # 入口：直接调用 DeepSeek，体验一次完整对话
├─ llm_client.py      # 封装：可复用的 LLM 调用函数 get_llm_response()
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
# 方式一：入口演示
python main.py

# 方式二：测试封装的客户端
python llm_client.py
```

运行成功会输出模型回答和本次消耗的 token 统计。

## 代码说明

### main.py

最小可运行的 LLM 调用示例：加载 `.env` → 创建 OpenAI 兼容客户端（指向 DeepSeek）→ 发起对话 → 打印回答与 token 用量。

### llm_client.py

把对话逻辑封装成函数，供后续 RAG / Agent 代码复用：

```python
from llm_client import get_llm_response

answer, usage = get_llm_response("什么是RAG？一句话")
```

## Roadmap

- [x] LLM 基础调用（DeepSeek）
- [ ] Prompt 模板与多轮对话
- [ ] RAG：文档切分 + 向量检索 + 上下文注入
- [ ] Agent：工具调用（Function Calling）
- [ ] 简单 Web UI

## 注意事项

- `.env` 存有 API Key，已被 `.gitignore` 排除，**任何时候都不要手动提交或截图泄露**
- `temperature=0.1` 让输出更稳定，适合学习调试
