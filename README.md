# DebugGym: CI/CD Failure Recovery Environment 🐛⚙️

## Overview

DebugGym is a **production-grade OpenEnv environment** that simulates real-world software debugging workflows inside CI/CD pipelines.

Instead of solving artificial coding problems, agents must:

* Diagnose runtime failures
* Handle malformed inputs
* Fix broken business logic
* Recover from invalid configurations

This mirrors how real engineers debug backend systems under pressure.

---

## Why DebugGym?

Debugging accounts for **40–60% of engineering time** in production systems.

Most benchmarks test:

* Code generation ❌
* Algorithm solving ❌

DebugGym evaluates what actually matters:

* **Bug detection**
* **Fix correctness**
* **Edge-case handling**
* **Recovery under constraints**

---

## Core Features

### 🧠 Multi-Step Reasoning

Agents can:

* Edit code
* Analyze failing tests
* Suggest fixes
* Explain bugs

### 📊 Dense Reward System

Reward is based on:

* Test pass rate
* Improvement over previous steps
* Efficiency (fewer steps = higher score)
* Penalization for bad edits and runtime failures

### 🔒 Safe Execution Sandbox

Prevents:

* OS calls
* Subprocess execution
* Dangerous imports

---

## Tasks (Real Production Scenarios)

### 1. Email Validation Failure (Easy)

Broken user input validation causing crashes on missing or malformed emails.

### 2. User Data Parsing API (Medium)

Handles inconsistent API payloads with missing fields and mixed types.

### 3. Transaction Processing System (Hard)

Processes payments while tracking failed transactions correctly.

### 4. Config Loader Failure (Expert)

Robust config parsing with invalid JSON and missing keys.

### 5. Nested API Response Debugging (Expert+)

Fix deeply nested dictionary access with partial/missing data.

---

## Observation Space

* `code`: Current Python function
* `error_message`: Runtime or syntax error
* `test_results`: List of booleans per test
* `hint`: Feedback on progress
* `logs`: Debug logs including traceback
* `tests_passed`: Number of passing tests
* `tests_total`: Total tests
* `step_count`: Current step
* `max_steps`: Max allowed steps
* `task_name`: Active task

---

## Action Space

* `edit`: Modify one line of code
* `run`: Execute tests
* `explain_bug`: Provide reasoning
* `suggest_fix`: Suggest code improvement
* `analyze_tests`: Inspect failing tests

---

## Reward Function

Reward ∈ [0, 1], computed using:

* Base score: % tests passed
* Improvement bonus: progress vs previous step
* Efficiency bonus: fewer steps = higher score
* Penalties:

  * Invalid edits
  * Runtime errors
  * No-op actions

---

## Environment API

* `reset()` → returns initial observation
* `step(action)` → returns (observation, reward, done, info)
* `state()` → current environment state

---

## Setup

```bash
pip install -r requirements.txt
python inference.py
```

---

## Docker

```bash
docker build -t debuggym .
docker run -e OPENAI_API_KEY=your_key debuggym
```

---

## Baseline Performance

| Task      | Score |
| --------- | ----- |
| easy      | ~0.9  |
| medium    | ~0.8  |
| hard      | ~0.7  |
| expert    | ~0.6  |
| api_debug | ~0.85 |

Average: **~0.77**

---

## Deployment

This environment is fully deployable on Hugging Face Spaces with OpenEnv compatibility.

---

## Why This Matters

DebugGym evaluates a **missing dimension in AI capability**:

> Can an agent fix real-world production failures?

This makes it highly valuable for:

* LLM evaluation
* RL fine-tuning
* Autonomous debugging agents

---

## License

MIT
