from typing import Dict, Any, Optional
from pydantic import BaseModel


class CallToolRequest(BaseModel):
    """
    특정 MCP 서버의 특정 tool을 호출할 때 사용하는 요청 모델

    필드:
    - server: 서버 이름 (예: "calculator", "library", "news", "text_processor")
    - tool: 호출할 도구 이름 (예: "add")
    - args: 도구에 전달할 인자들 (키-값 dict)
    - timeout: 선택적 타임아웃(초 단위)

    예시:

    {
      "server": "calculator",
      "tool": "add",
      "args": {"a": 2, "b": 3},
      "timeout": 5.0
    }

    {
    "server": "library",
    "tool": "search_by_year",
    "args": {"year":2023},
    "timeout": 5.0
    }

    {
    "server": "news",
    "tool": "search_by_category",
    "args": {"category": "IT"},
    "timeout": 5.0
    }
    """
    server: str = "calculator"
    tool: str = "add"
    args: Optional[Dict[str, Any]] = {"a": 2, "b": 3}
    timeout: Optional[float] = 5.0