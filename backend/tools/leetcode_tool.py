# A small curated dataset simulating a LeetCode problem database, organized by topic.
PROBLEM_DATABASE = {
    "dynamic programming": [
        {"id": 70, "title": "Climbing Stairs", "difficulty": "Easy"},
        {"id": 322, "title": "Coin Change", "difficulty": "Medium"},
        {"id": 300, "title": "Longest Increasing Subsequence", "difficulty": "Medium"},
    ],
    "graphs": [
        {"id": 200, "title": "Number of Islands", "difficulty": "Medium"},
        {"id": 133, "title": "Clone Graph", "difficulty": "Medium"},
        {"id": 994, "title": "Rotting Oranges", "difficulty": "Medium"},
    ],
    "arrays": [
        {"id": 1, "title": "Two Sum", "difficulty": "Easy"},
        {"id": 53, "title": "Maximum Subarray", "difficulty": "Medium"},
    ],
    "system design": [
        {"id": 0, "title": "Design a URL Shortener (conceptual, not LeetCode-numbered)", "difficulty": "Medium"},
    ],
}


def get_practice_problems(topic: str) -> list[dict]:
    """
    Given a topic name, returns a list of recommended practice problems.
    This is the actual 'tool' function the LLM will be able to call.
    """
    topic_key = topic.lower().strip()
    return PROBLEM_DATABASE.get(topic_key, [])
