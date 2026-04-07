# DebugGym: CI/CD Failure Recovery Environment 🐛⚙️

> *Can an AI agent fix a broken production pipeline at 3am?*

DebugGym is a **product---
title: Debuggym
emoji: ⚡
colorFrom: green
colorTo: yellow
sdk: docker
pinned: false
license: mit
short_description: Create a new Space Spaces are Git repositories that host app
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
ion-grade OpenEnv environment** that simulates real-world CI/CD failure recovery. Instead of solving toy problems, agents must diagnose runtime crashes, fix broken business logic, handle malformed inputs, and recover from misconfigurations — the exact scenarios engineers face under pressure.

---

## Why DebugGym?

Debugging accounts for **40–60% of engineering time** in production systems. Most AI benchmarks test code *generation* from scratch. DebugGym evaluates a missing dimension:

> **Can an agent fix what's already broken?**

This makes it directly valuable for:
- Evaluating LLMs on real-world engineering tasks
- RL fine-tuning for autonomous debugging agents
- CI/CD bot development and testing

---

## 🧠 Unique Features

- **Hybrid Debugging Agent**: Combines rule-based fixes with LLM reasoning for robust, efficient performance on production-like bugs
- **Production-like Failure Scenarios**: Malformed APIs, config crashes, rate limiting bugs, type mismatches, missing fields — all drawn from real-world incidents
- **Dense Reward Shaping**: Agents receive credit for partial progress (fixing 2/3 tests) and are incentivized for efficiency (fewer steps = higher score)
- **Safety-Aware Execution**: Blocks dangerous operations (`os.system`, `subprocess`, `__import__`) ensuring safe sandboxed debugging
- **Environment-Aware Actions**: Rule engine dispatches fixes based on task context, not brittle string matching

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_BASE_URL` | LLM API endpoint | `https://router.huggingface.co/v1` |
| `MODEL_NAME` | Model identifier | `Qwen/Qwen2.5-7B-Instruct` |
| `HF_TOKEN` | Hugging Face / API key | *(required)* |

---

## OpenEnv Compliance

- ✅ Typed Pydantic models (`DebugObservation`, `DebugAction`, `DebugReward`)
- ✅ `step()` / `reset()` / `state()` API
- ✅ `openenv.yaml` metadata with full task registry
- ✅ Reward in `[0.0, 1.0]` range with partial progress signals
- ✅ Reproducible baseline inference script (`inference.py`)
- ✅ Containerized via Docker, deployable to HF Spaces

---

## Tasks (7 Real Production Scenarios)

### 1. 📧 Email Validation Failure — `easy`
Broken user input validation crashes on missing or malformed email fields. Agent must add safe access and return `"invalid"` for bad inputs.

**Tests:** 3 | **Max Steps:** 12

### 2. 👤 User Data Parsing API — `medium`
Handles inconsistent API payloads with missing fields and mixed types (`str` vs `int` for age). Agent must add safe defaults without breaking valid cases.

**Tests:** 3 | **Max Steps:** 12

### 3. 💳 Transaction Processing System — `hard`
Processes payments but fails to track failed (negative) transactions. The `failed` list is always returned empty. Agent must fix the collection logic.

**Tests:** 2 | **Max Steps:** 18

### 4. 🔧 JSON Schema Repair — `hard`
A webhook ingestion pipeline normalizer crashes on `None` values, missing keys, and non-numeric amounts. Agent must make it resilient and return safe defaults for all malformed payloads.

**Tests:** 4 | **Max Steps:** 20

### 5. ⚙️ Config Loader Failure — `expert`
Robust config parsing with invalid JSON strings and missing required keys. Agent must wrap unsafe calls and provide fallback values.

**Tests:** 3 | **Max Steps:** 18

### 6. 🚦 Rate Limiter Audit — `expert`
A production rate limiter has a critical bug: it tracks a global counter instead of per-user counts, causing all users to share a single limit. Agent must fix the per-user tracking logic.

**Tests:** 4 | **Max Steps:** 20

### 7. 🔗 Nested API Response Debugging — `expert_plus`
Fix deeply nested dictionary access that raises `KeyError` on partial/missing response data. Agent must use safe chained `.get()` calls.

**Tests:** 3 | **Max Steps:** 18

---

## Observation Space

