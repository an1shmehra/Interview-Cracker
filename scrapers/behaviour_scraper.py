import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# Fetch the page
url = "https://github.com/ashishps1/awesome-behavioral-interviews"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the README content
readme = soup.find('article', class_='markdown-body')

questions = []
seen_titles = set()

if readme:
    # Find ALL <details> tags in the document
    all_details = readme.find_all('details')
    
    print(f"Found {len(all_details)} total <details> tags")
    
    # Find the "Questions you can ask the interviewer" heading to know where to stop
    stop_heading = None
    for h2 in readme.find_all('h2'):
        if 'you can ask' in h2.get_text().lower():
            stop_heading = h2
            break
    
    # Process each detail tag
    for detail in all_details:
        summary = detail.find('summary')
        if summary:
            question_text = summary.get_text(strip=True)
            
            # Skip if this detail comes after "Questions you can ask" heading
            if stop_heading:
                # Check if detail comes before the stop heading in the HTML
                try:
                    # Get all elements to determine order
                    all_elements = list(readme.descendants)
                    detail_index = all_elements.index(detail)
                    stop_index = all_elements.index(stop_heading)
                    
                    # If detail comes after the stop heading, skip it
                    if detail_index > stop_index:
                        continue
                except (ValueError, AttributeError):
                    pass  # If we can't determine order, include it
            
            # Skip duplicates and very short questions
            if question_text not in seen_titles and len(question_text) > 5:
                seen_titles.add(question_text)
                
                question = {
                    "title": question_text,
                    "titleSlug": question_text.lower().replace(' ', '-').replace('?', '').replace(',', '').replace('.', ''),
                    "difficulty": "Unknown",
                    "content": question_text,
                    "topicTags": [
                        {"name": "Behavioral", "slug": "behavioral"}
                    ],
                    "companyTags": None,
                    "solutionLinks": [],
                    "source": "GitHub - ashishps1/awesome-behavioral-interviews",
                    "url": url,
                    "scrapedAt": datetime.now().isoformat()
                }
                questions.append(question)
                print(f"Added: {question_text[:60]}...")

# Create directory
os.makedirs('data/raw/Behavioral', exist_ok=True)

# Save to JSON
output_file = 'data/raw/Behavioral/github_behavioral_questions.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"\n✅ Saved {len(questions)} behavioral questions to {output_file}")

# Preview
print("\nFirst 10 questions:")
for i, q in enumerate(questions[:10], 1):
    print(f"{i}. {q['title']}")