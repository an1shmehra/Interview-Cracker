import json
import os
from datetime import datetime

def load_json(filepath):
    """Load a JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  File not found: {filepath}")
        return []
    except Exception as e:
        print(f"✗ Error loading {filepath}: {e}")
        return []

def standardize_question(q, category):
    """Standardize question format - make all questions have same structure"""
    
    # Clean title
    title = q.get("title", "").strip()
    
    # Generate titleSlug if missing
    title_slug = q.get("titleSlug", "")
    if not title_slug and title:
        title_slug = title.lower().replace(' ', '-').replace('?', '').replace(',', '').replace('.', '').replace('(', '').replace(')', '')
    
    # Standardize difficulty
    difficulty = q.get("difficulty", "Unknown")
    
    # Ensure topicTags is a list
    topic_tags = q.get("topicTags", [])
    if not isinstance(topic_tags, list):
        topic_tags = []
    
    # Ensure companyTags is a list or None
    company_tags = q.get("companyTags")
    if company_tags and not isinstance(company_tags, list):
        company_tags = []
    
    # Ensure solutionLinks is a list
    solution_links = q.get("solutionLinks", [])
    if not isinstance(solution_links, list):
        solution_links = []
    
    return {
        "title": title,
        "titleSlug": title_slug,
        "difficulty": difficulty,
        "content": q.get("content", title),
        "category": category,  # Add category!
        "topicTags": topic_tags,
        "companyTags": company_tags,
        "solutionLinks": solution_links,
        "source": q.get("source", "Unknown"),
        "url": q.get("url", ""),
        "acRate": q.get("acRate"),  # Only LeetCode has this
        "scrapedAt": q.get("scrapedAt", datetime.now().isoformat())
    }

def normalize_company_names(questions):
    """Normalize company names to avoid duplicates like 'Google' vs 'google'"""
    for q in questions:
        if q.get("companyTags"):
            normalized = []
            for company in q["companyTags"]:
                if isinstance(company, dict):
                    name = company.get("name", "").strip().title()  # Capitalize properly
                    if name:
                        normalized.append({"name": name})
                elif isinstance(company, str):
                    name = company.strip().title()
                    if name:
                        normalized.append({"name": name})
            q["companyTags"] = normalized if normalized else None
    return questions

def clean_all_data():
    """Clean and consolidate all scraped data"""
    
    all_questions = []
    seen_titles = set()  # Track duplicates by title
    stats = {"dsa": 0, "system_design": 0, "behavioral": 0, "duplicates": 0}
    
    print("=" * 60)
    print("CLEANING AND CONSOLIDATING DATA")
    print("=" * 60)
    
    # 1. Load DSA questions (LeetCode)
    print("\n📚 Loading DSA questions (LeetCode)...")
    leetcode = load_json('data/raw/DSA/leetcode_questions.json')
    for q in leetcode:
        standardized = standardize_question(q, "DSA")
        title = standardized['title']
        
        if title and title not in seen_titles:
            seen_titles.add(title)
            all_questions.append(standardized)
            stats["dsa"] += 1
        else:
            stats["duplicates"] += 1
    
    print(f"✓ Added {stats['dsa']} DSA questions")
    
    # 2. Load System Design questions
    print("\n🏗️  Loading System Design questions...")
    system_design_files = [
        ('data/raw/SystemDesign/system_design_questions.json', 'GitHub'),
        ('data/raw/SystemDesign/medium_system_design_questions.json', 'Medium'),
        ('data/raw/SystemDesign/devto_system_design_questions.json', 'Dev.to')
    ]
    
    for filepath, source_name in system_design_files:
        questions = load_json(filepath)
        count_before = len(all_questions)
        
        for q in questions:
            standardized = standardize_question(q, "System Design")
            title = standardized['title']
            
            if title and title not in seen_titles:
                seen_titles.add(title)
                all_questions.append(standardized)
                stats["system_design"] += 1
            else:
                stats["duplicates"] += 1
        
        added = len(all_questions) - count_before
        print(f"  ✓ {source_name}: +{added} questions")
    
    print(f"✓ Total System Design: {stats['system_design']} questions")
    
    # 3. Load Behavioral questions
    print("\n💬 Loading Behavioral questions...")
    behavioral_files = [
        ('data/raw/Behavioral/github_behavioral_questions.json', 'GitHub'),
        ('data/raw/Behavioral/tech_interview_handbook_questions.json', 'Tech Interview Handbook')
    ]
    
    for filepath, source_name in behavioral_files:
        questions = load_json(filepath)
        count_before = len(all_questions)
        
        for q in questions:
            standardized = standardize_question(q, "Behavioral")
            title = standardized['title']
            
            if title and title not in seen_titles:
                seen_titles.add(title)
                all_questions.append(standardized)
                stats["behavioral"] += 1
            else:
                stats["duplicates"] += 1
        
        added = len(all_questions) - count_before
        print(f"  ✓ {source_name}: +{added} questions")
    
    print(f"✓ Total Behavioral: {stats['behavioral']} questions")
    
    # 4. Normalize company names
    print("\n🏢 Normalizing company names...")
    all_questions = normalize_company_names(all_questions)
    
    # 5. Save cleaned data
    print("\n💾 Saving cleaned data...")
    os.makedirs('data/cleaned', exist_ok=True)
    output_file = 'data/cleaned/all_questions.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)
    
    # 6. Print summary
    print("\n" + "=" * 60)
    print("✅ DATA CLEANING COMPLETE!")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"  • Total questions: {len(all_questions)}")
    print(f"  • Duplicates removed: {stats['duplicates']}")
    print(f"  • Saved to: {output_file}")
    print(f"\n📂 Breakdown by category:")
    print(f"  • DSA: {stats['dsa']} questions")
    print(f"  • System Design: {stats['system_design']} questions")
    print(f"  • Behavioral: {stats['behavioral']} questions")
    print("\n🎉 Ready for database import!")
    print("=" * 60)

if __name__ == "__main__":
    clean_all_data()