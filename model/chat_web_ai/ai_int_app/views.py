# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json



# from django.shortcuts import render

# def home(request):
#     return render(request, "ai_int_app/index.html")


# question_flow = [
#     "Tell me about yourself.",
#     "What are your strengths?",
#     "What are your weaknesses?",
#     "Why do you want this job?",
#     "Do you have any questions for us?"
# ]

# @csrf_exempt
# def chatbot_api(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         current_index = int(data.get('question_index', 0))
#         user_answer = data.get('answer', '')

#         # You can save answer in DB if needed here

#         next_index = current_index + 1
#         if next_index < len(question_flow):
#             return JsonResponse({
#                 'next_question': question_flow[next_index],
#                 'question_index': next_index
#             })
#         else:
#             return JsonResponse({
#                 'done': True,
#                 'message': "Interview completed!"
#             })

# ai_int_app/views.py

import json
import random
from django.http import JsonResponse
from django.shortcuts import render
import spacy

nlp = spacy.load("en_core_web_sm")

SKILL_KEYWORDS = set([
    "python", "java", "javascript", "react", "node.js", "aws", "azure", "gcp", "sql", "nosql",
    "docker", "kubernetes", "git", "api", "rest", "graphql", "frontend", "backend", "fullstack",
    "machine learning", "ai", "deep learning", "data science", "cloud", "agile", "scrum", "devops",
    "testing", "security", "linux", "windows", "mobile", "web", "database", "design patterns",
    "architecture", "communication", "teamwork", "problem solving", "leadership", "management",
    "analytical", "critical thinking", "collaboration", "mentoring", "debugging", "scalability",
    "performance", "optimization", "microservices", "ci/cd", "data structures", "algorithms", "oop"
])

QUESTION_TEMPLATES = [
    "Can you explain your experience with {}?",
    "What challenges have you faced while working with {}?",
    "How would you rate your proficiency in {} and why?",
    "Can you share a project where you used {}?",
    "What are some best practices you follow in {}?"
]

POSITIVE_REMARKS = [
    "Great explanation!", "Excellent clarity!", "That's a strong answer!",
    "Well said!", "Impressive experience!", "You’ve demonstrated solid understanding!"
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
    return random.choice(QUESTION_TEMPLATES).format(topic)

def is_response_good(topic, response):
    return all(word.lower() in response.lower() for word in topic.split())

def provide_feedback(is_good):
    if is_good:
        return random.choice(POSITIVE_REMARKS)
    return "That's a good start! Consider including more specific details or examples."

def interview_page(request):
    return render(request, "ai_int_app/index.html")

def interview_chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        answer = data.get("answer", "")
        index = int(data.get("question_index", -1))

        if "topics" not in request.session or index == -1:
            jd = """
                We're hiring a Full Stack Developer with experience in React, Node.js, REST APIs, and AWS.
                Familiarity with Docker, CI/CD, and Agile methodology is a plus.
            """
            request.session["topics"] = extract_skills_from_jd(jd)
            request.session["max_questions"] = 5
            index = -1
            request.session.modified = True

        topics = request.session["topics"]
        max_q = request.session["max_questions"]

        if 0 <= index < len(topics):
            topic = topics[index]
            good = is_response_good(topic, answer)
            feedback = provide_feedback(good)
        else:
            feedback = ""

        index += 1
        if index >= min(len(topics), max_q):
            return JsonResponse({"done": True, "message": "Interview complete. Thank you!"})

        next_topic = topics[index]
        next_question = generate_question(next_topic)

        return JsonResponse({
            "done": False,
            "question_index": index,
            "next_question": next_question,
            "feedback": feedback
        })
