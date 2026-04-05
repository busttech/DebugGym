import ast

def is_valid_python(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False

def count_lines(code: str) -> int:
    return len(code.strip().split("\n"))

def sanitize_code(code: str) -> str:
    banned = [
        "os.system",
        "subprocess",
        "shutil.rmtree",
        "__import__",
    ]
    for b in banned:
        if b in code:
            code = code.replace(b, "# REMOVED_UNSAFE")
    return code

def get_hint(results, error, code):
    if error:
        return f"Runtime/Syntax error: {error}"

    passed = sum(results)
    total = len(results)

    if passed == 0:
        return "No tests passing. Check the core logic completely."
    elif passed < total:
        return f"{passed}/{total} tests passing. You are close, check edge cases."
    else:
        return "All tests passing! Well done."