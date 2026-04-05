def get_task(task_name: str):

    if task_name == "easy":
        return {
            "name": "easy",
            "code": "def calculate_discount(price, percent):\n    return price / (percent / 100)",
            "tests": [
                ("calculate_discount(100, 10)", 10.0),
                ("calculate_discount(200, 20)", 40.0),
            ]
        }

    elif task_name == "medium":
        return {
            "name": "medium",
            "code": "def parse_user_age(data):\n    return int(data['age'])",
            "tests": [
                ("parse_user_age({'age': '25'})", 25),
                ("parse_user_age({'age': 30})", 30),
            ]
        }

    elif task_name == "hard":
        return {
            "name": "hard",
            "code": "def process_transactions(transactions):\n    total = 0\n    failed = []\n    for t in transactions:\n        if t >= 0:\n            total += t\n        else:\n            failed.append(t)\n    return total, []",
            "tests": [
                ("process_transactions([100, -50, 200])", (300, [-50])),
                ("process_transactions([0])", (0, [])),
            ]
        }

    elif task_name == "expert":
        return {
            "name": "expert",
            "code": "import json\n\ndef load_config(config_str):\n    try:\n        config = json.loads(config_str)\n        return config[\"host\"], int(config[\"port\"])\n    except Exception:\n        return \"localhost\", 3000",
            "tests": [
                ('load_config(\'{"host":"localhost","port":8080}\')', ("localhost", 8080)),
                ('load_config(\'{"host":"prod.com","port":443}\')', ("prod.com", 443)),
                ('load_config(\'{}\')', ("localhost", 3000)),
                ('load_config(\'invalid\')', ("localhost", 3000)),
            ]
        }

    elif task_name == "api_debug":
        return {
            "name": "api_debug",
            "code": "def fetch_user(data):\n    return data[\"user\"][\"age\"]",
            "tests": [
                ("fetch_user({'user': {'age': 25}})", 25),
                ("fetch_user({'user': {'age': 0}})", 0),
            ]
        }

    else:
        raise ValueError("Invalid task")