import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from debuggym.env import DebugGymEnv
from debuggym.models import DebugAction
load_dotenv()

# ================= CONFIG =================

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-7B-Instruct")  # safer than 72B
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

TASKS = ["easy", "medium", "hard", "expert", "api_debug"]
MAX_STEPS = 8


# ================= HELPERS =================

def safe_parse_json(text):
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
    except:
        return None


def fallback_action(obs):
    if obs.error_message:
        return DebugAction(
            action_type="edit",
            line_number=0,
            new_code="# fix error"
        )

    if obs.tests_passed < obs.tests_total:
        return DebugAction(
            action_type="suggest_fix",
            new_code="# improve logic"
        )

    return DebugAction(action_type="run")


def get_action_from_llm(obs):
    prompt = f"""
Fix the Python code.

Code:
{obs.code}

Error:
{obs.error_message}

Tests:
{obs.test_results}

Return ONLY JSON:
{{
 "action_type": "edit",
 "line_number": 0,
 "new_code": "..."
}}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=120
        )

        text = response.choices[0].message.content or ""
        parsed = safe_parse_json(text)

        if parsed:
            return DebugAction(**parsed)

    except:
        pass

    return fallback_action(obs)


# ================= MAIN =================

def run_task(task_name):
    env = DebugGymEnv(task_name=task_name)
    obs = env.reset()

    rewards = []
    success = False
    step = 0

    print(f"[START] task={task_name} env=debuggym model={MODEL_NAME}")

    try:
        for step in range(1, MAX_STEPS + 1):

            action = get_action_from_llm(obs)

            obs, reward, done, _ = env.step(action)

            rewards.append(reward)

            error_val = obs.error_message if obs.error_message else None
            error_str = error_val if error_val else "null"

            print(
                f"[STEP] step={step} action={action.action_type} "
                f"reward={reward:.2f} done={str(done).lower()} error={error_str}"
            )

            if done:
                success = all(obs.test_results)
                break

    except Exception:
        success = False

    finally:
        score = sum(rewards) / len(rewards) if rewards else 0.0
        score = max(0.0, min(1.0, score))

        rewards_str = ",".join(f"{r:.2f}" for r in rewards)

        print(
            f"[END] success={str(success).lower()} "
            f"steps={step} score={score:.2f} rewards={rewards_str}"
        )

        try:
            env.close()
        except:
            pass


if __name__ == "__main__":
    for task in TASKS:
        run_task(task)