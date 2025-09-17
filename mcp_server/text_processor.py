# text_processor.py

from fastmcp import FastMCP

# 새로운 서버 객체를 생성합니다.
mcp = FastMCP(name="Text Processor Server")

@mcp.prompt("summarize")
async def summarize_prompt(text: str) -> list[dict]:
    """제공된 텍스트를 요약하도록 지시하는 LLM 프롬프트를 생성합니다."""
    print(f"프롬프트 생성: summarize")
    return [
        {"role": "system", "content": "당신은 주어진 텍스트의 핵심 내용을 간결하게 요약하는 전문가입니다."},
        {"role": "user", "content": f"다음 텍스트를 3줄로 요약해 주세요:\n\n---\n{text}\n---"}
    ]

@mcp.prompt("translate_to_korean")
async def translate_to_korean_prompt(text: str) -> list[dict]:
    """제공된 텍스트를 자연스러운 한국어로 번역하도록 지시하는 LLM 프롬프트를 생성합니다."""
    print(f"프롬프트 생성: translate_to_korean")
    return [
        {"role": "system", "content": "You are a professional translator who translates English into fluent, natural Korean."},
        {"role": "user", "content": f"Please translate the following text into Korean:\n\n---\n{text}\n---"}
    ]


# Server 실행
# fastmcp run text_processor.py:mcp --transport sse --port 8084 --host localhost
if __name__ == "__main__":
    print("--- Text Processor Server - SSE ---")

    mcp.run(
        transport="sse",
        host="localhost",
        port=8084
    )
