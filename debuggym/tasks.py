def get_task(task_name: str):

    if task_name == "easy":
        return {
            "name": "easy",
            "code": "def calculate_discount(price, percent):\n    # Bug: should multiply not divide\n    return price / (percent / 100)",
            "tests": [
                ("calculate_discount(100, 10)", 10.0),
                ("calculate_discount(200, 20)", 40.0),
                ("calculate_discount(50, 50)", 25.0)
            ]
        }

    elif task_name == "medium":
        return {
            "name": "medium",
            "code": "def parse_user_age(data):\n    # Bug: no type conversion safety\n    return int(data['age'])",
            "tests": [
                ("parse_user_age({'age': '25'})", 25),
                ("parse_user_age({'age': 30})", 30),
                ("parse_user_age({'age': '0'})", 0)
            ]
        }

    elif task_name == "hard":
        return {
            "name": "hard",
            "code": "def process_payments(transactions):\n    total = 0\n    negatives = []\n    for t in transactions:\n        if t > 0:\n            total += t\n        else:\n            negatives.append(t)\n    return total, []",
            "tests": [
                ("process_payments([100, -50, 200])", (300, [-50])),
                ("process_payments([500, -100, -200])", (500, [-100, -200])),
                ("process_payments([100])", (100, []))
            ]
        }

    elif task_name == "expert":
        return {
            "name": "expert",
            "code": 'import json\n\ndef parse_config(config_str):\n    try:\n        config = json.loads(config_str)\n        # Bug: missing .get() with defaults, crashes on missing keys\n        return config["host"], config["port"]\n    except json.JSONDecodeError:\n        return "localhost", 3000',
            "tests": [
                ('parse_config(\'{"host":"localhost","port":8080}\')', ("localhost", 8080)),
                ('parse_config(\'{"host":"prod.server.com","port":443}\')', ("prod.server.com", 443)),
                ('parse_config(\'{}\')', ("localhost", 3000)),
                ('parse_config(\'invalid json\')', ("localhost", 3000))
            ]
        }

    else:
        raise ValueError(f"Invalid task: {task_name}")