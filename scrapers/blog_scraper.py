import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# Fetch the page
url = "https://medium.com/@systemdesignio/45-curated-system-design-questions-and-solutions-i-practiced-to-crack-faang-interviews-1bbe5908d689"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all divs that contain questions (they have h2 + p structure)
question_divs = soup.find_all('div', class_='cp bi gq gr gs gt')

print(f"Found {len(question_divs)} question blocks")

questions = []

for div in question_divs:
    # Find the h2 (question title)
    h2 = div.find('h2')
    if not h2:
        continue
    
    question_title = h2.get_text(strip=True)
    
    # Find the paragraph with company names
    company_p = div.find('p', class_='pw-post-body-paragraph')
    company_names = []
    
    if company_p:
        company_text = company_p.get_text(strip=True)
        # Extract company names after "Company(s) asked:"
        if "Company(s) asked" in company_text:
            # Remove the "Company(s) asked:" part and get the company list
            companies_str = company_text.replace("Company(s) asked:", "").strip()
            companies_str = companies_str.replace("Company(s) asked", "").strip()
            # Split by comma
            company_list = [c.strip() for c in companies_str.split(',')]
            company_names = company_list
    
    # Find solution links
    blockquote = div.find('blockquote')
    solution_links = []
    if blockquote:
        links = blockquote.find_all('a')
        solution_links = [link['href'] for link in links if link.get('href')]
    
    # Create question object
    question = {
        "title": question_title,
        "titleSlug": question_title.lower().replace(' ', '-').replace('?', '').replace(':', ''),
        "difficulty": "Unknown",
        "content": question_title,
        "topicTags": [
            {"name": "System Design", "slug": "system-design"}
        ],
        "companyTags": [{"name": company} for company in company_names] if company_names else None,
        "solutionLinks": solution_links,
        "source": "Medium - systemdesignio",
        "url": url,
        "scrapedAt": datetime.now().isoformat()
    }
    questions.append(question)

# Create directory if it doesn't exist
os.makedirs('data/raw/SystemDesign', exist_ok=True)

# Save to JSON file
output_file = 'data/raw/SystemDesign/medium_system_design_questions.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"✅ Saved {len(questions)} questions to {output_file}")

# Preview first 3 questions
print("\nFirst 3 questions:")
for i, q in enumerate(questions[:3], 1):
    print(f"\n{i}. {q['title']}")
    print(f"   Companies: {[c['name'] for c in q['companyTags']] if q['companyTags'] else 'None'}")
    print(f"   Solution links: {len(q['solutionLinks'])}")