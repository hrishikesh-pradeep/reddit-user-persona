# Reddit User Persona Analyzer

## Overview

This Python script analyzes the public Reddit activity of a user to generate a detailed **User Persona**. It uses the Groq API with LLaMA 3 (70B) for advanced language analysis and Reddit’s API (via PRAW) to collect the user’s public posts and comments.

The output is a structured report that includes inferred demographics, personality traits (Big Five), interests, values, behavioral patterns, and summary statistics.

---

## Features

- Accepts a Reddit profile URL as input
- Scrapes public posts and comments using Reddit API
- Uses LLaMA 3 (Groq API) for multi-layered persona inference
- Outputs structured persona with confidence scores and source evidence
- Includes proper logging and error handling
- All settings managed via a `.env` configuration file

---

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/hrishikesh-pradeep/reddit-user-persona.git
cd reddit-user-persona
```

2. **Install dependencies**
```bash
pip install praw openai python-dotenv
```

3. **Create a `.env` file**
Create a file named `.env` in the project directory with the following:
```env
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
GROQ_API_KEY=your_groq_api_key
```

---

## Usage

Run the script and enter the Reddit user profile URL when prompted:

```bash
python reddit_scraper.py
```

Example input:
```
Enter link to user profile: https://www.reddit.com/user/Hungry-Move-6603/
```

This will fetch the user’s content, analyze it, and create:
```
Hungry-Move-6603_persona.txt
```

---

## Output Format

The output includes:

- Username and analysis timestamp
- Number of posts and comments analyzed
- Demographic Inference
- Personality Traits (Big Five)
- Values and Beliefs
- Interests and Expertise
- Behavioral Patterns
- Summary (most active subreddits, themes, sentiment)
- Disclaimer about public data usage

---

## Example Output (Excerpt)

```
[User Persona: Hungry-Move-6603]
========================================

## Basic Profile
- Username: Hungry-Move-6603
- Analysis Date: 2025-07-14 UTC
- Content Analyzed: 85 posts, 97 comments

## Demographic Inference
- Age: 25–34 (confidence: 80%)
  • Evidence: "I'm almost 30..." (r/AskReddit, 2024-08-01)
  • Source: https://www.reddit.com/...
```

---

## Ethical Notice

This script:
- Uses only publicly available Reddit data
- Does not store or track private or sensitive information
- Is intended solely for research or academic use

Users are responsible for complying with Reddit’s API and content policies.

---

## License

Licensed under the [MIT License](LICENSE).