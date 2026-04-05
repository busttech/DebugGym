def get_task(task_name: str):

    if task_name == "easy":
        return {
            "name": "easy",
            "code": """def calculate_discount(price, percent):
    return price / (percent / 100)
""",
            "tests": [
                ("calculate_discount(100, 10)", 10.0),
                ("calculate_discount(200, 20)", 40.0),
            ]
        }

    elif task_name == "medium":
        return {
            "name": "medium",
            "code": """def parse_user_age(data):
    return int(data['age'])
""",
            "tests": [
                ("parse_user_age({'age': '25'})", 25),
                ("parse_user_age({})", 0),
            ]
        }

    elif task_name == "hard":
        return {
            "name": "hard",
            "code": """def process_transactions(transactions):
    total = 0
    failed = []
    for t in transactions:
        if t >= 0:
            total += t
        else:
            failed.append(t)
    return total, []
""",
            "tests": [
                ("process_transactions([100, -50, 200])", (300, [-50])),
                ("process_transactions([0])", (0, [])),
            ]
        }

    elif task_name == "expert":
        return {
            "name": "expert",
            "code": """import json
def load_config(config_str):
    config = json.loads(config_str)
    return config["host"], int(config["port"])
""",
            "tests": [
                ('load_config(\'{}\')', ("localhost", 3000)),
                ('load_config(\'invalid json\')', ("localhost", 3000)),
            ]
        }

    elif task_name == "api_debug":
        return {
            "name": "api_debug",
            "code": """def fetch_user(data):
    return data["user"]["age"]
""",
            "tests": [
                ("fetch_user({'user': {'age': 25}})", 25),
                ("fetch_user({})", 0),
            ]
        }

    else:
        raise ValueError("Invalid task")