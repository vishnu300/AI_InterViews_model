import streamlit as st
import spacy
import random

# Load spaCy model
@st.cache_resource
def load_nlp_model():
    return spacy.load("en_core_web_sm")

nlp = load_nlp_model()

# Keywords for extracting relevant skills
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

def extract_skills_from_jd(text):
    doc = nlp(text.lower())
    found = set()

    for token in doc:
        if token.text in SKILL_KEYWORDS:
            found.add(token.text)

    for chunk in doc.noun_chunks:
        if chunk.text.strip() in SKILL_KEYWORDS:
            found.add(chunk.text.strip())

    return sorted(found)

def generate_question(topic):
    templates = [
        f"Can you explain your experience with {topic}?",
        f"What challenges have you faced while working with {topic}?",
        f"How would you rate your proficiency in {topic} and why?",
        f"Can you share a project where you used {topic}?",
        f"What are some best practices you follow in {topic}?"
    ]
    return random.choice(templates)

def is_response_good(topic, response):
    keywords = topic.split()
    return all(word.lower() in response.lower() for word in keywords)

def provide_feedback(is_good):
    if is_good:
        return random.choice(POSITIVE_REMARKS)
    else:
        return "That's a good start! Try to include more specific details or examples."

# Streamlit UI
st.title("🧠 AI Interview Assistant")
st.write("Paste a job description to begin the interview session.")

jd_input = st.text_area("📄 Job Description", height=200)

if st.button("Start Interview"):
    if not jd_input.strip():
        st.warning("Please provide a job description.")
    else:
        skills = extract_skills_from_jd(jd_input)
        if not skills:
            st.error("No recognizable skills found in the job description.")
        else:
            st.session_state.topics = skills[:5]
            st.session_state.index = 0
            st.session_state.history = []

# Initialize state
if "topics" in st.session_state and st.session_state.index < len(st.session_state.topics):
    topic = st.session_state.topics[st.session_state.index]
    question = generate_question(topic)
    
    st.subheader(f"Question {st.session_state.index + 1}")
    st.markdown(f"**💬 {question}**")

    response = st.text_area("Your Answer", key=f"response_{st.session_state.index}")

    if st.button("Submit Answer"):
        good = is_response_good(topic, response)
        feedback = provide_feedback(good)
        st.success(f"🤖 Feedback: {feedback}")
        st.session_state.history.append((question, response, feedback))
        st.session_state.index += 1

# Show past questions & feedback
if "history" in st.session_state and st.session_state.history:
    st.markdown("---")
    st.subheader("📜 Interview History")
    for i, (q, a, f) in enumerate(st.session_state.history):
        st.markdown(f"**Q{i+1}: {q}**")
        st.markdown(f"*Your Answer:* {a}")
        st.markdown(f"*AI Feedback:* {f}")
        st.markdown("---")

if "index" in st.session_state and st.session_state.index >= 5:
    st.balloons()
    st.success("✅ Interview complete. Good job!")
