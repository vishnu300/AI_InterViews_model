import spacy
import random
import pyttsx3
import speech_recognition as sr
from typing import List

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def speak(text: str):
    engine.say(text)
    engine.runAndWait()

def load_nlp_model(model_name: str = "en_core_web_sm"):
    try:
        return spacy.load(model_name)
    except OSError:
        raise SystemExit(f"Model '{model_name}' not found. Please run: python -m spacy download {model_name}")

nlp = load_nlp_model()

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

def generate_question(topic: str) -> str:
    templates = [
        f"Can you explain your experience with {topic}?",
        f"What challenges have you faced while working with {topic}?",
        f"How would you rate your proficiency in {topic} and why?",
        f"Can you share a project where you used {topic}?",
        f"What are some best practices you follow in {topic}?"
    ]
    return random.choice(templates)

def is_response_good(topic: str, response: str) -> bool:
    keywords = topic.split()
    return all(word.lower() in response.lower() for word in keywords)

def provide_feedback(is_good: bool) -> str:
    if is_good:
        return random.choice(POSITIVE_REMARKS)
    else:
        return "That's a good start! Consider including more specific details or examples."

def get_voice_input(timeout=5) -> str:
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎤 Listening... (speak clearly)")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=timeout)
            response = recognizer.recognize_google(audio)
            print(f"You said: {response}")
            return response
        except sr.WaitTimeoutError:
            print("⏱️ No speech detected (timeout).")
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"API error: {e}")

    return ""

def run_interview(job_description: str, max_questions: int = 5):
    print("\n--- AI Interview Started ---\n")
    speak("Welcome to your AI-powered interview session.")

    topics = extract_skills_from_jd(job_description)

    if not topics:
        print("Could not identify relevant topics from job description.")
        speak("Sorry, I could not identify relevant skills in the job description.")
        return

    print(f"Identified Skills: {', '.join(topics)}")
    speak("I have identified the key skills. Let's start the interview.")

    asked = 0
    for topic in topics[:max_questions]:
        question = generate_question(topic)
        print(f"\n AI: {question}")
        speak(question)

        response = get_voice_input()

        if not response:
            print("!! No response detected. Skipping topic.\n")
            speak("No response detected. Let's skip this one.")
            continue

        good = is_response_good(topic, response)
        feedback = provide_feedback(good)
        print(f"AI Feedback: {feedback}")
        speak(feedback)
        asked += 1

    print("\n Interview Concluded")
    speak("Great job! The interview is complete. Keep practicing for more confidence.")

# Run program
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
