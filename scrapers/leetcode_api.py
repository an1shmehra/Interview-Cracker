import requests
import json
import os
import time

os.makedirs("data/raw", exist_ok=True)

def load_famous_slugs():
    with open("data/famous_problems.txt") as f:
        return [line.strip() for line in f if line.strip()]

def fetch_problem_detail(slug):
    query = {
        "query": """
        query questionContent($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            title
            titleSlug
            difficulty
            acRate
            content
            topicTags { name slug }
          }
        }
        """,
        "variables": {"titleSlug": slug},
    }
    res = requests.post("https://leetcode.com/graphql", json=query)
    if res.status_code == 200:
        return res.json()
    print(f"Failed for {slug}")
    return None

def fetch_famous_problems():
    famous_slugs = load_famous_slugs()
    for slug in famous_slugs:
        print(f"Fetching {slug} ...")
        detail = fetch_problem_detail(slug)
        if detail:
            with open(f"data/raw/{slug}.json", "w") as f:
                json.dump(detail, f, indent=2)
        time.sleep(0.5)
    print("✅ Done fetching famous problems!")

if __name__ == "__main__":
    fetch_famous_problems()
