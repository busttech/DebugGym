def get_task(task_name: str):

    if task_name == "email_validation":
        return {
            "name": "email_validation",
            "description": "Fix broken user input validation causing crashes on missing/malformed emails.",
            "difficulty": "easy",
            "code": "def get_domain(user):\n    return user['email'].split('@')[1]",
            "tests": [
                ("get_domain({'email': 'test@gmail.com'})", "gmail.com"),
                ("get_domain({'email': None})", "invalid"),
                ("get_domain({})", "invalid"),
            ]
        }

    elif task_name == "user_api":
        return {
            "name": "user_api",
            "description": "Handle inconsistent API payloads with missing fields and mixed types.",
            "difficulty": "medium",
            "code": "def parse_user(data):\n    return int(data['age'])",
            "tests": [
                ("parse_user({'age': '25'})", 25),
                ("parse_user({'age': 30})", 30),
                ("parse_user({})", 0),
            ]
        }

    elif task_name == "payments":
        return {
            "name": "payments",
            "description": "Process payments while correctly tracking failed transactions.",
            "difficulty": "hard",
            "code": "def process(transactions):\n    total = 0\n    failed = []\n    for t in transactions:\n        if t > 0:\n            total += t\n    return total, []",
            "tests": [
                ("process([100, -50, 200])", (300, [-50])),
                ("process([0, -10])", (0, [-10])),
            ]
        }

    elif task_name == "config_loader":
        return {
            "name": "config_loader",
            "description": "Robust config parsing with invalid JSON and missing keys.",
            "difficulty": "expert",
            "code": "import json\n\ndef load(cfg):\n    data = json.loads(cfg)\n    return data['host'], int(data['port'])",
            "tests": [
                ('load(\'{"host":"localhost","port":8080}\')', ("localhost", 8080)),
                ('load(\'{}\')', ("localhost", 3000)),
                ('load(\'invalid\')', ("localhost", 3000)),
            ]
        }

    elif task_name == "nested_api":
        return {
            "name": "nested_api",
            "description": "Fix deeply nested dictionary access with partial/missing data.",
            "difficulty": "expert_plus",
            "code": "def get_age(data):\n    return data['user']['profile']['age']",
            "tests": [
                ("get_age({'user': {'profile': {'age': 25}}})", 25),
                ("get_age({'user': {}})", 0),
                ("get_age({})", 0),
            ]
        }

    elif task_name == "json_schema_repair":
        return {
            "name": "json_schema_repair",
            "description": (
                "A webhook ingestion pipeline receives malformed API responses. "
                "The normalizer crashes on missing fields, wrong types, and null values. "
                "Fix it to return safe defaults and never raise."
            ),
            "difficulty": "hard",
            "code": (
                "def normalize(payload):\n"
                "    return {\n"
                "        'id': payload['id'],\n"
                "        'amount': float(payload['amount']),\n"
                "        'currency': payload['currency'].upper(),\n"
                "        'status': payload['status']\n"
                "    }"
            ),
            "tests": [
                (
                    "normalize({'id': 'txn_1', 'amount': '49.99', 'currency': 'usd', 'status': 'ok'})",
                    {'id': 'txn_1', 'amount': 49.99, 'currency': 'USD', 'status': 'ok'}
                ),
                (
                    "normalize({'id': 'txn_2', 'amount': None, 'currency': None, 'status': 'pending'})",
                    {'id': 'txn_2', 'amount': 0.0, 'currency': 'UNKNOWN', 'status': 'pending'}
                ),
                (
                    "normalize({})",
                    {'id': 'unknown', 'amount': 0.0, 'currency': 'UNKNOWN', 'status': 'unknown'}
                ),
                (
                    "normalize({'id': 'txn_3', 'amount': 'bad', 'currency': 'EUR', 'status': 'fail'})",
                    {'id': 'txn_3', 'amount': 0.0, 'currency': 'EUR', 'status': 'fail'}
                ),
            ]
        }

    elif task_name == "rate_limiter_audit":
        return {
            "name": "rate_limiter_audit",
            "description": (
                "A production rate limiter has a critical bug: it doesn't correctly "
                "track per-user request counts, allowing unlimited requests and blocking "
                "new users. Fix the logic to enforce per-user limits and return correct audit info."
            ),
            "difficulty": "expert",
            "code": (
                "def check_rate(user_id, requests, limit):\n"
                "    count = requests.get('all', 0)\n"
                "    if count > limit:\n"
                "        return False, count\n"
                "    requests['all'] = count + 1\n"
                "    return True, count"
            ),
            "tests": [
                ("check_rate('u1', {}, 3)", (True, 0)),
                ("check_rate('u1', {'u1': 2}, 3)", (True, 2)),
                ("check_rate('u1', {'u1': 3}, 3)", (False, 3)),
                ("check_rate('u2', {'u1': 3}, 3)", (True, 0)),
            ]
        }

    else:
        raise ValueError(f"Invalid task: {task_name}")