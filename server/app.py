from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from debuggym.env import DebugGymEnv
from debuggym.models import DebugAction
import time

app = FastAPI(
    title="DebugGym API",
    description="CI/CD Failure Recovery Environment for AI Agents",
    version="1.1.0"
)

VALID_TASKS = [
    "email_validation", "user_api", "payments",
    "config_loader", "nested_api", "json_schema_repair", "rate_limiter_audit"
]

# Global env instance
env = DebugGymEnv()

# Global metrics
_metrics = {
    "total_resets": 0,
    "total_steps": 0,
    "total_episodes_completed": 0,
    "rewards_history": [],
    "start_time": time.time()
}


# ---------- HEALTH CHECK ----------
@app.get("/")
def root():
    return {"status": "ok", "version": "1.1.0", "environment": "DebugGym"}


# ---------- RESET (default task) ----------
@app.post("/reset")
@app.get("/reset")
def reset():
    global env
    _metrics["total_resets"] += 1
    obs = env.reset()
    return obs.model_dump()


# ---------- RESET (specific task) ----------
@app.post("/reset/{task_name}")
@app.get("/reset/{task_name}")
def reset_task(task_name: str):
    global env
    if task_name not in VALID_TASKS:
        raise HTTPException(status_code=400, detail=f"Unknown task. Valid tasks: {VALID_TASKS}")
    env = DebugGymEnv(task_name=task_name)
    _metrics["total_resets"] += 1
    obs = env.reset()
    return obs.model_dump()


# ---------- STEP ----------
@app.post("/step")
def step(req: dict):
    if "action" in req:
        action_data = req["action"]
    else:
        action_data = req

    try:
        action = DebugAction(**action_data)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    obs, reward, done, info = env.step(action)
    _metrics["total_steps"] += 1
    _metrics["rewards_history"].append(reward)

    if done:
        _metrics["total_episodes_completed"] += 1

    # Keep rewards_history from growing unbounded
    if len(_metrics["rewards_history"]) > 1000:
        _metrics["rewards_history"] = _metrics["rewards_history"][-1000:]

    return {
        "observation": obs.model_dump(),
        "reward": reward,
        "done": done,
        "info": info,
    }


# ---------- STATE ----------
@app.get("/state")
def state():
    return env.state()


# ---------- LIST TASKS ----------
@app.get("/tasks")
def list_tasks():
    from debuggym.tasks import get_task
    task_info = []
    for t in VALID_TASKS:
        task = get_task(t)
        task_info.append({
            "name": t,
            "description": task.get("description", ""),
            "difficulty": task.get("difficulty", "unknown"),
            "num_tests": len(task.get("tests", []))
        })
    return {"tasks": task_info}


# ---------- METRICS ----------
@app.get("/metrics")
def metrics():
    rewards = _metrics["rewards_history"]
    uptime_seconds = round(time.time() - _metrics["start_time"], 1)
    return {
        "uptime_seconds": uptime_seconds,
        "total_resets": _metrics["total_resets"],
        "total_steps": _metrics["total_steps"],
        "total_episodes_completed": _metrics["total_episodes_completed"],
        "avg_reward": round(sum(rewards) / len(rewards), 4) if rewards else 0.0,
        "max_reward": max(rewards) if rewards else 0.0,
        "min_reward": min(rewards) if rewards else 0.0,
    }

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()