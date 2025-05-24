import spacy
import time
from typing import List, Set, Dict

# -------------------- Constants --------------------
SKILL_KEYWORDS = {
    "python", "java", "javascript", "react", "node.js", "aws", "azure", "gcp",
    "sql", "nosql", "docker", "kubernetes", "git", "api", "rest", "graphql",
    "frontend", "backend", "fullstack", "machine learning", "ai", "deep learning",
    "data science", "cloud", "agile", "scrum", "devops", "testing", "security",
    "linux", "windows", "mobile", "web", "database", "design patterns", "architecture",
    "communication", "teamwork", "problem solving", "leadership", "management",
    "analytical", "critical thinking", "collaboration", "mentoring", "debugging",
    "scalability", "performance", "optimization", "microservices", "ci/cd",
    "data structures", "algorithms", "oop", "object-oriented programming"
}

GENERIC_TERMS = {
    "experience", "years", "role", "team", "responsibilities", "candidate", "skills",
    "knowledge", "ability"
}

# -------------------- NLP Setup --------------------
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("SpaCy model 'en_core_web_sm' not found.")
    print("Please run: python -m spacy download en_core_web_sm")
    exit(1)

# -------------------- Core Functions --------------------

def analyze_job_description(text: str) -> List[str]:
    """
    Extract relevant skill-based keywords from a job description using SpaCy.
    """
    doc = nlp(text.lower())
    extracted_topics: Set[str] = set()

    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.strip()
        if any(keyword in chunk_text for keyword in SKILL_KEYWORDS):
            extracted_topics.add(chunk_text)

    for token in doc:
        token_text = token.text.strip()
        if token_text in SKILL_KEYWORDS:
            extracted_topics.add(token_text)
        # Handle compound phrases like "problem solving"
        if token_text == "problem" and token.head.text.lower() == "solving":
            extracted_topics.add("problem solving")
        if token_text == "data" and token.head.text.lower() == "science":
            extracted_topics.add("data science")

    return sorted(
        topic for topic in extracted_topics
        if topic not in GENERIC_TERMS and len(topic.split()) <= 4
    )


def simulate_llm_question_generation(topic: str, context: str = "") -> str:
    """
    Simulates LLM behavior to generate an interview question.
    """
    print(f"\n--- Generating question for: '{topic}' ---")
    if context:
        default_question = f"Can you elaborate more on your experience with {topic}, specifically regarding {context}?"
    else:
        default_question = f"Tell me about your experience with {topic}."

    time.sleep(1)
    print("LLM is thinking...")
    time.sleep(1)

    custom_question = input(f"Suggested: '{default_question}'\nOverride (or press Enter to use): ")
    return custom_question.strip() or default_question


def simulate_llm_response_analysis(question: str, response: str) -> Dict[str, List[str]]:
    """
    Simulates LLM response analysis for coverage and follow-up depth.
    """
    print(f"\n--- Analyzing response for: '{question}' ---")
    print(f"Candidate: '{response}'")

    time.sleep(1)
    print("LLM is analyzing...")
    time.sleep(1)

    covered_input = input("Covered topics from JD (comma-separated): ")
    delve_input = input("Sub-topics needing deeper discussion (comma-separated): ")

    covered_topics = [t.strip().lower() for t in covered_input.split(',') if t.strip()]
    needs_delving = [t.strip() for t in delve_input.split(',') if t.strip()]

    return {
        "covered_topics": covered_topics,
        "needs_delving": needs_delving,
        "sentiment": "positive"  # Placeholder for future enhancement
    }

def run_interview(job_description: str, max_questions: int = 10) -> None:
    """
    Main function to orchestrate the AI-driven interview process.
    """
    print("\n--- Analyzing Job Description ---")
    topics = analyze_job_description(job_description)
    
    if not topics:
        print("No identifiable topics found in the job description.")
        return

    print(f"Identified Topics: {', '.join(topics)}")
    
    remaining = list(topics)
    covered = set()
    delving = []
    history = []
    count = 0

    print("\n--- Starting Interview ---")
    while count < max_questions and (remaining or delving):
        if delving:
            topic = delving.pop(0)
            context = topic
            print(f"\nDiving deeper into: {topic}")
        else:
            topic = remaining.pop(0)
            context = ""
            print(f"\nAsking about: {topic}")

        question = simulate_llm_question_generation(topic, context)
        print(f"\nAI: {question}")
        
        response = input("You: ").strip()
        if not response:
            print("No response received. Skipping to next.")
            continue

        count += 1
        history.append((question, response))

        analysis = simulate_llm_response_analysis(question, response)

        for t in analysis["covered_topics"]:
            covered.add(t)
            if t in remaining:
                remaining.remove(t)

        for sub in analysis["needs_delving"]:
            if sub not in delving:
                delving.append(sub)

        # Interview status snapshot
        print("\n--- Status Update ---")
        print(f"Questions Asked: {count}/{max_questions}")
        print(f"Covered: {', '.join(covered) if covered else 'None'}")
        print(f"Remaining: {', '.join(remaining) if remaining else 'None'}")
        print(f"To Delve Deeper: {', '.join(delving) if delving else 'None'}")
        print("-----------------------")

    # Final report
    print("\n--- Interview Concluded ---")
    for idx, (q, a) in enumerate(history, 1):
        print(f"\nQ{idx}: {q}\nA{idx}: {a}")

    print("\nFinal Summary:")
    print(f"Questions Asked: {count}")
    print(f"Covered Topics: {', '.join(covered)}")
    print(f"Uncovered Topics: {', '.join(remaining)}")
    print("Note: This is a simulation. Production would include scoring, logs, and NLP insights.")

# -------------------- Entry Point --------------------

if __name__ == "__main__":
    SAMPLE_JD = """
    We are seeking a highly motivated Senior Software Engineer with 5+ years of experience
    in building scalable web applications. The ideal candidate will have strong expertise
    in React and Node.js, with a solid understanding of RESTful APIs and database design
    (SQL and NoSQL). Experience with AWS cloud services (EC2, S3, Lambda) and Docker
    for containerization is a plus. You will be responsible for designing, developing,
    and deploying high-quality code, collaborating with cross-functional teams, and
    mentoring junior developers. Excellent problem-solving and communication skills are
    essential. Agile/Scrum experience preferred.
    """

    print("Welcome to the Dynamic AI Interview Simulator")
    print("Paste your Job Description (Press Enter twice to finish):")
    user_input_lines = []
    while True:
        line = input()
        if not line:
            break
        user_input_lines.append(line)
    job_desc = "\n".join(user_input_lines).strip() or SAMPLE_JD

    run_interview(job_desc, max_questions=5)
