print("setup started")

import os
import json
from openai import OpenAI

from debuggym.env import DebugGymEnv
from debuggym.models import DebugAction

# ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

TASKS = ["easy", "medium", "hard"]
MAX_STEPS = 8


def get_action_from_llm(observation):
    prompt = f"""
Fix the following Python code.

Code:
{observation.code}

Error:
{observation.error_message}

Tests:
{observation.test_results}

Return ONLY JSON:
{{
 "action_type": "edit",
 "line_number": 0,
 "new_code": "return a + b"
}}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=100
        )

        text = response.choices[0].message.content
        action_json = json.loads(text)
        return DebugAction(**action_json)

    except:
        return DebugAction(action_type="run")


def run_task(task_name):
    env = DebugGymEnv(task_name=task_name)
    obs = env.reset()

    rewards = []
    success = False

    print(f"[START] task={task_name} env=debuggym model={MODEL_NAME}")

    for step in range(1, MAX_STEPS + 1):

        action = get_action_from_llm(obs)

        obs, reward, done, info = env.step(action)

        rewards.append(f"{reward:.2f}")

        error_msg = obs.error_message if obs.error_message else "null"

        print(
            f"[STEP] step={step} action={action.action_type} "
            f"reward={reward:.2f} done={str(done).lower()} error={error_msg}"
        )

        if done:
            success = all(obs.test_results)
            break

    score = sum(float(r) for r in rewards) / len(rewards)

    print(
        f"[END] success={str(success).lower()} "
        f"steps={step} score={score:.2f} rewards={','.join(rewards)}"
    )


if __name__ == "__main__":
    for task in TASKS:
        run_task(task)
        