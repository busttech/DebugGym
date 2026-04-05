from pydantic import BaseModel
from typing import List, Optional, Literal


class DebugObservation(BaseModel):
    code: str
    error_message: Optional[str] = None
    test_results: List[bool]
    step_count: int
    max_steps: int
    task_name: str
    hint: Optional[str] = None
    logs: Optional[str] = None
    tests_passed: int = 0
    tests_total: int = 0


class DebugAction(BaseModel):
    action_type: Literal[
        "edit",
        "run",
        "explain_bug",
        "suggest_fix",
        "analyze_tests"
    ]
    line_number: Optional[int] = None
    new_code: Optional[str] = None
    bug_explanation: Optional[str] = None


class DebugReward(BaseModel):
    reward: float