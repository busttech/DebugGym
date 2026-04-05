import ast

def check_syntax(code):
    try:
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, str(e)

def run_tests(code, tests):
    results = []
    error_message = None

    syntax_ok, syntax_error = check_syntax(code)
    if not syntax_ok:
        return [False] * len(tests), syntax_error

    try:
        local_env = {}
        exec(code, {}, local_env)

        for expr, expected in tests:
            try:
                result = eval(expr, {}, local_env)
                results.append(result == expected)
            except:
                results.append(False)

    except Exception as e:
        error_message = str(e)
        results = [False] * len(tests)

    return results, error_message


def compute_reward(results, step_penalty, code):
    if len(results) == 0:
        return 0.0

    syntax_ok, _ = check_syntax(code)
    syntax_bonus = 0.05 if syntax_ok else -0.1

    base_score = sum(results) / len(results)
    reward = max(0.0, min(1.0, base_score + syntax_bonus - step_penalty))
    return round(reward, 2)