| Field | Type | Description |
|-------|------|-------------|
| `code` | `str` | Current Python function under debug |
| `error_message` | `Optional[str]` | Runtime or syntax error |
| `test_results` | `List[float]` | Per-test scores (0.0–1.0) |
| `hint` | `Optional[str]` | Contextual feedback on progress |
| `logs` | `Optional[str]` | Debug logs including traceback |
| `tests_passed` | `int` | Count of fully passing tests |
| `tests_total` | `int` | Total number of tests |
| `step_count` | `int` | Current step in episode |
| `max_steps` | `int` | Episode step limit |
| `task_name` | `str` | Active task identifier |

---

## Action Space

| Action | Fields | Description |
|--------|--------|-------------|
| `edit` | `line_number`, `new_code` | Replace one line of code |
| `run` | — | Execute tests without editing |
| `explain_bug` | `bug_explanation` | Provide reasoning about the bug (reward bonus) |
| `suggest_fix` | `new_code` | Suggest a fix (reward bonus) |
| `analyze_tests` | — | Inspect failing tests (small reward bonus) |

---

## Reward Function

Reward ∈ `[0.0, 1.0]`, computed every step:

```
reward = base_reward × 0.5
       + improvement_bonus     # progress vs previous step
       + efficiency_bonus      # fewer steps = higher score
       + reasoning_bonus       # for explain_bug actions
       - error_penalty         # for runtime errors
       - action_penalty        # for invalid/no-op edits
```

The reward provides **dense signals throughout the episode**, not just at the end. Agents receive credit for partial progress (e.g. fixing 2/3 tests).

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/reset` | GET, POST | Reset default task |
| `/reset/{task_name}` | GET, POST | Reset specific task |
| `/step` | POST | Submit action, get observation + reward |
| `/state` | GET | Current environment state |
| `/tasks` | GET | List all tasks with metadata |
| `/metrics` | GET | Live reward and episode statistics |

---

## Baseline Scores

Scores from running `inference.py` with rule-based + LLM fallback agent:

| Task | Difficulty | Score | Steps | Success |
|------|-----------|-------|-------|---------|
| `email_validation` | easy | 0.89 | 1 | ✅ |
| `user_api` | medium | 0.79 | 1 | ✅ |
| `payments` | hard | 0.84 | 1 | ✅ |
| `json_schema_repair` | hard | 0.92 | 1 | ✅ |
| `config_loader` | expert | 0.89 | 1 | ✅ |
| `rate_limiter_audit` | expert | 0.80 | 1 | ✅ |
| `nested_api` | expert_plus | 0.89 | 1 | ✅ |
| **Average** | | **0.86** | | **7/7** |

---

## Setup & Usage

### Local

```bash
pip install -r requirements.txt

# Set environment variables
export API_BASE_URL=https://router.huggingface.co/v1
export MODEL_NAME=Qwen/Qwen2.5-7B-Instruct
export HF_TOKEN=your_token_here

# Run inference
python inference.py
```

### Docker

```bash
docker build -t debuggym .
docker run -e HF_TOKEN=your_token debuggym
```

### API Usage Example

```python
import requests

# Reset to a task
obs = requests.get("http://localhost:7860/reset/email_validation").json()

# Submit an action
result = requests.post("http://localhost:7860/step", json={
    "action_type": "edit",
    "line_number": 1,
    "new_code": "    return (user.get('email') or '').split('@')[1] if '@' in str(user.get('email')) else 'invalid'"
}).json()

print(result["reward"])   # 0.89
print(result["done"])     # True
```

---

## Project Structure

```
debuggym/
├── __init__.py         # Package entry
├── env.py              # DebugGymEnv — core environment
├── models.py           # Pydantic typed models
├── tasks.py            # 7 task definitions
├── grader.py           # Safe test execution + scoring
├── utils.py            # Helpers: sanitize, hints, formatting
inference.py            # Baseline agent (rule-based + LLM)
server/app.py           # FastAPI HTTP server
openenv.yaml            # OpenEnv spec metadata
Dockerfile              # Container definition
requirements.txt        # Python dependencies
```

---

## Safe Execution

The sandbox blocks dangerous operations:
- `os.system` calls
- `subprocess` execution
- Dynamic `__import__`

All agent code edits are validated for syntax before execution.

---

## License

MIT
