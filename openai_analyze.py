import os
import requests
import json
import sys

api_key = os.getenv("OPENAI_API_KEY")
diff_text = os.getenv("DIFF_DATA")
last_sha = os.getenv("LAST_SHA")
curr_sha = os.getenv("CURR_SHA")

if not api_key:
    with open("ai_summary.txt", "w") as f:
        f.write("Skipping AI Summary: Missing Key.")
    sys.exit(0)

if not diff_text:
    with open("ai_summary.txt", "w") as f:
        f.write("Skipping AI Summary: Missing Diff.")
    sys.exit(0)

url = "https://api.openai.com/v1/responses"

prompt = f"""
你是一个资深 AI 编译器工程师。

请分析 ExecuTorch 从 commit {last_sha} 到 {curr_sha} 的代码变化。

重点关注：
- Qualcomm QNN backend
- MediaTek backend
- native_functions.yaml

输出要求：
1. 技术演进总结
2. 新增算子
3. API变化
4. 架构重构点
5. 对端侧部署的影响

代码 diff：
{diff_text}
"""

payload = {
    "model": "gpt-4.1-mini",
    "input": prompt,
    "max_output_tokens": 1200
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

try:
    resp = requests.post(url, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()

    result = resp.json()
    text = result["output"][0]["content"][0]["text"]

    with open("ai_summary.txt", "w", encoding="utf-8") as f:
        f.write(text)

except Exception as e:
    with open("ai_summary.txt", "w", encoding="utf-8") as f:
        f.write("AI Analysis failed: " + str(e))
