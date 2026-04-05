import ast


def sanitize_code(code: str) -> str:
    banned = ["os.system", "subprocess", "__import__"]
    for b in banned:
        if b in code:
            code = code.replace(b, "# BLOCKED")
    return code


def format_error(error):
    if not error:
        return None

    return f"""
Traceback (most recent call last):
{error}
"""


def get_hint(results, error, code):
    passed = sum(results)
    total = len(results)

    if error:
        return "Error detected. Check logic or data handling."

    if passed == 0:
        return "Logic is incorrect."

    if passed < total:
        return "Edge case failing."

    return "All tests passing."