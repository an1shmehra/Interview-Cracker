# Interview Cracker

An AI-powered interview prep platform that brings together coding problems, system design questions, and behavioral interview questions all in one place. Built this to help me and other students stop jumping between LeetCode, YouTube, and random blogs when preparing for interviews.

**[Try it here](https://interview-cracker-ten.vercel.app)**

<img width="1440" height="683" alt="Screenshot 2026-01-08 at 3 55 15 PM" src="https://github.com/user-attachments/assets/39720cfe-b1df-4b0c-b535-846d15f41bc0" />


## What it does

- **1000+ Questions**: Coding challenges, system design scenarios, and behavioral questions scraped from various sources
- **AI Assistant**: Chat with an AI that knows your progress and recommends what to practice next
- **Smart Recommendations**: ML algorithm that figures out if you should practice easy, medium, or hard problems based on what you've completed
- **Progress Tracking**: Keeps track of what you've solved so you don't repeat the same questions
- **Company Tags**: Filter by companies like Google, Meta, Amazon, etc.

## How it works

**Backend**: Python with FastAPI handling the REST API. Used BeautifulSoup to scrape questions from different sites and store everything in PostgreSQL.

**Frontend**: React app with a simple UI. Deployed on Vercel.

**Database**: PostgreSQL hosted on Neon (free tier). Stores questions, companies, topics, and your progress.

## Running it locally

### Backend

You'll need Python 3.9+ and PostgreSQL installed.

```bash
cd backend
pip install -r requirements.txt
Create a .env file:
DATABASE_URL=your_postgres_connection_string
GROQ_API_KEY=your_groq_api_key
Run it:
uvicorn app.main:app --reload
Frontend
You'll need Node.js installed.
cd frontend
npm install
Create a .env file:
VITE_API_URL=http://localhost:8000/api
Run it:
npm run dev
Tech stack
React + Vite
FastAPI
PostgreSQL
BeautifulSoup (for scraping)
Groq API (LLaMA 3.3 70B)
Deployed on Vercel + Render
Contributing
If you find bugs or want to add features, feel free to open an issue or submit a PR. Would love to add more questions or improve the AI recommendations.
Note
This is a personal project I built for interview prep. The questions are scraped from public sources for educational purposes. If you're a content owner and want something removed, just let me know.
