import spacy
import time
import random
from typing import List, Dict

# Load SpaCy model safely
def load_nlp_model(model_name: str = "en_core_web_sm"):
    try:
        return spacy.load(model_name)
    except OSError:
        raise SystemExit(f"Model '{model_name}' not found. Please run: python -m spacy download {model_name}")

nlp = load_nlp_model()

# Define static keywords (can be loaded from config/database)
SKILL_KEYWORDS = set([
    "python", "java", "javascript", "react", "node.js", "aws", "azure", "gcp", "sql", "nosql",
    "docker", "kubernetes", "git", "api", "rest", "graphql", "frontend", "backend", "fullstack",
    "machine learning", "ai", "deep learning", "data science", "cloud", "agile", "scrum", "devops",
    "testing", "security", "linux", "windows", "mobile", "web", "database", "design patterns",
    "architecture", "communication", "teamwork", "problem solving", "leadership", "management",
    "analytical", "critical thinking", "collaboration", "mentoring", "debugging", "scalability",
    "performance", "optimization", "microservices", "ci/cd", "data structures", "algorithms", "oop",
    "object-oriented programming"
])

POSITIVE_REMARKS = [
    "Great explanation!",
    "Excellent clarity!",
    "That's a strong answer!",
    "Well said!",
    "Impressive experience!",
    "You’ve demonstrated solid understanding!"
]

# Extract skills from job description
def extract_skills_from_jd(text: str) -> List[str]:
    doc = nlp(text.lower())
    found = set()

    for token in doc:
        if token.text in SKILL_KEYWORDS:
            found.add(token.text)

    for chunk in doc.noun_chunks:
        if chunk.text.strip() in SKILL_KEYWORDS:
            found.add(chunk.text.strip())

    return sorted(found)

# Generate a relevant question for a topic
def generate_question(topic: str) -> str:
    templates = [
        f"Can you explain your experience with {topic}?",
        f"What challenges have you faced while working with {topic}?",
        f"How would you rate your proficiency in {topic} and why?",
        f"Can you share a project where you used {topic}?",
        f"What are some best practices you follow in {topic}?"
    ]
    return random.choice(templates)

# Simulated comparison to ideal answers (mocked)
def is_response_good(topic: str, response: str) -> bool:
    keywords = topic.split()
    return all(word.lower() in response.lower() for word in keywords)

# Provide positive reinforcement and suggestions
def provide_feedback(is_good: bool) -> str:
    if is_good:
        return random.choice(POSITIVE_REMARKS)
    else:
        return "That's a good start! Consider including more specific details or examples."

# Interactive AI interview session
def run_interview(job_description: str, max_questions: int = 5):
    print("\n--- AI Interview Started ---\n")
    topics = extract_skills_from_jd(job_description)
    
    if not topics:
        print("!! Could not identify relevant topics from job description.")
        return

    print(f"Identified Skills: {', '.join(topics)}")

    asked = 0
    for topic in topics[:max_questions]:
        print(f"\n AI: {generate_question(topic)}")
        response = input(" You: ").strip()

        if not response:
            print("!! No response detected. Skipping topic.\n")
            continue

        # Simulated analysis
        good = is_response_good(topic, response)
        feedback = provide_feedback(good)
        print(f"🤖 AI Feedback: {feedback}")
        asked += 1

    print("\n🎉 Interview Concluded")
    print(" Great job! Keep practicing for more confidence.")

# Demo mode with optional user JD
if __name__ == "__main__":
    default_jd = """
    We're hiring a Full Stack Developer with experience in React, Node.js, REST APIs, and AWS.
    Familiarity with Docker, CI/CD, and Agile methodology is a plus.
    """

    print(" Paste your Job Description (press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)

    jd_input = "\n".join(lines).strip()
    if not jd_input:
        print("\n Using sample job description.\n")
        jd_input = default_jd

    run_interview(jd_input)
