from fastapi import FastAPI
from pydantic import BaseModel
from debuggym.env import DebugGymEnv
from debuggym.models import DebugAction

app = FastAPI()

# global env instance
env = DebugGymEnv()


# ---------- REQUEST MODEL ----------
class StepRequest(BaseModel):
    action_type: str
    line_number: int | None = None
    new_code: str | None = None
    bug_explanation: str | None = None


# ---------- RESET ----------
@app.get("/reset")
def reset():
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


# ---------- HEALTH CHECK ----------
@app.get("/")
def root():
    return {"status": "ok"}