from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from debuggym.env import DebugGymEnv
from debuggym.models import DebugAction

app = FastAPI()

# global env instance
env = DebugGymEnv()


# ---------- REQUEST MODEL ----------
class StepRequest(BaseModel):
    action_type: str
    line_number: Optional[int] = None
    new_code: Optional[str] = None
    bug_explanation: Optional[str] = None


# ---------- HEALTH CHECK ----------
@app.get("/")
def root():
    return {"status": "ok"}


# ---------- RESET (default task) ----------
@app.get("/reset")
def reset():
    obs = env.reset()
    return obs.model_dump()


# ---------- RESET (specific task) ----------
@app.get("/reset/{task_name}")
def reset_task(task_name: str):
    global env
    env = DebugGymEnv(task_name=task_name)
    obs = env.reset()
    return obs.model_dump()


# ---------- STEP ----------
@app.post("/step")
def step(req: StepRequest):
    action = DebugAction(**req.model_dump())
    obs, reward, done, info = env.step(action)
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
    return {
        "tasks": ["email_validation", "user_api", "payments", "config_loader", "nested_api"]
    }