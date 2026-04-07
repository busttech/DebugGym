def get_task(task_name: str):

    if task_name == "email_validation":
        return {
            "name": "email_validation",
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
            "code": "def process(transactions):\n    total = 0\n    failed = []\n    for t in transactions:\n        if t > 0:\n            total += t\n    return total, []",
            "tests": [
                ("process([100, -50, 200])", (300, [-50])),
                ("process([0, -10])", (0, [-10])),
            ]
        }

    elif task_name == "config_loader":
        return {
            "name": "config_loader",
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
            "code": "def get_age(data):\n    return data['user']['profile']['age']",
            "tests": [
                ("get_age({'user': {'profile': {'age': 25}}})", 25),
                ("get_age({'user': {}})", 0),
                ("get_age({})", 0),
            ]
        }

    else:
        raise ValueError("Invalid task")