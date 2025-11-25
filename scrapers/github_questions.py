import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# Fetch the page
url = "https://github.com/shashank88/system_design"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all <ul dir="auto"> tags
ul_tags = soup.find_all('ul', {'dir': 'auto'})

# Pick the specific one you want
index = 4  # Change this to get different ul
ul_tag = ul_tags[index]

# Extract and structure the data
questions = []
li_tags = ul_tag.find_all('li')

for i, li in enumerate(li_tags, 1):
    text = li.get_text(strip=True)
    
    # Try to extract links if they exist
    link_tag = li.find('a')
    question_url = link_tag['href'] if link_tag else None
    
    question = {
        "title": text,
        "titleSlug": text.lower().replace(' ', '-').replace('?', ''),
        "difficulty": "Unknown",  # System design doesn't have difficulty ratings
        "content": text,  # The full text of the question
        "topicTags": [{"name": "System Design", "slug": "system-design"}],
        "source": "GitHub - shashank88/system_design",
        "url": question_url if question_url else url,
        "scrapedAt": datetime.now().isoformat()
    }
    questions.append(question)

# Create directory if it doesn't exist
os.makedirs('data/raw/SystemDesign', exist_ok=True)

# Save to JSON file
output_file = 'data/raw/SystemDesign/system_design_questions.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"✅ Saved {len(questions)} questions to {output_file}")