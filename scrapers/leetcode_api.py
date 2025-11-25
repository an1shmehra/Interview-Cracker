import requests
import json
import os
import time

os.makedirs("data/raw/DSA", exist_ok=True)

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
            companyTags { name slug }
          }
        }
        """,
        "variables": {"titleSlug": slug},
    }
    
    try:
        res = requests.post("https://leetcode.com/graphql", json=query, timeout=15)
    except Exception as e:
        print(f"Request error for {slug}: {e}")
        return None
    
    if res.status_code != 200:
        print(f"Failed for {slug} (status {res.status_code})")
        return None
    
    data = res.json()
    
    # check for GraphQL errors
    if data.get("errors"):
        print(f"GraphQL errors for {slug}: {data['errors']}")
        return None
    
    question = data.get("data", {}).get("question")
    if not question:
        print(f"No question data for {slug}")
        return None
    
    # add metadata: source + url
    question["source"] = "LeetCode"
    question["url"] = f"https://leetcode.com/problems/{slug}/"
    
    return question

def fetch_famous_problems():
    famous_slugs = load_famous_slugs()
    all_questions = []  # Store all questions in a list
    
    for slug in famous_slugs:
        print(f"Fetching {slug} ...")
        detail = fetch_problem_detail(slug)
        
        if detail:
            all_questions.append(detail)  # Add to the list
        
        time.sleep(0.5)
    
    # Save ALL questions to ONE file
    output_file = "data/raw/DSA/leetcode_questions.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Done! Saved {len(all_questions)} questions to {output_file}")

if __name__ == "__main__":
    fetch_famous_problems()

    