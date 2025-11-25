import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import re

# Fetch the page
url = "https://www.techinterviewhandbook.org/behavioral-interview-questions/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

questions = []
seen_titles = set()

# Find the main content area
main_content = soup.find('article') or soup.find('main') or soup.find('div', class_='markdown')

if main_content:
    # Find all list items that contain questions
    # Questions are usually in <li> tags and end with '?'
    list_items = main_content.find_all('li')
    
    print(f"Found {len(list_items)} list items")
    
    for li in list_items:
        text = li.get_text(strip=True)
        
        # Only process if it's a question (contains ?)
        if '?' not in text:
            continue
        
        # Extract company names if they exist
        # Pattern 1: "Question [Company1, Company2]"
        # Pattern 2: "Question (Company)"
        company_names = []
        clean_question = text
        
        # Check for companies in brackets [Company1, Company2]
        bracket_match = re.search(r'\[(.*?)\]', text)
        if bracket_match:
            companies_str = bracket_match.group(1)
            company_names = [c.strip() for c in companies_str.split(',')]
            clean_question = re.sub(r'\s*\[.*?\]', '', text).strip()
        
        # Check for companies in parentheses (Company)
        elif re.search(r'\([A-Z][^)]{2,30}\)', text):  # Match (Capitalized words)
            paren_match = re.search(r'\((.*?)\)', text)
            if paren_match:
                companies_str = paren_match.group(1)
                # Check if it's likely a company name (capitalized, not too long)
                if companies_str[0].isupper() and len(companies_str) < 50:
                    company_names = [c.strip() for c in companies_str.split(',')]
                    clean_question = re.sub(r'\s*\(.*?\)', '', text).strip()
        
        # Skip duplicates
        if clean_question not in seen_titles and len(clean_question) > 10:
            seen_titles.add(clean_question)
            
            question = {
                "title": clean_question,
                "titleSlug": clean_question.lower().replace(' ', '-').replace('?', '').replace(',', '').replace('.', ''),
                "difficulty": "Unknown",
                "content": clean_question,
                "topicTags": [
                    {"name": "Behavioral", "slug": "behavioral"}
                ],
                "companyTags": [{"name": company} for company in company_names] if company_names else None,
                "solutionLinks": [],
                "source": "Tech Interview Handbook",
                "url": url,
                "scrapedAt": datetime.now().isoformat()
            }
            questions.append(question)
            
            companies_display = company_names if company_names else "None"
            print(f"✓ {clean_question[:50]}... | {companies_display}")

else:
    print("⚠️ Could not find main content area")

# Create directory
os.makedirs('data/raw/Behavioral', exist_ok=True)

# Save to JSON
output_file = 'data/raw/Behavioral/tech_interview_handbook_questions.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"\n✅ Saved {len(questions)} behavioral questions to {output_file}")

# Preview first 5
print("\nFirst 5 questions:")
for i, q in enumerate(questions[:5], 1):
    companies = [c['name'] for c in q['companyTags']] if q['companyTags'] else []
    print(f"\n{i}. {q['title'][:70]}...")
    print(f"   Companies: {companies if companies else 'None'}")