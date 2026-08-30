from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm_response(prompt:str):
    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),base_url="https://api.deepseek.com")
    res = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role":"user","content":prompt}],
        temperature=0.1
    )
    return res.choices[0].message.content, res.usage

if __name__ == "__main__":
    ans,usage = get_llm_response("什么是Agent？一句话")
    print(ans)
    print(usage)