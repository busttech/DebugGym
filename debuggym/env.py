from debuggym.models import DebugObservation, DebugAction
from debuggym.tasks import get_task
from debuggym.grader import run_tests
from debuggym.utils import sanitize_code, get_hint, format_error


class DebugGymEnv:

    def __init__(self, task_name="email_validation"):
        self.task_name = task_name
        self.max_steps = 12 if task_name == "email_validation" else 18
        self.code = ""
        self.tests = []
        self.step_count = 0
        self.prev_results = []
        self.last_action = None

    def reset(self):
        task = get_task(self.task_name)
        self.code = task["code"]
        self.tests = task["tests"]
        self.step_count = 0

        results, error = run_tests(self.code, self.tests)
        self.prev_results = results

        return DebugObservation(
            code=self.code,
            error_message=error,
            test_results=results,
            step_count=0,
            max_steps=self.max_steps,
            task_name=self.task_name,
            hint=get_hint(results, error, self.code),
            logs=format_error(error),
            tests_passed=int(sum(1 for r in results if r == 1.0)),
            tests_total=len(self.tests)
        )

    def step(self, action: DebugAction):
        self.step_count += 1
        penalty = 0.0
        reward = 0.0

        self.last_action = action.action_type

        # ===== ACTION HANDLING =====

        if action.action_type == "edit":
            lines = self.code.split("\n")

            if action.line_number is None or action.line_number >= len(lines):
                penalty += 0.2
            else:
                new_line = sanitize_code(action.new_code or "")

                if lines[action.line_number] == new_line:
                    penalty += 0.1  # useless edit

                lines[action.line_number] = new_line
                self.code = "\n".join(lines)

        elif action.action_type == "explain_bug":
            if action.bug_explanation and len(action.bug_explanation) > 15:
                reward += 0.2
            else:
                penalty += 0.1

        elif action.action_type == "suggest_fix":
            if action.new_code and len(action.new_code) > 5:
                reward += 0.1
            else:
                penalty += 0.1

        elif action.action_type == "analyze_tests":
            reward += 0.05

        elif action.action_type == "run":
            pass

        else:
            penalty += 0.2

        # ===== TEST EXECUTION =====

        results, error = run_tests(self.code, self.tests)

        prev_passed = sum(self.prev_results)
        current_passed = sum(results)
        total = len(results)

        # ===== REWARD SYSTEM =====

        base_reward = current_passed / total if total > 0 else 0.0

        # smarter improvement logic (with regression penalty)
        improvement = current_passed - prev_passed
        if improvement > 0:
            improvement_bonus = (improvement / total) * 0.3
        elif improvement < 0:
            improvement_bonus = -0.1
        else:
            improvement_bonus = 0.0

        efficiency_bonus = max(0.0, 1.0 - (0.04 * self.step_count))

        reward += base_reward * 0.5 + improvement_bonus + efficiency_bonus * 0.2

        # extra reward for reasoning (judge bonus)
        if action.action_type == "explain_bug":
            reward += 0.05

        if error:
            reward -= 0.1

        reward -= penalty
        reward = max(0.0, min(1.0, round(reward, 2)))

        self.prev_results = results

        # ✅ FIXED DONE CONDITION (IMPORTANT)
        done = (sum(results) == total) or self.step_count >= self.max_steps

        logs = f"""
{format_error(error)}

Last Action: {self.last_action}
Progress: {current_passed}/{total}
"""

        return (
            DebugObservation(
                code=self.code,
                error_message=error,
                test_results=results,
                step_count=self.step_count,
                max_steps=self.max_steps,
                task_name=self.task_name,
                hint=get_hint(results, error, self.code),
                logs=logs,
                tests_passed=int(sum(1 for r in results if r == 1.0)),
                tests_total=total
            ),
            reward,
            done,
            {"penalty": penalty}
        )

    def state(self):
        return {
            "code": self.code,
            "step_count": self.step_count,
            "task_name": self.task_name,
            "tests_passed": int(sum(1 for r in self.prev_results if r == 1.0)),
            "tests_total": len(self.tests)
        }

    def close(self):
        pass