import os 
import json
from unittest import result
import requests
import time
from groq import Groq 
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
DEV_API_KEY = os.environ.get("DEV_API_KEY")
HISTORY_FILE = "history.json"
print("GROQ_API_KEY:", GROQ_API_KEY)
print("DEV_API_KEY:", DEV_API_KEY)

def loadHistory():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def saveHistory(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


def getGroqClient():
    """
    Returns a Groq client instance using the API key from environment variables.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set.")
    
    return Groq(api_key=api_key)

CURRICULUM = [
    # Week 1 — Foundations
    "What an AI agent actually is: the ReAct pattern explained through a support-bot example",
    "Tool calling from scratch: giving an LLM 'hands' without any framework, in plain Python",
    "Why single-shot LLM calls break down: the context-window-as-to-do-list problem",
    "Your first LangGraph agent: building a StateGraph that survives more than 2 turns",
    "State vs memory in LangGraph: the mistake that makes your agent forget who it's talking to",
    "Conditional edges in LangGraph: teaching an agent to branch instead of following a script",
    "Checkpointing in LangGraph: letting your agent crash mid-task and resume exactly where it left off",
    # Week 2 — Core agent patterns
    "The ReAct loop inside LangGraph: reason, act, observe, repeat — with real tool failures included",
    "Human-in-the-loop agents: pausing execution to ask permission before something risky happens",
    "Building a research agent that actually cites its sources instead of making them up",
    "Handling hallucinated tool calls: what to do when the model invents a function that doesn't exist",
    "Streaming an agent's reasoning to a frontend in real time instead of a loading spinner",
    "Teaching an agent to self-correct: the reflection pattern with a critic node",
    "Debugging a LangGraph agent when you have no idea why it looped forever",
    # Week 3 — Multi-agent orchestration
    "Why one agent isn't enough: the case for specialist agents over one giant prompt",
    "The Supervisor pattern: a manager agent that delegates to specialized workers",
    "Orchestrator-worker with LangGraph's Send API: running agents in parallel correctly",
    "Shared scratchpad vs isolated state: how to actually decide the way your agents talk to each other",
    "Building a 3-agent content pipeline: researcher, writer, and editor agents working in sequence",
    "When agents disagree: building a review/critique loop between two independent agents",
    "Avoiding the multi-agent groupchat spiral: guardrails that stop agents talking in circles",
    # Week 4 — MCP and production
    "What MCP actually solves: the MxN integration problem, explained by wrapping one real API",
    "Building your first MCP server: exposing a single tool to any MCP-compatible AI app",
    "MCP primitives explained: Tools vs Resources vs Prompts, and when to reach for each",
    "Connecting a LangGraph agent to an MCP server: wiring the two together end to end",
    "Local stdio vs remote Streamable HTTP: picking the right MCP transport for your use case",
    "Securing an MCP server: consent flows, scoped credentials, and why trusting the LLM is not a security model",
    "Observability for agents: exactly what to log so a 2am agent failure is debuggable at 2:05am",
    "Deploying a LangGraph + MCP agent: going from a local script to a service that stays up",
    "Capstone: building an end-to-end support-ticket triage agent using everything from this series",
]
 
# Broad themes for dynamic generation once the 30-day curriculum is exhausted



THEMES = [
    "Advanced LangGraph patterns beyond the basics",
    "Production MCP server design",
    "AI agent evaluation and testing",
    "Agent memory and long-term context strategies",
    "Multi-agent system failure modes and recovery",
    "Cost and latency optimization for agentic systems",
    "Real-world agent case studies and postmortems",
]

def callGroq(system_prompt, user_prompt, temperature=0.6, max_tokens=2000):
    try: 
        client = getGroqClient()
        model = "llama-3.3-70b-versatile"
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

    except Exception as e:
        print("An error occurred while calling Groq:", str(e))
        return None
    
def pickTopic(history):
    day_number = len(history["topics"]) + 1
 
    if day_number <= len(CURRICULUM):
        # Curriculum mode: days 1-30, fixed topic, fixed order
        topic = CURRICULUM[day_number - 1]
        return day_number, topic
 
    # Fallback mode: day 31+, dynamic generation via Groq
    past_topics = "\n".join(f"- {t}" for t in history["topics"][-30:]) or "None yet"
    theme = THEMES[(day_number - len(CURRICULUM) - 1) % len(THEMES)]
 
    system = (
        "You are a technical content strategist for a developer blog focused on "
        "agentic AI, LangGraph, and MCP. You pick specific, narrow, non-generic "
        "blog topics grounded in real production problems — not broad overviews."
    )
    user = f"""Theme for today: {theme}
 
Topics already covered (do NOT repeat these or anything too similar):
{past_topics}
 
Give me ONE specific, narrow blog post topic within this theme, ideally still
connected to agentic AI / LangGraph / MCP where it makes sense.
Reply with ONLY the topic as a single line, no numbering, no quotes, no explanation."""
 
    topic = callGroq(system, user, temperature=0.9, max_tokens=60)
    return day_number, topic.strip().strip('"')

def writeArticle(topic,day_number, is_curriculum):
    system = (
        "You are a senior AI engineer writing Day-by-Day developer blog posts on "
        "building agentic AI systems with LangGraph and MCP (Model Context Protocol). "
        "Your audience is developers who can code but are new to agents — treat them "
        "as capable, not clueless. Write in clear, human, conversational prose, like "
        "explaining something to a colleague over coffee, not narrating documentation. "
        "Ground every post in a REAL problem an engineer would actually hit in "
        "production (a support bot that forgets context, an agent that loops forever, "
        "a tool call that hallucinates, etc.) — never a generic 'here's what X is' "
        "overview. Include at least one working, realistic Python code snippet using "
        "actual LangGraph or MCP APIs (StateGraph, add_node, add_conditional_edges, "
        "checkpointers, MCP tools/resources/prompts, etc. as relevant to the topic). "
        "Avoid fluff, avoid listicle tone, avoid restating the title as the intro. "
        "Aim for 800-1100 words in Markdown."
    )
 
    series_note = (
        f"This is Day {day_number} of a 30-day 'Agentic AI with LangGraph + MCP' series."
        if is_curriculum
        else "This is a standalone deep-dive in an ongoing agentic AI series."
    )
 
    user = f"""{series_note}
 
Write a complete blog post on this topic:
 
"{topic}"
 
Open with a concrete scenario or problem (a specific bug, a specific failure, a
specific 'why doesn't this work' moment) — not a definition. Walk through the
concept using that scenario. Include a real, runnable-looking code example.
End with one practical gotcha or lesson learned, then a short forward-looking
line connecting to tomorrow's topic in the series (keep it vague/general, don't
invent a specific day-31 topic).
 
Output ONLY the markdown body (no title/H1, that's handled separately)."""
 
    return callGroq(system, user, temperature=0.7, max_tokens=2000)
    
def generateMetadata(topic, body,day_number, is_curriculum):
    system = (
        "You generate publishing metadata for a dev.to blog post that is part of a "
        "30-day 'Agentic AI with LangGraph + MCP' series. "
        "Always reply with STRICT valid JSON only, no markdown fences, no commentary."
    )
    day_prefix = f"Day {day_number}/30: " if is_curriculum else ""
    user = f"""Topic: {topic}
 
Article body:
---
{body[:3000]}
---
 
Return JSON with exactly these keys:
- "title": a punchy, specific, non-clickbait title (under 70 chars, NOT counting
  the day prefix). Do not include "Day {day_number}" yourself, that gets added separately.
- "tags": an array of up to 4 lowercase tags, no spaces, no '#'. Prefer relevant ones
  from this pool where applicable: langgraph, mcp, agenticai, python, ai, llm,
  machinelearning, tutorial — but only include tags that genuinely fit the content.
- "description": a 1-sentence meta description (under 150 chars)"""
 
    raw = callGroq(system, user, temperature=0.5, max_tokens=300)
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    meta = json.loads(raw)
    meta["title"] = f"{day_prefix}{meta['title']}"
    return meta

# ---------- Step 4: Publisher ----------
def publish(title, body_markdown, tags, description, published=True):
    url = "https://dev.to/api/articles"
    headers = {"api-key": DEV_API_KEY, "Content-Type": "application/json"}
    payload = {
        "article": {
            "title": title,
            "body_markdown": body_markdown,
            "published": published,
            "tags": tags,
            "description": description,
        }
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()



    
def main():
    try: 
        print("date: ", time.strftime("%Y-%m-%d %H:%M:%S"))
        print("step 1: Loading history...")
        history = loadHistory()
        print("history loaded")
        print("step 2: Picking a topic...")
        day_number, topic = pickTopic(history)
        is_curriculum = day_number <= len(CURRICULUM)
        print(f"  -> Day {day_number} ({'curriculum' if is_curriculum else 'dynamic'}): {topic}")
        print(f"Selected topic: {topic}")
        print("step 3: Writing the article...")
        body = writeArticle(topic, day_number, is_curriculum)
        print("Article written")
        print("step 4: Generating metadata...")
        metadata = generateMetadata(topic, body, day_number, is_curriculum)
        print("Metadata generated")
        print(f"  -> title: {metadata['title']}")
        print(f"  -> tags: {metadata['tags']}")
        full_body = f"# {metadata['title']}\n\n{body}"
        print(full_body)
        print("step 5: Publishing the article...")
        result = publish(metadata["title"], full_body, metadata["tags"], metadata["description"])
        print("Article published successfully!")
        print(f"  -> published: {result['url']}")
        print("Step 5: updating history...")
        history["topics"].append(topic)
        history["posts"].append(
            {
                "day": day_number,
                "topic": topic,
                "title": metadata["title"],
                "url": result["url"],
                "ts": int(time.time()),
            }
        )
        saveHistory(history)
        print("Done.")

    except Exception as e:
        print("An error occurred:", str(e)) 

main()