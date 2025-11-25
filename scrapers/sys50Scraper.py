import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import re

# Fetch the page
url = "https://dev.to/somadevtoo/top-50-system-design-interview-questions-for-2024-5dbk"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the article body
article_body = soup.find('div', class_='crayons-article__body')

questions = []
seen_titles = set()

if article_body:
    paragraphs = article_body.find_all('p')
    
    for p in paragraphs:
        text = p.decode_contents()
        lines = re.split(r'<br\s*/?>', text)
        
        for line in lines:
            line_soup = BeautifulSoup(line, 'html.parser')
            clean_text = line_soup.get_text(strip=True)
            
            # Check if it starts with a number
            if re.match(r'^\d+\.', clean_text):
                # Remove the number prefix
                question_text = re.sub(r'^\d+\.\s*', '', clean_text)
                question_text = re.sub(r'\[.*?\]$', '', question_text).strip()
                
                # FILTER: Only include questions that start with "How to Design" or "Design"
                # This excludes the "What is..." comparison questions
                if (question_text.startswith("Design ") or 
                    question_text.startswith("How to Design") or
                    question_text.startswith("How to design")):
                    
                    # Extract solution link if exists
                    solution_link = None
                    link_tag = line_soup.find('a')
                    if link_tag and link_tag.get('href'):
                        solution_link = link_tag['href']
                    
                    # Skip duplicates
                    if question_text not in seen_titles:
                        seen_titles.add(question_text)
                        
                        question = {
                            "title": question_text,
                            "titleSlug": question_text.lower().replace(' ', '-').replace('?', ''),
                            "difficulty": "Unknown",
                            "content": question_text,
                            "topicTags": [
                                {"name": "System Design", "slug": "system-design"}
                            ],
                            "companyTags": None,
                            "solutionLinks": [solution_link] if solution_link else [],
                            "source": "Dev.to - somadevtoo",
                            "url": url,
                            "scrapedAt": datetime.now().isoformat()
                        }
                        questions.append(question)

# Create directory if it doesn't exist
os.makedirs('data/raw/SystemDesign', exist_ok=True)

# Save to JSON file
output_file = 'data/raw/SystemDesign/devto_system_design_questions.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"✅ Saved {len(questions)} design questions to {output_file}")

# Preview first 5 questions
print("\nFirst 5 questions:")
for i, q in enumerate(questions[:5], 1):
    print(f"\n{i}. {q['title']}")