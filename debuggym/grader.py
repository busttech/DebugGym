import ast
import json as _json


def check_syntax(code):
    try:
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, str(e)


def compare_outputs(result, expected):
    # perfect match
    if result == expected:
        return 1.0

    # partial credit for tuple outputs
    if isinstance(result, tuple) and isinstance(expected, tuple):
        matches = sum(r == e for r, e in zip(result, expected))
        return matches / len(expected)

    # partial credit for lists
    if isinstance(result, list) and isinstance(expected, list):
        if len(expected) == 0:
            return 1.0 if len(result) == 0 else 0.0
        matches = sum(r == e for r, e in zip(result, expected))
        return matches / len(expected)

    return 0.0


def run_tests(code, tests):
    scores = []
    error_message = None

    syntax_ok, syntax_error = check_syntax(code)
    if not syntax_ok:
        return [0.0] * len(tests), syntax_error

    try:
        global_env = {"json": _json}
        local_env = {}
        exec(code, global_env, local_env)

        for expr, expected in tests:
            try:
                result = eval(expr, global_env, local_env)
                score = compare_outputs(result, expected)
                scores.append(score)
            except:
                scores.append(0.0)

    except Exception as e:
        error_message = str(e)
        scores = [0.0] * len(tests)

    return scores, error_message