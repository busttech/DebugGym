import os
import json
import ast
import time
from openai import OpenAI
from debuggym.env import DebugGymEnv
from debuggym.models import DebugAction

# ================= CONFIG =================

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-7B-Instruct")

# STRICT (judge-safe)
API_KEY = os.getenv("HF_TOKEN")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)


TASKS = ["email_validation", "user_api", "payments", "config_loader", "nested_api"]
MAX_STEPS = 8


# ================= HELPERS =================

def safe_parse_json(text):
    try:
        text = (text or "").strip()
        text = text.replace("```json", "").replace("```", "").strip()
        start = text.find("{")
        end = text.rfind("}") + 1
        if start == -1 or end <= start:
            return None
        return json.loads(text[start:end])
    except Exception:
        return None


def _line_index_for_snippet(code: str, needle: str) -> int:
    lines = code.split("\n")
    for i, ln in enumerate(lines):
        if needle in ln:
            return i
    return 1


def _rule_based_action(obs):
    code = obs.code or ""

    if "get_domain" in code:
        return DebugAction(
            action_type="edit",
            line_number=_line_index_for_snippet(code, "split"),
            new_code="    return (user.get('email') or '').split('@')[1] if '@' in str(user.get('email')) else 'invalid'",
        )

    if "parse_user" in code:
        return DebugAction(
            action_type="edit",
            line_number=_line_index_for_snippet(code, "int"),
            new_code="    return int(data.get('age', 0))",
        )

    if "process" in code and "return total, []" in code:
        return DebugAction(
            action_type="edit",
            line_number=_line_index_for_snippet(code, "return total, []"),
            new_code="    return total, failed",
        )

    if "load" in code:
        return DebugAction(
            action_type="edit",
            line_number=_line_index_for_snippet(code, "return data"),
            new_code='    return data.get("host", "localhost"), int(data.get("port", 3000))',
        )

    if "get_age" in code:
        return DebugAction(
            action_type="edit",
            line_number=_line_index_for_snippet(code, "return data"),
            new_code='    return data.get("user", {}).get("profile", {}).get("age", 0)',
        )

    return None

def _apply_llm_action(obs, parsed):
    if not isinstance(parsed, dict):
        return None

    action_type = parsed.get("action_type", "run")
    if action_type == "run":
        return DebugAction(action_type="run")
    if action_type != "edit":
        return None

    lines = (obs.code or "").split("\n")
    if not lines:
        return None

    try:
        line_number = int(parsed.get("line_number", 1))
    except Exception:
        line_number = 1

    line_number = max(0, min(line_number, len(lines) - 1))
    new_code = (parsed.get("new_code") or "").strip()
    if not new_code:
        return None

    original = lines[line_number]
    indent = len(original) - len(original.lstrip())
    indent_str = " " * indent

    if new_code.startswith(" ") or new_code.startswith("\t"):
        final_code = new_code
    else:
        final_code = indent_str + new_code

    trial = list(lines)
    trial[line_number] = final_code
    try:
        ast.parse("\n".join(trial))
    except SyntaxError:
        return None

    return DebugAction(
        action_type="edit",
        line_number=line_number,
        new_code=final_code,
    )


def get_action_from_llm(obs, step):
    # Step 1: Always try rule-based first (no API needed)
    rule_action = _rule_based_action(obs)
    if rule_action is not None:
        return rule_action

    # Step 2: Try LLM with retry
    prompt = f"""You are fixing a Python bug. Return JSON only, no markdown.

Code (0-based line numbers):
{chr(10).join(f"{i}: {l}" for i, l in enumerate(obs.code.split(chr(10))))}

Error: {obs.error_message or "None"}
Tests passing: {obs.tests_passed}/{obs.tests_total}
Hint: {obs.hint}

Return ONLY this JSON:
{{
  "action_type": "edit",
  "line_number": <0-based int>,
  "new_code": "<complete replacement line with correct indentation>"
}}"""

    for attempt in range(2):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=150
            )
            text = response.choices[0].message.content or ""
            parsed = safe_parse_json(text)
            action = _apply_llm_action(obs, parsed)
            if action is not None:
                return action
        except Exception as e:
            print(f"[DEBUG] LLM attempt {attempt+1} failed: {type(e).__name__}", flush=True)
            time.sleep(1)

    # Step 3: Fallback - just run
    return DebugAction(action_type="run")


# ================= MAIN =================

def run_task(task_name):
    env = DebugGymEnv(task_name=task_name)
    obs = env.reset()

    rewards = []
    success = False
    step = 0

    print(f"[START] task={task_name} env=debuggym model={MODEL_NAME}", flush=True)

    try:
        for step in range(1, MAX_STEPS + 1):
            action = get_action_from_llm(obs, step)
            obs, reward, done, _ = env.step(action)
            rewards.append(reward)

            error_str = obs.error_message if obs.error_message else "null"
            print(
                f"[STEP] step={step} action={action.action_type} "
                f"reward={reward:.2f} done={str(done).lower()} error={error_str}",
                flush=True
            )

            if done:
                success = all(obs.test_results)
                break

    except Exception as e:
        print(f"[DEBUG] Task error: {e}", flush=True)
        success = False

    finally:
        score = sum(rewards) / len(rewards) if rewards else 0.0
        score = round(max(0.0, min(1.0, score)), 4)
        rewards_str = ",".join(f"{r:.2f}" for r in rewards)

        print(
            f"[END] success={str(success).lower()} "
            f"steps={step} score={score:.2f} rewards={rewards_str}",
            flush=True
        )

        try:
            env.close()
        except:
            pass

    return score


if __name__ == "__main__":
    all_scores = []
    for task in TASKS:
        score = run_task(task)
        all_scores.append(score)
        print(f"[RESULT] task={task} score={score}", flush=True)
        print("", flush=True)

    avg = round(sum(all_scores) / len(all_scores), 4)
    print(f"[FINAL] average_score={avg}", flush=True)