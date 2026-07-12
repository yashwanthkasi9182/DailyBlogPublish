# Daily Blog Publish 📝

An automated daily blog publishing system that generates, writes, and publishes developer blog posts to [dev.to](https://dev.to) using AI (Groq LLM). Perfect for maintaining a consistent publication schedule on topics like agentic AI, LangGraph, and MCP.

## Features ✨

- **Automated Content Generation**: Uses Groq API to generate high-quality blog posts
- **30-Day Curriculum**: Built-in 30-day series on "Agentic AI with LangGraph + MCP"
- **Dynamic Topics**: After day 30, automatically generates new topics based on themes
- **Metadata Generation**: Auto-creates titles, tags, and descriptions
- **Direct Publishing**: Publishes articles directly to dev.to via API
- **History Tracking**: Maintains a JSON history of all published articles
- **One-Command Automation**: Single script handles the entire workflow

## Prerequisites 📋

- Python 3.8+
- A [Groq API key](https://console.groq.com) (for content generation)
- A [dev.to API key](https://dev.to/settings/account) (for publishing)
- Active internet connection

## Installation 🚀

### 1. Clone the Repository

```bash
git clone https://github.com/yashwanthkasi9182/DailyBlogPublish.git
cd DailyBlogPublish
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Or manually install:**
```bash
pip install groq requests python-dotenv
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root with your API keys:

```env
GROQ_API_KEY='your_groq_api_key_here'
DEVTO_API_KEY='your_devto_api_key_here'
```

**How to get the keys:**

- **Groq API Key**: Visit https://console.groq.com, sign up, and create an API key in the dashboard
- **dev.to API Key**: Go to https://dev.to/settings/account, scroll to "DEV Community API Keys", and create one

⚠️ **Important**: Never commit your `.env` file to version control (it's already in `.gitignore`)

## Usage 🎯

### Run the Script

```bash
python3 daily_blog_publish.py
```

The script will:
1. Load publishing history from `history.json`
2. Pick a topic (curriculum-based for days 1-30, dynamically generated after)
3. Generate a complete blog post using Groq API
4. Create metadata (title, tags, description)
5. Publish to dev.to
6. Update the history file

### Example Output

```
date:  2024-01-15 10:30:45
step 1: Loading history...
history loaded
step 2: Picking a topic...
  -> Day 1 (curriculum): What an AI agent actually is: the ReAct pattern explained through a support-bot example
Selected topic: What an AI agent actually is: the ReAct pattern explained through a support-bot example
step 3: Writing the article...
Article written
step 4: Generating metadata...
Metadata generated
  -> title: Day 1/30: Understanding AI Agents and the ReAct Pattern
  -> tags: ['agenticai', 'langgraph', 'python', 'tutorial']
step 5: Publishing the article...
Article published successfully!
  -> published: https://dev.to/yashwanthkasi/day-1-understanding-ai-agents-abc123
Step 5: updating history...
Done.
```

## How It Works 🔧

### Workflow

```
Start
  ↓
Load History (history.json)
  ↓
Pick Topic (curriculum or dynamic)
  ↓
Generate Article (Groq API)
  ↓
Generate Metadata (title, tags, description)
  ↓
Publish to dev.to (API)
  ↓
Save History
  ↓
Done
```

### Topic Selection

**Days 1-30**: Uses the built-in curriculum (see `CURRICULUM` in the script)
- Fixed topics in order
- Covers foundations, core patterns, multi-agent orchestration, and production deployment

**Days 31+**: Dynamically generates topics based on themes
- Themes include: Advanced patterns, MCP design, agent evaluation, memory strategies, failure modes, optimization, and case studies
- Rotates through themes to maintain variety

### Content Generation

The script uses three AI prompts:

1. **Topic Picker** (for day 31+): Generates new topics based on themes and past coverage
2. **Article Writer**: Creates 800-1100 word blog posts with:
   - Real problem scenarios
   - Production-focused examples
   - Working Python code snippets
   - Practical gotchas and lessons

3. **Metadata Generator**: Creates:
   - Punchy, SEO-friendly titles (under 70 chars)
   - Relevant tags (langgraph, mcp, agenticai, python, ai, llm, machinelearning, tutorial)
   - Meta descriptions (under 150 chars)

## Project Structure 📁

```
DailyBlogPublish/
├── daily_blog_publish.py      # Main script
├── history.json               # Tracks published articles
├── requirements.txt           # Python dependencies
├── .env                       # API keys (DO NOT COMMIT)
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
└── .github/workflows/         # CI/CD workflows (optional)
```

## History File Format 📊

The `history.json` file tracks all publications:

```json
{
    "topics": [
        "What an AI agent actually is: the ReAct pattern explained through a support-bot example",
        "Tool calling from scratch: giving an LLM 'hands' without any framework, in plain Python"
    ],
    "posts": [
        {
            "day": 1,
            "topic": "What an AI agent actually is: the ReAct pattern explained through a support-bot example",
            "title": "Day 1/30: Understanding AI Agents and the ReAct Pattern",
            "url": "https://dev.to/yashwanthkasi/day-1-understanding-ai-agents-abc123",
            "ts": 1705315845
        }
    ]
}
```

## Configuration 🎛️

### Adjust Article Quality

Edit the `callGroq()` parameters:

```python
callGroq(system, user, temperature=0.6, max_tokens=2000)
```

- **temperature**: 0 = deterministic, 1 = creative (0.6-0.7 recommended for articles)
- **max_tokens**: Maximum response length (2000 is good for articles)

### Change the Curriculum

Edit the `CURRICULUM` list in the script to modify topics:

```python
CURRICULUM = [
    "Your custom topic 1",
    "Your custom topic 2",
    # ... more topics
]
```

### Change the Themes

Edit the `THEMES` list for post-day-30 topic generation:

```python
THEMES = [
    "Your custom theme 1",
    "Your custom theme 2",
]
```

## Automation 🤖

### Schedule with Cron (macOS/Linux)

Run the script daily at 9 AM:

```bash
0 9 * * * cd /path/to/DailyBlogPublish && /path/to/venv/bin/python3 daily_blog_publish.py
```

Edit crontab:
```bash
crontab -e
```

### GitHub Actions (Optional)

Use the included workflow or create `.github/workflows/publish.yml`:

```yaml
name: Daily Blog Publish
on:
  schedule:
    - cron: '0 9 * * *'  # Every day at 9 AM UTC

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Publish blog post
        env:
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
          DEVTO_API_KEY: ${{ secrets.DEVTO_API_KEY }}
        run: python3 daily_blog_publish.py
```

Store API keys as GitHub Secrets in your repository settings.

## Troubleshooting 🐛

### Issue: "GROQ_API_KEY environment variable is not set"

**Solution**: Ensure `.env` file exists and `python-dotenv` is installed:
```bash
pip install python-dotenv
```

### Issue: "Need to specify how to reconcile divergent branches"

**Solution**: Run the fix command:
```bash
git config pull.rebase false
git pull --tags origin main
```

### Issue: "401 Unauthorized" when publishing to dev.to

**Solution**: Verify your dev.to API key:
1. Check your `.env` file for typos
2. Generate a new API key at https://dev.to/settings/account
3. Make sure the key hasn't expired

### Issue: Article published but with wrong content

**Solution**: Check the Groq API response:
1. Verify your Groq account has credits
2. Check rate limits (Groq has free tier limits)
3. Try increasing `max_tokens` or adjusting `temperature`

## Development 💻

### Run in Draft Mode

Modify the `publish()` function call:

```python
result = publish(metadata["title"], full_body, metadata["tags"], metadata["description"], published=False)
```

This publishes as a draft instead of live.

### Debug Mode

Uncomment debug prints in the script:

```python
# print("GROQ_API_KEY:", GROQ_API_KEY)
# print("DEVTO_API_KEY:", DEVTO_API_KEY)
```

### Test Topic Selection

```bash
python3 -c "from daily_blog_publish import *; history={'topics':[]}; print(pickTopic(history))"
```

## API Limits ⚠️

- **Groq**: Free tier has rate limits (~30 requests/minute)
- **dev.to**: No hard limits on article publishing, but avoid spam behavior

## Contributing 🤝

Feel free to fork, improve, and submit PRs! Some ideas:
- Support for other platforms (Medium, Hashnode, etc.)
- Custom templates for article structure
- Better error handling and retry logic
- Scheduling improvements

## License 📜

This project is open source. Use it for your blog or modify as needed!

## Support 💬

If you encounter issues or have questions:
1. Check the **Troubleshooting** section above
2. Review the `.env` file setup
3. Verify API keys are valid and have sufficient credits
4. Check the terminal output for detailed error messages

---

**Happy blogging!** 🎉 Automate your publishing and focus on ideas, not logistics.
