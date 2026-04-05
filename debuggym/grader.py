import ast
import json as _json


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
        global_env = {"json": _json}
        local_env = {}
        exec(code, global_env, local_env)

        for expr, expected in tests:
            try:
                result = eval(expr, global_env, local_env)
                results.append(result == expected)
            except:
                results.append(False)

    except Exception as e:
        error_message = str(e)
        results = [False] * len(tests)

    return results, error_message