from debuggym.models import DebugObservation, DebugAction
from debuggym.tasks import get_task
from debuggym.grader import run_tests, compute_reward
from debuggym.utils import sanitize_code, get_hint

class DebugGymEnv:

    def __init__(self, task_name="easy"):
        self.task_name = task_name
        self.max_steps = 8
        self.code = ""
        self.tests = []
        self.step_count = 0

    def reset(self):
        task = get_task(self.task_name)
        self.code = task["code"]
        self.tests = task["tests"]
        self.step_count = 0

        results, error = run_tests(self.code, self.tests)
        hint = get_hint(results, error, self.code)

        return DebugObservation(
            code=self.code,
            error_message=error,
            test_results=results,
            step_count=0,
            max_steps=self.max_steps,
            task_name=self.task_name,
            hint=hint,
            tests_passed=sum(results),
            tests_total=len(self.tests)
        )

    def step(self, action: DebugAction):
        self.step_count += 1
        penalty = 0.0

        if action.action_type == "edit":
            lines = self.code.split("\n")
            if action.line_number is None or action.line_number >= len(lines):
                penalty += 0.1
            else:
                new_line = action.new_code or ""
                new_line = sanitize_code(new_line)
                lines[action.line_number] = new_line
                self.code = "\n".join(lines)

        elif action.action_type == "run":
            pass

        else:
            penalty += 0.1

        results, error_message = run_tests(self.code, self.tests)
        step_penalty = 0.02 * self.step_count + penalty
        reward = compute_reward(results, step_penalty, self.code)
        done = all(results) or self.step_count >= self.max_steps
        hint = get_hint(results, error_message, self.code)

        return (
            DebugObservation(
                code=self.code,
                error_message=error_message,
                test_results=results,
                step_count=self.step_count,
                max_steps=self.max_steps,
                task_name=self.task_name,
                hint=hint,
                tests_passed=sum(results),
                tests_total=len(results)
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
            "tests_passed": sum(run_tests(self.code, self.tests)[0]),
            "tests_total": len(self.tests)
        }

    def close(self):
        pass